from fastapi import HTTPException
import aiosmtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from dotenv import load_dotenv

load_dotenv()

smtp_hostname = os.getenv('SMTP_HOST_NAME')
smtp_port = int(os.getenv('SMTP_PORT', 587)) #587 -> standard port for mail submission
smtp_username = os.getenv('SMTP_USERNAME')
smtp_password = os.getenv('SMTP_PASSWORD')


templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
env = Environment(loader=FileSystemLoader(templates_dir), autoescape=select_autoescape(['html', 'xml']))


async def send_email(to_email: str, subject: str, context: dict):
    template = env.get_template('email_template.html')
    html_content = template.render(context)
    
    message = EmailMessage()
    message["from"] = smtp_username
    message["to"] = to_email
    message["subject"] = subject
    message.set_content("This is a plain content") 
    message.add_alternative(html_content, subtype="html")
    
    try:
        await aiosmtplib.send(
            message,
            hostname=smtp_hostname,
            port=smtp_port,
            username=smtp_username,
            password=smtp_password,
            start_tls=True
        )
        print("Email sent successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email in file email_Service.py: {e}")
