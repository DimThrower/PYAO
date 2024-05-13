import asyncio, time, pickle, aiofiles, os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import imaplib, subprocess
import email
from AutoOffer import settings
import inspect

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


async def check_element_exists(browser, css_selector, timeout=None, count=10, calling_line=None):
    start_time = time.time()
    counter = 0

    while True:
        try:
            # Find the element using the CSS selector
            element = browser.find_element(By.CSS_SELECTOR, css_selector)
            print(f"Element for check_element_exists: {element}")
            if element.is_displayed() and element.is_enabled():
                return element  # Return the element when found
        except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
            pass  # Continue checking if the element is not found

        # Add a delay before checking again
        await asyncio.sleep(0.5)

        if counter % count == 0:
            print(f"Checking element... (called from line {calling_line})")  # Print the calling line every 60 iterations

        if timeout and time.time() - start_time >= timeout:
            break  # Stop the loop if timeout is reached
    print(f"Could not find selector: {css_selector}")
    return None  # Return None if element is not found within the timeout

async def check_only_element_exists(element, timeout=None, count=10, calling_line=None):
    start_time = time.time()
    counter = 0

    while True:
        try:
            # Find the element using the CSS selector
            if element.is_displayed() and element.is_enabled():
                return element  # Return the element when found
        except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
            pass  # Continue checking if the element is not found

        # Add a delay before checking again
        await asyncio.sleep(0.5)

        if counter % count == 0:
            print(f"Checking element... (called from line {calling_line})")  # Print the calling line every 60 iterations

        if timeout and time.time() - start_time >= timeout:
            break  # Stop the loop if timeout is reached

    return None  # Return None if element is not found within the timeout

async def check_elements_exists(browser, css_selector, timeout=None, count=10, calling_line=None):
    start_time = time.time()
    counter = 0

    while True:
        try:
            # Find the elements using the CSS selector
            elements = browser.find_elements(By.CSS_SELECTOR, css_selector)
            return elements  # Return the element when found
        except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
            pass  # Continue checking if the element is not found

        # Add a delay before checking again
        await asyncio.sleep(0.5)

        if counter % count == 0:
            print(f"Checking element... (called from line {calling_line})")  # Print the calling line every 60 iterations

        if timeout and time.time() - start_time >= timeout:
            break  # Stop the loop if timeout is reached

    return None  # Return None if element is not found within the timeout

async def check_element_exists_xpath(browser, xpath, timeout=None, count=10, calling_line=None):
    start_time = time.time()
    counter = 0

    while True:
        try:
            # Find the element using the CSS selector
            element = browser.find_element(By.XPATH, xpath)
            # if element.is_displayed() and element.is_enabled():
            return element  # Return the element when found
        except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
            pass  # Continue checking if the element is not found

        # Add a delay before checking again
        await asyncio.sleep(0.5)

        if counter % count == 0:
            print(f"Checking element... (called from line {calling_line})")  # Print the calling line every 60 iterations

        if timeout and time.time() - start_time >= timeout:
            break  # Stop the loop if timeout is reached

    return None  # Return None if element is not found within the timeout

async def check_element_exists_tag(browser, tag_name, timeout=None, count=10, calling_line=None):
    start_time = time.time()
    counter = 0

    while True:
        try:
            # Find the element using the CSS selector
            element = browser.find_element(By.TAG_NAME, tag_name)
            # if element.is_displayed() and element.is_enabled():
            return element  # Return the element when found
        except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
            pass  # Continue checking if the element is not found

        # Add a delay before checking again
        await asyncio.sleep(0.5)

        counter += 1  # Increment the counter

        if counter % count == 0:
            print(f"Checking element... (called from line {calling_line})")  # Print the calling line every 60 iterations

        if timeout and time.time() - start_time >= timeout:
            break  # Stop the loop if timeout is reached

    return None  # Return None if element is not found within the timeout

async def check_elements_exists_tag(browser, tag_name, timeout=None, count=10, calling_line=None, include_stale=True):
    start_time = time.time()
    counter = 0

    while True:
        try:
            # Find the element using the CSS selector
            element = browser.find_elements(By.TAG_NAME, tag_name)
            return element  # Return the element when found
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            if not include_stale and isinstance(e, StaleElementReferenceException):
                pass  # Continue checking if the element is stale
            else:
                raise e  # Re-raise the exception if it's not a stale element

        # Add a delay before checking again
        await asyncio.sleep(0.5)

        counter += 1  # Increment the counter

        if counter % count == 0:
            print(f"Checking element... (called from line {calling_line})")  # Print the calling line every 60 iterations

        if timeout and time.time() - start_time >= timeout:
            break  # Stop the loop if timeout is reached

    return None  # Return None if element is not found within the timeout


def split_dictionary(dictionary, num_parts):
    dict_length = len(dictionary)
    dict_keys = list(dictionary.keys())

    # Calculate the number of keys in each part
    part_size = dict_length // num_parts
    remaining_keys = dict_length % num_parts

    parts = []
    start_idx = 0

    # Iterate over each part
    for i in range(num_parts):
        end_idx = start_idx + part_size

        # Include remaining keys in the last part
        if i == num_parts - 1:
            end_idx += remaining_keys

        # Create a new dictionary for the current part
        part_dict = {key: dictionary[key] for key in dict_keys[start_idx:end_idx]}

        # Add the part dictionary to the list of parts
        parts.append(part_dict)

        # Update the start index for the next part
        start_idx = end_idx

    return parts

