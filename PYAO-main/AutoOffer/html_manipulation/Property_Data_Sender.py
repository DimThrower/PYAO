import inspect, time, re, socket, pickle, schedule
from datetime import datetime
from bs4 import BeautifulSoup
from HTML import HTML, PropertyProfile
from AutoOffer import settings
from AutoOffer.db import db_funct
from AutoOffer.misc import *
from HTML_ACTIONS import click, innerHTML_Drill
from AutoOffer.calculations.offer_calcs import offer_calc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import asyncio

# Check to see if db needs to be created
# db_funct.create_db()

# Initialize PropertyProfile Class
pp = PropertyProfile()

# If True it will only save listings based on confindednce lvlv
# If false it will save all the listsing
strict = False
if strict:
    print("CODE IS STRICT: Properties must meet confidence levels")
else:
    print('CODE IS NOT STRICT: Confidence levels disregarded')

def HAR():
    # Check to see if db needs to be created
    db_funct.create_db()
    
    testing = False
    if not testing:
        # Create HTML instance to pull values objects from
        html = HTML()

        # Set the HAR web address
        url = html.webaddress['har']

        chromeDriverPath = settings.chromeDrivePath

        options = Options()

        # Keep the browser from showing by making it headless
        options.add_argument("--headless")
    
        # Saves on GPU process since images aren't rendered
        options.add_argument("--disable-gpu")

        # Decide on what number of listing to start at.
        start_listing_num = 0

   
        # Initalize broser instance
        browser = webdriver.Chrome(executable_path=chromeDriverPath, options=options)  

         # Will get all the mls_ids of the rows in db
        saved_listings = db_funct.fetch_sorted_rows(sort_column=pp.last_updated, column=pp.mls_id)
        # print(f'Saved Listing from DB: {saved_listings}')

        # Convert listings into a set, which should cut down on look up time 
        saved_listings_set = set(saved_listings)
        # print(f'Saved Listing set: {saved_listings_set}')

        try:
            # Opening Browser
            browser.get(url)
            time.sleep(2)

            # Log into HAR
            username_element = browser.find_element(By.CSS_SELECTOR, html.selectors['har']['user'])
            browser.execute_script("arguments[0].value = arguments[1];", username_element, settings.HAR_USERNAME)

            password_element = browser.find_element(By.CSS_SELECTOR, html.selectors['har']['password'])
            browser.execute_script("arguments[0].value = arguments[1];", password_element, settings.HAR_PASSWORD)

            # Click login btn
            click(browser, wait=2, e_type='css', element=html.selectors['har']['login_btn'], errmsg=f'({inspect.currentframe().f_lineno}) - Could not click login btn')
            time.sleep(10)

            # Click Matrix
            click(browser, wait=2, e_type='css', element=html.selectors['har']['matrix'], errmsg=f'({inspect.currentframe().f_lineno}) - Could not click matrix')
            time.sleep(2)

            #Closing first tab
            browser.switch_to.window(browser.window_handles[0])
            browser.close()

            # Wait for the first window to close
            time.sleep(.5)

            #Switch back to new tab
            browser.switch_to.window(browser.window_handles[0])

            # go back to url, now that you're logged in
            browser.get(url)

            # Create soup instance
            soup = BeautifulSoup(browser.page_source, 'html.parser')

            # find PYAO auto email tag
            a_tag = soup.find(lambda tag: tag.name == 'a' and html.innerHTML['saved search page']['saved search name'] in tag.text)

            # Extract the id of the tag
            a_tag_id = a_tag['id']

            # Click on PYAO
            click(browser, wait=2, e_type='id', element=a_tag_id, errmsg=f"({inspect.currentframe().f_lineno}) - Could not click {html.innerHTML['saved search page']['saved search name']}")

            time.sleep(1)
            #Refreshing soup instance
            soup = BeautifulSoup(browser.page_source, 'html.parser')

            # Find the tage with Results as the inner html
            a_tag = soup.find(lambda tag: tag.name == 'a' and html.innerHTML['saved search page']['results'] in tag.text)

            # Extract the id of the tag
            a_tag_id = a_tag['id']

            # Click on PYAO
            click(browser, wait=2, e_type='id', element=a_tag_id, errmsg=f"({inspect.currentframe().f_lineno}) - Could not click {html.innerHTML['saved search page']['results']}")


            # Click the first mls link
            click(browser, wait=10, e_type='css', element=html.selectors['har']['first_mls_link'], errmsg=f'({inspect.currentframe().f_lineno}) - Cannot click MLS link btn')
            print(f'Click the first MLS link')

            current_num = 1
            final_num = 1000

            # Initialize end_code to be True
            end_code = False

            # Put listing page and tax page selectors into one list
            # Searcging the tax listing first to see if it the cofindence score is high enough
            selector_dictionaries = [html.innerHTML['listing_page'], html.innerHTML['tax_page']]

            # Loop through all the pages
            while current_num+1 <= 3:
                print(f'Curent number: {current_num}')
                temp_prop_dict = {}

                # Check if code should continue
                if end_code:
                    print('Waiting for next scheduled run')
                    break

                # Initialize skip_listing to be False
                skip_listing = False

                # Check to ensure the page is on the right listing
                while start_listing_num < 1:
                    # Get the page into soup
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    if start_listing_num-1 > int(innerHTML_Drill(soup.select_one(html.selectors['har']['current_num']))):
                        # Click the next button
                        click(browser, wait=10, e_type='css', element=html.selectors['har']['next_btn'], errmsg=f'({inspect.currentframe().f_lineno}) - Cannot click Next btn')
                        # (check_element_exists_BLOCK(browser=browser, css_selector=html.selectors['har']['next_btn'], calling_line=line())).click()
                    else:
                        # Set the curent_num listing equal to the current listing number
                        current_num = int(innerHTML_Drill(soup.select_one(html.selectors['har']['current_num'])))

                        # Set the start_listing_page to Done so loop won't hapen anymore
                        start_listing_num = -1000
                        break

                # Interate though all the selectors 
                for index, dictionay in enumerate(selector_dictionaries):

                    if index == 0:
                        # Click on the listing tab
                        # click(browser, wait=10, e_type='css', element=html.selectors['har']['listing_link'], errmsg=f'({inspect.currentframe().f_lineno}) - Cannot click listing link btn')
                        (check_element_exists_BLOCK(browser=browser, css_selector=html.selectors['har']['listing_link'], calling_line=line())).click()
                        print(f'Clicked Linked Page')

                        # Check to ensure listing page has loaded
                        WebDriverWait(browser,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, html.selectors['har']['listing_dom_check'])))

                        # Refreshing soup instance
                        soup = BeautifulSoup(browser.page_source, 'html.parser')

                        mls_id_element = soup.select_one(html.selectors['har']['mls_id_html'])
                        # print(f'MLS Id element from Beautiful Soup {mls_id_element}')
                        mls_id = int(innerHTML_Drill(current_tag=mls_id_element))
                        print(f'MLS ID: {mls_id}')

                        # Check to see if this listing is already in the DB
                        if saved_listings_set:
                            # Check to see if the most current MLS ID has alraedy been check
                            # if so then end the search and begin schedule for the next run     
                            # print(f" {temp_prop_dict[pp.mls_id]} : {lastest_listings[pp.mls_id]}")      
                            if mls_id in saved_listings_set:
                                print(f'Already looked at saved this listing {mls_id}')
                
                                # Set end_code to True so code know to stop looking
                                # Also set skip listing to true, so code does not try and save it
                                skip_listing = True
                                # end_code = True
                                break
                    
                    # When index is 1 it's on the Listing page, if 0 it's on the tax page
                    else:
                        
                        # Set default to save listing
                        save_listing = True  
                        # Click on the tax tab
                        # click(browser, wait=10, e_type='css', element=html.selectors['har']['tax_link'], errmsg=f'({inspect.currentframe().f_lineno}) - Cannot click Tax link btn')
                        (check_element_exists_BLOCK(browser=browser, css_selector=html.selectors['har']['tax_link'], calling_line=line())).click()
                        print(f'Clicked Tax Page')

                        # Check to ensure tax page has loaded
                        try:
                            WebDriverWait(browser,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, html.selectors['har']['tax_dom_check'])))
                        except TimeoutException:
                            print('Tax page doesn\'t exist')
                            skip_listing = True
                            break

                        # Refreshing soup instance
                        soup = BeautifulSoup(browser.page_source, 'html.parser')

                        # Get the innerHTML adjacent to the Confidence Score
                        conf_score = html.innerHTML['tax_page_cs'][pp.confidence_score]

                        if conf_score:
                            # Find the older sibling tag the cofidence number
                            seed_tag = soup.find(lambda tag: (tag.name == 'span' or tag.name == 'a') and  conf_score == tag.string)

                            # Go to the parent and then the sibling of the parent OF THE seed tag
                            if seed_tag:
                                parent_tag = seed_tag.parent
                                # print(f'parent_tag: {parent_tag}')

                            else:
                                # No confidence scroe found, so break and got to next listing
                                # Trigger to save listing set to Flase
                                save_listing = False
                                # print(f"Save Listing?: {save_listing}")
                                continue

                            sibling_of_parent = parent_tag.find_next_sibling()
                            # print(f'sibling_of_parent_tag: {sibling_of_parent}')

                            # Extract the innerHTML
                            confidence_val = int(innerHTML_Drill(sibling_of_parent))
                            # print(f'confindence_val: {confidence_val}')

                            # Create a confidence score key and set it equal to the html
                            temp_prop_dict[list(html.innerHTML['tax_page_cs'].keys())[0]] = confidence_val

                            # Get the innerHTML adjacent to the Forcast SD
                            conf_score_sd = html.innerHTML['tax_page_cs'][pp.forcast_sd]

                            # Get the older sibling tag the cofidence number standard deviation
                            seed_tag = soup.find(lambda tag: (tag.name == 'span' or tag.name == 'a') and  conf_score_sd == tag.string)

                            # Go to the parent and then the sibling of the parent OF THE seed tag
                            parent_tag = seed_tag.parent

                            # Find the next sibling of the parent tag
                            sibling_of_parent = parent_tag.find_next_sibling()
                            # print(f'sibling_of_parent_tag: {sibling_of_parent}')

                            # Extract the innerHTML
                            stdev_val = int(innerHTML_Drill(sibling_of_parent))
                            # print(f'stdev_val: {stdev_val}')

                            # Create a confidense score standard deviation key and set it equal to the html
                            temp_prop_dict[list(html.innerHTML['tax_page_cs'].keys())[1]] = stdev_val
                            # print(f'temp_prop_dict: {temp_prop_dict}')

                            # Check to see if confidence level is high enough to save
                            # But only if strict is set to true
                            if strict and ((confidence_val - stdev_val) < html.innerHTML['tax_page_cs'][pp.confidence_score_tolerance_lvl]):
                                # print(f"Confidence lvl low: {confidence_val - stdev_val}")

                                # Trigger to save listing set to False
                                save_listing = False

                                # print(f"Save Listing?: {save_listing}")
                                continue
                            else:
                                pass

                    if not skip_listing:
                        for key, value in dictionay.items():
                            # Set all keys to a default of None
                            temp_prop_dict.setdefault(key, None)

                            # Find the tag that contains the target innerHTML
                            seed_tag = soup.find(lambda tag: (tag.name == 'span' or tag.name == 'a') and value == tag.get_text())
                            # print(f'seed_tag: {seed_tag}')
                            
                            if seed_tag:
                                # Handle the Public and Agent Remarks
                                if (html.innerHTML['listing_page'][pp.public_remarks] in seed_tag):
                                    # Get the parent <td>
                                    parent_tr = seed_tag.find_parent('tr')

                                    # Get the next <tr> tag after the parent <tr>
                                    next_tr = parent_tr.find_next('tr')
                                    # print(f'next_tr: {next_tr}')

                                    # Get the innerHTML
                                    innerHTML = innerHTML_Drill(next_tr)
                                    # print(f'innerHTML: {innerHTML}')

                                    # pass the value into temp_prop_dict
                                    temp_prop_dict[key] = innerHTML
                                    continue

                                        
                            # Go to the parent and then the sibling of the parent OF THE seed tag
                            if seed_tag:
                                parent_tag = seed_tag.parent
                                # print(f'parent_tag: {parent_tag}')
                            else:
                                continue

                            sibling_of_parent = parent_tag.find_next_sibling()
                            # print(f'sibling_of_parent_tag: {sibling_of_parent}')

                            # Extract the innerHTML
                            innerHTML = innerHTML_Drill(sibling_of_parent)
                            # print(f'innerHTML: {innerHTML}')

                            # Handle agent first and last name
                            if html.innerHTML['listing_page'][pp.agent_first_name] in value:
                                # Extracting the first name out of the innerHTML
                                match = re.search(r'/([A-Za-z]+)\s', innerHTML)
                                if match:
                                    first_name = match.group(1)
                                    # print(first_name)
                                    temp_prop_dict[key] = first_name
                                else:
                                    print('Could not extract first name')

                                # Extracting the last name out of the innerHTML
                                match = re.search(r"\b(\w+)$", innerHTML)
                                if match:
                                    last_name = match.group(1)
                                    # print(last_name)
                                    temp_prop_dict[pp.agent_last_name] = last_name
                                else:
                                    print('Could not extract first name')   

                            # Handle Public and Agent Remarks


                            # Handel HOA
                            elif html.innerHTML['listing_page'][pp.hoa] in value:
                                sibling_tag = seed_tag.find_next_sibling()
                                innerHTML = innerHTML_Drill(sibling_tag)
                                temp_prop_dict[key] = innerHTML

                            # Handle MUD
                            elif html.innerHTML['tax_page'][pp.mud] in value and innerHTML:
                                temp_prop_dict[key] = 'Yes'

                            # Determine if LBP needed from year and inputting the year built
                            elif html.innerHTML['tax_page'][pp.year_built] in value and innerHTML:
                                # This should input the year built
                                temp_prop_dict[key] = innerHTML

                                if (int(innerHTML) <= 1978) and not None:
                                    temp_prop_dict[pp.lead_based_paint] = 'Yes'
                                else:
                                    temp_prop_dict[pp.lead_based_paint] = None

                            else:
                                temp_prop_dict[key] = innerHTML
                            # print(f"{key}:{innerHTML}")

                        # print(f'temp_prop_dict: {temp_prop_dict}')

                # print(f'Temp_prop_dict: {temp_prop_dict}')

                # Put in default on Offer Sent, GHL Check, and Deal Taken, and Offer Path, ect
                
                # temp_prop_dict[pp.ghl_check] = None
                # temp_prop_dict[pp.deal_taken] = None
                # temp_prop_dict[pp.pdf_offer_path] = None
                # temp_prop_dict[pp.email_body] = None
                # temp_prop_dict[pp.offer_sent] = None

                # Will get the latest updated listing
                # lastest_listings = db_funct.fetch_sorted_rows(sort_column=pp.last_updated, column=pp.mls_id)

                # # Convert listings into a set, which should cut down on look up time 
                # lastest_listings_set = set(lastest_listings)
                # # print(lastest_listings)
                # # print(temp_prop_dict) 

                # # Check to see if the lastest_listing has a value
                # if lastest_listings:
                #     # Check to see if the most current MLS ID has alraedy been check
                #     # if so then end the search and begin schedule for the next run     
                #     # print(f" {temp_prop_dict[pp.mls_id]} : {lastest_listings[pp.mls_id]}")      
                #     if (int(temp_prop_dict[pp.mls_id]) in lastest_listings_set):
                #         print(f'Already looked at saved this listing {temp_prop_dict[pp.mls_id]}')
                #         current_num = 1000000
                #         break


                # Click the next page
                click(browser, wait=10, e_type='css', element=html.selectors['har']['next_btn'], errmsg=f'({inspect.currentframe().f_lineno}) - Cannot click Next btn')

                # Wait for new page to load
                time.sleep(3)

                # Get the current and final number
                current_num = int(innerHTML_Drill(soup.select_one(html.selectors['har']['current_num'])))
                final_num =  int(innerHTML_Drill(soup.select_one(html.selectors['har']['final_num'])))
                # print(f"current_num: {current_num} - final_num: {final_num}")

                # Check if listing was skipped
                if not skip_listing:
                    # Check if listing should be saved
                    print(f"Save Listing?: {save_listing}")
                    if save_listing:
                        # Go back to Listing link to get data for next property
                        click(browser, wait=10, e_type='css', element=html.selectors['har']['listing_link'], errmsg=f'({inspect.currentframe().f_lineno}) - Cannot click Listing link btn')

                        # Add the state key,value pair
                        temp_prop_dict[pp.state] = "TX"

                        # Attaching the offer dictionary
                        temp_prop_dict.update(html.offer_details)
                        # print(f'google dict: {html.googlesheet}')
                        # print(f'After update: {temp_prop_dict}')                

                        # Calculate repair, offer price, and earnest money
                        offer_calc(temp_prop_dict)

                        # Get the MLS Id
                        mls_id = temp_prop_dict.pop(pp.mls_id)

                        # Add the listing to the db
                        db_funct.multi_db_update(mls_id=mls_id, data_dict=temp_prop_dict)
                        
                        # Add to the temp_Dict to the prop_dict, using the ml id as the key
                        # prop_dict[mls_id] = temp_prop_dict
                        # print(prop_dict)

        finally:
            # Close the browser
            browser.quit()

        # print(prop_dict)
    else:
        # Test Dictionary
        prop_dict = {
            '1': {'Street Address': "2509 Stuart St", 'Zip Code': '77004'},
            '2': {'Street Address': "2029 Woodhead St", 'Zip Code': '77019'},
        }


    # Socket settings
    # SOCKET_SERVER_ADDRESS = ('localhost', 5700)  # Replace with the appropriate server address

    # # Will only send a message to Server if new_serialized_data has data
    # if len(new_deserialized_data)<10:
    #     while True:
    #         try:
    #             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    #                 # This will keep the attemp to connect going
    #                 while True:
    #                     try:
    #                         client_socket.connect(SOCKET_SERVER_ADDRESS)

    #                         # Send data to the server
    #                         def send_to_server():
    #                             server_response = ""

    #                             # Serialize the string using pickle
    #                             serialized_data = pickle.dumps('GO')

    #                             # Tell Server to go if there is new datat to process
    #                             # client_socket.sendall(serialized_data)

    #                             server_response = client_socket.recv(1024)

    #                             # Deserialize the pickled server response
    #                             server_response = pickle.loads(server_response)

    #                             #Return deserialized server response
    #                             return server_response
                            
    #                         # Initialize request counter
    #                         request_counter = 0

    #                         while True:
    #                             # print(f"Property Dictionary: {prop_dict}")
    #                             print(f"Request Count: {request_counter}")
    #                             server_response = send_to_server()
    #                             client_socket.close()

    #                             if server_response['state'] == "READY": 
    #                                 break
    #                             else: 
    #                                 # Wait the request_wait time sent by the server
    #                                 request_counter = request_counter + 1
    #                                 time.sleep(server_response["request_wait"])
    #                                 continue
    #                         break
    #                     except (ConnectionRefusedError):
    #                         print('Will try to connect again')
    #                         time.sleep(2)
    #                         continue
    #         except (ConnectionResetError):
    #             print('Connection unexpetedly closed, Trying to recconect')
    #             time.sleep(2)
    #             continue
                
    #         client_socket.close()

# This will run the code as soon as it's starting rather than waiting
HAR()

# This will run the code as soon as it's starting rather than waiting
schedule.every(10).minutes.do(HAR)

# Run any pending tasks before entering the while loop
# schedule.run_pending()

while True:
    schedule.run_pending()
    time.sleep(1)
