from datetime import datetime
from icalendar import Event, Calendar
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import io

def create_ics_file(event_name, start_datetime, end_datetime, location, description):
    cal = Calendar()
    event = Event()
    event.add('summary', event_name)
    event.add('dtstart', start_datetime)
    event.add('dtend', end_datetime)
    event.add('location', location)
    event.add('description', description)
    
    cal.add_component(event)
    
    # Write to a file-like object
    ics_file = io.BytesIO()
    ics_file.write(cal.to_ical())
    ics_file.seek(0)
    
    return ics_file

def send_email_with_attachment(subject, body, recipients, attachment_file, smtp_server, smtp_port, smtp_user, smtp_password):
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Attach the calendar invite
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment_file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="invite.ics"')
    msg.attach(part)

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, recipients, msg.as_string())

# Example usage
event_name = "Meeting with Mentor"
start_datetime = datetime(2024, 8, 10, 10, 0, 0)  # Start time: August 10, 2024 10:00 AM
end_datetime = datetime(2024, 8, 10, 11, 0, 0)    # End time: August 10, 2024 11:00 AM
location = "Conference Room 1"
description = "Discussion on upcoming projects and strategy."

# Create ICS file
ics_file = create_ics_file(event_name, start_datetime, end_datetime, location, description)

# Send email
subject = "Calendar Invitation: Meeting with Mentor"
body = "Please find the attached calendar invite for our upcoming meeting."
recipients = ['recipient1@example.com', 'recipient2@example.com']
smtp_server = 'smtp.example.com'
smtp_port = 587
smtp_user = 'your-email@example.com'
smtp_password = 'your-password'

send_email_with_attachment(subject, body, recipients, ics_file, smtp_server, smtp_port, smtp_user, smtp_password)
