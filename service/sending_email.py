import smtplib
from email.message import EmailMessage


def sending_email(data):
    email_address = "hieu.dh3t1@gmail.com"
    email_password = "mgcduoaczanjwwzk"
    # create email
    msg = EmailMessage()
    msg['Subject'] = "Email subject"
    msg['From'] = email_address
    msg['To'] = data.get('email')  # type Email
    msg.set_content(
        f"""\
    Name : {data.get('name')}
    Email : {data.get('email')}
    Message : {data.get('message')}    
    """,

    )
    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

    return "email successfully sent"
