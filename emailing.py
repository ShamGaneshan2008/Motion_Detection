import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import imghdr

load_dotenv()

PASSWORD =  os.getenv("EMAIL_PASSWORD")
SENDER = os.getenv("EMAIL_SENDER")
RECEIVER =  os.getenv("EMAIL_RECEIVER")


def send_email(image_path):
    print("send_email function started")

    if not PASSWORD or not SENDER or not RECEIVER:
        raise ValueError("Email credentials not set in environment variables.")

    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hey, we just saw a new customer")

    with open(image_path, "rb") as file:
        data = file.read()

    email_message.add_attachment(data,
                                 maintype="image",
                                 subtype=imghdr.what(None, data))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()
    print("send_email function ended")


if __name__ == "__main__":
    send_email(image_path="images/77.png")

