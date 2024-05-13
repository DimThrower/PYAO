from selenium.common.exceptions import NoSuchElementException


class URLs:
    har = 'https://matrix.harmls.com/Matrix/SavedSearches.aspx'

class InnerHTML:
    owner_name = "Owner Name"
    lot = "Lot #"
    block = "Block #"
    subdivision = 'Subdivision'
    legal_description = 'Legal Description'
    zip_code = "Tax Billing Zip"
    city = "Township"


    year_built = "Effective Year Built:"
    bed = 'Bedrooms:'
    bath = 'Full Baths:'
    half_bath = 'Half Baths:'
    sqft = "Building Sq Ft:"
    mud = "M.U.D. Information:"
    arv = "RealAVM:"

class Selectors:
    # Har Selectors
    user = '#username'
    password = '#password'
    login_btn = '#login_btn'
    matrix_btn = 'body > div.pageContent > div.pc_content.color_carbon > div:nth-child(2) > div.col-md-4.col-12.order-md-2.order-0 > div:nth-child(1) > a'
    first_mls_link = '#wrapperTable > td:nth-child(11) > span'
    listing_link = '#wrapperTable > div > div > div:nth-child(3) > div > span > div.mtx-containerNavTabs > ul > li:nth-child(1)'
    tax_link = '#wrapperTable > div > div > div:nth-child(3) > div > span > div.mtx-containerNavTabs > ul > li:nth-child(2)'
    next_btn = '#m_lblPagingSummary > span > a:nth-child(2)'
    current_num = '#m_lblPagingSummary > b:nth-child(2)'
    final_num = '#m_lblPagingSummary > b:nth-child(3)'
    listing_dom_check = '#wrapperTable'
    tax_dom_check = '#wrapperTable > div > div > div:nth-child(1) > div > div > div.d-borderWidthBottom--1.d-borderStyle--solid.d-bordercolor--systemDark.d-borderWidthRight--0.d-borderWidthTop--0.d-borderWidthLeft--0.d-marginTop--10.col-sm-8 > span'
    mls_id_html = '#wrapperTable > tbody > tr > td > span > table > tbody > tr:nth-child(5) > td.display.d48m10 > table > tbody > tr.d48m11 > td.d48m15 > table > tbody > tr:nth-child(3) > td.d48m27 > span'
    tax_drp_dwn = '#m_topNavList > li:nth-child(7) > ul'
    tax_dom_check = '#mat-expansion-panel-header-12 > span.mat-content.ng-tns-c92-41 > mat-panel-title'
    new_postpone_btn = '#NewsDetailPostpone'

    # Realist Selectors
    realist_btn = "#m_topNavList > li:nth-child(7) > ul > li:nth-child(1) > a"
    realist_address_input = "#cdk-accordion-child-0 > div > fieldset > div > div > div > div > div > input"
    realist_submit_btn = "body > rlst-root > rlst-dashboard > mat-sidenav-container > mat-sidenav > div > rlst-search-panel > div.card.h-100 > div > div > rlst-quick-search > form > div.search-controls > button.btn.btn-default.btn-dark.ml-5.search-btn.btn-lg"
    realist_address_header = "body > rlst-root > rlst-reports > rlst-subheader > header > div > div > h1"
    
from selenium.webdriver.common.by import By

class Buttons:
    save = '#download'
    previous = '#previous'
    next = '#next'
    scale_dpdwn = '#scaleSelect'
    fitpage = '#pageFitOption'

