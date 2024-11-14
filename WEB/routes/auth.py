from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from WEB.model import Customers, Category
from werkzeug.security import generate_password_hash, check_password_hash
from WEB.ext import db, generate_csrf_token, validate_csrf_token, login_user, logout_user, current_user, login_required
from WEB.api_scraper.category import get_cached_category_links
auth = Blueprint("auth", __name__, url_prefix="/")


@auth.route("/")
def overview():
    data = []
    url = "https://www.jumia.com.ng/?gad_source=1&gclid=Cj0KCQiA0MG5BhD1ARIsAEcZtwQEskgvscM7H4ALDZOiv89BdT_H3jAGH_0xLTBsqUHW588mqdKvzFIaAhySEALw_wcB"
    get_cached_category_links(url)
    category = Category.query.all()
    for product in category:
        data.append(
            {
                'name':product.name,
                'link':product.link
            }
        )
    return render_template("overview.html", current_user=current_user, data=data)


    
    
@auth.route("/login", methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    
    
    if request.method == "POST":
        session['username'] = username = request.form.get("username")
        password = request.form.get('password')
        check_user = Customers.query.filter_by(username=username).first()
        username = username
        if check_user:
            if check_password_hash(check_user.password, password):
                flash("logged-in successfully")
                login_user(check_user)
                return redirect(url_for("home.index"))
            else:
                flash("incorrect password")
                return redirect(url_for("auth.login"))
        flash("no user found")
        return redirect(url_for("auth.login"))
    try:
        return render_template("loginform.html", username=session['username'])
    except KeyError:
        return render_template("loginform.html", username='')




@auth.route('/register', methods = ['POST', 'GET'])
def register():
    
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    
    
    username = ''
    email = ''
    phone = ''
    email_ext = ['gmail.com', 'hotmail.com' ,'outlook.com']
    if request.method == "POST":
        token = request.form.get("csrf_token")
        if validate_csrf_token(token=token):
            session["username"] = username = request.form.get("username")
            session["email"] = email = request.form.get("email")
            session["phone"] = phone = request.form.get("phone")
            password = request.form.get('password')
            validate_email = True if email.split('@')[1] in email_ext else False
            check_user_email = Customers.query.filter_by(email=email).first()
            check_user_name = Customers.query.filter_by(username=username).first()
            if len(username)<2:
                flash("Username too short")
                return redirect(url_for("auth.register"))
            elif not validate_email:
                flash("invalid email, email should be either gmail.com, hotmail.com or outlook.com")
                return redirect(url_for("auth.register"))
            elif len(phone) < 10 or len(phone)>12 :
                flash("number must be 11-digts")
                return redirect(url_for("auth.register"))
            elif len(password)< 6:
                flash("password too short")
                return redirect(url_for("auth.register"))
            
            if not check_user_name:
                if not check_user_email:
                    add_user = Customers(
                        username=username,
                        email=email,
                        password=generate_password_hash(password),
                        phone=phone
                    )
                    db.session.add(add_user)
                    db.session.commit()
                    flash("registered successfully")
                    
                    login_user(add_user)
                    
                    return redirect(url_for("auth.login"))
                else:
                    flash("email already used")
                    return redirect(url_for('auth.register'))
            else:
                flash("username already used")
                return redirect(url_for('auth.register'))               
        else:
            flash("csrf token expired")
    try:

        return render_template("regform.html", csrf_token=generate_csrf_token(), username=session['username'], email=session['email'], phone=session['phone'])
    except KeyError:
        return render_template("regform.html", csrf_token=generate_csrf_token(), username='', email='', phone='')


@auth.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    flash("logged out successfully")
    return redirect(url_for("auth.login"))