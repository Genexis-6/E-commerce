from flask import Blueprint, redirect, url_for, render_template, request, flash, session
from WEB.model import Customers
from WEB.ext import Message,mail, otp, db, login_user
from WEB.config import Config
from werkzeug.security import generate_password_hash

email = Blueprint("email", __name__, url_prefix='/forgetpass')


@email.route("/emailreg", methods = ['POST', 'GET'])
def reg_email():
    session['email'] = None
    if request.method == 'POST':
        get_email = request.form['email']
        check_user_email = Customers.query.filter_by(email = get_email).first()
        if check_user_email:
            session['email'] = get_email
            return redirect(url_for('email.sendOTP'))
        else:
            flash("email not registered😔")
            return redirect(url_for("auth.register"))
    return render_template('forget_password.html')



@email.route("/otp")
def sendOTP():
    config = Config()
    session['otp'] = code = otp()
    title = "OTP CODE"
    sender = config.MAIL_USERNAME
    recipients = [session['email']]
    msg = Message(
        title,
        sender=sender,
        recipients=recipients
    )
    msg.body = f"OTP -- {code}"
    try:
        mail.send(msg)
        flash(f"otp sent to {session['email']}")
        return redirect(url_for("email.validate_otp"))
    except Exception as e:
        flash(f"error due to {e}")
        print(e)
        return redirect(url_for("email.reg_email"))
    

    
@email.route("/validate", methods=['POST', 'GET'])
def validate_otp():
    if 'otp' in session:
        if request.method == 'POST':
            otp = request.form['otp']
            if otp == session['otp']:
                flash("OTP validated successfully")
                return redirect(url_for('email.change_pass'))
            else:
                flash("wrong OTP")
                return redirect(url_for("email.reg_email"))
    else:
        flash("error generating otp... enter your email again")
        return redirect(url_for("email.reg_email"))
    return render_template("otp.html", email=session['email'])


@email.route('/updatePassword', methods=['GET', 'POST'])
def change_pass():
    get_user = Customers.query.filter_by(email = session['email']).first()
    if request.method == 'POST':
        password = request.form['password']
        get_user.password=generate_password_hash(password)
        flash("password updated successfully")
        db.session.commit()
        login_user(get_user)
        return redirect(url_for('home.index'))
    return render_template("update_detail.html", username=get_user.username, email=get_user.email, phone=get_user.phone)