async def wait_until_disappeared(browser, css_element, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = browser.find_element(By.CSS_SELECTOR, css_element)
            if not element.is_displayed():
                print(f'element not present: {css_element}')
                return True
        except (NoSuchElementException, StaleElementReferenceException):
            return True
        await asyncio.sleep(0.5)  # Polling interval
    print(f"Element still there: {css_element}")
    return False

# Check to see if element is displayed and clickable
async def wait_until_appeared(browser, css_element, timeout=None, count=10, calling_line=None):
    start_time = time.time()
    counter = 0

    while True:
        try:
            element = browser.find_element(By.CSS_SELECTOR, css_element)
            # if element.is_displayed() and element.is_enabled():
            print(f'element can be clicked: {css_element}')
            return True
        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException):
            pass
        await asyncio.sleep(0.5)  # Polling 
        
        counter += 1  # Increment the counter

        if counter % count == 0:
            print(f"Checking element... (called from line {calling_line})")  # Print the calling line every 60 iterations

        if timeout and time.time() - start_time > timeout:
            print(f"Cannot find: {css_element}")
            return False

async def wait_until_disappeared_element(element, timeout=None, count=10, calling_line=None):
    start_time = time.time()
    counter = 0  # Initialize the counter variable

    while True:
        try:
            if not element.is_displayed():
                print('element not present')
                return True
        except (NoSuchElementException, StaleElementReferenceException):
            return True
        await asyncio.sleep(0.5)  # Polling interval

        counter += 1  # Increment the counter

        if counter % count == 0:
            print(f"Checking element... (called from line {calling_line})")  # Print the calling line every 60 iterations
        
        if timeout and time.time() - start_time > timeout:
            print(f"Element still there: {element}")
            return False

# Check to see if element is displayed and clickable
async def wait_until_appeared_element(element, timeout=None, count=10, calling_line=None):
    start_time = time.time()
    counter = 0

    while True:
        try:
            if element.is_displayed() and element.is_enabled():
                print('element present')
                return True
        except (StaleElementReferenceException, NoSuchElementException):
            pass
        await asyncio.sleep(0.5)  # Polling interval

        counter += 1  # Increment the counter

        if counter % count == 0:
            print(f"Checking element... (called from line {calling_line})")  # Print the calling line every 60 iterations

        if timeout and time.time() - start_time > timeout:
            print(f"(Cannot find: {element}")
            return False

# Check to see if input element has a value
async def wait_until_value_appeared(browser, css_element, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = browser.find_element(By.CSS_SELECTOR, css_element)
            if element.get_attribute("value"):
                print('value present')
                return True
        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException):
            pass
        await asyncio.sleep(0.5)  # Polling interval
    print(f"Cannot find: {css_element}")
    return False

# Check to see when element with a tag appear
async def wait_until_value_appeared_tag(browser, tag_name, parent_element=None, timeout=10):
    start_time = time.time() 
    while time.time() - start_time < timeout:
        try:
            # Check to see if an parent_element was passed though
            if parent_element:
                element = parent_element.find_element(By.TAG_NAME, tag_name)
                if element.is_displayed() and element.is_enabled():
                    print('value present')
                    return True    
            # If not then just use the browser instance
            else:
                element = browser.find_element(By.TAG_NAME, tag_name)
                if element.is_displayed() and element.is_enabled():
                    print('value present')
                    return True
            
        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException):
            pass
        await asyncio.sleep(0.5)  # Polling interval
    print(f"Cannot find elements with tag name: {tag_name}")
    return False

# Check to see if input element has a value
async def wait_until_value_appeared_xpath(browser, xpath_element, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = browser.find_element(By.XPATH, xpath_element)
            if element.is_displayed() and element.is_enabled():
                print('value present')
                return True
        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException):
            pass
        await asyncio.sleep(0.5)  # Polling interval
    print(f"Cannot find: {xpath_element}")
    return False

# Check to see if input element has a value
async def wait_until_value_disappeared_xpath(browser, xpath_element, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = browser.find_element(By.XPATH, xpath_element)
            if not element.is_displayed() and element.is_enabled():
                print('value not present')
                return True
        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException):
            pass
        await asyncio.sleep(0.5)  # Polling interval
    print(f"Cannot find: {xpath_element}")
    return False

# Check to see if input element has a value
async def wait_until_value_appeared_element(element, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if element.get_attribute("value"):
                print('value present')
                return True
        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException):
            pass
        await asyncio.sleep(0.5)  # Polling interval
    print(f"Cannot find: element")
    return False

# Check to see if input element does not has a value
async def wait_until_value_disappeared(browser, css_element, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = browser.find_element(By.CSS_SELECTOR, css_element)
            if not element.get_attribute("value"):
                print('no value found')
                return True
        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException):
            pass
        await asyncio.sleep(0.5)  # Polling interval
    print(f"Cannot find: {css_element}")
    return False

# Check to see if input element does not has a value
async def wait_until_value_disappeared_element(element, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if not element.get_attribute("value"):
                print('no value found')
                return True
        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException):
            pass
        await asyncio.sleep(0.5)  # Polling interval
    print(f"Cannot find: element")
    return False


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

def convert_to_type(value, target_type):
    try:
        return target_type(value)
    except (ValueError, TypeError):
        return None