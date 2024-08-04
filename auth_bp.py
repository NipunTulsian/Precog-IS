from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from flask_login import login_user, logout_user, current_user
from models import db, Otp_table, Mentee, Mentor, Admin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_mail import  Message
from mail import mail
auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Mentee.query.filter_by(email=email).first()
        if user:
            password_cor=check_password_hash(user.password,password)
            if password_cor:
                login_user(user)
                session['email']=email
                return redirect(url_for('dashboard.dashboard'))
        user = Mentor.query.filter_by(email=email).first()
        if user:
            # password_cor=check_password_hash(user.password,password)
            if password==user.password:
                login_user(user)
                session['email']=email
                return redirect(url_for('dashboard.dashboard_mentor'))
        user=Admin.query.filter_by(email=email).first()
        if user:
            if user.password==password:
                login_user(user)
                session['email']=email
                return redirect(url_for('dashboard.dashboard_admin'))
        else:
            flash('Invalid Credentials', 'danger')
    return render_template('login.html')

@auth_bp.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))

import secrets

def generate_otp():
    # Generate a 6-digit OTP (you can adjust the length as needed)
    otp = secrets.randbelow(10**6)
    return f"{otp:06d}"

@auth_bp.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if request.method=='POST':
        email = request.form.get('email')
        otp=generate_otp()
        otp_record=Otp_table.query.filter_by(email=email).first()
        if otp_record:
            otp_record.otp=otp
        else:
            new_otp = Otp_table(
                email=email,
                otp=otp
            )
            db.session.add(new_otp)
        db.session.commit()

        msg = Message('Reset Password for ACM!', sender ='nipun.tulsian.nt@gmail.com', recipients = [email])
        msg.body = "Otp for password Reset is : {}".format(otp)
        mail.send(msg)

        return redirect(url_for('auth.change_password',email=email))
        
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('reset_password.html')

@auth_bp.route("/change_password/<email>",methods=['GET', 'POST'])
def change_password(email):
    if request.method=='POST':
        otp = request.form.get('otp')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')
        single_record = Otp_table.query.filter_by(email=email).first()
        if single_record.otp==otp:
            if new_password!=confirm_new_password:
                flash("Passwords Didn't match", 'danger')
                return render_template('change_password.html',email=email)
            user = Mentor.query.filter_by(email=email).first()
            if user:
                user.password = generate_password_hash(new_password)
            user = Mentee.query.filter_by(email=email).first()
            if user:
                user.password = generate_password_hash(new_password)
            user = Admin.query.filter_by(email=email).first()
            db.session.delete(single_record)
            db.session.commit()
            flash("Password Updated",'success')
            return render_template('change_password.html',email=email)
        else:
            flash('Enter Correct Otp.', 'danger')
            return render_template('change_password.html',email=email)
    single_record = Otp_table.query.filter_by(email=email).first()
    if single_record:
        return render_template('change_password.html',email=email)
    else:
        return redirect(url_for('auth.reset_password'))