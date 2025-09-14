from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException, ElementNotInteractableException, NoSuchElementException
# from shared import shared_statics


seller = "seller"
buyer = "buyer"
lot = "lot"
block = "block"
subdivision = "subdivision"
city = "city"
county = "county"
address = "address"
exclusions = "exclusions"
cash_portion = "cash_portion"
third_party_finance = "third_party_finance"
finance_portion = "finance_portion"
total_price = "total_price"
escrow_agent = "escrow_agent"
title_address = "title_address"
em = "em"
om = "om"
add_em = "add_em"
add_em_days = "add_em_days"
option_days = "option_days"
title_company_name = "title_company_name"
survey_days = "survey_days"
objections = "objections"
objection_days = "objection_days"
req_notices = "req_notices"
sd_days = "sd_days"
service_contract = "service_contract"
broker_disclosure = "broker_disclosure"
closing_date = "closing_date"
special_prov1 = "special_prov1"
special_prov2 = "special_prov2"
special_prov3 = "special_prov3"
flat_commission_amount = 'flat_commission_amount'
percent_commission_amount = 'percent_commission_amount'
seller_max_contribution = "seller_max_contribution"
buy_address = "buy_address"
buy_email = "buy_email"

prop_add1 = "prop_add1"
prop_add2 = "prop_add2"
prop_add3 = "prop_add3"
prop_add4 = "prop_add4"
prop_add5 = "prop_add5"
prop_add6 = "prop_add6"
prop_add7 = "prop_add7"
prop_add8 = "prop_add8"
prop_add9 = "prop_add9"
prop_add10 = "prop_add10"
                
init_pg1 = "init_pg1"
init_pg2 = "init_pg2"
init_pg3 = "init_pg3"
init_pg4 = "init_pg4"
init_pg5 = "init_pg5"
init_pg6 = "init_pg6"
init_pg7 = "init_pg7"
init_pg8 = "init_pg8"

seller_pay_title_policy = "seller_pay_title_policy"
buyer_pay_title_policy = "buyer_pay_title_policy"
no_amend_or_del = "no_amend_or_del"
buyer_pay_survey = "buyer_pay_survey"
yes_hoa = "yes_hoa"
no_hoa = "no_hoa"
seller_disclosure = "seller_disclosure"
as_is = "as_is"
buyer_poss = "buyer_poss"
hoa_addendum = "hoa_addendum"
lbp_addendum = "lbp_addendum"
tpf_addendum = "tpf_addendum"
flat_commission = 'flat_commission'
percent_commission = 'percent_commission'

# Sellers Disclosure
sd_prop_1 = "sd_prop_1"
sd_prop_2 = "sd_prop_2"
sd_prop_3 = "sd_prop_3"
sd_prop_4 = "sd_prop_4"

# LBP
lbp_prop_1 = "lbp_prop_1"

# EM Deposit
rd_prop_1 = "rd_prop_1"
rd_buyer = "rd_buyer"
rd_buyer_phone = "rd_buyer_phone"
rd_buyer_address = "rd_buyer_address"
rd_earnest_money = "rd_earnest_money"

# Finance
tpa_prop_1 = "tpa_prop_1"
tpa_other_fin = "tpa_other_fin"
tpa_lender_name = "tpa_lender_name"
tpa_principal = "tpa_principal"
tpa_loan_yrs = "tpa_loan_yrs"
tpa_loan_interst = "tpa_loan_interst"
tpa_first_year_interest = "tpa_first_year_interest"
tpa_origination_charge = "tpa_origination_charge"
tpa_waive_rights_yes = "tpa_waive_rights_yes"
tpa_waive_rights_no = "tpa_waive_rights_no"
tpa_lender_approval_yes = "tpa_lender_approval_yes"
tpa_lender_approval_days = "tpa_lender_approval_days"


tpa_prop_2 = "tpe_prop_1"

# offer_defaults = {
#         # repair: None,
#         shared_statics.om: 50,
#         shared_statics.option_days: 15,
#         shared_statics.close_days: 21,

#         # Set the default values for these
#         shared_statics.escrow_agent: 'StarTex Title (Carrie Morrison)',
#         shared_statics.title_company_address: '1111 N Loop W Suite 1100, 77008',
#         shared_statics.title_company_name: 'StarTex Title (Carrie)',          
# }

