import smtplib
from email.message import EmailMessage

from fastapi import Body

from config import SMTP_PASSWORD, SMTP_USER
from schemas.ad import AdListSchema

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def get_email_template(payload: AdListSchema = Body()):
    email = EmailMessage()
    email['Subject'] = 'Размещение рекламы'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    email.set_content(
        '<div>'
        f'<h1 style="color: Black;">Заявка на рекламу от пользователя: {payload.user_name}.</h1>'
        '<h3>Информация:</h3>'
        f'<h4>Название заведения: {payload.name}</h4>'
        f'<h4>Город и адрес заведения: {payload.city}, {payload.address}</h4>'
        f'<h4>Тариф: {payload.price}</h4>'
        
        # '-management-dashboard-ui-design-template-suitable-designing-application-for-android-and-ios-clean-style-app'
        # '-mobile-free-vector.jpg" width="600">'
        f'<p>Пожалуйста, ответьте клиенту оперативно и подробно на почту {payload.email}</p>'
        '</div>',
        subtype='html'
    )
    return email


def send_email(username: str):
    email = get_email_template(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