class TextFields:
    seller = 'Seller Name'
    buyer = 'Buyer Name'
    lot = 'Lot'
    block = 'Block'
    subdivision = 'Addition'
    city = 'City Name'
    county = 'County Name'
    address = 'Address/ZIP code'
    exclusions = 'Improvements and accessories to be retained by Seller and removed prior to delivery of posession'
    cash_portion = 'Amount 3(A)'
    finance_portion = 'Amount 3B'
    total_price = 'Amount 3C'
    escrow_agent = '5A Escrow Agent'
    title_address = '5A Escrow Agent Address'
    em = '5A Amount (Earnest Money)'
    om = '5A Amount (Option Fee)'
    add_em = '5A(1) Amount'
    add_em_days = '5A(1) Number of Days'
    option_days = '5B Number of Days'
    title_company_name = 'Name of Title Company'
    survey_days = 'Number of Days (6(C)2)'
    objections = '6D Prohibitions on use or activity'
    objection_days = 'Number of Days 6D(ii)'
    req_notices = '6E(11) Required Notices 1'
    sd_days = 'Number of Days'
    service_contract = '7H Amount'
    broker_discolsure = '8A Brokers and Sales Agent Disclosure'
    closing_date = 'Date Number 1'
    special_prov1 = '11 Special Provisions'
    special_prov2 = '11 Special Provisions Blank 1'
    special_prov3 = '11 Special Provisions Blank 2'
    other_exp = '12A(1)(b) Amount'
    buy_address = 'Buyer Address 1'
    buy_email = 'Buyer Email/Fax Number 1'

    prop_add1 = 'Address of Property Page 2'
    prop_add2 = 'Address of Property Page 3'
    prop_add3 = 'Address of Property Page 4'
    prop_add4 = 'Address of Property Page 5'
    prop_add5 = 'Address of Property Page 6'
    prop_add6 = 'Address of Property Page 7'
    prop_add7 = 'Address of Property Page 8'
    prop_add8 = 'Address of Property Page 9'
    prop_add9 = 'Address of Property Page 10'
    prop_add10 = 'Address of Property Page 11'
                        
    init_pg1 = 'Buyer 1 Initial Page 1'
    init_pg2 = 'Buyer 1 Initial Page 2'
    init_pg3 = 'Buyer 1 Initial Page 3'
    init_pg4 = 'Buyer 1 Initial Page 4'
    init_pg5 = 'Buyer 1 Initial Page 5'
    init_pg6 = 'Buyer 1 Initial Page 6'
    init_pg7 = 'Buyer 1 Initial Page 7'
    init_pg8 = 'Buyer 1 Initial Page 8'        

class CheckBoxes:
    # buyer_pay_title_policy = 'Buyer’s expense'
    buyer_pay_title_policy = 'Buyer?s expense'
    no_amend_or_del = 'Checkbox 6A(8)(i)'
    buyer_pay_survey = '6C(2) Checkbox'
    yes_hoa = 'Is checkbox'
    no_hoa = 'Is not checkbox'
    seller_disclosure = '7B(2) Buyer has not received the Notice checkbox'
    as_is = '7D(1) Buyer accepts Property As Is Checkbox'
    buyer_poss = '10A upon closing and funding'
    hoa_addendum = 'Addendum for Property Subject to Mandatory Membership in a Property Owners Association'
    lbp_addendum = 'Addendum for Seller\'s Disclosure of Information on Lead-based Paint and Lead-Based Paint Hazards as Required by Federal Law'

text_field = TextFields()
check_box = CheckBoxes()
btns = Buttons()

class TREC_el_pg_1:
    def __init__(self, browser):
        # PAGE 1
        self.seller = browser.find_element(By.NAME, text_field.seller)
        self.buyer = browser.find_element(By.NAME, text_field.buyer)
        self.lot = browser.find_element(By.NAME, text_field.lot)
        self.block = browser.find_element(By.NAME, text_field.block)
        self.subdivision = browser.find_element(By.NAME, text_field.subdivision)
        self.city = browser.find_element(By.NAME, text_field.city)
        self.county = browser.find_element(By.NAME, text_field.county)
        self.address = browser.find_element(By.NAME, text_field.address)
        self.exclusions = browser.find_element(By.NAME, text_field.exclusions)
        self.cash_portion = browser.find_element(By.NAME, text_field.cash_portion)
        self.finance_portion = browser.find_element(By.NAME, text_field.finance_portion)
        self.total_price = browser.find_element(By.NAME, text_field.total_price)
        self.init_pg1 = browser.find_element(By.NAME, text_field.init_pg1)

class TREC_el_pg_2:
    def __init__(self, browser):
        # PAGE 2
        self.prop_add1 = browser.find_element(By.NAME, text_field.prop_add1)
        self.escrow_agent = browser.find_element(By.NAME, text_field.escrow_agent)
        self.title_address = browser.find_element(By.NAME, text_field.title_address)
        self.em = browser.find_element(By.NAME, text_field.em)
        self.om = browser.find_element(By.NAME, text_field.om)
        self.add_em = browser.find_element(By.NAME, text_field.add_em)
        self.add_em_days = browser.find_element(By.NAME, text_field.add_em_days)
        self.option_days = browser.find_element(By.NAME, text_field.option_days)
        self.title_name = browser.find_element(By.NAME, text_field.title_company_name)
        try:
            self.buyer_pay_title_policy = browser.find_element(By.NAME, check_box.buyer_pay_title_policy)
        except NoSuchElementException:
            self.buyer_pay_title_policy = browser.find_element(By.NAME, check_box.buyer_pay_title_policy_1)
        self.no_amend_or_del = browser.find_element(By.NAME, check_box.no_amend_or_del)
        self.init_pg2 = browser.find_element(By.NAME, text_field.init_pg2)

