from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import db, Meet_details, Mentor, Mentee
from sqlalchemy import and_
from datetime import datetime
from config import Config
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/dashboard",methods=['GET','POST'])
@login_required
def dashboard():
    try:
        meets = Meet_details.query.filter(and_(Meet_details.mentee_id==current_user.id, Meet_details.status=="pending")).all()
        meets_pending=[]
        meets_completed=[]
        datetime_format = '%Y-%m-%d %H:%M:%S'
        for meet in meets:
            mentor=Mentor.query.filter_by(id=meet.mentor_id).first()
            mentor = f"{mentor.first_name} {mentor.last_name}"
            datetime_str=f"{meet.date_of_meet} {meet.time_of_meet}"
            specified_datetime = datetime.strptime(datetime_str, datetime_format)
            current_timestamp = datetime.now()

            if specified_datetime < current_timestamp:
                meets_completed.append({"mentor":mentor, "research":meet.research_problem, "feedback":meet.feedback, "date":meet.date_of_meet, "time":meet.time_of_meet})
                curr_meet = Meet_details.query.filter_by(id=meet.id).first()
                curr_meet.status = "completed"
                db.session.commit()
            else:
                meets_pending.append({"mentor":mentor, "research":meet.research_problem, "feedback":meet.feedback, "date":meet.date_of_meet, "time":meet.time_of_meet})
        return render_template('dashboard.html', meets_completed=meets_completed, meets_pending = meets_pending)
    except Exception as e:
        print(e)
        return render_template('dashboard.html',err=str(e))

@dashboard_bp.route("/dashboard_admin",methods=['GET','POST'])
@login_required
def dashboard_admin():
    try:
        meets = Meet_details.query.filter_by(status="pending").all()
        meets_pending=[]
        meets_completed=[]
        datetime_format = '%Y-%m-%d %H:%M:%S'
        for meet in meets:
            mentor=Mentor.query.filter_by(id=meet.mentor_id).first()
            mentee=Mentee.query.filter_by(id=meet.mentee_id).first()
            mentor = f"{mentor.first_name} {mentor.last_name}"
            mentee = f"{mentee.first_name} {mentee.last_name}"
            datetime_str=f"{meet.date_of_meet} {meet.time_of_meet}"
            specified_datetime = datetime.strptime(datetime_str, datetime_format)
            current_timestamp = datetime.now()

            if specified_datetime < current_timestamp:
                meets_completed.append({"ID":meet.id,"mentor":mentor, "mentee":mentee, "affiliation":meet.affiliation, "research":meet.research_problem, "feedback":meet.feedback, "date":meet.date_of_meet, "time":meet.time_of_meet})
                curr_meet = Meet_details.query.filter_by(id=meet.id).first()
                curr_meet.status = "completed"
                db.session.commit()
            else:
                meets_pending.append({"ID":meet.id, "mentor":mentor, "mentee":mentee, "affiliation":meet.affiliation, "research":meet.research_problem, "feedback":meet.feedback, "date":meet.date_of_meet, "time":meet.time_of_meet})

        return render_template('dashboard_admin.html', meets_completed=meets_completed, meets_pending = meets_pending)
    except Exception as e:
        return render_template('dashboard_admin.html',err=str(e))

@dashboard_bp.route("/dashboard_mentor",methods=['GET','POST'])
@login_required
def dashboard_mentor():
    try:
        meets = Meet_details.query.filter(and_(Meet_details.mentor_id==current_user.id, Meet_details.status=="pending")).all()
        meets_pending=[]
        meets_completed=[]
        datetime_format = '%Y-%m-%d %H:%M:%S'
        for meet in meets:
            mentee=Mentee.query.filter_by(id=meet.mentee_id).first()
            mentee = f"{mentee.first_name} {mentee.last_name}"
            datetime_str=f"{meet.date_of_meet} {meet.time_of_meet}"
            specified_datetime = datetime.strptime(datetime_str, datetime_format)
            current_timestamp = datetime.now()

            if specified_datetime < current_timestamp:
                meets_completed.append({"mentee":mentee, "affiliation":meet.affiliation, "research":meet.research_problem, "feedback":meet.feedback, "date":meet.date_of_meet, "time":meet.time_of_meet})
                curr_meet = Meet_details.query.filter_by(id=meet.id).first()
                curr_meet.status = "completed"
                db.session.commit()
            else:
                meets_pending.append({"mentee":mentee, "affiliation":meet.affiliation, "research":meet.research_problem, "feedback":meet.feedback, "date":meet.date_of_meet, "time":meet.time_of_meet})

        return render_template('dashboard_mentor.html', meets_completed=meets_completed, meets_pending = meets_pending)
    except Exception as e:
        return render_template('dashboard_mentor.html',err=str(e))

@dashboard_bp.route("/details",methods=["GET","POST"])
@login_required
def details():
    try:
        if request.method == 'POST':
            selected_options = request.form.getlist('options')
            meet_link = request.form.get('meet_link')
            selected_options = ",".join(selected_options)
            mentor = Mentor.query.filter_by(id=current_user.id).first()
            mentor.meet_link = meet_link
            mentor.slots = selected_options
            db.session.commit()
            
        pre_selected = []
        if current_user.slots:
            pre_selected = current_user.slots.split(',')
            pre_selected = [int(option.strip()) for option in pre_selected]
        return render_template('details_mentor.html', slots = Config.slots, pre_selected=pre_selected)
    except Exception as e:
        return render_template('details_mentor.html',err=str(e))

@dashboard_bp.route("/all_mentors",methods=["GET"])
@login_required
def all_mentors():
    try:
        mentors = Mentor.query.all()
        data =[]
        for mentor in mentors:
            data.append({"ID":mentor.id, "First Name":mentor.first_name, "Last Name":mentor.last_name,"Email":mentor.email, "Description":mentor.Description, "Meet Link":mentor.meet_link})
        return render_template('display_mentors.html',data=data)
    except Exception as e:
        return render_template('display_mentors.html',data=[],err=str(e))

@dashboard_bp.route("/all_mentees",methods=["GET"])
@login_required
def all_mentees():
    try:
        mentees = Mentee.query.all()
        data =[]
        for mentee in mentees:
            data.append({"ID":mentee.id, "First Name":mentee.first_name, "Last Name":mentee.last_name,"Email":mentee.email, "Registration Date":mentee.registration_date})
        return render_template('display_mentees.html',data=data)
    except Exception as e:
        return render_template('display_mentees.html',data=[],err=str(e))

