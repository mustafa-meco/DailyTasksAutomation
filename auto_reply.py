import imaplib
import smtplib
from email.mime.text import MIMEText


# Function to send an email
def send_email(subject, body, to_email, sender_email, sender_password):
    try:
        msg = MIMEText(body)
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")

# Function for auto-reply service
def auto_reply(email, password, reply_message, log_text, stop_flag):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email, password)
        mail.select('inbox')

        while not stop_flag["stop"]:
            status, emails = mail.search(None, 'UNSEEN')
            if status == "OK":
                for email_id in emails[0].split():
                    status, email_data = mail.fetch(email_id, '(RFC822)')
                    email_msg = email_data[0][1].decode('utf-8')

                    # Placeholder for sender email extraction (adjust based on email structure)
                    sender_email = "example_sender@example.com"  # Replace with parsing logic
                    
                    send_email("Auto-reply", reply_message, sender_email, email, password)
                    log_text.insert("end", f"Replied to {sender_email}\n")
            
            log_text.see("end")  # Auto-scroll log
    except Exception as e:
        log_text.insert("end", f"Error: {e}\n")