class TREC_el_pg_3:
    def __init__(self, browser):
        #PAGE 3
        self.prop_add2 = browser.find_element(By.NAME, text_field.prop_add2)
        self.buyer_pay_survey = browser.find_element(By.NAME, check_box.buyer_pay_survey)
        self.survey_days = browser.find_element(By.NAME, text_field.survey_days)
        self.objections = browser.find_element(By.NAME, text_field.objections)
        self.objection_days = browser.find_element(By.NAME, text_field.objection_days)
        self.yes_hoa = browser.find_element(By.NAME, check_box.yes_hoa)
        self.no_hoa = browser.find_element(By.NAME, check_box.no_hoa)
        self.init_pg3 = browser.find_element(By.NAME, text_field.init_pg3)

class TREC_el_pg_4:
    def __init__(self, browser):
        #PAGE 4
        self.prop_add3 = browser.find_element(By.NAME, text_field.prop_add3)
        self.req_notices = browser.find_element(By.NAME, text_field.req_notices)
        self.seller_disclosure = browser.find_element(By.NAME, check_box.seller_disclosure)
        self.sd_days = browser.find_element(By.NAME, text_field.sd_days)
        self.init_pg4 = browser.find_element(By.NAME, text_field.init_pg4)

class TREC_el_pg_5:
    def __init__(self, browser):
        #PAGE 5
        self.prop_add4 = browser.find_element(By.NAME, text_field.prop_add4)
        self.as_is = browser.find_element(By.NAME, check_box.as_is)
        self.service_contract = browser.find_element(By.NAME, text_field.service_contract)
        self.broker_discolsure = browser.find_element(By.NAME, text_field.broker_discolsure)
        self.closing_date = browser.find_element(By.NAME, text_field.closing_date)
        self.init_pg5 = browser.find_element(By.NAME, text_field.init_pg5)

class TREC_el_pg_6:
    def __init__(self, browser):
        #PAGE 6
        self.prop_add5 = browser.find_element(By.NAME, text_field.prop_add5)
        self.buyer_poss = browser.find_element(By.NAME, check_box.buyer_poss)
        self.special_prov1 = browser.find_element(By.NAME, text_field.special_prov1)
        self.special_prov2 = browser.find_element(By.NAME, text_field.special_prov2)
        self.special_prov3 = browser.find_element(By.NAME, text_field.special_prov3)
        self.other_exp = browser.find_element(By.NAME, text_field.other_exp)
        self.init_pg6 = browser.find_element(By.NAME, text_field.init_pg6)

class TREC_el_pg_7:
    def __init__(self, browser):
        #PAGE 7
        self.prop_add6 = browser.find_element(By.NAME, text_field.prop_add6)
        self.init_pg7 = browser.find_element(By.NAME, text_field.init_pg7)

class TREC_el_pg_8:
    def __init__(self, browser):
        #PAGE 8
        self.prop_add7 = browser.find_element(By.NAME, text_field.prop_add7)
        self.buy_address = browser.find_element(By.NAME, text_field.buy_address)
        self.buy_email = browser.find_element(By.NAME, text_field.buy_email)
        self.init_pg8 = browser.find_element(By.NAME, text_field.init_pg8)
        self.hoa_addendum = browser.find_element(By.NAME, check_box.hoa_addendum)
        self.lbp_addendum = browser.find_element(By.NAME, check_box.lbp_addendum)

class TREC_el_pg_9:
    def __init__(self, browser):
        #PAGE 9
        self.prop_add8 = browser.find_element(By.NAME, text_field.prop_add8)

class TREC_el_pg_10:
    def __init__(self, browser):
        #PAGE 10
        self.prop_add9 = browser.find_element(By.NAME, text_field.prop_add9)

class TREC_el_pg_11:
    def __init__(self, browser):
        #PAGE 10
        self.prop_add10 = browser.find_element(By.NAME, text_field.prop_add10)
