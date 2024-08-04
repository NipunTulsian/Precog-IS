from flask import render_template,request,redirect,url_for,Blueprint
from flask_login import login_required, current_user
from models import db, Mentor, Meet_details, Admin
from datetime import datetime, timedelta
from config import Config
import calendar
from sqlalchemy import and_
from icalendar import Event, Calendar
import io
from flask_mail import  Message
from mail import mail

register_bp=Blueprint('register',__name__)

@register_bp.route('/register',methods=['GET','POST'])
@login_required
def register():
    mentors_df = Mentor.query.all()
    mentors = [{'id':record.id, 'desc': f"{record.first_name} {record.last_name},{record.Description}"} for record in mentors_df]
    time_options = ['Attending for the 1st time', 'Attending for the 2nd time', 'Attending for the 3rd time', 'More than thrice']
    return render_template('register.html', mentors=mentors, time_options = time_options)

@register_bp.route('/register_form',methods=['GET','POST'])
@login_required
def register_form():
    if request.method=='POST':
        affiliation=request.form.get('affiliation')
        research=request.form.get('research_problem')
        feedback=request.form.get('feedback')
        mentor=request.form.get('mentor')
        times=request.form.get('times')

        possible_slot=get_timeslot(mentor)

        new_meet = Meet_details(
            mentee_id=current_user.id,
            mentor_id=mentor,
            affiliation=affiliation,
            research_problem=research,
            feedback=feedback,
            times_before=times,
            status="pending",
            time_of_meet=possible_slot[1],
            date_of_meet=possible_slot[0]
        )
        db.session.add(new_meet)
        db.session.commit()

        send_calendar_invite(mentor, current_user.id, possible_slot)
        
    return redirect(url_for('dashboard.dashboard'))

def send_calendar_invite(mentor_id, mentee_id, possible_slot):
    cal = Calendar()
    event = Event()
    mentor=Mentor.query.filter_by(id=mentor_id).first()
    start_time = datetime.strptime(f"{possible_slot[0]} {possible_slot[1]}", "%Y-%m-%d %H:%M:%S")
    event.add('summary', "Ph.D Clinic Meet")
    event.add('dtstart', start_time)
    event.add('dtend', start_time+timedelta(hours=2))
    event.add('location', mentor.meet_link)
    event.add('description', "Join the meeting using the link")
    
    cal.add_component(event)
    
    ics_file = io.BytesIO()
    ics_file.write(cal.to_ical())
    ics_file.seek(0)

    subject = "Calendar Invitation: Meeting with Mentor"
    body = "Please find the attached calendar invite for our upcoming meeting."
    recipients = [current_user.email, mentor.email]

    admins = Admin.query.all()
    for admin in admins:
        recipients.append(admin.email)

    msg = Message(subject, sender='nipun.tulsian.nt@gmail.com', recipients=recipients)
    msg.body = body

    msg.attach('invite.ics', 'text/calendar', ics_file.read())
    mail.send(msg)
    return


def get_timeslot(mentor_id):
    mentor = Mentor.query.filter_by(id=mentor_id).first()
    slots = mentor.slots.split(",")
    slots = [int(slot) for slot in slots]
    num_dates = 10
    start_date = datetime.now() + timedelta(days=7)
    possible_slots_mentor=[]
    for slot in slots:
        slot_str = Config.slots[slot-1]["slot"]
        day, time, ampm = slot_str.split(" ")
        
        weekday = list(calendar.day_name).index(day)
        current_date = start_date

        days_ahead = weekday - current_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7

        for _ in range(num_dates):
            current_date += timedelta(days=days_ahead)
            possible_slots_mentor.append((current_date.strftime("%Y-%m-%d")   , convert_to_24_hour_format(time.split("-")[0], ampm)))
            days_ahead = 7
    possible_slots_mentor = sorted(possible_slots_mentor, key=lambda x: (x[0], x[1]))

    meetings = Meet_details.query.filter(and_(Meet_details.mentor_id==mentor_id, Meet_details.status=="pending")).all()
    meeting_slots = [(meeting.date_of_meet.strftime("%Y-%m-%d"), meeting.time_of_meet.strftime("%H:%M:%S")) for meeting in meetings]
    available_slots = [slot for slot in possible_slots_mentor if (slot[0], slot[1]) not in meeting_slots]
    return available_slots[0]

def convert_to_24_hour_format(time_str, ampm):
    time = datetime.strptime(time_str +"-"+ ampm, "%I-%p")
    return time.strftime("%H:%M:%S")