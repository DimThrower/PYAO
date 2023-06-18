import asyncio, re, time, traceback, pickle, socket, threading, schedule, aiofiles, asyncio, cProfile
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, NoSuchWindowException, \
    StaleElementReferenceException
from HTML import HTML, PropertyProfile
from HTML_ACTIONS import click, innerHTML_Drill, sim_click
from chrome_settings import custom_chrome_options, un_custom_chrome_options, generate_random_number
#import undetected_chromedriver as uc
from AutoOffer.misc import *
from AutoOffer.db import db_funct
from selenium.webdriver.common.keys import Keys
from AutoOffer import settings
import aiomysql, mysql.connector
import asyncio
import inspect

testing = False

html = HTML ()

pp = PropertyProfile ()

chromeDriverPath = settings.chromeDrivePath

# Initialize browser instance list
browsers = []

# Initialize conns instance list
conns = []

# Set what number of browser to run
browser_num = 1


async def task(browser, task_id, prop_dict_part, cursor):
    # Run GHL checker if there are new updates to HAR
    if prop_dict_part:

        print (f"({task_id}) ({task_id}) Starting task {task_id}")
        print (f'({task_id})-({line ()}) prop_parts: {prop_dict_part}')
        # This is where my code for puting info in Rhino Needs to go
        # and possible 
        try:
            # Go though all the properties assigned to this task
            for prop_dict in prop_dict_part:
                print (f'({task_id})-({line ()}) prop_dict: {prop_dict}')
                if testing:
                    prop_dict = {1: {'Agent First Name': 'Mary',
                                     'Street Address': '233 Johnson Way',
                                     'City': "Houston",
                                     'Zip Code': '77823',
                                     'Bed': 3,
                                     'Bath': 2,
                                     'Half Bath': None,
                                     'HOA': 'Yes',
                                     'State': 'TX',
                                     'Agent Email': 'agent@example.com',
                                     'Agent Cell': '713-453-123',
                                     'Owner Name': None,
                                     'County': 'Harris',
                                     'Subdivision': 'Sterling Lakes',
                                     'Lot': 123,
                                     'Block': 456,
                                     'Legal Description': 'Sterling Lakes Lot 123 Block 456',
                                     'SQFT': 2000,
                                     'Year Built': 1990,
                                     'ARV': 300000,
                                     'Repair': 50000,
                                     'List Price': 250000,
                                     'Offer Amount': 230000,
                                     'Earnest Money': 5000,
                                     'Option Money': 500,
                                     'Option Days': 10,
                                     'Escrow Agent': 'Carrie Morrison',
                                     'Title Company Address': '1111 N Loop W Suite 1100, 77008',
                                     'Title Company': 'StarTex Title (Carrie)',
                                     }
                                 }

                # Get the property details using the mls id
                # prop_dict = prop_dict_part[mls_id]
                print (f'({task_id})-({line ()}) prop_dict: {prop_dict}')

                # Get the current prop_dict
                # curr_prop_dict = prop_dict[prop_dict_keys[0]]
                curr_prop_dict = prop_dict

                # Get just the street name from the address
                # Define the regex patter
                pattern = r"\d+\s+(\w+)"

                # Find the matches, seperates everything by whitespace
                matches = re.search (pattern, curr_prop_dict[pp.steet_address])

                # Get the street_number from the matches
                street_number = matches.group (0)
                print (f"({task_id}) Address to search: {street_number}")

                # Find the opportunities search element
                input_element = await check_element_exists (browser=browser, css_selector=html.innerHTML['GHL']['Main'][
                    'Opportunities Search'], calling_line=line ())

                # Keep running until the Opporutnity Search bar is clear 
                while True:
                    if await wait_until_value_disappeared_element (element=input_element, timeout=0.5):
                        # Make sure you can send keys to the element
                        if await wait_until_appeared_element (element=input_element, calling_line=line ()):

                            (await check_only_element_exists (element=input_element, calling_line=line ())).send_keys (
                                street_number)

                            # Get the current value of the input field
                            # current_value = input_element.get_attribute("value")
                            # Give some time for HTML to proces keeys are there
                            await asyncio.sleep (0.5)

                            # Get the current value of the input field
                            current_value = browser.execute_script (
                                f"return document.querySelector('{html.innerHTML['GHL']['Main']['Opportunities Search']}').value;")

                            # Ensure that the value is there in the text box
                            if current_value == street_number:
                                print (f'({task_id})-({line ()}) Inputted Address into search bar: {street_number}')
                                break
                            else:
                                print (
                                    f'({task_id})-({line ()}) Wrong value found correct value:{street_number} found value:{current_value}')

                    else:
                        # Removing the previous entry via backspace 
                        for _ in range (1, 15):
                            (await check_only_element_exists (element=input_element, calling_line=line ())).send_keys (
                                Keys.BACKSPACE)
                        print (f'({task_id})-({line ()}) Opportunity search bar not clear. Attempt clear again')

                # Wait for the cards to refresh
                await asyncio.sleep (10)

                # Wait for cards to show
                await wait_until_appeared (browser=browser,
                                           css_element=f".{html.innerHTML['GHL']['Main']['Card Class']}", timeout=10,
                                           calling_line=line ())

                # Parse current DOM
                soup = BeautifulSoup (browser.page_source, 'html.parser')

                # Get all the elements with class="card-info"
                card_elements = soup.find_all (class_=html.innerHTML['GHL']['Main']['Card Class'])

                # Sort through each card to see if the street address name matches
                if card_elements:
                    # Interate throught the card elements to see if there is a match
                    for card_element in card_elements:
                        # Find the innerHTML of each card, which should be an address
                        card_innerHtml = innerHTML_Drill (card_element)
                        print (f"({task_id}) card innerHTML: {card_innerHtml}")

                        # Street name would be the second match
                        street_name = matches.group (1)
                        print(f'Card html: {card_innerHtml.lower()}, street address: {street_number.lower()}')

                        # Check for a deal in GHL
                        if card_innerHtml and (street_name.lower() in card_innerHtml.lower()):
                            # Need to pop the property from the matrix before sending it to make offer
                            # print(f"({task_id}) card innerHTML: {card_innerHtml}")
                            print (f'({task_id})-({line ()}) Deal taken')

                            # Continuous loop to ensure the card is clicked, so futher details can be added
                            while True:
                                try:
                                    # Click on the card based on it's innerHTML
                                    card_element = await check_element_exists_xpath (browser=browser,
                                                                                 xpath=f"//*[contains(text(), '{card_innerHtml}')]",
                                                                                 calling_line=f'({task_id})-({line ()})')
                                    # Go up 4 element to get the the over card to click on
                                    # This will open up the opportunity page automatically
                                    get_parent_element(element=card_element, parent_lvl=4).click()
                                    

                                    print (f"({task_id})-({line ()}) Clicking deal card: {card_innerHtml}")
                                    break
                                except (NoSuchElementException, StaleElementReferenceException,
                                        ElementClickInterceptedException):
                                    continue

                            # Wait for first field in page deal
                            await wait_until_appeared (browser=browser,
                                               css_element=html.innerHTML['GHL']['Main']['Contact Name'],
                                               calling_line=f'({task_id})-({line ()})')
                            

                            # Find the drop down list for "Stage"
                            drpdwn_btn = await check_element_exists (browser=browser,
                                                             css_selector=html.innerHTML['GHL']['Main']['Stage'],
                                                             calling_line=f'({task_id})-({line ()})')
                            
                            # Click the drpdwn list
                            drpdwn_btn.click ()     

                            # Click Made offer selection
                            (await check_element_exists(browser=browser,
                                                        css_selector=html.innerHTML['GHL']['Main']['Offer Made'],
                                                        calling_line=f'({task_id})-({line ()})')).click()
                            
                            # Click the update btn
                            (await check_element_exists(browser=browser,
                                                        css_selector=html.innerHTML['GHL']['Main']['Create Button'],
                                                        calling_line=f'({task_id})-({line ()})')).click()
                            
                            # Updated the DB to say
                            await db_funct.async_multi_db_update(cursor=cursor,
                                                                 mls_id=curr_prop_dict[pp.mls_id],
                                                                 data_dict={pp.ghl_offer_made: datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
                                                                 overwrite=True)

                await asyncio.sleep(10)
        #
        except NoSuchWindowException:
            pass

    print (f"({task_id}) Task {task_id} finished")


async def run_tasks(browsers, browser_num):
    queue = asyncio.Queue ()

    # Enqueue initial tasks
    # I think is where the first batch of proprties 
    # will go when the function is first opend
    for i in range (1, 2):
        await queue.put (i)

    # This limits the number of cocurrent operations to 5
    semaphore = asyncio.Semaphore (5)

    # Function the processes an async task
    async def process_task(browser, task_id, cursor, prop_dict_part):
        # Require task to wait aquire a permit from Semaphore 
        async with semaphore:
            # After semaphore grants premit  

            # Await for the completion of the task
            await task (browser, task_id=task_id, cursor=cursor, prop_dict_part=prop_dict_part)
            # finally:
            #     browser.quit()

    while True:
        # Initialize list to store tasks
        tasks = []

        # Continuously retrieves tasks from a queue and 
        # creates asyncio tasks to process them concurrently
        # Check to ensure list is not empty
        while not queue.empty ():
            # Retrieve the latest queued task from queue
            task_id = await queue.get ()

            # Initialize conn listing for the connections
            conns = []
            cursors = []

            # Connect to the database and create a connect for each browser
            for _ in browsers:
                conn = await aiomysql.connect (
                    host=settings.db_host,
                    user=settings.db_user,
                    password=settings.db_password,
                    db=settings.db_name,
                    autocommit=True
                )
                conns.append (conn)

            for conn in conns:
                cursors.append (await conn.cursor ())

            # Get the list of properties that have not been checked with GHL
            properties = await db_funct.async_get_sorted_rows_with_null_and_not_null (cursor=cursors[0], 
                                                                                      sort_column=pp.last_updated,
                                                                                      not_null_list=[pp.offer_sent],
                                                                                      null_list=[pp.ghl_offer_made])
                                                                                        

            # Close the database connectio
            # await conn.close()

            # Check to see if there are any properties to check
            if properties:

                # Split properties evenly amon the browsers
                prop_dict_parts = split_list_evenly (list=properties, num_splits=browser_num)
                print (f"({task_id}) prop_dict_parts: {prop_dict_parts}")

                # Make a task for each part of the dictionary
                for index, prop_dict_part in enumerate (prop_dict_parts):
                    # Create an asyncio task and add it to the task list
                    tasks.append (asyncio.create_task (
                        process_task (browser=browsers[index], task_id=index, cursor=cursors[index],
                                      prop_dict_part=prop_dict_part)))
            else:
                print (f'({task_id})-({line ()}) No properties to switch over, run at next schedule')

        # Check to see if tasks list is empty
        if not tasks:
            # Exit the loop if there are no more tasks
            break

        # Wait for all tasks to complete
        # The "*" unpacks the tasks list into seperate elements
        await asyncio.gather (*tasks)

        # This is where I might use a socket to send more que more tasks
        # Add more tasks dynamically if needed
        # for i in range(len(tasks)):
        #     # Add more tasks to the que
        #     await queue.put(i + 1)


'''
Socket Section

'''

# Global flag to indicate server availability
server_available = True

# Function to handle the scheduled task
def scheduled_task(browsers, browser_num):
    # Check to see if db needs to be created
    db_funct.create_db ()

    global server_available
    if server_available:
        server_available = False
        # Run the tasks
        loop = asyncio.get_event_loop ()
        loop.run_until_complete (run_tasks (browsers, browser_num))
        # for i in range(1,10):
        #     print(i)
        #     time.sleep(1)

        print (f"(Running hourly task...")
        server_available = True

# Function to handle client requests
def handle_client(connection):
    global server_available
    while True:
        try:
            # Receive data from the property program
            received_data = connection.recv (1000)
            if not received_data:
                break

            if server_available:

                # Deserialize the received data using pickle
                deserialized_data = pickle.loads (received_data)
                print (f'Data from client: {deserialized_data}')
                if deserialized_data == 'GO':
                    # Run the hourly task
                    loop = asyncio.get_event_loop ()
                    loop.run_until_complete (run_tasks (browsers, browser_num))

                response = ({'state': "READY", 'request_wait': 0})
                server_available = True
            else:
                # If server is busy, send "BUSY" response and wait 60 seconds before next request
                response = ({'state': "BUSY", 'request_wait': 5})

            # Pickle the response
            pickle_data = pickle.dumps (response)

            # Send the data back to the client
            connection.send (pickle_data)
        except (ConnectionError, ConnectionResetError):
            continue


# Function to accept incoming connections
def accept_connections(socket):
    # While loop keeps socket open to accept connections
    while True:
        # Accept incoming client connection
        connection, addr = socket.accept ()

        # Print a message indicating a new connection from the client's address
        print (f"New connection from: {addr}")

        # Create a new thread to handle client communication
        client_thread = threading.Thread (target=handle_client, args=(connection,))

        # Start the client thread to handle communication with the client
        client_thread.start ()

# Check to see if db needs to be created
db_funct.create_db ()

try:
    for i in range (0, browser_num):
        # Initialize browser instance
        browser = webdriver.Chrome (executable_path=chromeDriverPath)

        # Set email
        email = settings.GHL_USERNAME

        # Set password
        password = settings.GHL_PASSWORD

        # Opening GHL 
        browser.get (html.webaddress['GHL'])

        # Maximize Window
        browser.maximize_window()

        # Make sure we're not already loging into the page by checking for opportunities
        # if not wait_until_appeared_BLOCK(browser=browser, css_element=html.innerHTML['GHL']['Main']['Opportunities'], timeout=30):
        if wait_until_appeared_BLOCK (browser=browser, css_element=html.innerHTML['GHL']['Main']['Login Page'],
                                      timeout=30):
            # await asyncio.sleep(10)
            wait_until_appeared_BLOCK (browser=browser, css_element=html.innerHTML['GHL']['Main']['Email'], timeout=10)

            while wait_until_value_disappeared_BLOCK (browser=browser,
                                                      css_element=html.innerHTML['GHL']['Main']['Email'], timeout=3):
                # Inputting Email
                check_element_exists_BLOCK (browser=browser, css_selector=html.innerHTML['GHL']['Main']['Email'],
                                            calling_line=line ()).send_keys (email)

                # while wait_until_value_disappeared_BLOCK(browser=browser, css_element=html.innerHTML['GHL']['Main']['Password'], timeout=3):
                # Inputting Password
            check_element_exists_BLOCK (browser=browser, css_selector=html.innerHTML['GHL']['Main']['Password'],
                                        calling_line=line ()).send_keys (password)

            # Clicking the Login Button
            check_element_exists_BLOCK (browser=browser, css_selector=html.innerHTML['GHL']['Main']['Login btn'],
                                        calling_line=line ()).click ()

            # Wait until the send security code button is visiable
            wait_until_appeared_BLOCK (browser=browser, css_element=html.innerHTML['GHL']['Main']['Send Secruity btn'],
                                       timeout=500)

            # Clicking the Security btn
            check_element_exists_BLOCK (browser=browser,
                                        css_selector=html.innerHTML['GHL']['Main']['Send Secruity btn'],
                                        calling_line=line ()).click ()

            # Get the code from email
            while True:
                # Get the body of the Security Code Email
                email_body = main (EMAIL_ADDRESS=settings.EMAIL_ADDRESS, EMAIL_PASSWORD=settings.EMAIL_PASSWORD,
                                   FOLDER_NAME=settings.FOLDER_NAME)
                print (f'Body of email: {email_body}')
                if email_body is None:
                    time.sleep (2)
                    continue
                else:
                    # Extract the code from the email body
                    code_numbers = re.findall (r"\d{6}", email_body)[0]
                    print (f'Code Numbers: {code_numbers}')
                    break

            # Input security code
            input_code (browser, code_numbers)

            # Clicking the confirm button
            check_element_exists_BLOCK (browser=browser,
                                        css_selector=html.innerHTML['GHL']['Main']['Send Secruity btn'],
                                        calling_line=line ()).click ()

            # Wait unit the opportunities button in available
            wait_until_appeared_BLOCK (browser=browser, css_element=html.innerHTML['GHL']['Main']['Opportunities'],
                                       timeout=10000)

        # Make sure we're not already loging into the page by checking for opportunities
        wait_until_appeared_BLOCK (browser=browser, css_element=html.innerHTML['GHL']['Main']['Opportunities'],
                                   timeout=10000)

        # Click locations
        check_element_exists_BLOCK (browser=browser, css_selector=html.innerHTML['GHL']['Main']['Locations'],
                                    calling_line=line ()).click ()

        # Wait unit the locations div to show
        wait_until_appeared_BLOCK (browser=browser, css_element=html.innerHTML['GHL']['Main']['Locations Search'],
                                   timeout=30)

        # Find the Locations Search
        input_element = browser.find_element (By.CSS_SELECTOR, html.innerHTML['GHL']['Main']['Locations Search'])
        print (f"element: {input_element}")

        # Ensure input text to find location is there
        while wait_until_value_disappeared_element_BLOCK (element=input_element, timeout=1):
            # Input text to find location
            input_element.send_keys ('aquisitions')

        # Wait on Houston Location to appear
        wait_until_appeared_BLOCK (browser=browser, css_element=html.innerHTML['GHL']['Main']['Houston Location'],
                                   timeout=30)

        # The wait_until_appeared still seem not to be long enough. Putting manual wait for assurance
        time.sleep (10)

        # Click the Houston Location
        check_element_exists_BLOCK (browser=browser, css_selector=html.innerHTML['GHL']['Main']['Houston Location'],
                                    calling_line=line ()).click ()

        # Click opportunities
        check_element_exists_BLOCK (browser=browser, css_selector=html.innerHTML['GHL']['Main']['Opportunities'],
                                    calling_line=line ()).click ()

        # Wait for page to load a bit
        time.sleep (3)

        # Add browser instance to list
        browsers.append (browser)

        # Create a socket server
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    #     server_address = ('localhost', 5700)  # Replace with the appropriate server address
    #     server_socket.bind(server_address)

    #     # Make a queue of 1 connection
    #     server_socket.listen(1)

    #     print(f'({task_id})-({line()}) Receiver program listening for connections...')

    #     # Start accepting connections in a separate thread
    #     accept_thread = threading.Thread(target=accept_connections, args=(server_socket,))
    #     accept_thread.start()

    # This will run the code as soon as it's starting rather than waiting
    scheduled_task (browsers, browser_num)

    # This will run the code after a set amount of tim
    schedule.every().hour.do(lambda: scheduled_task (browsers, browser_num))

    # Run the scheduled task and handle client connections
    while True:
        schedule.run_pending ()
        time.sleep (1)

finally:
    for browser in browsers:
        browser.quit ()
