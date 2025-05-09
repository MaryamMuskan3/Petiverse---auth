import smtplib
from email.mime.text import MIMEText
import random
import string

EMAIL_ADDRESS = "noreply.petiverse@gmail.com"
EMAIL_PASSWORD = "morxbkwqyknwdnkc"

def generate_otp(length=6):
    """Generate a numeric OTP of given length (default is 6 digits)."""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(to_email: str, otp: str):
    subject = "Your OTP Code - Petiverse"
    body = f"Petiverse Account Verification\n\nYour OTP code is: {otp}\nDon't share this code with anyone."

    msg = MIMEText(body)
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Email send failed: {e}")
        return False
