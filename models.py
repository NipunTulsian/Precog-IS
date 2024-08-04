from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
db = SQLAlchemy()

class Mentee(db.Model, UserMixin):
    id=db.Column(db.Integer,autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=True, default="mentee")
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def get_id(self):
        return f"mentee-{self.id}"

class Mentor(db.Model, UserMixin):
    id=db.Column(db.Integer,autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=True, default="mentor")
    Description = db.Column(db.Text, nullable=True)
    slots = db.Column(db.Text, nullable=True, default="1,5,9")
    meet_link = db.Column(db.String(1024), nullable=True)

    def get_id(self):
        return f"mentor-{self.id}"

class Admin(db.Model, UserMixin):
    id=db.Column(db.Integer,autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=True, default="admin")

    def get_id(self):
        return f"admin-{self.id}"

class Otp_table(db.Model):
    email=db.Column(db.String(255),primary_key=True, nullable=True)
    otp=db.Column(db.String(255), nullable=True)

class Meet_details(db.Model):
    id=db.Column(db.Integer,autoincrement=True, primary_key=True)
    mentee_id = db.Column(db.Integer, db.ForeignKey('mentee.id'), nullable=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'), nullable=True)
    affiliation = db.Column(db.Text, nullable=False)
    research_problem = db.Column(db.Text, nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    times_before = db.Column(db.String(256), nullable=False)
    date_of_meet = db.Column(db.Date, nullable=True)
    time_of_meet = db.Column(db.Time, nullable=True)
    status = db.Column(db.String(256), nullable=False, default="pending")
    slot_index = db.Column(db.Integer, nullable=True)