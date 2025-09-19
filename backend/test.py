"""import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Set your API key (you can also set it as an environment variable)
SENDGRID_API_KEY = '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'

message = Mail(
    from_email='cmi.city.eu@gmail.com',  # Verified sender
    to_emails='bine.tavcar@gmail.com',
    subject='Hello from Python!',
    html_content='<strong>This is a test email sent using SendGrid!</strong>'
)

try:
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    print(f'Status code: {response.status_code}')
    print(f'Response body: {response.body}')
    print(f'Response headers: {response.headers}')
except Exception as e:
    print(e)
"""

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, DynamicTemplateData

SENDGRID_API_KEY = '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'

message = Mail(
    from_email='cmi.city.eu@gmail.com',  # Verified sender
    to_emails='bine.tavcar@gmail.com',
)
message.template_id = 'd-a2cf4800999b4d3b9ab3f8c62e511206'

# Dynamic values for placeholders in your template
message.dynamic_template_data = {
    'first_name': 'John',
}

try:
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    print(f'Status code: {response.status_code}')
except Exception as e:
    print(e)
