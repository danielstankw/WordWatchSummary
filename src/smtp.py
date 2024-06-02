from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
import os
import json
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def send_mail():
    # Load the .env file
    load_dotenv()

    email_password = os.getenv("EMAIL_PASSWORD")
    email_sender = os.getenv("EMAIL_SENDER")
    email_receiver = os.getenv("EMAIL_RECEIVER")

    # Ensure required environment variables are set
    if not email_password or not email_sender or not email_receiver:
        raise ValueError(
            "Required environment variables (EMAIL_PASSWORD, EMAIL_SENDER, EMAIL_RECEIVER) are missing."
        )

    # Define the path to the directory containing JSON files
    directory = "./data/summary"

    subject = "Your Daily update"

    articles = []

    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        # Construct the full path to the file
        filepath = os.path.join(directory, filename)

        # Read the JSON data from the file
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Extract the URL and Summary from the JSON data
            link = data["url"]
            description = data["summary"]

            # Add the link and description to the articles list
            articles.append({"link": link, "description": description})

    # Print the populated articles list
    # print(articles)

    # Create HTML content for the email
    html_content = "<html><body>"
    html_content += "<h2>Article Updates</h2>"

    for article in articles:
        html_content += f"<p><a href='{article['link']}'>{article['link']}</a><br>{article['description']}</p><hr>"

    html_content += "</body></html>"

    email = EmailMessage()
    email["From"] = email_sender
    email["To"] = email_receiver
    email["Subject"] = subject
    email.set_content(html_content, subtype="html")

    context = ssl.create_default_context()


    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, email.as_string())
        logging.info("Email sent successfully.")
    except smtplib.SMTPAuthenticationError:
        print("Failed to authenticate with the SMTP server. Check your email and password.")
    except smtplib.SMTPRecipientsRefused:
        print("The recipient address was refused by the server.")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
