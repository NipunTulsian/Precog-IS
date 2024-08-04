from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from werkzeug.security import generate_password_hash
from models import Mentee, db, Mentor
from datetime import datetime
signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/signup', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            # Check if user already exists
            user_exists = Mentee.query.filter_by(email=email).first()
            if user_exists:
                flash('Email already registered.', 'danger')
                return redirect(url_for('register.register'))

            # Check if passwords match
            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return redirect(url_for('.register'))

            # Create new user with hashed password
            new_user = Mentee(
                email=email,
                password=generate_password_hash(password),
                first_name=first_name,
                last_name=last_name,
                role="mentee",
                registration_date=datetime.utcnow(),
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful. Please log in.', 'success')

        # If it's a GET request, just render the registration template
        return render_template('sign_up.html')
    except Exception as e:
        return jsonify({'error': str(e)}),404

@signup_bp.route('/signup_mentor', methods=['GET', 'POST'])
def register_mentor():
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            desc = request.form.get('desc')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            # Check if user already exists
            user_exists = Mentor.query.filter_by(email=email).first()
            if user_exists:
                flash('Email already registered.', 'danger')
                return redirect(url_for('register.register'))

            # Check if passwords match
            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return redirect(url_for('.register'))

            # Create new user with hashed password
            new_user = Mentor(
                email=email,
                password=generate_password_hash(password),
                first_name=first_name,
                last_name=last_name,
                role="mentor",
                Description=desc,
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful. Please log in.', 'success')

        # If it's a GET request, just render the registration template
        return render_template('sign_up_mentor.html')
    except Exception as e:
        return jsonify({'error': str(e)}),404

