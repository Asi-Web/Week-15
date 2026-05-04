## Asiwome Agbleze
## CMSC 111/1 -4: Login Automation and Welcome Message
## Spring 2026

# login_scraper.py
# This program logs into a dummy practice website and extracts the welcome message.
# It uses requests.Session() so cookies persist after login.
# It uses BeautifulSoup to parse the HTML response and find the message in the
# element with id="flash".
#
# Error handling included:
# - If the login page cannot be loaded, it prints:
#   Failed to load login page.
# - If the login attempt does not succeed, it prints:
#   Login failed.
# - It also handles request exceptions and missing HTML elements safely.

import requests
from bs4 import BeautifulSoup

LOGIN_URL = "https://the-internet.herokuapp.com/login"
POST_URL = "https://the-internet.herokuapp.com/authenticate"

USERNAME = "tomsmith"
PASSWORD = "SuperSecretPassword!"


def clean_flash_text(text):
    """Remove extra whitespace and the close-button character from the flash message."""
    return " ".join(text.replace("×", "").split()).strip()


def main():
    """Run the login scraper."""
    try:
        with requests.Session() as session:
            # Step 1: Load the login page first
            try:
                login_page_response = session.get(LOGIN_URL, timeout=10)

                if login_page_response.status_code != 200:
                    print("Failed to load login page.")
                    return

            except requests.RequestException:
                print("Failed to load login page.")
                return

            # Step 2: Submit login form data
            payload = {
                "username": USERNAME,
                "password": PASSWORD
            }

            try:
                login_response = session.post(POST_URL, data=payload, timeout=10)
                login_response.raise_for_status()
            except requests.RequestException:
                print("Login failed.")
                return

            # Step 3: Parse the returned page and find the flash message
            soup = BeautifulSoup(login_response.text, "html.parser")
            flash_message = soup.find(id="flash")

            if flash_message is None:
                print("Login failed.")
                return

            message_text = clean_flash_text(flash_message.get_text())

            # Step 4: Check whether login really succeeded
            # The site shows a success message for correct credentials.
            if "You logged into a secure area!" in message_text:
                print(f"Welcome message: {message_text}")
            else:
                print("Login failed.")

    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    main()
    