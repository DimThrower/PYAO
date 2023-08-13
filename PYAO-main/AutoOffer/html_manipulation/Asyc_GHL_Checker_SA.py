import asyncio, re, time, traceback, pickle, socket, threading, schedule, aiofiles, asyncio, cProfile
from calendar import SATURDAY
from operator import call
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, NoSuchWindowException, \
    StaleElementReferenceException
from HTML_SA import HTML, PropertyProfile
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

save_in_db = True

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

                # Get the mls_id, and remove it from the dictionary
                mls_id = prop_dict.pop (pp.mls_id)

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

                            # Input the Street Address into the search bar
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
                await asyncio.sleep (20)

                # Wait for cards to show
                await wait_until_appeared (browser=browser,
                                           css_element=f".{html.innerHTML['GHL']['Main']['Card Class']}", timeout=10,
                                           calling_line=line ())

                # Parse current DOM
                soup = BeautifulSoup (browser.page_source, 'html.parser')

                # Get all the elements with class="card-info"
                card_elements = soup.find_all (class_=html.innerHTML['GHL']['Main']['Card Class'])

                # Initialize create_opp object
                create_opp = True

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

                        # Check for a deal in GHL and make string all lowercase to make the comparable
                        if card_innerHtml and (street_number.lower() in card_innerHtml.lower()):
                            # Need to pop the property from the matrix before sending it to make offer
                            # print(f"({task_id}) card innerHTML: {card_innerHtml}")
                            print (f'({task_id})-({line ()}) Deal taken')

                            # Set the GHL_Check to True and the Deal taken to True
                            await db_funct.async_multi_db_update (
                                cursor=cursor,
                                mls_id=mls_id,
                                data_dict={
                                    pp.ghl_check: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    pp.deal_taken: 'Yes'
                                },
                                overwrite=True
                            )

                            # Set create_opp to False
                            create_opp = False
                            break

                if create_opp:
                    print (f"({task_id}) New deal not taken")

                    # Click New Deal btn
                    # Execute JavaScript to find and click the element using the CSS selector
                    browser.execute_script ("document.querySelector(arguments[0]).click();",
                                            html.innerHTML['GHL']['Main']['New Deal btn'])

                    # Find the element for the window that creates deeal, This should cut down on load time
                    create_op_win = await check_element_exists (browser=browser,
                                                                css_selector=html.innerHTML['GHL']['Main'][
                                                                    'Create Op Window'], calling_line=line ())

                    # Wait for first field in page deal
                    await wait_until_appeared (browser=browser,
                                               css_element=html.innerHTML['GHL']['Main']['Contact Name'],
                                               calling_line=line ())

                    # Find the opportunity name element
                    input_element = await check_element_exists (browser=create_op_win,
                                                                css_selector=html.innerHTML['GHL']['Main'][
                                                                    'Opportunity Name'], calling_line=line ())

                    # Input the property address into the name if it's clear
                    input_element.send_keys (
                        f"{curr_prop_dict[pp.steet_address]}, {curr_prop_dict[pp.city]}, TX {curr_prop_dict[pp.zip_Code]}")

                    # Find the contact name element
                    input_element = await check_element_exists (browser=create_op_win,
                                                                css_selector=html.innerHTML['GHL']['Main'][
                                                                    'Contact Name'], calling_line=line ())

                    # Input contact Name
                    input_element.send_keys (
                        f'{curr_prop_dict[pp.agent_first_name]} {curr_prop_dict[pp.agent_last_name]} ~PY~')

                    # Find the create new contact button 
                    create_contact_btn = await check_element_exists (browser=browser,
                                                css_selector=html.innerHTML['GHL']['Main']['Create Contact'],
                                                calling_line=line ())

                    # Click the create new contact btn
                    create_contact_btn.click()

                    # Need to press enter so the Contact name doesn't disappear
                    # input_element.send_keys (Keys.ENTER)

                    # Find the lead value element
                    input_element = await check_element_exists (browser=create_op_win,
                                                                css_selector=html.innerHTML['GHL']['Main'][
                                                                    'Lead Value'])

                    # Clear out any values alrady inside the lead value field                    
                    browser.execute_script ("arguments[0].value = '';", input_element)

                    # Input lead value 
                    input_element.send_keys ('15000')

                    # Find the drop down list
                    drpdwn_btn = await check_element_exists (browser=create_op_win,
                                                             css_selector=html.innerHTML['GHL']['Main']['Owner'],
                                                             calling_line=line ())

                    # Click the drpdwn list
                    drpdwn_btn.click ()

                    # Find the element that contains the list of items
                    drpdwn_list = await check_element_exists (browser=browser,
                                                              css_selector=html.innerHTML['GHL']['Main'][
                                                                  'Owner drpdwn'], calling_line=line ())

                    # Wait until the items show in the drop down list
                    if await wait_until_value_appeared_tag (browser=browser,
                                                            tag_name='span',
                                                            parent_element=drpdwn_list,
                                                            timeout=30):
                        # Find all the items located inside the drpdwn_list to be checked
                        items = drpdwn_list.find_elements (By.TAG_NAME, 'span')
                        print (f'({task_id})-({line ()}) Items in list: {items}')
                    else:
                        print (f'({task_id})-({line ()}) Cannot find drop down items in create opportunity page')

                    # Interate throught all the span elements untill a match is found
                    for item in items:
                        # Find the innerHTML of each item
                        item_innerHTML = item.get_attribute ('innerHTML')
                        print (f'({task_id})-({line ()}) Item check: {item_innerHTML}')

                        # Check to for a matching innterHtml
                        if html.innerHTML['GHL']['Main']['My Name'] in item_innerHTML:
                            # Click the matching name

                            (await check_only_element_exists (element=item, calling_line=line ())).click ()
                            print (f'({task_id})-({line ()}) Clicked the owner: {item_innerHTML}')
                            break

                    # Find the opportunity source element
                    input_element = await check_element_exists (browser=create_op_win,
                                                                css_selector=html.innerHTML['GHL']['Main'][
                                                                    'Opportunity Source'], calling_line=line ())

                    # while await wait_until_value_disappeared_element(element=input_element, timeout=1):
                    # Input opportunity source
                    opp_source = f'{curr_prop_dict[pp.agent_first_name]}-MLS/PYAO'
                    input_element.send_keys (opp_source)


                    # Click the Create button
                    create_btn = await check_element_exists (browser=create_op_win,
                                                             css_selector=html.innerHTML['GHL']['Main'][
                                                                 'Create Button'], calling_line=line ())
                    create_btn.click ()

                    await asyncio.sleep (10)

                    # Close the Opportunity Window
                    close_op_win = await check_element_exists (browser=browser,
                                                              css_selector=html.innerHTML['GHL']['Main']['Close Op Window'], calling_line=line())

                    close_op_win.click ()

                    print (f'({task_id})-({line ()}) Click the Save button to create the opportunity')
                    # await asyncio.sleep(20)

                    # Update DB to show that deal is available and has been checked
                    if save_in_db:
                        await db_funct.async_multi_db_update (
                            cursor=cursor,
                            mls_id=mls_id,
                            data_dict={
                                pp.ghl_check: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                pp.deal_taken: 'No'
                            },
                            overwrite=True
                        )

                    # Contiuasly run until cards appear
                    while True:
                        # Find the card that was just created
                        # Parse the current DOM
                        soup = BeautifulSoup (browser.page_source, 'html.parser')

                        # Get all the elements with class="card-info"
                        card_elements = soup.find_all (class_=html.innerHTML['GHL']['Main']['Card Class'])

                        # Sleep so that the resources don't get ate up
                        await asyncio.sleep (0.5)

                        if card_elements:
                            # print(f"({task_id}) Card elements: {card_elements}")
                            break

                    for card_element in card_elements:
                        # Find the innerHTML of each card
                        # The only visable card should be the one we just created
                        card_innerHtml = innerHTML_Drill (card_element)
                        print (f"({task_id})-({line ()}) card innerHTML: {card_innerHtml}")

                        # Street name would be the second match
                        street_name = matches.group (1)

                        # Check for the deal just made
                        if card_innerHtml and (street_name in card_innerHtml):
                            # print(f"({task_id}) card innerHTML: {card_innerHtml}")
                            print (f'({task_id})-({line ()}) Inputing deal details')

                            # Continuous loop to ensure the card is clicked, so futher details can be added
                            while True:
                                try:
                                    # Click on the card based on it's innerHTML
                                    new_card = await check_element_exists_xpath (browser=browser,
                                                                                 xpath=f"//*[contains(text(), '{card_innerHtml}')]",
                                                                                 calling_line=line ())
                                    new_card.click ()

                                    print (f"({task_id})-({line ()}) Clicking deal card: {card_innerHtml}")
                                    break
                                except (NoSuchElementException, StaleElementReferenceException,
                                        ElementClickInterceptedException):
                                    continue

                            '''
                            Contact Tab
                            '''
                            # Ensure Contact tab has loaded
                            while True:
                                if await wait_until_appeared (browser=browser,
                                                              css_element=html.innerHTML['GHL']['Details'][
                                                                  'Contact Check Field'], timeout=1,
                                                              calling_line=line ()):
                                    # Find contact tab element
                                    contact_tab = await check_element_exists (browser=browser, css_selector=
                                    html.innerHTML['GHL']['Details']['Contact'], calling_line=line ())

                                    # Click to close Contact tab
                                    contact_tab.click ()

                                    print (f"({task_id})-({line ()}) click Contact Tab")

                                    # Sleep to give tab time to close
                                    await asyncio.sleep (0.5)
                                else:
                                    print (f'({task_id})-({line ()}) Contact tab closed')
                                    break

                            '''
                            General Tab
                            '''
                            # Ensure General tab has loaded
                            while True:
                                if await wait_until_disappeared (browser=browser,
                                                                 css_element=html.innerHTML['GHL']['Details'][
                                                                     'General Check Field'], timeout=0.5):
                                    # Find General tab element
                                    general_tab = await check_element_exists (browser=browser, css_selector=
                                    html.innerHTML['GHL']['Details']['General'],
                                                                              calling_line=(f'{line ()} General Tab'))

                                    # Scroll to the element so elements can be in view
                                    browser.execute_script ("arguments[0].scrollIntoView();", general_tab)

                                    # Click to open Contact tab
                                    general_tab.click ()
                                    print (f"({task_id})-({line ()}) click General Tab")

                                    # Sleep to give tab time to open
                                    await asyncio.sleep (0.5)
                                else:
                                    print (f'({task_id})-({line ()}) General tab open')
                                    break

                            '''
                            Additional Tab
                            '''
                            # Ensure Additional tab has loaded
                            while True:
                                if await wait_until_disappeared (browser=browser,
                                                                 css_element=html.innerHTML['GHL']['Details'][
                                                                     'Additional Check Field'], timeout=1):
                                    # Find General tab element
                                    additional_tab = await check_element_exists (browser=browser, css_selector=
                                    html.innerHTML['GHL']['Details']['Additional'], calling_line=line ())

                                    # Scroll to the element so elements can be in view
                                    browser.execute_script ("arguments[0].scrollIntoView();", additional_tab)

                                    # Click to open Contact tab
                                    additional_tab.click ()
                                    print (f"({task_id})-({line ()}) click Additional Tab")

                                    # Sleep to give tab time to open
                                    await asyncio.sleep (0.5)
                                else:
                                    print (f'({task_id})-({line ()}) Additional tab open')
                                    break

                            # Find the div element you want to scroll within
                            main_scroll_element = await check_element_exists (browser=browser, css_selector=
                            html.innerHTML['GHL']['Details']['Scroll Window'], calling_line=line ())

                            # Get the starting time
                            start_time = time.time ()

                            # Take some time second to scroll to the bottom
                            # while time.time () - start_time < 0.5:
                                # Scroll to the bottom of the div
                            #    browser.execute_script ("arguments[0].scrollTop = arguments[0].scrollHeight;",
                            #                            main_scroll_element)
                                # print(f"({task_id}) Scolling to bottom of detials page")

                          # Keep scroll down slowing so all elements can load
                            print(f"Scrolling to the bottom of the page")
                            while time.time () - start_time < 30:

                                #Scroll to the bottom of page
                                browser.execute_script (
                                        "arguments[0].scrollBy(0, 120);",
                                    main_scroll_element)
                                await asyncio.sleep (0.5)

                            # Wait some time for all the form elements to load
                            time.sleep(2)

                            # Find elements for the visibile form-grop class element
                            form_group_elements = await check_elements_exists (browser=browser, css_selector=
                            html.innerHTML['GHL']['Details']['Class'], calling_line=line ())
                            print (f"({task_id})-({line ()}) Found {len(form_group_elements)} form-group class elements")

                            # Initialize a dictionary to combine general and additional dictionaries
                            all_inputs = {}

                            # Combine general and additional into all_inputs
                            all_inputs.update (html.innerHTML['GHL']['Details']['General Inputs'])
                            all_inputs.update (html.innerHTML['GHL']['Details']['Additional Inputs'])

                            # Interate over all the form-group elements
                            for form_group_element in form_group_elements:
                                # print(f"({task_id}) Iterating thorugh all the form-group class elements")

                                # Make both child object false as not to cause error
                                title_child_element = False

                                # Find the child element of each form group
                                try:
                                    title_child_element = form_group_element.find_element (By.XPATH, "./div")
                                # If element does not exit, then continue to next
                                except (NoSuchElementException, StaleElementReferenceException):
                                    continue

                                print(f"({task_id}) Was the child element form-group div found?: {title_child_element}")
                                # Get the innerHTML of the input 
                                if title_child_element:
                                    innerHTML_input = title_child_element.get_attribute ("innerHTML")
                                    print(f"({task_id}) Input value: {innerHTML_input}")

                                    # Check is the current form-group class element has a title that matches any value in the all_inputs list
                                    if innerHTML_input in all_inputs:
                                        # This first try is for input fields
                                        # Get the input element of the for-group class
                                        # Find the iput tag located in the form-group element                                   
                                        try:  
                                            # This will get the field where the actual data is inputted
                                            input_element = form_group_element.find_element (By.TAG_NAME, "input")
                                            print(f'Input element: {input_element}')
                                            # This will handle the Escrow Agent and Title company
                                            if any (keyword in innerHTML_input for keyword in
                                                    ['Escrow Agent', 'Title Company Address']):

                                                start_time = time.time ()
                                                while time.time () - start_time < 0.5:
                                                    # Scroll to the bottom of the div
                                                    browser.execute_script (
                                                        "arguments[0].scrollTop = arguments[0].scrollHeight;",
                                                        main_scroll_element)
                                                    # print(f"({task_id}) Scolling to bottom of detials page")

                                                # Click on the drop down 
                                                try:
                                                    # Click on the drop down 
                                                    input_element.find_element (By.XPATH, '..').click ()
                                                except (StaleElementReferenceException, NoSuchElementException):
                                                    print (f"({task_id}) Trying to click the drop down menu")
                                                    continue

                                                # Find all the items for the drpdwn element
                                                drpdwn_elements = form_group_element.find_elements (By.TAG_NAME, "li")
                                                # print(f"({task_id}) Toggle {drpdwn_element}")

                                                # Iterate through the items until a match is found
                                                for drpdwn_element in drpdwn_elements:
                                                    try:
                                                        # Find the innerHTML of each ext_element
                                                        innerHTML = drpdwn_element.get_attribute ("innerHTML")
                                                        # print(f"({task_id}) drpdwn innerHTML: {innerHTML}")

                                                    except StaleElementReferenceException:
                                                        print (
                                                            f"({task_id}) Trying to click the innerHTML of the drpdwn")
                                                        continue

                                                    # Use innerHTML to get the correct key in curr_prop_dict
                                                    curr_prop_dict_key = all_inputs[innerHTML_input]
                                                    # print(f"({task_id}) curr_prop_dic_key: {curr_prop_dict_key}")

                                                    # Set the target value based on the prop_dict
                                                    target_value = curr_prop_dict[curr_prop_dict_key]
                                                    print (
                                                        f"({task_id}) target_Value: {target_value} and innerHtml: {innerHTML}")

                                                    # Check to to if innerHTML matches my name for Escrow Agent
                                                    if target_value in innerHTML:
                                                        try:
                                                            # Click the item
                                                            drpdwn_element.click ()
                                                        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException):
                                                            print (f"({task_id}) Trying to click {target_value}")
                                                            continue
                                                        print (f"({task_id}) Clicked {target_value}")
                                                        break

                                            # Skip the send keys for the Escrow Agent and Title Company Address so the preious actions arean't over wrritten
                                            if not any (keyword in innerHTML_input for keyword in
                                                        ['Escrow Agent', 'Title Company Address', 'Bed/Bath',
                                                         'Contract', 'HOA', 'Policy']):
                                                # Use innerHTML to get the correct key in curr_prop_dict
                                                curr_prop_dict_key = all_inputs[innerHTML_input]
                                                # print(f"({task_id}) curr_prop_dic_key: {curr_prop_dict_key}")

                                                # Get the value the corresponds to that key
                                                target_value = curr_prop_dict[curr_prop_dict_key]

                                                # Check that there is a target value isn't non
                                                if target_value:
                                                    # Wait for element to be interacable
                                                    await wait_until_appeared_element (element=input_element,
                                                                                       timeout=20, calling_line=line ())

                                                    while await wait_until_value_disappeared_element (
                                                            element=input_element, timeout=1):
                                                        # Fill field with appropriate value
                                                        input_element.send_keys (target_value)
                                                        print (f"({task_id}) Typing {target_value}")
                                                        # print(f"({task_id}) curr_prop_dict_value: {curr_prop_dict[curr_prop_dict_key]}")
                                                else:
                                                    continue

                                            # Need a special case for the bed and bath field becouse
                                            if "Bed/Bath" in innerHTML_input:
                                                # Get the key for the property dictionary
                                                curr_prop_dict_key = all_inputs[innerHTML_input]

                                                # Get the value the corresponds to that key
                                                target_value = curr_prop_dict[curr_prop_dict_key]

                                                # Get the beds, baths, and half baths
                                                bed = target_value
                                                bath = curr_prop_dict[pp.bath]
                                                half_bath = curr_prop_dict[pp.half_bath]

                                                layout = [bed, bath, half_bath]

                                                layout_nums = ''

                                                # Find the ones that are not none and put them in a group (Ex. 32 or 421)
                                                for num in layout:
                                                    if num is not None:
                                                        layout_nums = f"{layout_nums}{num}"

                                                # Puts a slash between digits (Ex. 3/2 or 4/2/1)
                                                # Makes sure there is more than one digit
                                                if len (layout_nums) >= 2:
                                                    layout_input = '/'.join (layout_nums)
                                                else:
                                                    layout_input = layout_nums

                                                # Wait for the input element to be empty
                                                while True:
                                                    bool = await wait_until_value_disappeared_element (
                                                        element=input_element, timeout=1)
                                                    if bool:
                                                        # Input the layout in to Bed/Bath Field                    
                                                        input_element.send_keys (layout_input)
                                                        print (f"({task_id}) Typing {target_value}")
                                                        break

                                            # Searching for the words that are found in the title of the fields in GHL
                                            if any (keyword in innerHTML_input for keyword in
                                                    ['Contract', 'HOA', 'Policy']):
                                                print (f'({task_id})-({line ()}) Handling HOA, TREC, Policy')

                                                start_time = time.time ()
                                                while time.time () - start_time < 0.5:
                                                    # Scroll to the bottom of the div
                                                    browser.execute_script (
                                                        "arguments[0].scrollTop = arguments[0].scrollHeight;",
                                                        main_scroll_element)
                                                    # print(f"({task_id}) Scolling to bottom of detials page")

                                                # Keep scrolling until the Title Policy button is found
                                                while True:
                                                    # Find the Title Policy button
                                                    title_policy = await check_element_exists (browser=browser,
                                                                                               css_selector=
                                                                                               html.innerHTML['GHL'][
                                                                                                   'Details'][
                                                                                                   'Title Policy'],
                                                                                               timeout=0.5,
                                                                                               calling_line=line ())

                                                    print(f"title policy before: {title_policy}")
                                                    if title_policy:
                                                        print(f"title policy after: {title_policy}")
                                                        break

                                                    #Scroll to the Title Policy Button
                                                    browser.execute_script (
                                                            "arguments[0].scrollBy(0, -10);",
                                                        main_scroll_element)

                                                start_time = time.time ()
                                                while time.time () - start_time < 0.5:
                                                    # Scroll to the bottom of the div
                                                    browser.execute_script (
                                                        "arguments[0].scrollTop = arguments[0].scrollHeight;",
                                                        main_scroll_element)
                                                    # print(f"({task_id}) Scolling to bottom of detials page")

                                                # Click the Title Policy button
                                                (await check_only_element_exists (element=title_policy,
                                                                                  calling_line=line ())).click ()

                                                start_time = time.time ()
                                                while time.time () - start_time < 0.5:
                                                    # Scroll to the bottom of the div
                                                    browser.execute_script (
                                                        "arguments[0].scrollTop = arguments[0].scrollHeight;",
                                                        main_scroll_element)
                                                    # print(f"({task_id}) Scolling to bottom of detials page")

                                                # Find the HOA Yes and No button
                                                # Wait for title policy element to appear
                                                yes_hoa_element = await check_element_exists (browser=browser,
                                                                                              css_selector=
                                                                                              html.innerHTML['GHL'][
                                                                                                  'Details']['Yes HOA'],
                                                                                              calling_line=line ())
                                                no_hoa_element = await check_element_exists (browser=browser,
                                                                                             css_selector=
                                                                                             html.innerHTML['GHL'][
                                                                                                 'Details']['No HOA'],
                                                                                             calling_line=line ())

                                                # Scroll to HOA buttons
                                                # browser.execute_script("arguments[0].scrollIntoView();", yes_hoa_element)

                                                # Check the apprpriate HOA box
                                                if "Yes" in curr_prop_dict['HOA']:
                                                    yes_hoa_element.click ()
                                                else:
                                                    no_hoa_element.click ()

                                                start_time = time.time ()
                                                while time.time () - start_time < 0.5:
                                                    # Scroll to the bottom of the div
                                                    browser.execute_script (
                                                        "arguments[0].scrollTop = arguments[0].scrollHeight;",
                                                        main_scroll_element)
                                                    # print(f"({task_id}) Scolling to bottom of detials page")

                                                # Find the Trec element
                                                trec_element = await check_element_exists (browser=browser,
                                                                                           css_selector=
                                                                                           html.innerHTML['GHL'][
                                                                                               'Details']['TREC'],
                                                                                           calling_line=line ())

                                                # Click the "Trec 1-4" Button
                                                trec_element.click ()

                                        except NoSuchElementException:
                                            print (f'({task_id})-({line ()}) InnerHTML: {innerHTML_input}')
                                            # Scroll to the element so elements can be in view
                                            #browser.execute_script ("arguments[0].scrollIntoView();",
                                            #                        form_group_element)

                                            # Find and click the button element to open the list element
                                            drpdwn_btn = await check_element_exists_tag (browser=form_group_element,
                                                                                         tag_name="button",
                                                                                         calling_line=line ())
                                            drpdwn_btn.click ()

                                            # Find all the items for the drpdwn element
                                            drpdwn_elements = await check_elements_exists_tag (
                                                browser=form_group_element, tag_name="li", calling_line=line ())
                                            print (f'({task_id})-({line ()}) Handling the drpdwn elements')

                                            # Iterate through the items until a match is found
                                            for drpdwn_element in drpdwn_elements:

                                                try:
                                                    # Find the innerHTML of each ext_element
                                                    innerHTML = drpdwn_element.get_attribute ("innerHTML")
                                                    print (f"({task_id}) drpdwn innerHTML: {innerHTML}")

                                                except StaleElementReferenceException:
                                                    continue

                                                    # Check to to if innerHTML matches my name for Manager
                                                if html.innerHTML['GHL']['Details']['My Name'] in innerHTML:
                                                    # Scroll to the element so elements can be in view
                                                    browser.execute_script ("arguments[0].scrollIntoView();",
                                                                            drpdwn_element)

                                                    try:
                                                        # Click the item
                                                        (await check_only_element_exists (element=drpdwn_element,
                                                                                          calling_line=line ())).click ()
                                                        print (
                                                            f"({task_id}) Clicked on {html.innerHTML['GHL']['Details']['My Name']}")
                                                        break

                                                    except (NoSuchElementException, StaleElementReferenceException):
                                                        print (f"({task_id}) Trying to click the Agent manager drpdwn")
                                                        continue

                                                        # Check to see if innerHTML matches lead source
                                                if html.innerHTML['GHL']['Details']['Lead Source'] in innerHTML:
                                                    # Scroll to the element so elements can be in view
                                                    browser.execute_script ("arguments[0].scrollIntoView();",
                                                                            drpdwn_element)

                                                    try:
                                                        # Click the item
                                                        (await check_only_element_exists (element=drpdwn_element,
                                                                                          calling_line=line ())).click ()
                                                        print (
                                                            f"({task_id}) Clicked on {html.innerHTML['GHL']['Details']['Lead Source']}")
                                                        break

                                                    except (NoSuchElementException, StaleElementReferenceException):
                                                        print (f"({task_id}) Trying to click the Lead Source drpdwn")
                                                        continue

                                                # Check to see if innerHTML matches Title Company Name
                                                if curr_prop_dict[pp.title_company_name] in innerHTML:
                                                    print (f'({task_id})-({line ()}) Selecting the title company name')
                                                    # Scroll to the element so elements can be in view
                                                    browser.execute_script ("arguments[0].scrollIntoView();",
                                                                            drpdwn_element)
                                                    try:
                                                        (await check_only_element_exists (element=drpdwn_element,
                                                                                          calling_line=line ())).click ()
                                                        print (
                                                            f"({task_id}) Clicked on {curr_prop_dict[pp.title_company_name]}")
                                                        break

                                                    except (NoSuchElementException, StaleElementReferenceException):
                                                        print (f"({task_id}) Trying to click the Title company drpdwn")
                                                        continue

                if create_opp:
                    print (f"({task_id}) Finish inputing details and waiting for save button")

                    # Find the save button
                    save_btn_element = await check_element_exists (browser=browser,
                                                                   css_selector=html.innerHTML['GHL']['Details'][
                                                                       'Save btn'])

                    # Click the save button
                    save_btn_element.click ()

                    # Wait for the save button to disappear
                    while not (await wait_until_disappeared_element (element=save_btn_element, timeout=30,
                                                              calling_line=line ())):
                        # Click the save button
                        (await check_only_element_exists (element=save_btn_element, calling_line=line ())).click ()

                # Go back to opporunities to put in next property                                        
                opportunity_btn = await check_element_exists (browser=browser,
                                                              css_selector=html.innerHTML['GHL']['Main'][
                                                                  'Opportunities'], calling_line=line ())
                opportunity_btn.click ()
                print (f'({task_id})-({line ()}) Task is done, going back to opportunities page for next schduled task')

                # Wait untill you can see the Add Deal button
                await wait_until_appeared (browser=browser, css_element=html.innerHTML['GHL']['Main']['New Deal btn'],
                                           calling_line=line ())
                # await asyncio.sleep(60)
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
            properties = await db_funct.async_get_all_sorted_with_null (cursor=cursors[0], sort_column=pp.last_updated,
                                                                        null_column=pp.ghl_check)
      
            # Close the database connectio
            # await conn.close()

            # Check to see if there are any properties to check
            if properties:

                # Initialize filtered list
                filtered_list = []

                # Remove all properties not in HOU
                for index, property in enumerate(properties):
                    if property[pp.location] == "SA":
                        filtered_list.append(property)

                properties = filtered_list

                print(f"Number of properties to check: {len(properties)}")

                if len(properties) == 0:
                    break



                # print(f"Properties: {properties}")

                # Split properties evenly amon the browsers
                prop_dict_parts = split_list_evenly (list=properties, num_splits=browser_num)
                # print (f"({task_id}) prop_dict_parts: {prop_dict_parts}")

                # Make a task for each part of the dictionary
                for index, prop_dict_part in enumerate (prop_dict_parts):
                    # Create an asyncio task and add it to the task list
                    tasks.append (asyncio.create_task (
                        process_task (browser=browsers[index], task_id=index, cursor=cursors[index],
                                      prop_dict_part=prop_dict_part)))
            else:
                print (f'({task_id})-({line ()}) No properties to update, run at next schedule')

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
# pkl_file_path = settings.prop_pkl_file_path

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
    chromeDriverPath = settings.chromeDrivePath

    for i in range (0, browser_num):
        # Initialize browser instance
        browser = webdriver.Chrome (executable_path=chromeDriverPath)

        # Set email
        email = settings.GHL_USERNAME

        # Set password
        password = settings.GHL_PASSWORD

        # Opening GHL 
        browser.get (html.webaddress['GHL'])

        # Maximize the window
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
            input_element.send_keys ('sa acquisitions')

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
    schedule.every(10).minutes.do (lambda: scheduled_task (browsers, browser_num))

    # Run the scheduled task and handle client connections
    while True:
        schedule.run_pending ()
        time.sleep (1)

finally:
    for browser in browsers:
        browser.quit ()
