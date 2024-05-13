from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import os
import pyautogui
import shutil
import schedule
import ctypes
from selenium.webdriver.firefox.options import Options
from AutoOffer import settings
from HTML import TextFields, CheckBoxes, Buttons
from AutoOffer.html_manipulation.HTML import PropertyProfile
from AutoOffer.misc import *
from AutoOffer import settings
from AutoOffer.db import db_funct
from AutoOffer.html_manipulation.HTML import PropertyProfile
from AutoOffer.Offer_Generator.misc import generate_closing_date
from AutoOffer.Offer_Generator import write_offer
from AutoOffer.Offer_Generator import write_offer_v2
import HTML_TREC

# Create Db
# db_funct.create_db()

pp = PropertyProfile()
pdf_text_fields = HTML_TREC.TextFields()
pdf_box_fields = HTML_TREC.CheckBoxes()
na = "N/A"
checked = "/On"

time.sleep(4)

def create_offers():
    # Check to see if db needs to be created
    db_funct.create_db()

    prop_dicts = db_funct.get_sorted_rows_with_values_and_null(
        sort_column='Last_Updated',
        null_column=pp.pdf_offer_path,
                    value_dict={pp.deal_taken: 'No', }
    )

    # Check to see if are any properties to make offers
    if (prop_dicts):
        print(f'Number of properties are {len(prop_dicts)}')
        # Filter out the properties that need an offer created
        for prop_dict in prop_dicts:
            # Only creating offers for properties that do not have them
            if prop_dict[pp.pdf_offer_path] is None:

                
                # write_offer.create_offer(doc_name=f"Offer for {prop_dict[pp.steet_address]}",
                #         address=prop_dict[pp.steet_address],
                #         seller_name=prop_dict[pp.owner_name],
                #         buyer_name="Cornerstone Home Solutions, LLC",
                #         price=prop_dict[pp.offer_price],
                #         lot=prop_dict[pp.lot],
                #         block=prop_dict[pp.block],
                #         closing_date=generate_closing_date(21),
                #         title_company=prop_dict[pp.title_company_name],
                #         legal_description=prop_dict[pp.legal_description],
                #         title_company_address=prop_dict[pp.title_company_address],
                #         earnest_money=prop_dict[pp.em],
                #         option_money=prop_dict[pp.om],
                #         city=prop_dict[pp.city],
                #         zip_code=prop_dict[pp.zip_Code],
                #         subdivision=prop_dict[pp.subdivision],
                #         county=prop_dict[pp.county],
                #         escrow_agent=prop_dict[pp.escrow_agent],
                #         option_days=prop_dict[pp.option_days],
                #         trec_path=settings.blank_TREC_file_path,
                #         mls_id=prop_dict[pp.mls_id],                                              
                # )

                
                contract_concerning = f'{prop_dict[pp.steet_address]}, {prop_dict[pp.city]}, TX {prop_dict[pp.zip_Code]}'

                
                if prop_dict[pp.lead_based_paint]:
                    lbp_check_box = checked
                else:
                    lbp_check_box = ""

                if 'Yes' in prop_dict[pp.hoa]:
                    hoa_yes_check_box = checked
                    hoa_no_check_box = ""
                else:
                    hoa_yes_check_box = ""
                    hoa_no_check_box = checked

                pdf_data_dict = {
                        #1st Page
                        pdf_text_fields.seller: prop_dict[pp.owner_name],
                        pdf_text_fields.buyer: "Cornerstone Home Solutions, LLC",
                        pdf_text_fields.lot: str(prop_dict[pp.lot]),
                        pdf_text_fields.block: str(prop_dict[pp.block]),
                        pdf_text_fields.subdivision: prop_dict[pp.subdivision],
                        pdf_text_fields.city: prop_dict[pp.city],
                        pdf_text_fields.county: prop_dict[pp.county],
                        pdf_text_fields.address: f"{prop_dict[pp.steet_address]}, {prop_dict[pp.zip_Code]}",
                        pdf_text_fields.exclusions: na,
                        pdf_text_fields.cash_portion: str(prop_dict[pp.offer_price]),
                        pdf_text_fields.finance_portion: na,
                        pdf_text_fields.total_price: str(prop_dict[pp.offer_price]),

                        #2nd Page
                        pdf_text_fields.prop_add1: contract_concerning,
                        pdf_text_fields.escrow_agent: prop_dict[pp.escrow_agent],
                        pdf_text_fields.title_address: prop_dict[pp.title_company_address],
                        pdf_text_fields.em: prop_dict[pp.em],
                        pdf_text_fields.add_em_days: na,
                        pdf_text_fields.om: prop_dict[pp.om],
                        pdf_text_fields.option_days: prop_dict[pp.option_days],
                        pdf_box_fields.buyer_pay_title_policy: checked,
                        pdf_text_fields.title_company_name: prop_dict[pp.title_company_name],
                        pdf_box_fields.no_amend_or_del: checked,

                        #3rd Page
                        pdf_text_fields.prop_add2: contract_concerning,
                        pdf_box_fields.buyer_pay_survey: checked,
                        pdf_text_fields.survey_days: "5",
                        pdf_text_fields.objections: "Single-Family",
                        pdf_text_fields.objection_days: "3",
                        pdf_box_fields.yes_hoa: hoa_yes_check_box,
                        pdf_box_fields.no_hoa: hoa_no_check_box,

                        #4th Page
                        pdf_text_fields.prop_add3: contract_concerning,
                        pdf_text_fields.req_notices: na,
                        pdf_box_fields.seller_disclosure: checked,
                        pdf_text_fields.sd_days: "5",

                        #5th Page
                        pdf_text_fields.prop_add4: contract_concerning,
                        pdf_box_fields.as_is: checked,
                        pdf_text_fields.service_contract: na,
                        pdf_text_fields.broker_discolsure: na,
                        pdf_text_fields.closing_date: str(generate_closing_date(21)),

                        #6th Page
                        pdf_text_fields.prop_add5: contract_concerning,
                        pdf_text_fields.service_contract: na,
                        pdf_box_fields.buyer_poss: checked,
                        pdf_text_fields.special_prov1: prop_dict[pp.legal_description],
                        pdf_text_fields.special_prov2: 'Buyers agrees to pay all standard closing cost, excluding due taxes, liens, and brokerage fees',
                        pdf_text_fields.special_prov3: 'Option period to begin day after contract lockbox placed on property and code given to buyer',
                        pdf_text_fields.other_exp: na,   

                        #7th Page
                        pdf_text_fields.prop_add6: contract_concerning,

                        #8th Page
                        pdf_text_fields.prop_add7: contract_concerning,
                        pdf_box_fields.lbp_addendum: lbp_check_box,
                        pdf_box_fields.hoa_addendum: hoa_yes_check_box,
                        pdf_text_fields.buy_email: "charles@cornerstonehomesolutions.com",

                        #9th Page
                        pdf_text_fields.prop_add8: contract_concerning,

                        #10th Page
                        pdf_text_fields.prop_add9: contract_concerning,

                        #11th Page
                        pdf_text_fields.prop_add10: contract_concerning,
                        }
                
                offer_folder = os.path.join(settings.filled_TREC_file_path_HOU, f"{str(prop_dict[pp.mls_id])}")
                
                try:
                    os.mkdir(offer_folder)
                except FileExistsError:
                    print(f'Delete old folder to make new: {offer_folder}')
                    os.rmdir(offer_folder)
                    os.mkdir(offer_folder)

                output_pdf_path = os.path.join(offer_folder, f"Offer for {prop_dict[pp.steet_address].replace('/','-')}, {prop_dict[pp.zip_Code]}.pdf")

                save_successsful = write_offer_v2.fill_pdf(input_pdf_path=settings.blank_TREC_file_path,
                                                 output_pdf_path=output_pdf_path,
                                                 pdf_data_dict=pdf_data_dict)
                if save_successsful:
                    db_funct.multi_db_update(mls_id=prop_dict[pp.mls_id],
                                            data_dict={
                                                pp.close_date: str(generate_closing_date(21)),
                                                pp.pdf_offer_path: output_pdf_path,
                                            },
                                            overwrite=True,)
                    
                    print(f"{prop_dict[pp.steet_address]} file saved")

        print(f'All offer made, waiting for next scheduled run')
        
    else:
        print('No properties to send offer on. Waits for next schedule')

# This will run the code as soon as code is run
create_offers()

# This will run the code after a set amount of tim
schedule.every(1).minutes.do(lambda: create_offers())

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

