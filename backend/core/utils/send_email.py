from flask_mail import Message
from core.extensions import mail

def send_email(recipient, subject, body, attachments=None):
    msg = Message(
        sender="mediflow@example.com",
        recipients=[recipient],
        subject=subject,
        body=body
    )
    if attachments:
        for file in attachments:
            msg.attach(
                filename=file["filename"],
                content_type=file["content_type"],
                data=file["data"]
            )
    mail.send(msg)