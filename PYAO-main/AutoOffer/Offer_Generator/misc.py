import asyncio, time, pickle, os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import imaplib, subprocess
import email
from AutoOffer import settings
import inspect, re

#This will help get the line being called
def line():
    caller_frame = inspect.currentframe().f_back
    caller_line = inspect.getframeinfo(caller_frame).lineno
    return caller_line

def get_parent_element(element, parent_lvl):
    if parent_lvl == 0:
        return element

    element = element.find_element(By.XPATH, value='..')
    return get_parent_element (element, parent_lvl=parent_lvl-1)

'''
NON-SYNC FUNCTION
'''
def check_element_exists_BLOCK(browser, css_selector, timeout=None, count=10, calling_line=None):
    start_time = time.time()
    counter = 0

    while True:
        try:
            # Find the element using the CSS selector
            element = browser.find_element(By.CSS_SELECTOR, css_selector)
            if element.is_displayed() and element.is_enabled():
                return element  # Return the element when found
        except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
            pass  # Continue checking if the element is not found

        # Add a delay before checking again
        time.sleep(0.5)

        if counter % count == 0:
            print(f"Checking element... (called from line {calling_line})")  # Print the calling line every 60 iterations

        if timeout and time.time() - start_time >= timeout:
            break  # Stop the loop if timeout is reached

    return None  # Return None if element is not found within the timeout

def check_element_exists_XPATH(browser, xpath, timeout=None, count=10, calling_line=None):
    start_time = time.time()
    counter = 0

    while True:
        try:
            # Find the element using the CSS selector
            element = browser.find_element(By.XPATH, xpath)
            if element.is_displayed() and element.is_enabled():
                return element  # Return the element when found
        except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
            pass  # Continue checking if the element is not found

        # Add a delay before checking again
        time.sleep(0.5)

        if counter % count == 0:
            print(f"Checking element... (called from line {calling_line})")  # Print the calling line every 60 iterations

        if timeout and time.time() - start_time >= timeout:
            break  # Stop the loop if timeout is reached

    return None  # Return None if element is not found within the timeout

