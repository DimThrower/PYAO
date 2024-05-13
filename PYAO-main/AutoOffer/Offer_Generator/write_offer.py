from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import os
import pyautogui
import ctypes
from selenium.webdriver.firefox.options import Options
from AutoOffer.Offer_Generator.HTML_TREC import (TextFields, CheckBoxes, Buttons, TREC_el_pg_1,
                              TREC_el_pg_2,TREC_el_pg_3,TREC_el_pg_4,TREC_el_pg_5,
                              TREC_el_pg_6,TREC_el_pg_7,TREC_el_pg_8,TREC_el_pg_9,
                              TREC_el_pg_10, TREC_el_pg_11)
from AutoOffer.Offer_Generator import misc
from AutoOffer import settings
import pygetwindow as gw
from AutoOffer.db import db_funct
from AutoOffer.html_manipulation.HTML import PropertyProfile

pp=PropertyProfile()

# Disable the fail-safe feature
pyautogui.FAILSAFE = False

def create_offer(doc_name, address, seller_name,
                buyer_name, price, lot, block,
                closing_date, title_company, legal_description,
                title_company_address,
                earnest_money, option_money, city, zip_code,
                subdivision, county, escrow_agent, option_days, trec_path, mls_id,
                ):
    
    try:
        # Specify the Firefox binary location
        binary = FirefoxBinary(firefox_path=settings.firefoxDrivePath)

        # Create Firefox options
        options = Options()

        # Run browser in headless mode
        # options.add_argument("--headless")

        # Create WebDriver instance
        browser = webdriver.Firefox(firefox_binary=binary, options=options)

        # Intialize TextFields, CheckBoxes, Elements, PropertyProfile classes
        text_field = TextFields()
        check_box = CheckBoxes()
        btns = Buttons()

        

        # Define some repetitive inputs
        initial = ''
        na = 'N/A'
        objecions_use = 'Single Family'
        sleep = 0

        # Check if the text is non
        def text_none_check(text):
            if text is None:
                return ""
            else:
                return text

        # Create the contract conenring input that goes at the top of the TREC page
        contract_concerning = f'{address}, {city}, TX {zip_code}'

        # Create a new window
        browser.execute_script("window.open();")

        # CLose the old window
        browser.close()

        # Switch to the new window
        browser.switch_to.window(browser.window_handles[-1])

        # Open the pdf TREC file
        browser.get(trec_path)

        # Click previous a bunch to go back to the first page
        for _ in range(1, 12):
            browser.find_element(
                By.CSS_SELECTOR, btns.previous).click()

        # Wait for the pdf to load so elements can find all the elements
        # misc.wait_until_appeared_BLOCK(
        #     browser=browser, css_element=text_field.seller, timeout=2)

        # Scale the page so that all the elements are visable
        browser.find_element(
            By.CSS_SELECTOR, btns.scale_dpdwn).click()
        browser.find_element(By.CSS_SELECTOR, btns.fitpage).click()

        # Find the next page button
        next_page_btn = browser.find_element(
            By.CSS_SELECTOR, btns.next)

        

        # First Page
        el_pg_1 = TREC_el_pg_1(browser=browser)
        el_pg_1.seller.send_keys(
            text_none_check(seller_name))
        el_pg_1.buyer.send_keys(
            text_none_check(buyer_name))
        el_pg_1.lot.send_keys(
            text_none_check(lot))
        el_pg_1.block.send_keys(
            text_none_check(block))
        el_pg_1.subdivision.send_keys(
            text_none_check(subdivision))
        el_pg_1.city.send_keys(
            text_none_check(city))
        el_pg_1.county.send_keys(
            text_none_check(county))
        el_pg_1.address.send_keys(
            text_none_check(f'{address} {zip_code}'))
        el_pg_1.exclusions.send_keys(
            text_none_check(na))
        el_pg_1.cash_portion.send_keys(
            text_none_check(price))
        el_pg_1.finance_portion.send_keys(
            text_none_check(na))
        el_pg_1.total_price.send_keys(
            text_none_check(price))
        el_pg_1.init_pg1.send_keys(
            text_none_check(initial))
        time.sleep(sleep)
        # Click the button to the next  page
        next_page_btn.click()
        time.sleep(sleep)

        
        # Second Page
        el_pg_2 = TREC_el_pg_2(browser=browser)
        el_pg_2.prop_add1.send_keys(
            text_none_check(contract_concerning))
        el_pg_2.escrow_agent.send_keys(
            text_none_check(escrow_agent))
        el_pg_2.title_address.send_keys(
            text_none_check(title_company_address))
        el_pg_2.em.send_keys(
            text_none_check(earnest_money))
        el_pg_2.om.send_keys(
            text_none_check(option_money))
        el_pg_2.add_em.send_keys(
            text_none_check(na))
        el_pg_2.add_em_days.send_keys(
            text_none_check(na))
        el_pg_2.option_days.send_keys(
            text_none_check(option_days))
        el_pg_2.buyer_pay_title_policy.click()
        el_pg_2.title_name.send_keys(
            text_none_check(title_company))
        el_pg_2.no_amend_or_del.click()
        el_pg_2.init_pg2.send_keys(
            text_none_check(initial))
        time.sleep(sleep)
        # Click the button to the next  page
        next_page_btn.click()
        time.sleep(sleep)

        # Third Page
        el_pg_3 = TREC_el_pg_3(browser=browser)
        el_pg_3.prop_add2.send_keys(
            text_none_check(contract_concerning))
        el_pg_3.buyer_pay_survey.click()
        el_pg_3.survey_days.send_keys(
            text_none_check('5'))
        el_pg_3.objections.send_keys(
            text_none_check(objecions_use))
        el_pg_3.objection_days.send_keys(
            text_none_check('3'))
        # if 'yes' in prop_dict[pp.hoa]:
        #     browser.find_element(
        #         By.CSS_SELECTOR, check_box.yes_hoa).click()
        # else:
        #     browser.find_element(
        #         By.CSS_SELECTOR, check_box.no_hoa).click()

        el_pg_3.no_hoa.click()
        el_pg_3.init_pg3.send_keys(
            text_none_check(initial))
        time.sleep(sleep)
        # Click the button to the next  page
        next_page_btn.click()
        time.sleep(sleep)

        # Fourth Page
        el_pg_4 = TREC_el_pg_4(browser=browser)
        el_pg_4.prop_add3.send_keys(
            text_none_check(contract_concerning))
        el_pg_4.req_notices.send_keys(
            text_none_check(na))
        el_pg_4.seller_disclosure.click()
        el_pg_4.sd_days.send_keys(
            text_none_check('5'))
        el_pg_4.init_pg4.send_keys(
            text_none_check(initial))
        time.sleep(sleep)
        # Click the button to the next  page
        next_page_btn.click()
        time.sleep(sleep)

        # Fifth Page
        el_pg_5 = TREC_el_pg_5(browser=browser)
        el_pg_5.prop_add4.send_keys(
            text_none_check(contract_concerning))
        el_pg_5.as_is.click()
        el_pg_5.service_contract.send_keys(
            text_none_check(na))
        el_pg_5.broker_discolsure.send_keys(
            text_none_check(na))#'Buyer has an active realtor license'))
        # Set the closing date
        cd = closing_date
        el_pg_5.closing_date.send_keys(
            text_none_check(cd))
        el_pg_5.init_pg5.send_keys(
            text_none_check(initial))
        time.sleep(sleep)
        # Click the button to the next  page
        next_page_btn.click()
        time.sleep(sleep)

        # Sixth Page
        el_pg_6 = TREC_el_pg_6(browser=browser)
        el_pg_6.prop_add5.send_keys(
            text_none_check(contract_concerning))
        el_pg_6.buyer_poss.click()
        el_pg_6.special_prov1.send_keys(
            text_none_check(legal_description))
        el_pg_6.special_prov2.send_keys(
            text_none_check('Buyers agrees to pay all standard closing cost, excluding due taxes, liens, and brokerage fees'))
        el_pg_6.special_prov3.send_keys(
            text_none_check('Option period to begin day after contract lockbox placed on property and code given to buyer'))
        el_pg_6.other_exp.send_keys(
            text_none_check(na))
        el_pg_6.init_pg6.send_keys(
            text_none_check(initial))
        time.sleep(sleep)
        # Click the button to the next  page
        next_page_btn.click()
        time.sleep(sleep)

        # Seventh Page
        el_pg_7 = TREC_el_pg_7(browser=browser)
        el_pg_7.prop_add6.send_keys(
            text_none_check(contract_concerning))
        el_pg_7.init_pg7.send_keys(
            text_none_check(initial))
        time.sleep(sleep)
        # Click the button to the next  page
        next_page_btn.click()
        time.sleep(sleep)

        # Eighth Page
        el_pg_8 = TREC_el_pg_8(browser=browser)
        el_pg_8.prop_add7.send_keys(
            text_none_check(contract_concerning))
        el_pg_8.buy_address.send_keys(
            text_none_check(""))#'2404 S Grand Blvd, Pearland, TX 77581'))
        el_pg_8.buy_email.send_keys(
            text_none_check(""))#'info@rightwayhomesolutions.com'))
        # if 'yes' in prop_dict[pp.hoa]:
        #     browser.find_element(
        #         By.CSS_SELECTOR, check_box.hoa_addendum).click()
        # if prop_dict[pp.lead_based_paint] is not None:
        el_pg_8.lbp_addendum.click()
        el_pg_8.init_pg8.send_keys(
            text_none_check(initial))
        time.sleep(sleep)
        # Click the button to the next  page
        next_page_btn.click()
        time.sleep(sleep)

        # Ninth Page
        el_pg_9 = TREC_el_pg_9(browser=browser)
        el_pg_9.prop_add8.send_keys(
            text_none_check(contract_concerning))
        time.sleep(sleep)
        # Click the button to the next  page
        next_page_btn.click()
        time.sleep(sleep)

        # Temth Page
        el_pg_10 = TREC_el_pg_10(browser=browser)
        el_pg_10.prop_add9.send_keys(
            text_none_check(contract_concerning))
        time.sleep(sleep)
        # Click the button to the next  page
        next_page_btn.click()
        time.sleep(sleep)

        # Eleventh Page
        el_pg_11 = TREC_el_pg_11(browser=browser)
        el_pg_11.prop_add10.send_keys(
            text_none_check(contract_concerning))

        # Click the download button
        browser.find_element(By.CSS_SELECTOR, '#download').click()

        # Wait some time for 'Save As' window to appear
        time.sleep(5)

        # Set contract save path
        # offer_folder = settings.contract_save_path


        # offer_folder = f'{settings.filled_TREC_file_path_HOU}\\{mls_id}'
        offer_folder = os.path.join(str(settings.filled_TREC_file_path_HOU), str(mls_id))

        if not os.path.exists(offer_folder):
            # Create the folder
            os.mkdir(offer_folder)
        else:
            print(f"Delete empty folder due to error and remake it")
            os.rmdir(offer_folder)
            os.mkdir(offer_folder)
        
        print(f"Create Houston Contract")



        # Generate appropriates file path, take out "/" and replace with "-"
        modified_string_filename = doc_name.replace(
            "/", "-")

        # Set path for pdf file
        # file_path = f'{offer_folder}\\{modified_string_filename}.pdf'
        file_path = os.path.join(offer_folder,f'{modified_string_filename}.pdf')
        print(
            f"Path for file offer_folder: {offer_folder}\nmodified_string_filename: {modified_string_filename}\nfile path: {file_path}")

        start_time = time.time()
        while True:
            # Find the save as window
            windows = gw.getWindowsWithTitle('Save As')

            if len(windows) > 0:
                # Get save as window from windows
                save_as_window = windows[0]

                # Activate the save as window
                ctypes.windll.user32.SetForegroundWindow(
                    save_as_window._hWnd)

                # Make the pdf file name
                pyautogui.typewrite(file_path)
                time.sleep(1)

                # Activate the save as window
                ctypes.windll.user32.SetForegroundWindow(
                    save_as_window._hWnd)

                # Press enter on the Save as window to save pdf
                pyautogui.press('enter')

            if time.time() - start_time > 20:
                print(f'File did not save: {file_path}')
                return "file already exist", file_path
                
            if os.path.isfile(file_path):
                print(f'File saved: {file_path}')

                db_funct.multi_db_update(mls_id=mls_id,
                                            data_dict={
                                                pp.close_date: cd,
                                                pp.pdf_offer_path: file_path,
                                            },
                                            overwrite=True,)


                return "file saved", file_path
            

            else:
                continue

    finally:
        time.sleep(1)
        browser.quit()
