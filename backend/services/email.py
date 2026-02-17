from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, DynamicTemplateData
from dotenv import load_dotenv
from pathlib import Path
import os

#load_dotenv(Path(r"D:\python\cmi\final\CMI-2\cmi.env"))
load_dotenv(Path(r"E:\CMI-2\CMI-2\cmi.env"))
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY") 
if not SENDGRID_API_KEY:
    raise RuntimeError("Missing SendGrid API key in environment")

def sendEmail(email, link):


    #$env:SENDGRID_API_KEY="APi key"
    #setx SENDGRID_API_KEY "APi key"
    #setx je permamently
    #set env je za ta session

    message = Mail(
        from_email='cmi.city.eu@gmail.com',
        to_emails= email,
    )
    message.template_id = 'd-a2cf4800999b4d3b9ab3f8c62e511206'
    message.dynamic_template_data = {
        'link': link
    }

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response
    except Exception as e:
        print("ERROR:", e)