def wait_until_disappeared_BLOCK(browser, css_element, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = browser.find_element(By.CSS_SELECTOR, css_element)
            if not element.is_displayed():
                return True
        except (NoSuchElementException, StaleElementReferenceException):
            return True
        time.sleep(0.5)  # Polling interval
    print(f"Element still there: {css_element}")
    return False

# Check to see if element is displayed and clickable
def wait_until_appeared_BLOCK(browser, css_element, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = browser.find_element(By.CSS_SELECTOR, css_element)
            if element.is_displayed() and element.is_enabled():
                print('element can be clicked')
                return True
        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException):
            pass
        time.sleep(0.5)  # Polling interval
    print(f"Cannot find: {css_element}")
    return False

def wait_until_disappeared_element_BLOCK(element, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if not element.is_displayed():
                return True
        except (NoSuchElementException, StaleElementReferenceException):
            return True
        time.sleep(0.5)  # Polling interval
    print(f"Element still there: {element}")
    return False

# Check to see if element is displayed and clickable
def wait_until_appeared_element_BLOCK(element, timeout=10):

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if element.is_displayed() and element.is_enabled():
                return True
        except (StaleElementReferenceException, NoSuchElementException):
            pass
        time.sleep(0.5)  # Polling interval
    print(f"(Cannot find: {element}")
    return False

# Check to see if input element has a value
def wait_until_value_appeared_BLOCK(browser, css_element, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = browser.find_element(By.CSS_SELECTOR, css_element)
            if element.get_attribute("value"):
                return True
        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException):
            pass
        time.sleep(0.5)  # Polling interval
    print(f"Cannot find: {css_element}")
    return False

# Check to see if input element has a value
def wait_until_value_appeared_element_BLOCK(element, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if element.get_attribute("value"):
                return True
        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException):
            pass
        time.sleep(0.5)  # Polling interval
    print(f"Cannot find: element")
    return False

# Check to see if input element does not has a value
def wait_until_value_disappeared_BLOCK(browser, css_element, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = browser.find_element(By.CSS_SELECTOR, css_element)
            if not element.get_attribute("value"):
                return True
        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException):
            pass
        time.sleep(0.5)  # Polling interval
    print(f"Cannot find: {css_element}")
    return False

# Check to see if input element does not has a value
def wait_until_value_disappeared_element_BLOCK(element, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if not element.get_attribute("value"):
                return True
        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException):
            pass
        time.sleep(0.5)  # Polling interval
    print(f"Cannot find: element")
    return False

# Define main function for read
def main_read_BLOCK(path):
    with open (path, 'rb') as file: 
        return pickle.load(file)

# Define main function for read
def main_write_BLOCK(path, data):
    with open(path, 'wb') as file:
        pickle.dump(data, path)

def add_weeks_and_get_business_day(weeks):
    # Get today's date
    today = datetime.today()

    # Add specified number of weeks to today's date
    future_date = today + timedelta(weeks=weeks)

    # Check if the resulting date falls on a weekend (Saturday or Sunday)
    if future_date.weekday() >= 5:  # Saturday is 5, Sunday is 6
        # Increment the date until it is a weekday (Monday to Friday)
        while future_date.weekday() >= 5:
            future_date += timedelta(days=1)

    # Format the date as "MAY 5, 2023"
    formatted_date = future_date.strftime("%b %d, %Y").upper()

    return formatted_date

def wait_for_file(file_path, timeout=60, poll_interval=1):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.isfile(file_path):
            return True
        time.sleep(poll_interval)
    return False


"""
Code for extracting data from Emails
"""
def extract_data(msg):
    # Extract the desired data from the email message
    # Modify this function to extract the relevant data based on your requirements
    subject = msg['Subject']
    sender = msg['From']
    body = ''

    if msg.is_multipart():
        for part in msg.get_payload():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode('utf-8')
                break
    else:
        body = msg.get_payload(decode=True).decode('utf-8')

    # Return the extracted data as a string
    return body

def main(EMAIL_ADDRESS, EMAIL_PASSWORD, FOLDER_NAME):
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(settings.IMAP_SERVER, settings.IMAP_PORT)
    mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    # Select the folder
    mail.select(FOLDER_NAME)

    # Search for unread email messages in the folder
    result, data = mail.search(None, 'ALL')
    if result == 'OK':
        email_ids = data[0].split()
        for email_id in email_ids:
            # Fetch the email data
            result, msg_data = mail.fetch(email_id, '(RFC822)')
            if result == 'OK':
                raw_email = msg_data[0][1]
                # Parse the raw email data
                msg = email.message_from_bytes(raw_email)
                # print(msg)

                # This will remove the email from the current folder, so that the next email will be recognized
                # when it comes in
                mail.store(email_id, '+FLAGS', '\\Deleted')

                # Expunge the deleted emails from the folder
                mail.expunge()

                # Disconnect from the server
                mail.logout()

                # Process the email
                return extract_data(msg)

    # Disconnect from the server
    mail.logout()


"""
Funtion to input code
"""
    # Checking to ensure authorization code went through
def input_code(browser, code_num):
    for index, num in enumerate(str(code_num), start=1):
        element = f"#app > div:nth-child(1) > div.undefined.flex.v2-open.sidebar-v2-agency > section > div.hl_login--body > div > div > div > div > div.form-group.mt-4 > div > div > div:nth-child({index}) > input"
        browser.find_element(By.CSS_SELECTOR, element).send_keys(num)
        # print(num)

# For spliting lists
def split_list_evenly(list, num_splits):
    split_size = len(list) // num_splits
    remainder = len(list) % num_splits

    splits = []
    start = 0

    for _ in range(num_splits):
        split_end = start + split_size + (1 if remainder > 0 else 0)
        splits.append(list[start:split_end])
        start = split_end
        remainder -= 1

    return splits

# For focusing on a particular window
def bring_window_to_front(window_title):
    if os.name == 'nt':  # Check if the operating system is Windows
        try:
            # Use the `subprocess` module to run a PowerShell command to bring the window to the front
            subprocess.run(["powershell.exe", "(Get-Process -Name '" + window_title + "').MainWindowHandle | ForEach-Object { (New-Object -TypeName System.Windows.Interop.HwndSourceParameters -ArgumentList $_).Handle } | ForEach-Object { [System.Windows.Interop.HwndSource]::FromHwnd($_).RootVisual.Dispatcher.Invoke([System.Action]{ }) }"])
        except Exception as e:
            print("Error:", e)
    else:
        print("This functionality is currently only supported on Windows.")

def properize (string):
    # Split the string into words
    words = string.split()

    # Capitalize the first letter of each word
    capitalized_words = [word.capitalize() for word in words]

    # Join the words back together with a space
    formatted_string = " ".join(capitalized_words)

    return formatted_string

def generate_closing_date(days_to_close=14):
    # Get today's date
    today = datetime.now()

    # Calculate the date 2 weeks from today
    closing_date = today + timedelta(days=days_to_close)

    # Check if it falls on a Saturday or Sunday
    if closing_date.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
        # If it's a Saturday or Sunday, add the necessary days to get to Monday
        days_until_monday = 7 - closing_date.weekday()
        closing_date += timedelta(days=days_until_monday)

    # Format the result as a string
    closing_date_string = closing_date.strftime("%m/%d/%Y")
    return(closing_date_string)

def rearrange_name(full_name):
    # Split the full name into parts using a comma and space
    name_parts = full_name.split(' ')
    #print(name_parts)

    if len(name_parts) >= 2:
        # Extract the first and last name
        last_name, first_name = name_parts[:2]

        # Reorder the names in the desired format
        formatted_name = f"{first_name} {last_name}"

        return formatted_name
    else:
        # Return the original name if it can't be split as expected
        return full_name

def generate_closing_date(days_to_close=21):
    # Get today's date
    today = datetime.now()

    # Calculate the date 2 weeks from today
    closing_date = today + timedelta(days=days_to_close)

    # Check if it falls on a Saturday or Sunday
    if closing_date.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
        # If it's a Saturday or Sunday, add the necessary days to get to Monday
        days_until_monday = 7 - closing_date.weekday()
        closing_date += timedelta(days=days_until_monday)

    # Format the result as a string
    closing_date_string = closing_date.strftime("%m/%d/%Y")
    return(closing_date_string)

def has_non_empty_string_or_true(tuple):
    return any(x and (isinstance(x, str) and x.strip() != "" or x is True) for x in tuple)

def convert_str_2_float(input_string):
    # This regex pattern will match any character that is NOT a digit or a period
    pattern = r'[^\d.]+'
    # Substitute all matched characters with an empty string
    cleaned_string = re.sub(pattern, '', input_string)
    return float(cleaned_string)