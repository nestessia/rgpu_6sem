from celery import shared_task
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


@shared_task
def send_email_task(subject, message, from_email, recipient_list):
    try:
        if not all([subject, message, from_email, recipient_list]):
            print("Failed to send email: One or more required parameters are None.")
            return False

        smtp_server = os.getenv('EMAIL_HOST')
        port = os.getenv('EMAIL_PORT')
        password = os.getenv('EMAIL_HOST_PASSWORD')
        # Устанавливаем соединение с SMTP-сервером
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(from_email, password)

        # Создаем объект сообщения
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ', '.join(recipient_list)
        msg['Subject'] = subject

        # Добавляем текст сообщения
        msg.attach(MIMEText(message, 'plain'))

        # Отправляем сообщение
        server.sendmail(from_email, recipient_list, msg.as_string())

        # Закрываем соединение
        server.quit()

        print("Email sent successfully!")
        return True
    except Exception as e:
        print("Failed to send email:", e)
        return False

