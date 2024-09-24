import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
import time
import json

load_dotenv()

# Email account credentials
username = "passion.testing1@gmail.com"
password = os.getenv("GMAILKEY_AK")

if not password:
    print("Error: Email password not found. Please check your environment variables.")
    exit(1)

# Directory to save attachments
attachment_dir = "/home/trainee/Project/InvoicePOC/mailPdfs"
os.makedirs(attachment_dir, exist_ok=True)

# File to store processed email IDs
processed_ids_file = "processed_email_ids.json"

# Load processed email IDs from file
def load_processed_ids():
    if os.path.exists(processed_ids_file):
        with open(processed_ids_file, "r") as f:
            return set(json.load(f))
    return set()

# Save processed email IDs to file
def save_processed_ids(processed_ids):
    with open(processed_ids_file, "w") as f:
        json.dump(list(processed_ids), f)

# Function to connect and login to the email server
def connect_to_email():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        print("Connected to the server.")
        mail.login(username, password)
        print("Login successful!")
        mail.select("inbox")
        print("Mailbox selected.")
        return mail
    except Exception as e:
        print(f"Failed to connect/login/select mailbox: {e}")
        exit(1)

# Function to fetch new emails
def fetch_emails(mail, processed_ids):
    try:
        status, data = mail.search(None, "ALL")
        if status != "OK":
            print(f"Failed to search emails: {status}")
            return

        email_ids = data[0].split()
        email_ids.reverse()

        pdfs_downloaded = False

        for email_id in email_ids:
            if email_id in processed_ids:
                continue

            try:
                status, msg_data = mail.fetch(email_id, "(RFC822)")
                if status != "OK":
                    print(f"Failed to fetch email ID {email_id}: {status}")
                    continue

                msg = email.message_from_bytes(msg_data[0][1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                
                if subject.lower() == "invoice":
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
            
                            if "attachment" in content_disposition:
                                filename = part.get_filename()
                                if filename and filename.lower().endswith(".pdf"):
                                    filepath = os.path.join(attachment_dir, filename)
                                    with open(filepath, "wb") as f:
                                        f.write(part.get_payload(decode=True))
                                    print(f"Saved PDF attachment: {filename}")
                                    pdfs_downloaded = True

                # Add the email ID to the processed set
                processed_ids.add(email_id.decode("utf-8"))

            except Exception as e:
                print(f"Failed to process email ID {email_id}: {e}")

            if pdfs_downloaded:
                break

    except imaplib.IMAP4.error as e:
        print(f"Failed to search emails: {e}")

# Keep a persistent connection and check for new emails
def main():
    processed_ids = load_processed_ids()
    mail = connect_to_email()
    try:
        while True:
            fetch_emails(mail, processed_ids)
            save_processed_ids(processed_ids)
            time.sleep(10)  # Check for new emails every 5 minutes
    except KeyboardInterrupt:
        print("Program interrupted. Logging out and exiting...")
    finally:
        mail.logout()
        print("Logged out and closed the connection.")

if __name__ == "__main__":
    main()
