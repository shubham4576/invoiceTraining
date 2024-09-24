import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
load_dotenv()

# Email account credentials
username = "passion.testing1@gmail.com"
password = os.getenv("GMAILKEY_AK")
# print(password)

if not password:
    print("Error: Email password not found. Please check your environment variables.")
    exit(1)

# Directory to save attachments
attachment_dir = "/home/trainee/Project/InvoicePOC/mailPdfs/"
os.makedirs(attachment_dir, exist_ok=True)

# Connect to the server
try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    print("Connected to the server.")
except Exception as e:
    print(f"Failed to connect to the server: {e}")
    exit(1)

# Login to your account
try:
    mail.login(username, password)
    print("Login successful!")
except imaplib.IMAP4.error as e:
    print(f"LOGIN failed: {e}")
    exit(1)

# Select the mailbox you want to use (e.g., Inbox)
try:
    mail.select("inbox")
    print("Mailbox selected.")
except imaplib.IMAP4.error as e:
    print(f"Failed to select mailbox: {e}")
    mail.logout()
    exit(1)

# Search for all emails in the selected mailbox
try:
    status, data = mail.search(None, "ALL")
    if status != "OK":
        print(f"Failed to search emails: {status}")
        mail.logout()
        exit(1)
    print("Email search completed.")
except imaplib.IMAP4.error as e:
    print(f"Failed to search emails: {e}")
    mail.logout()
    exit(1)

# Get list of email IDs
email_ids = data[0].split()
email_ids.reverse()

# Flag to track if we have downloaded any PDFs
pdfs_downloaded = False

for email_id in email_ids:
    try:
        # Fetch the email by ID
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        if status != "OK":
            print(f"Failed to fetch email ID {email_id}: {status}")
            continue

        # Parse the email content
        msg = email.message_from_bytes(msg_data[0][1])
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        
        # Check for the specific subject
        if subject.lower() == "invoice":
            # Extract email parts and save PDF attachments
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

    except Exception as e:
        print(f"Failed to process email ID {email_id}: {e}")

    # Exit if PDFs have been downloaded
    if pdfs_downloaded:
        break

# Logout and close the connection
mail.logout()
print("Logged out and closed the connection.")