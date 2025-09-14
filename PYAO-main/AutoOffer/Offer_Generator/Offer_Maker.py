
import logging
import os
from AutoOffer.Offer_Generator import pdf_statics, pdf_utils
# from shared import shared_statics, shared_config
from AutoOffer.html_manipulation.HTML import PropertyProfile
from AutoOffer.db import db_funct
from AutoOffer import settings
from AutoOffer.Offer_Generator.misc import generate_closing_date
import schedule
import time




logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

pp = PropertyProfile()

pdf_text_fields = pdf_statics.TextFields()
pdf_box_fields = pdf_statics.CheckBoxes()
pdf_lot_text_fields = pdf_statics.LotTextFields()
pdf_lot_box_fields = pdf_statics.LotCheckBoxes()

na = "N/A"
checked = "/On"


#def create_offer_1_to_4(prop_dict, input_file):
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

    #logging.info(f"Creating 1-4 Offer for {prop_dict["Page 1"][pdf_statics.address]}")

    # Realist tax has no ifo on hOA so always check no
    # hoa_no_check_box = checked

    # contract_concerning = f"{prop_dict[shared_statics.street_address]}, {prop_dict[shared_statics.city]}, {prop_dict[shared_statics.zipcode]} TX"

    # Determing if LBP needs to be checked
    # if int(prop_dict[shared_statics.year_built]) <= 1979:
    #     lbp_check_box = checked
    # else:
    #     lbp_check_box = ""

    # Always check no for HOA since realist doesn't say
    # hoa_no_check_box = checked

                property_full_addy = f'{prop_dict[pp.steet_address]}, {prop_dict[pp.city]}, TX {prop_dict[pp.zip_Code]}'

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
                    pdf_text_fields.cash_portion: str(pdf_utils.remove_non_numeric(prop_dict[pp.offer_price])),
                    pdf_text_fields.finance_portion: 0,
                    pdf_box_fields.third_party_finance: False, #True if int(prop_dict["Page 1"][pdf_statics.finance_portion])>0 else False,
                    pdf_text_fields.total_price: str(pdf_utils.remove_non_numeric(prop_dict[pp.offer_price])),

                    #2nd Page
                    pdf_text_fields.prop_add1: property_full_addy,#prop_dict["Page 2"][pdf_statics.prop_add1],
                    pdf_text_fields.escrow_agent: prop_dict[pp.escrow_agent],
                    pdf_text_fields.title_address: prop_dict[pp.title_company_address],
                    pdf_text_fields.em: prop_dict[pp.em],
                    pdf_text_fields.add_em: 0,
                    pdf_text_fields.add_em_days: 0,
                    pdf_text_fields.om: prop_dict[pp.om],
                    pdf_text_fields.option_days: prop_dict[pp.option_days],
                    pdf_box_fields.seller_pay_title_policy: "", #not prop_dict["Page 2"][pdf_statics.buyer_pay_title_policy],
                    pdf_box_fields.buyer_pay_title_policy: True, #prop_dict["Page 2"][pdf_statics.buyer_pay_title_policy],
                    pdf_text_fields.title_company_name: prop_dict[pp.title_company_name],
                    pdf_box_fields.no_amend_or_del: True, #prop_dict["Page 2"][pdf_statics.no_amend_or_del],

                    #3rd Page
                    pdf_text_fields.prop_add2: property_full_addy,#prop_dict["Page 3"][pdf_statics.prop_add2],
                    pdf_box_fields.buyer_pay_survey: True, #prop_dict["Page 3"][pdf_statics.buyer_pay_survey],
                    pdf_text_fields.survey_days: "10",#prop_dict["Page 3"][pdf_statics.survey_days],
                    pdf_text_fields.objections: "Single-Family", #prop_dict["Page 3"][pdf_statics.objections],
                    pdf_text_fields.objection_days: "3",#prop_dict["Page 3"][pdf_statics.objection_days],
                    pdf_box_fields.yes_hoa: True if prop_dict[pp.hoa] == "Yes" else False,
                    pdf_box_fields.no_hoa: True if prop_dict[pp.hoa] != "Yes" else False,

                    #4th Page
                    pdf_text_fields.prop_add3: property_full_addy,#prop_dict["Page 4"][pdf_statics.prop_add3],
                    pdf_text_fields.req_notices: "Buyer is a licensed Sales Agent",
                    pdf_box_fields.seller_disclosure: True,
                    pdf_text_fields.sd_days: "5",

                    #5th Page
                    pdf_text_fields.prop_add4: property_full_addy,#prop_dict["Page 5"][pdf_statics.prop_add4],
                    pdf_box_fields.as_is: True,
                    pdf_text_fields.service_contract: na,
                    pdf_text_fields.broker_discolsure: na,
                    pdf_text_fields.closing_date: str(pdf_utils.generate_closing_date(21)),

                    #6th Page
                    pdf_text_fields.prop_add5: property_full_addy,#prop_dict["Page 6"][pdf_statics.prop_add5],
                    pdf_box_fields.buyer_poss: True,
                    pdf_text_fields.special_prov1: "",#prop_dict["Page 6"][pdf_statics.special_prov1],
                    pdf_text_fields.special_prov2: "Buyers agrees to pay all standard closing cost, excluding due taxes, liens, and brokerage fees",
                    pdf_text_fields.special_prov3: 'Option period to begin day after contract lockbox placed on property and code given to buyer',
                    pdf_box_fields.flat_commission: "0",#True if int(prop_dict["Page 6"][pdf_statics.flat_commission_amount])>0 else False,
                    pdf_text_fields.flat_commission_amount:"0",# prop_dict["Page 6"][pdf_statics.flat_commission_amount],
                    pdf_box_fields.percent_commission:"0",#True if int(prop_dict["Page 6"][pdf_statics.percent_commission_amount])>0 else False,
                    pdf_text_fields.percent_commission_amount:"0",# prop_dict["Page 6"][pdf_statics.percent_commission_amount],
                    pdf_text_fields.seller_max_contribution:"0",# prop_dict["Page 6"][pdf_statics.seller_max_contribution],


                    #7th Page
                    pdf_text_fields.prop_add6: property_full_addy,#prop_dict["Page 7"][pdf_statics.prop_add6],

                    #8th Page
                    pdf_text_fields.prop_add7: property_full_addy,#prop_dict["Page 8"][pdf_statics.prop_add7],
                    pdf_box_fields.lbp_addendum: True if int(prop_dict[pp.year_built]) <= 1978 else False,
                    pdf_box_fields.hoa_addendum: True if prop_dict[pp.hoa] == "Yes" else False,
                    pdf_box_fields.tpf_addendum: False, #True if int(prop_dict["Page 1"][pdf_statics.finance_portion])>0 else False,
                    pdf_text_fields.buy_email: "charles@cornerstonehomesolutions.com",

                    #9th Page
                    pdf_text_fields.prop_add8: property_full_addy,#prop_dict["Page 9"][pdf_statics.prop_add8],

                    #10th Page
                    pdf_text_fields .prop_add9: property_full_addy,#prop_dict["Page 10"][pdf_statics.prop_add9],

                    #11th Page
                    pdf_text_fields.prop_add10: property_full_addy,#prop_dict["Page 11"][pdf_statics.prop_add10],

                    # Sellers Disclosure
                    # pdf_text_fields.sd_prop_1: property_full_addy,
                    # pdf_text_fields.sd_prop_2: property_full_addy,
                    # pdf_text_fields.sd_prop_3: property_full_addy,
                    # pdf_text_fields.sd_prop_4: property_full_addy,

                    # # LBP
                    # pdf_text_fields.lbp_prop_1: property_full_addy,

                    # # EM Deposit
                    # pdf_text_fields.rd_prop_1: property_full_addy,
                    # pdf_text_fields.rd_buyer: prop_dict["Page 1"][pdf_statics.buyer],
                    # pdf_text_fields.rd_buyer_phone: prop_dict["Backside"][pdf_statics.rd_buyer_phone],
                    # pdf_text_fields.rd_buyer_address: prop_dict["Backside"][pdf_statics.rd_buyer_address],
                    # pdf_text_fields.rd_earnest_money: f"${prop_dict["Page 2"][pdf_statics.em]}",

                    # #Finance Addendum
                    # pdf_text_fields.tpa_prop_1: property_full_addy,
                    # pdf_text_fields.tpa_lender_name: "Searchers Capital",
                    # pdf_text_fields.tpa_principal: str(prop_dict["Page 1"][pdf_statics.finance_portion]),
                    # pdf_text_fields.tpa_loan_yrs: "0.5",
                    # pdf_text_fields.tpa_loan_interst: prop_dict["Finance"][pdf_statics.tpa_loan_interst],
                    # pdf_text_fields.tpa_first_year_interest: "3",
                    # pdf_text_fields.tpa_origination_charge: "2",
                    # pdf_box_fields.tpa_waive_rights_yes: prop_dict["Finance"][pdf_statics.tpa_waive_rights_yes],
                    # pdf_box_fields.tpa_waive_rights_no: not prop_dict["Finance"][pdf_statics.tpa_waive_rights_yes],
                    # pdf_box_fields.tpa_other_fin: True if int(prop_dict["Page 1"][pdf_statics.finance_portion])>0 else False,
                    # pdf_box_fields.tpa_lender_approval_yes: True if int(prop_dict["Page 1"][pdf_statics.finance_portion])>0 else False,
                    # pdf_text_fields.tpa_lender_approval_days: 10,
                    # pdf_text_fields.tpa_prop_2: property_full_addy,
                    }
                
                #offer_folder = shared_config.saved_contract_path
                offer_folder = os.path.join(settings.filled_TREC_file_path_HOU, f"{str(prop_dict[pp.mls_id])}")
                try:
                    os.mkdir(offer_folder)
                except FileExistsError:
                    print(f'Delete old folder to make new: {offer_folder}')
                    os.rmdir(offer_folder)
                    os.mkdir(offer_folder)

                print(f'HOA value for {prop_dict[pp.steet_address]} is: {prop_dict[pp.hoa]}')

                output_pdf_path = os.path.join(offer_folder, f"Offer for {prop_dict[pp.steet_address].replace('/','-')}, {prop_dict[pp.zip_Code]}.pdf")

                save_successsful = pdf_utils.fill_pdf(input_pdf_path=settings.blank_TREC_file_path,
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
                # # output_pdf_path = os.path.join(offer_folder, f"Offer for {prop_dict[shared_statics.street_address].replace('/','-')}, {prop_dict[shared_statics.zipcode]}.pdf")
                # output_pdf_path = os.path.join(offer_folder, f"Offer for {prop_dict["Page 1"][pdf_statics.address].replace('/','-')}.pdf")


                # save_successsful = pdf_utils.fill_pdf(input_pdf_path=input_file,
                #                                     output_pdf_path=output_pdf_path,
                #                                     pdf_data_dict=pdf_data_dict)
                # if save_successsful:    
                #     logging.info(f"File Saved: {prop_dict["Page 1"][pdf_statics.address]}")
        