### For Personalized TREC Offer
class TextFields:
    seller = 'Text_seller'
    buyer = 'Text_buyer'
    lot = 'Text_lot'
    block = 'Text_block'
    subdivision = 'Text_subdivision'
    city = 'Text_city'
    county = 'Text_county'
    address = 'Text_address'
    exclusions = 'Text_exclusion_1'
    cash_portion = 'Text_cash_portion'
    finance_portion = 'Text_financing_number'
    total_price = 'Text_total_price'
    escrow_agent = 'Text_escrow_agent'
    title_address = 'Text_title_address_1'
    title_address_2 = 'Text_title_address_2'
    em = 'Text_earnest_money'
    om = 'Text_option_fee'
    add_em = "Text_add_em"
    add_em_days = "Text_add_em_days"
    option_days = 'Text_option_period'
    title_company_name = 'Text_title_company_name'
    survey_days = 'Text_buyer_survey_days'
    objections = 'Text_objections_use'
    objection_days = 'Text_objection_days'
    req_notices = 'Text_req_notice_2'
    sd_days = 'Text_sd_days'
    service_contract = 'Text_service_contracts'
    broker_discolsure = 'Text_broker_disclosure_1'
    closing_date = 'Text_closing_month_day'
    closing_date_2 = 'Text_closing_year'
    special_prov1 = 'Text_special_pro_1'
    special_prov2 = 'Text_special_pro_2'
    special_prov3 = 'Text_special_pro_3'
    flat_commission_amount = 'Text_flat_commission_amount'
    percent_commission_amount = 'Text_percent_commission_amount'
    seller_max_contribution = 'Text_amount_to_buyer_expense'
    buy_email = 'Text_buyer_email_1'

    prop_add1 = 'Text_prop_1'
    prop_add2 = 'Text_prop_2'
    prop_add3 = 'Text_prop_3'
    prop_add4 = 'Text_prop_4'
    prop_add5 = 'Text_prop_5'
    prop_add6 = 'Text_prop_6'
    prop_add7 = 'Text_prop_7'
    prop_add8 = 'Text_prop_8'
    prop_add9 = 'Text_prop_9'
    prop_add10 = 'Text_prop_10'

    # Sellers Disclosure
    sd_prop_1 = "Text_sd_prop_1"
    sd_prop_2 = "Text_sd_prop_2"
    sd_prop_3 = "Text_sd_prop_3"
    sd_prop_4 = "Text_sd_prop_4"

    # LBP
    lbp_prop_1 = "Text_lbp_prop_1"

    # EM Deposit
    rd_prop_1 = "Text_rd_prop_1"
    rd_buyer = "Text_rd_buyer"
    rd_buyer_phone = "Text_rd_buyer_phone"
    rd_buyer_address = "Text_rd_buyer_address"
    rd_earnest_money = "Text_rd_earnest_money"

    # Finance
    tpa_prop_1 = "Text_tpf_address_1"
    tpa_lender_name = "Text_lender_name"
    tpa_principal = "Text_principal_amount"
    tpa_loan_yrs = "Text_loan_yrs"
    tpa_loan_interst = "Text_loan_interest"
    tpa_first_year_interest = "Text_first_year_interest"
    tpa_origination_charge = "Text_origination_charge"
    tpa_prop_2 = "Text_tpf_address_2"
    tpa_lender_approval_days = "Text_temination_days"
                        
    # init_pg1 = 'Text_23bwnc'
    # init_pg2 = 'Text_44wqce'
    # init_pg3 = 'Text_62nuxy'
    # init_pg4 = 'Text_74pbh'
    # init_pg5 = 'Text_89wohs'
    # init_pg6 = 'Text_100rgp'
    # init_pg7 = 'Text_105mxtl'
    # init_pg8 = 'Text_155feww'        

class CheckBoxes:
    third_party_finance = 'CheckBox_third_party'
    seller_pay_title_policy = 'CheckBox_seller_pays_title'
    buyer_pay_title_policy = 'CheckBox_buyer_pays_title'
    no_amend_or_del = 'CheckBox_title_not_amended'
    buyer_pay_survey = 'CheckBox_buyer_pays_survey'
    yes_hoa = 'CheckBox_hoa_yes'
    no_hoa = 'CheckBox_hoa_no'
    seller_disclosure = 'CheckBox_received_sd_no'
    as_is = 'CheckBox_as_is'
    buyer_poss = 'CheckBox_vacant_closing'

    flat_commission = 'CheckBox_flat_commission'
    percent_commission = 'CheckBox_percent_commission'

    hoa_addendum = 'CheckBox_hoa_adden'
    lbp_addendum = 'CheckBox_lbp_adden'
    tpf_addendum = 'CheckBox-third-party-adden'

    # Finance Addendum
    tpa_other_fin = '6 Reverse Mortgage Financing A reverse mortgage loan also known as a Home Equity-1'
    tpa_waive_rights_yes = 'CheckBox_waive_rights_yes'
    tpa_waive_rights_no = 'CheckBox_waive_rights_no'
    tpa_lender_approval_yes = 'CheckBox_lender_approval_yes'


