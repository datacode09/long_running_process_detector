import logging
import time
from sendEmail import sendErrorEmail
import psutil

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
RECIPIENTS = ['abul.fahad@rbc.com']

def send_email(subject, message, dry_run):
    logging.info(message)
    if not dry_run:
        sendErrorEmail(RECIPIENTS, subject, message)
    logging.info("Email Sent")

def long_running_process_monitor(threshold):  # 30 minutes
    long_running_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'create_time', 'cmdline']):
        if time.time() - proc.info['create_time'] > threshold:
            if proc.info['cmdline'] and ('python' in proc.info['cmdline'][0] or 'sh' in proc.info['cmdline'][0]):
                long_running_processes.append(proc.info)
    return long_running_processes


def main():
    subject = "Long Running Process Alert"
    dry_run = False

    long_running_processes = long_running_process_monitor()
    if long_running_processes:
        message = "Long running processes detected:\n\n" + "\n".join(f"{proc['name']} (PID: {proc['pid']})" for proc in long_running_processes)
        send_email(subject, message, dry_run)

if __name__ == "__main__":
    main()
