import sendgrid
from sendgrid.helpers.mail import Mail, Email, To,Content

def alertMail(to_email,subject,content):
    try:
        sg = sendgrid.SendGridAPIClient(api_key="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")
        # from_email = Email("mohankumar.it.2001@gmail.com")  
        # to_email = To(to_email)  
        # content = Content("text/html", content)
        # mail = Mail(from_email, to_email, subject, content)
        # mail_json = mail.get()
        # response = sg.client.mail.send.post(request_body=mail_json)
        # print(response.status_code)
        # print(response.headers)
    except Exception as e: print("\n\n---------------------------------------------------------\n\nEMAILING ERROR:",e,"\n\n---------------------------------------------------------\n\nEMAILING ERROR:")
        # print("Just few hiccups")
