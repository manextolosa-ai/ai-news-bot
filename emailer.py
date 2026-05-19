import os
import smtplib
from email.mime.text import MIMEText

def send_email(content):
    msg = MIMEText(content)
    msg["Subject"] = "🧠 AI Daily Brief"
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = os.getenv("EMAIL_TO")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(
        os.getenv("EMAIL_FROM"),
        os.getenv("EMAIL_PASSWORD")
    )

    server.send_message(msg)
    server.quit()
