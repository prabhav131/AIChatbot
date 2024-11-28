import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

class MeetingTool:
    def __init__(self):
        self.recipients = []
        self.subject = "Meeting Invite"  # Hardcoded subject
        self.agenda = ""
        self.location = ""
        self.start_time = None
        self.duration = 0
        self.sender_email = os.getenv("EMAIL_USER") 
        self.sender_password = os.getenv("EMAIL_PASSWORD")
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT"))

    def extract_intent(self, user_message):
        """
        Detect if the user's intent is to schedule a meeting based on keywords.
        """
        user_message = user_message.lower()
        if "meeting" in user_message or "schedule" in user_message or "appointment" in user_message:
            return "schedule_meeting"
        return None

    def get_user_input(self):
        """
        Prompt the user for meeting details: recipients, agenda, location, date, time, and duration.
        """
        # Collect meeting details from the user
        recipients_input = input("Enter recipient email addresses (comma separated): ")
        self.recipients = [email.strip() for email in recipients_input.split(",")]
        
        self.agenda = input("Enter the agenda for the meeting: ")
        self.location = input("Enter the meeting location: ")

        # Date and time for the meeting
        date_str = input("Enter the meeting date (DD/MM/YY): ")
        time_str = input("Enter the meeting time (HH:MM, 24-hour format): ")
        self.start_time = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%y %H:%M")

        # Duration input
        self.duration = int(input("Enter the meeting duration in minutes: "))

    def create_ics_content(self):
        # Calculate the end time of the meeting
        end_time = self.start_time + timedelta(minutes=self.duration)

        # Format times for the .ics file in UTC format
        start_time_str = self.start_time.strftime("%Y%m%dT%H%M%SZ")
        end_time_str = end_time.strftime("%Y%m%dT%H%M%SZ")

        # Create the .ics calendar invite content
        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Organization//Your Product//EN
METHOD:REQUEST
BEGIN:VEVENT
UID:12345678@example.com
DTSTAMP:{start_time_str}
DTSTART:{start_time_str}
DTEND:{end_time_str}
SUMMARY:{self.subject}
DESCRIPTION:{self.agenda}
LOCATION:{self.location}
STATUS:CONFIRMED
SEQUENCE:0
END:VEVENT
END:VCALENDAR"""
        return ics_content

    def send_invite(self):
        # Create email message
        msg = MIMEMultipart("alternative")
        msg["From"] = self.sender_email
        msg["To"] = ", ".join(self.recipients)
        msg["Subject"] = self.subject

        # Attach the calendar invite (.ics)
        ics_content = self.create_ics_content()
        part = MIMEBase("text", "calendar", method="REQUEST", name="invite.ics")
        part.set_payload(ics_content)
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=invite.ics")
        msg.attach(part)

        # Add a simple text body (optional)
        body = f"Hello,\n\nYou are invited to the following meeting:\n\nSubject: {self.subject}\nLocation: {self.location}\nStart Time: {self.start_time}\nDuration: {self.duration} minutes\n\nAgenda: {self.agenda}"
        msg.attach(MIMEText(body, "plain"))

        # Send the email
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Enable TLS
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.recipients, msg.as_string())
                print("Meeting invite sent successfully!")
        except Exception as e:
            print(f"Failed to send invite: {e}")
            
    def schedule(self, user_message):
        
        user_input = user_message

        # Check for meeting intent
        if self.extract_intent(user_input) == "schedule_meeting":
            # If the intent is detected, gather meeting details
            self.get_user_input()
            
            # Send the meeting invite
            self.send_invite()
        else:
            print("No meeting intent detected.")
            
        return "continue"    
     

if __name__ == "__main__":
    meeting_tool = MeetingTool()
    user_input = input("You: ")
    meeting_tool.schedule(user_message=user_input)