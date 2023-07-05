from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time, os, pyautogui, shutil, schedule, ctypes
from selenium.webdriver.firefox.options import Options
from AutoOffer import settings
from HTML import TextFields, CheckBoxes, Buttons
from AutoOffer.html_manipulation.HTML import PropertyProfile
from AutoOffer.misc import *
from AutoOffer import settings
from AutoOffer.db import db_funct
import pygetwindow as gw

# Create Db
db_funct.create_db()



# Specify the Firefox binary location
binary = FirefoxBinary(firefox_path=settings.firefoxDrivePath)

# Create Firefox options
options = Options()

# Run browser in headless mode
options.add_argument("--headless")

# Create WebDriver instance
browser = webdriver.Firefox(firefox_binary=binary, options=options)

# Intialize TextFields, CheckBoxes, Elements, PropertyProfile classes
text_field = TextFields()
check_box = CheckBoxes()
pp = PropertyProfile()
btns = Buttons()

# Define some repetitive inputs
initial = 'JD'
na = 'N/A'
objecions_use = 'Single Family'
sleep = 0

# Check if the text is non
def text_none_check(text):
    if text is None:
        return ""
    else:
        return text
    

def create_offers():
    # Check to see if db needs to be created
    db_funct.create_db()

    prop_dicts = db_funct.get_sorted_rows_with_values_and_null(
                    sort_column='Last_Updated',
                    null_column=pp.pdf_offer_path,
                    value_dict={pp.deal_taken: 'No',}
                    )

    # Check to see if are any properties to make offers
    if (prop_dicts):   
        print(f'Number of properties are {len(prop_dicts)}')
        # Filter out the properties that need an offer created
        for prop_dict in prop_dicts:
            # Only creating offers for properties that do not have them
            if prop_dict[pp.pdf_offer_path] is None:

                # Get the mls_id from the matrix
                mls_id = prop_dict.pop(pp.mls_id)

                # Creat the contract conenring input that goes at the top of the TREC page
                contract_concerning = f'{prop_dict[pp.steet_address]}, {prop_dict[pp.city]}, {prop_dict[pp.state]} {prop_dict[pp.zip_Code]}'

                # Create a new window
                browser.execute_script("window.open();")

                # CLose the old window
                browser.close()

                # Switch to the new window
                browser.switch_to.window(browser.window_handles[-1])

                # Open the pdf TREC file
                browser.get(settings.blank_TREC_file_path)

                # Click previous a bunch to go back to the first page
                for _ in range(1, 12):
                    browser.find_element(By.CSS_SELECTOR, btns.previous).click()

                # Wait for the pdf to load so elements can find all the elements
                wait_until_appeared_BLOCK(browser=browser, css_element=text_field.seller, timeout=10)

                # Scale the page so that all the elements are visable
                browser.find_element(By.CSS_SELECTOR, btns.scale_dpdwn).click()
                browser.find_element(By.CSS_SELECTOR, btns.fitpage).click()

                # Find the next page button
                next_page_btn = browser.find_element(By.CSS_SELECTOR, btns.next)

                # First Page
                browser.find_element(By.CSS_SELECTOR, text_field.seller).send_keys(text_none_check(prop_dict[pp.owner_name]))
                browser.find_element(By.CSS_SELECTOR, text_field.buyer).send_keys(text_none_check('RWHS, LLC'))
                browser.find_element(By.CSS_SELECTOR, text_field.lot).send_keys(text_none_check(prop_dict[pp.lot]))
                browser.find_element(By.CSS_SELECTOR, text_field.block).send_keys(text_none_check(prop_dict[pp.block]))
                browser.find_element(By.CSS_SELECTOR, text_field.subdivision).send_keys(text_none_check(prop_dict[pp.subdivision]))
                browser.find_element(By.CSS_SELECTOR, text_field.city).send_keys(text_none_check(prop_dict[pp.city]))
                browser.find_element(By.CSS_SELECTOR, text_field.county).send_keys(text_none_check(prop_dict[pp.county]))
                browser.find_element(By.CSS_SELECTOR, text_field.address).send_keys(text_none_check(f'{prop_dict[pp.steet_address]} {prop_dict[pp.zip_Code]}'))
                browser.find_element(By.CSS_SELECTOR, text_field.exclusions).send_keys(text_none_check(na))
                browser.find_element(By.CSS_SELECTOR, text_field.cash_portion).send_keys(text_none_check(prop_dict[pp.offer_price]))
                browser.find_element(By.CSS_SELECTOR, text_field.finance_portion).send_keys(text_none_check(na))
                browser.find_element(By.CSS_SELECTOR, text_field.total_price).send_keys(text_none_check(prop_dict[pp.offer_price]))
                browser.find_element(By.CSS_SELECTOR, text_field.init_pg1).send_keys(text_none_check(initial))
                time.sleep(sleep)
                # Click the button to the next  page
                next_page_btn.click()
                time.sleep(sleep)

                # Second Page
                browser.find_element(By.CSS_SELECTOR, text_field.prop_add1).send_keys(text_none_check(contract_concerning))
                browser.find_element(By.CSS_SELECTOR, text_field.escrow_agent).send_keys(text_none_check(prop_dict[pp.escrow_agent]))
                browser.find_element(By.CSS_SELECTOR, text_field.title_address).send_keys(text_none_check(prop_dict[pp.title_company_address]))
                browser.find_element(By.CSS_SELECTOR, text_field.em).send_keys(text_none_check(prop_dict[pp.em]))
                browser.find_element(By.CSS_SELECTOR, text_field.om).send_keys(text_none_check(prop_dict[pp.om]))
                browser.find_element(By.CSS_SELECTOR, text_field.add_em).send_keys(text_none_check(na))
                browser.find_element(By.CSS_SELECTOR, text_field.add_em_days).send_keys(text_none_check(na))
                browser.find_element(By.CSS_SELECTOR, text_field.option_days).send_keys(text_none_check(prop_dict[pp.option_days]))
                browser.find_element(By.CSS_SELECTOR, check_box.buyer_pay_title_policy).click()
                browser.find_element(By.CSS_SELECTOR, text_field.title_company_name).send_keys(text_none_check(prop_dict[pp.title_company_name]))
                browser.find_element(By.CSS_SELECTOR, check_box.no_amend_or_del).click()
                browser.find_element(By.CSS_SELECTOR, text_field.init_pg2).send_keys(text_none_check(initial))
                time.sleep(sleep)
                # Click the button to the next  page
                next_page_btn.click()
                time.sleep(sleep)

                # Third Page
                browser.find_element(By.CSS_SELECTOR, text_field.prop_add2).send_keys(text_none_check(contract_concerning))
                browser.find_element(By.CSS_SELECTOR, check_box.buyer_pay_survey).click()
                browser.find_element(By.CSS_SELECTOR, text_field.survey_days).send_keys(text_none_check('5'))
                browser.find_element(By.CSS_SELECTOR, text_field.objections).send_keys(text_none_check(objecions_use))
                browser.find_element(By.CSS_SELECTOR, text_field.objection_days).send_keys(text_none_check('3'))
                if 'yes' in prop_dict[pp.hoa]:
                    browser.find_element(By.CSS_SELECTOR, check_box.yes_hoa).click()
                else:
                    browser.find_element(By.CSS_SELECTOR, check_box.no_hoa).click()
                browser.find_element(By.CSS_SELECTOR, text_field.init_pg3).send_keys(text_none_check(initial))
                time.sleep(sleep)
                # Click the button to the next  page
                next_page_btn.click()
                time.sleep(sleep)

                # Fourth Page
                browser.find_element(By.CSS_SELECTOR, text_field.prop_add3).send_keys(text_none_check(contract_concerning))
                browser.find_element(By.CSS_SELECTOR, text_field.req_notices).send_keys(text_none_check(na))
                browser.find_element(By.CSS_SELECTOR, check_box.seller_disclosure).click()
                browser.find_element(By.CSS_SELECTOR, text_field.sd_days).send_keys(text_none_check('5'))
                browser.find_element(By.CSS_SELECTOR, text_field.init_pg4).send_keys(text_none_check(initial))
                time.sleep(sleep)
                # Click the button to the next  page
                next_page_btn.click()
                time.sleep(sleep)

                # Fifth Page
                browser.find_element(By.CSS_SELECTOR, text_field.prop_add4).send_keys(text_none_check(contract_concerning))
                browser.find_element(By.CSS_SELECTOR, check_box.as_is).click()
                browser.find_element(By.CSS_SELECTOR, text_field.service_contract).send_keys(text_none_check(na))
                browser.find_element(By.CSS_SELECTOR, text_field.broker_discolsure).send_keys(text_none_check('Buyer has an active realtor license'))
                # Set the closing date
                cd = add_weeks_and_get_business_day(weeks=3)
                browser.find_element(By.CSS_SELECTOR, text_field.closing_date).send_keys(text_none_check(cd))
                browser.find_element(By.CSS_SELECTOR, text_field.init_pg5).send_keys(text_none_check(initial))
                time.sleep(sleep)
                # Click the button to the next  page
                next_page_btn.click()
                time.sleep(sleep)

                # Sixth Page
                browser.find_element(By.CSS_SELECTOR, text_field.prop_add5).send_keys(text_none_check(contract_concerning))
                browser.find_element(By.CSS_SELECTOR, check_box.buyer_poss).click()
                browser.find_element(By.CSS_SELECTOR, text_field.special_prov1).send_keys(text_none_check(prop_dict[pp.legal_description]))
                browser.find_element(By.CSS_SELECTOR, text_field.other_exp).send_keys(text_none_check(na))
                browser.find_element(By.CSS_SELECTOR, text_field.init_pg6).send_keys(text_none_check(initial))
                time.sleep(sleep)
                # Click the button to the next  page
                next_page_btn.click()
                time.sleep(sleep)

                # Seventh Page
                browser.find_element(By.CSS_SELECTOR, text_field.prop_add6).send_keys(text_none_check(contract_concerning))
                browser.find_element(By.CSS_SELECTOR, text_field.init_pg7).send_keys(text_none_check(initial))
                time.sleep(sleep)
                # Click the button to the next  page
                next_page_btn.click()
                time.sleep(sleep)

                # Eighth Page
                browser.find_element(By.CSS_SELECTOR, text_field.prop_add7).send_keys(text_none_check(contract_concerning))
                browser.find_element(By.CSS_SELECTOR, text_field.buy_address).send_keys(text_none_check('2404 S Grand Blvd, Pearland, TX 77581'))
                browser.find_element(By.CSS_SELECTOR, text_field.buy_email).send_keys(text_none_check('info@rightwayhomesolutions.com'))
                if 'yes' in prop_dict[pp.hoa]:
                    browser.find_element(By.CSS_SELECTOR, check_box.hoa_addendum).click()
                if prop_dict[pp.lead_based_paint] is not None:
                    browser.find_element(By.CSS_SELECTOR, check_box.lbp_addendum).click()
                browser.find_element(By.CSS_SELECTOR, text_field.init_pg8).send_keys(text_none_check(initial))
                time.sleep(sleep)
                # Click the button to the next  page
                next_page_btn.click()
                time.sleep(sleep)

                # Ninth Page
                browser.find_element(By.CSS_SELECTOR, text_field.prop_add8).send_keys(text_none_check(contract_concerning))
                time.sleep(sleep)
                # Click the button to the next  page
                next_page_btn.click()
                time.sleep(sleep)

                # Temth Page
                browser.find_element(By.CSS_SELECTOR, text_field.prop_add9).send_keys(text_none_check(contract_concerning))
                time.sleep(sleep)
                # Click the button to the next  page
                next_page_btn.click()
                time.sleep(sleep)

                # Eleventh Page
                browser.find_element(By.CSS_SELECTOR, text_field.prop_add10).send_keys(text_none_check(contract_concerning))

                # Click the download button
                browser.find_element(By.CSS_SELECTOR, '#download').click()

                # Wait some time for 'Save As' window to appear
                time.sleep(5)

                # Create the folder where the documents for this property will be held
                offer_folder = f'{settings.filled_TREC_file_path}\\{mls_id}'
                os.mkdir(offer_folder) # Make the folder the MLS ID

                # Generate appropriates file path, take out "/" and replace with "-"
                modified_string_filename = prop_dict[pp.steet_address].replace("/", "-")
                
                # Set path for pdf file
                file_path = f'{offer_folder}\\Cash Offer for {modified_string_filename}.pdf'
                print(f"Path for file offer_folder: {offer_folder} \nmodified_string_filename: {modified_string_filename}\nfile path: {file_path}")


                start_time = time.time()
                while True:
                    # Find the save as window
                    windows = gw.getWindowsWithTitle('Save As')

                    if len(windows) > 0:
                        # Get save as window from windows
                        save_as_window = windows[0]

                        # Activate the save as window
                        ctypes.windll.user32.SetForegroundWindow(save_as_window._hWnd)

                        # Make the pdf file name
                        pyautogui.typewrite(file_path)
                        time.sleep(1)

                        # Activate the save as window
                        ctypes.windll.user32.SetForegroundWindow(save_as_window._hWnd)

                        # Press enter on the Save as window to save pdf
                        pyautogui.press('enter')

                    if time.time() - start_time > 20:
                        # If the time limit is reached
                        # Remove the folder if it did not save
                        shutil.rmtree(offer_folder)
                        print("Folder deleted successfully.")
                        break

                    try:
                        files = os.listdir(offer_folder)
                        # print(f'{os.path.join(offer_folder, files[0])} AND {file_path}')
                        if os.path.join(offer_folder, files[0]) == file_path:
                            print(f'File saved: {file_path}')

                            db_funct.multi_db_update(mls_id=mls_id,
                                                    data_dict={
                                                        pp.close_date: cd,
                                                        pp.pdf_offer_path: file_path,
                                                    },
                                                    overwrite=True,)

                            break
                        else:
                            time.sleep(1)
                            print(f'File did not save: {file_path}')

                    except IndexError:
                        time.sleep(1)
                        print(f'File did not save: {file_path}')
        print(f'All offer made, waiting for next scheduled run')
    else:
        print('No properties to send offer on. Waits for next schedule')

# This will run the code as soon as code is run
create_offers()

# This will run the code after a set amount of tim
schedule.every(10).minutes.do(lambda: create_offers())

# Run the scheduled task and handle client connections
while True:
    # Check to see if db needs to be created
    schedule.run_pending()
    time.sleep(1)

# import os

# folder_path = '/path/to/folder'

# # List files in the folder
# files = os.listdir(folder_path)

# # Check if there is only one file in the folder
# if len(files) == 1:
#     file_path = os.path.join(folder_path, files[0])
#     print("File path:", file_path)
# else:
#     print("There is not exactly one file in the folder.")
