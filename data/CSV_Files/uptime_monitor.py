## Asiwome Agbleze
## CMSC 111/1 -Assignment 3
## Spring 2026


# uptime_monitor.py
# This program checks whether a website is online.
# If the website is down, it sends an email alert.
# It also writes every check to a log file named uptime_log.txt.
#
# Beginner-friendly notes:
# - requests is used to send the website check
# - datetime is used to add a timestamp
# - os is used to read environment variables for email settings
# - smtplib and email.message are used to send email alerts
# - a small state file is used to remember whether the website was last ONLINE or DOWN
# - try/except blocks are used for error handling

import os
from pathlib import Path
from datetime import datetime
import requests
import smtplib
from email.message import EmailMessage


# -----------------------------
# SETTINGS YOU CAN CHANGE
# -----------------------------
URL_TO_CHECK = "https://example.com"
TIMEOUT_SECONDS = 5

# Gmail example:
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# File names
LOG_FILE = "uptime_log.txt"
STATE_FILE = "last_state.txt"


def get_timestamp():
    """Return the current date and time as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def load_last_state():
    """Read the last known website state from the state file."""
    state_path = Path(STATE_FILE)

    if state_path.exists():
        try:
            return state_path.read_text(encoding="utf-8").strip()
        except Exception:
            return "UNKNOWN"

    return "UNKNOWN"


def save_last_state(state):
    """Save the current website state to the state file."""
    state_path = Path(STATE_FILE)

    try:
        state_path.write_text(state, encoding="utf-8")
    except Exception as error:
        print(f"Could not save state file: {error}")


def write_log_line(url, status, details):
    """Append one line to uptime_log.txt."""
    timestamp = get_timestamp()
    log_line = f"{timestamp} - {url} - {status} - {details}\n"

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(log_line)
    except Exception as error:
        print(f"Could not write to log file: {error}")


def send_email_alert(url, timestamp, details):
    """
    Send an email alert when the website goes down.
    Uses environment variables instead of hard-coded credentials.
    """
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    email_to = os.getenv("EMAIL_TO")

    if not email_user or not email_pass or not email_to:
        print("Email credentials not found. Please configure your settings.")
        return

    subject = "Website Down Alert"
    body = (
        f"The website appears to be down.\n\n"
        f"URL: {url}\n"
        f"Time: {timestamp}\n"
        f"Details: {details}\n"
    )

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = email_user
    message["To"] = email_to
    message.set_content(body)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.send_message(message)

        print("Email alert sent.")
    except Exception as error:
        print(f"Could not send email alert: {error}")


def check_website():
    """
    Check the website and return:
    - status: ONLINE or DOWN
    - details: status code or error message
    """
    try:
        response = requests.get(URL_TO_CHECK, timeout=TIMEOUT_SECONDS)

        if 200 <= response.status_code <= 399:
            return "ONLINE", f"Status code {response.status_code}"
        else:
            return "DOWN", f"Status code {response.status_code}"

    except requests.Timeout:
        return "DOWN", "Request timed out"

    except requests.ConnectionError:
        return "DOWN", "Connection failed"

    except requests.RequestException as error:
        return "DOWN", f"Request error: {error}"

    except Exception as error:
        return "DOWN", f"Unexpected error: {error}"


def main():
    """Main function for running one website check."""
    current_time = get_timestamp()
    last_state = load_last_state()

    status, details = check_website()

    print(f"{status} - {current_time} - {URL_TO_CHECK}")
    write_log_line(URL_TO_CHECK, status, details)

    # Send one email only when the site changes from not-DOWN to DOWN
    if status == "DOWN" and last_state != "DOWN":
        send_email_alert(URL_TO_CHECK, current_time, details)

    # Save the new state for the next run
    save_last_state(status)


if __name__ == "__main__":
    main()
    