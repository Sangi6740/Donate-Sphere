import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_emails(sender_email, sender_password, recipient_emails, subject, body):
    """
    Function to send emails to multiple recipients.

    Parameters:
        sender_email (str): Sender's email address.
        sender_password (str): Sender's email password.
        recipient_emails (list): List of recipient email addresses.
        subject (str): Email subject.
        body (str): Email body.

    Returns:
        None
    """
    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send email to each recipient
        for recipient_email in recipient_emails:
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            text = message.as_string()
            server.sendmail(sender_email, recipient_email, text)

        # Close SMTP server
        server.quit()
        print("Emails sent successfully!")

    except Exception as e:
        print("Error:", e)

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123",
    database="project"
)
cursor = conn.cursor()

# Retrieve email addresses from the database
cursor.execute("SELECT email FROM donation d, details de WHERE d.username = de.username AND donation_type='Blood'")

emails = cursor.fetchall()

# Close database connection
cursor.close()
conn.close()

# Email configuration
sender_email = "sangeethar159@gmail.com"
sender_password = "sreeramapuri"
subject = "Blood Donation"
body = "if there is any blood donation camps present, you will be notified about it."

# Call the function to send emails
send_emails(sender_email, sender_password, [email[0] for email in emails], subject, body)

