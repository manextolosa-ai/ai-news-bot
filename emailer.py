import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def send_email(content: str) -> None:
    email_from = _require_env("EMAIL_FROM")
    email_to = _require_env("EMAIL_TO")
    email_password = _require_env("EMAIL_PASSWORD")

    msg = MIMEText(content, _subtype="plain", _charset="utf-8")
    msg["Subject"] = str(Header("🧠 AI Daily Brief", "utf-8"))
    msg["From"] = email_from
    msg["To"] = email_to

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email_from, email_password)
    server.send_message(msg)
    server.quit()
