from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, DynamicTemplateData
import os

def sendEmail(email, link):
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY") 

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