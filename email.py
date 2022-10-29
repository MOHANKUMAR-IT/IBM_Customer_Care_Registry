from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='mohankumar.it.2001@gmail.com',
    to_emails='mohankumar@student.tce.edu',
    subject='TESTING MAIL MOKI',
    html_content='<strong>THANKS & REGARDS NAGALAKSHMI SUBRAMANIAN</strong>')
try:
    #sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
    sg = SendGridAPIClient('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')
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)