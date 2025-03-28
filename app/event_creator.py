import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate
import datetime
from icalendar import Calendar, Event, vCalAddress, vText
from config import Config

def create_and_send_ics_file(title, date_str, time_str, location, recipient_email, description=""):
    try:
        organizer_email = Config.SMTP_USERNAME

        start_datetime = datetime.datetime.strptime(f"{date_str} {time_str}", '%d/%m/%Y %H:%M')
        end_datetime = start_datetime + datetime.timedelta(hours=1)

        cal = Calendar()
        cal.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')
        cal.add('version', '2.0')
        cal.add('method', 'REQUEST')

        event = Event()
        event.add('summary', title)
        event.add('dtstart', start_datetime)
        event.add('dtend', end_datetime)
        event.add('dtstamp', datetime.datetime.utcnow())
        event.add('location', vText(location))
        event.add('description', description)
        event['uid'] = f"{datetime.datetime.utcnow().timestamp()}@{Config.SMTP_SERVER}"

        organizer = vCalAddress(f"MAILTO:{organizer_email}")
        organizer.params['cn'] = vText('Organizer')
        organizer.params['role'] = vText('CHAIR')
        event['organizer'] = organizer

        attendee = vCalAddress(f"MAILTO:{recipient_email}")
        attendee.params['cn'] = vText(recipient_email)
        attendee.params['RSVP'] = 'TRUE'
        attendee.params['role'] = vText('REQ-PARTICIPANT')
        event.add('attendee', attendee, encode=False)

        cal.add_component(event)

        ical_content = cal.to_ical().decode('utf-8')

        msg = MIMEMultipart('mixed')
        msg['Subject'] = f"Invitación a evento: {title}"
        msg['From'] = organizer_email
        msg['To'] = recipient_email
        msg['Date'] = formatdate(localtime=True)

        alternative_part = MIMEMultipart('alternative')

        part_html = MIMEText(f"""<html><body>
<h3>Invitación al evento: {title}</h3>
<p>Fecha: {date_str}<br>Hora: {time_str}<br>Lugar: {location}<br>Descripción: {description}</p>
<p>Por favor acepta la invitación desde tu calendario.</p>
</body></html>""", "html")

        part_cal = MIMEText(ical_content, 'calendar; method=REQUEST; charset=UTF-8')
        part_cal.add_header('Content-Disposition', 'inline')

        alternative_part.attach(part_html)
        alternative_part.attach(part_cal)

        msg.attach(alternative_part)

        ics_attachment = MIMEBase('application', "octet-stream")
        ics_attachment.set_payload(ical_content.encode('utf-8'))
        encoders.encode_base64(ics_attachment)
        ics_attachment.add_header('Content-Disposition', 'attachment; filename="invite.ics"')

        msg.attach(ics_attachment)

        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
            server.sendmail(organizer_email, [recipient_email], msg.as_string())

        return f"La invitación con iCalendar fue enviada correctamente a {recipient_email}."

    except Exception as e:
        return f"Error al enviar la invitación: {str(e)}"
