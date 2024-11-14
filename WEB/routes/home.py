from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from WEB.ext import login_required, current_user, allowd_file
from WEB.model import Customers, CategoryProduct, Category, PaymentRecord
from WEB.config import Config
from WEB.ext import db
import os
from werkzeug.utils import secure_filename
from WEB.api_scraper.category import get_product_cache_details, get_searched_product
import json
from random import choice

home = Blueprint("home", __name__, url_prefix="/home")

@home.route("/", methods= ['POST', 'GET'])
@login_required
def index():
    choices = ['phones', 'fashion', "toys", 'baby stuff', "supermarket", "shirts"]
    value = choice(choices)
    if request.method == 'POST':
        value = request.form['value']    
        return redirect(url_for("home.home_loading", value=value))
    
    if "value" in session:
        value = session['value']
    output = get_searched_product(value=value)
    return render_template("search.html", output=output, value=value, output_length=len(output),show_search_bar=True)


@home.route("/loading/home/<value>")
def home_loading(value):
    session['value'] = value
    return render_template("home_loadAnimation.html")




@home.route("/profile", methods = ['POST', 'GET'])
@login_required
def view_profile():
    config = Config()
    get_user = Customers.query.get(current_user.id)
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        file = request.files['profile_photo']
        
        if file and allowd_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(config.UPLOAD_FOLDER, filename).replace("\\", '/')
            file.save(file_path)
            
            if username != '':
                get_user.username = username 
            elif email == '':
                get_user.email = email
            elif phone == '':
                get_user.phone = phone
            
            get_user.profile_image = file_path
            db.session.commit()
            flash("updated...")
            return redirect(url_for('home.view_profile'))
        else:
            if username != '':
                get_user.username = username 
            elif email == '':
                get_user.email = email
            elif phone == '':
                get_user.phone = phone
            db.session.commit()
            flash("updated...")
            return redirect(url_for('home.view_profile'))
    photo_data = None    
    if get_user.profile_image:
        photo_data = get_user.profile_image
    try:
        if photo_data != None:
            return render_template("profile.html", username=get_user.username, 
                           email=get_user.email, 
                           phone=get_user.phone, photo =photo_data.split('/static/')[1])
        return render_template("profile.html", username=get_user.username, 
                           email=get_user.email, 
                           phone=get_user.phone, photo='empty')
    except:
        if photo_data != None:
            return render_template("profile.html", username=get_user.username, 
                           email=get_user.email, 
                           phone=get_user.phone, photo =photo_data.split('/static/')[1])
        return render_template("profile.html", username=get_user.username, 
                           email=get_user.email, 
                           phone=get_user.phone, photo ='empty')
        
        
        
@home.route('/delete')
@login_required
def delete_dp():
    get_user = Customers.query.get(current_user.id)
    get_user.profile_image = None
    db.session.commit()
    flash("profile image deleted successfully")
    return redirect(url_for("home.view_profile"))
    
@home.route('/history')
@login_required
def history():
    get_record = PaymentRecord.query.filter_by(customer_id=current_user.id).order_by(PaymentRecord.date).all()
    return render_template("history.html",get_record=get_record)