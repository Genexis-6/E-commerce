from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from WEB.model import Category, CategoryProduct, Product, Searched_Product, CartList, Customers, PaymentRecord
from WEB.ext import login_required, current_user, db
from WEB.api_scraper.category import get_product_cache_details, get_particular_product_detail, get_searched_product, get_particular_product_search
import json

service = Blueprint("service", __name__, url_prefix="/products")

@service.route("/<name>")
def products(name):
    data = []
    get_pproduct_link = Category.query.filter_by(name=name).first()
    if get_pproduct_link:
        link = get_pproduct_link.link
        category_id = get_pproduct_link.id
        get_product_cache_details(link, category_id=category_id)
        prodt = CategoryProduct.query.filter_by(category_id=category_id).all()
        for items in prodt:
            data.append({
                "heading": items.heading,
                "discription": items.description,
                "image_url":items.img_url,
                "info_url":items.info_url,
                "price": items.price,
                "previous_price":items.previous_price,
                "discount": items.discount
            })
    heading = []
    for num in range(len(data)):
        head = data[num]['heading']
        if head in heading:
            pass
        else:
            heading.append(
                head
            )
    heading_length = len(heading)
    data_length = len(data)
    
    return render_template("service.html",data=data,
                           heading_length=heading_length,
                           data_length=data_length,
                           heading=heading
                           )
    
@service.route('/loading/<product>')
def loading(product):
    session['product'] = product.replace("_", "/")
    return render_template("load.html")



@service.route('/loading/<name>/<input_>')
def search_loading(name, input_):
    session['name'] = name.replace("_", "/")
    session['input'] = input_
    return render_template("default_loading.html")


@service.route("/product_item")
def particular_product():
    get_product = CategoryProduct.query.filter_by(description=session['product']).first()
    if get_product:
        get_particular_product_detail(get_product.info_url,product_id=get_product.id)
        output = Product.query.filter_by(categoryProduct_id=get_product.id).first()
        return render_template("product.html",output=output,current_user=current_user)
    return "no product found"





@service.route('/searched_product-item')
def particular_searched_product():
    outputList = get_searched_product(session['input'])
    url = 'https://www.jumia.com.ng'
    for items in range(len(outputList)):
        if session['name'] == outputList[items]['name']:
            url += outputList[items]['details']
    get_particular_product_search(url, session["input"])
    output= Searched_Product.query.filter_by(name=session['name']).first()
    return render_template("product.html",output=output,current_user=current_user)


@service.route("/view-cart")
@login_required
def view_cart():
    cart = CartList.query.filter_by(customers_id= current_user.id).all()
    return render_template("view_cart.html",cart=cart)


@service.route("/add-cart/<pname>/<price>")
@login_required
def add_product(pname, price):
    session['pname'] = pname.replace("_", "/")
    check_1 = Product.query.filter_by(name=session['pname']).first()
    check_2 = Searched_Product.query.filter_by(name=session['pname']).first()
    if check_1:
        session['image'] = check_1.img_url
    elif check_2:
        session['image'] = check_2.img_url
        
    cart = CartList.query.filter_by(product_name=session['pname']).first()
    if not cart:
        cart = CartList(
            product_name =session['pname'],
            price = price,
            customers_id = current_user.id,
            image = session['image']
        )
        db.session.add(cart)
        db.session.commit()
        flash("product added successfully")
        return redirect(url_for("service.view_cart"))
    
    flash("product already in cart")
    return redirect(url_for("service.view_cart"))


@service.route("/delete-product-fromCart/<ID>")
@login_required
def delete_product(ID):
    get_product = CartList.query.get(ID)
    product_name = get_product.product_name
    db.session.delete(get_product)
    db.session.commit()
    flash(f"{product_name} removed from cart list successfully")
    return redirect(url_for("service.view_cart"))


@service.route('/view-product/<name>')
@login_required
def view_product(name):
    session['name'] = name.replace("_", "/")
    check_1 = Product.query.filter_by(name=session['name']).first()
    check_2 = Searched_Product.query.filter_by(name=session['name']).first()
    if check_1:
        output = check_1
    elif check_2:
        output = check_2
    return render_template("product.html",output=output,current_user=current_user)
    
    
@service.route('/buy-now/<tobuy>', methods=['POST', 'GET'])
@login_required
def buy(tobuy):
    price = ''
    img = ''
    session['tobuy'] = tobuy.replace("_", "/")
    check_1 = Product.query.filter_by(name=session['tobuy']).first()
    check_2 = Searched_Product.query.filter_by(name=session['tobuy']).first()
    if check_1:
        price = check_1.price
        img = check_1.img_url
    elif check_2:
        price = check_2.price
        img = check_2.img_url
        
    get_user = Customers.query.get(current_user.id)
    if request.method == "POST":
        address = request.form["shipping-address"]
        payment_method = request.form.get('payment-method')
        
        payment = PaymentRecord(
            product_name = tobuy, 
            price=price,
            payment_method=payment_method,
            address=address,
            customer_id=current_user.id
            
        )
        db.session.add(payment)
        db.session.commit()
        flash("payment proceedure completed")
        get_product = CartList.query.filter_by(product_name=session['tobuy']).first()
        try:
            db.session.delete(get_product)
            db.session.commit()
            return redirect(url_for("service.view_cart"))
        except Exception as e:
            return redirect(url_for("home.index"))
    return render_template("buynow.html", name=get_user.username, email=get_user.email, product=tobuy, price=price,image=img)
