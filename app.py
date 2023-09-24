import requests
from bs4 import BeautifulSoup
import smtplib
import time

# Global variable to store the last declared result
last_declared_result = ""
defined_result = "Result of BE SEM 4" # you have to replace your desired result text with this
email_sender = 0

# Function to scrape GTU results and send the last result
def scrape_gtu_results():
    global last_declared_result
    global email_sender


    # Make a GET request to the GTU result page
    url = "https://gtu.ac.in/result.aspx"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the HTML elements containing result information
        result_items = soup.find("h3", class_="Content")  # Replace with your actual li class

        if result_items:
            # Get the last result item (most recent result)
            last_result_item = result_items
            # Extract the text from the last result item
            latest_result = last_result_item.get_text()
            result_link=result_items.find("a").get("href")
            final_msg = latest_result + result_link

            # Compare with the last declared result
            if latest_result.startswith(defined_result):
                    
                # Send the email three times
                if email_sender < 3:
                    for _ in range(3):
                        send_email("New GTU Result Declared", final_msg)
                        email_sender += 1
                        time.sleep(5)
                    last_declared_result = latest_result
                    print("New result link starts with the defined keyword.")
                else:
                    print("Email has already been sent 3 times. Exiting.")
                    exit()
            else:
                print("New result link does not start with the defined keyword.")
        else:
            print("No result items found on the page.")
    else:
        print("Failed to retrieve the page.")

# Function to send email notification (unchanged from previous code)
def send_email(subject, message):
    # SMTP server and port for Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    sender_email = "your_email@gmail.com"
    sender_password = "your_email_password" #you have to create an app password from your google account please refer to this link if you don't know how to create one "https://www.youtube.com/watch?v=hXiPshHn9Pw&pp=ygUSYXBwIHBhc3N3b3JkIGdtYWls"
    receiver_email = "receiver_email@gmail.com"

    # Create an SMTP connection
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Compose the email
    email_content = f"Subject: {subject}\n\n{message}"

    # Send the email
    server.sendmail(sender_email, receiver_email, email_content)

    # Close the SMTP connection
    server.quit()

def is_between_4pm_and_8pm():
    current_time = time.localtime()
    current_hour = current_time.tm_hour

    # Convert current hour to Indian Standard Time
    current_hour_in_ist = (current_hour + 5) % 24

    return current_hour_in_ist >= 16 and current_hour_in_ist < 20

while True:
    if is_between_4pm_and_8pm():
        scrape_gtu_results()
        if email_sender >= 3:
            break
    else:
        print("Not within the specified time frame.")
    time.sleep(60)  # Check for new results every minute