pdf_data_dict = {
    "Page 1": {
        "Har Access": True,
        seller: "",
        buyer: "Cornerstone Home Solutions, LLC",
        lot: "",
        block: "",
        subdivision: "",
        city: "",
        county: "",
        address: "",
        exclusions: "",
        cash_portion: "0",
        finance_portion: "0",
    },
    "Page 2": {
        escrow_agent: "StarTex Title (Carrie)",
        title_address: "1111 N Loop W Suite 1100, 77008",
        em: "500",
        om: "50",
        option_days: "10",
        buyer_pay_title_policy: True,
        title_company_name: "StarTex Title (Carrie Morrison)",
        no_amend_or_del: True,
    },
    "Page 3": {
        buyer_pay_survey: True,
        survey_days: "10",
        objections: "Single-Family",
        objection_days: "3",
        yes_hoa: False,
        # no_hoa: True,
    },
    "Page 4": {
        req_notices: "N/A",
        seller_disclosure: True,
        sd_days: "5",
    },
    "Page 5": {
        as_is: True,
        service_contract: "N/A",
        broker_disclosure: "Buyer is a licensed Sales Agent",
        closing_date: 21,
    },
    "Page 6": {
        buyer_poss: True,
        special_prov1: "",
        special_prov2: "Buyers agree to pay all standard closing costs, excluding taxes, liens, and brokerage fees.",
        special_prov3: "Option period to begin the day after the contract lockbox is placed on property and code given to the buyer.",
        # flat_commission: False,
        flat_commission_amount: '',
        # percent_commission: False,
        percent_commission_amount: '',
        seller_max_contribution: '',
    },
    "Page 8": {
        lbp_addendum: False,
        # hoa_addendum: False,
        buy_email: "charles@cornerstonehomesolutions.com",
    },
    "Finance":{
        # third_party_finance: False,
        # tpf_addendum: False,
        tpa_loan_interst: "10",
        tpa_waive_rights_yes: False,
        # tpa_waive_rights_no: False,
    },
    "Backside": {
        # EM Deposit
        rd_buyer_phone: "",
        rd_buyer_address: "",
    }
}



### For Lot Offers
class LotTextFields:
    seller = '1 PARTIES The parties to this contract are'
    buyer = 'and'
    lot = '2 PROPERTY Lot'
    block = 'Block'
    subdivision = 'Addition'
    city = 'City of'
    county = 'County of'
    address = 'Texas known as'
    cash_portion = 'undefined'
    finance_portion = "undefined_2"
    total_price = 'undefined_3'
    mineral_lease_days = "within the time required Seller may terminate this contract or exercise Sellers remedies under"

    escrow_agent = 'as earnest money to'
    title_address = 'undefined_4'
    em = 'earnest money of'
    om = 'undefined_5'
    add_em = 'agent at'
    add_em_days = '3 days'
    option_days = '4 days'
    title_company_name = 'title insurance Title Policy issued by'


    survey_days = 'at Buyers expense Buyer is deemed to receive the survey on the date of actual receipt or'
    objections = 'undefined_8'
    objection_days = 'Buyer must object the earlier of i the Closing Date or ii'

    req_notices = 'following specific repairs and treatments-1'

    service_contract = '7H Amount'
    broker_discolsure = 'Disclose'
    closing_date = 'A The closing of the sale will be on or before'
    special_prov1 = 'Text2-4'
    special_prov2 = 'Text2-3'
    other_exp = 'escrow fee and other expenses payable by Seller under this contract'
    buy_address = 'Buyer Address 1'
    buy_email = 'Buyer Email/Fax Number 1'

    prop_add1 = 'Contract Concerning'
    prop_add2 = 'Contract Concerning_2'
    prop_add3 = 'Contract Concerning_3'
    prop_add4 = 'Page 5 of 9'
    prop_add5 = 'Page 6 of 9'
    prop_add6 = 'Contract Concerning_4'
    prop_add7 = 'Contract Address 8'
    prop_add8 = 'Address of Property'
    prop_add9 = 'Address of Property_2'
                        
    init_pg1 = 'Buyer 1 Initial Page 1'
    init_pg2 = 'Buyer 1 Initial Page 2'
    init_pg3 = 'Buyer 1 Initial Page 3'
    init_pg4 = 'Buyer 1 Initial Page 4'
    init_pg5 = 'Buyer 1 Initial Page 5'
    init_pg6 = 'Buyer 1 Initial Page 6'
    init_pg7 = 'Buyer 1 Initial Page 7'
    init_pg8 = 'Buyer 1 Initial Page 8'        

class LotCheckBoxes: 
    # buyer_pay_title_policy = 'Buyer’s expense'
    no_mineral_rights = "Buyers expense an owners policy of"
    yes_mineral_rights = "Sellers"
    seller_not_given_mineral_lease = "ii will be amended to read shortages in area at the expense of"
    buyer_pay_title_policy = 'Seller'
    no_amend_or_del = 'i 1'
    buyer_pay_survey = '2 Within'
    yes_hoa_rect =  "DOES NOT WORK"
    no_hoa = 'is_2'
    seller_disclosure = '7B(2) Buyer has not received the Notice checkbox'
    no_ag_developement_district = 'is not 2'
    yes_ag_developement_district = 'is no. 1'

    as_is = '1 Buyer accepts the Property As Is'
    hoa_addendum = 'Addendum for Property Subject to'