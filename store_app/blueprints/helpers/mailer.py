from flask_mail import Message

from store_app.extensions import mail


def send_email(to, subject, template):
    msg = Message(
        recipients=[to],
        subject=subject,
        html=template
    )
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print e.message
        print "Send mail failed"
    return False


def send_confirmation_email(to, token, subject="Please confirm your email"):

    template = "<p>To begin using your account, please <a href='http://localhost:8080/confirm?token=" \
               + token + "'>confirm your email</a></p>"

    return send_email(to, subject, template)
