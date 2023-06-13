from selenium.webdriver.common.by import By

class Buttons:
    def __init__(self):
        self.save = '#download'
        self.previous = '#previous'
        self.next = '#next'
        self.scale_dpdwn = '#scaleSelect'
        self.fitpage = '#pageFitOption'

class TextFields:
    def __init__(self):
        self.seller = '#pdfjs_internal_id_663R'
        self.buyer = '#pdfjs_internal_id_664R'
        self.lot = '#pdfjs_internal_id_665R'
        self.block = '#pdfjs_internal_id_666R'
        self.subdivision = '#pdfjs_internal_id_667R'
        self.city = '#pdfjs_internal_id_668R'
        self.county = '#pdfjs_internal_id_669R'
        self.address = '#pdfjs_internal_id_670R'
        self.exclusions = '#pdfjs_internal_id_671R'
        self.cash_portion = '#pdfjs_internal_id_673R'
        self.finance_portion = '#pdfjs_internal_id_678R'
        self.total_price = '#pdfjs_internal_id_679R'
        self.escrow_agent = '#pdfjs_internal_id_260R'
        self.title_address = '#pdfjs_internal_id_264R'
        self.em = '#pdfjs_internal_id_266R'
        self.om = '#pdfjs_internal_id_268R'
        self.add_em = '#pdfjs_internal_id_269R'
        self.add_em_days = '#pdfjs_internal_id_261R'
        self.option_days = '#pdfjs_internal_id_262R'
        self.title_company_name = '#pdfjs_internal_id_259R'
        self.survey_days = '#pdfjs_internal_id_287R'
        self.objections = '#pdfjs_internal_id_290R'
        self.objection_days = '#pdfjs_internal_id_292R'
        self.req_notices = '#pdfjs_internal_id_300R'
        self.sd_days = '#pdfjs_internal_id_307R'
        self.service_contract = '#pdfjs_internal_id_321R'
        self.broker_discolsure = '#pdfjs_internal_id_317R'
        self.closing_date = '#pdfjs_internal_id_331R'
        self.special_prov1 = '#pdfjs_internal_id_341R'
        self.special_prov2 = '#pdfjs_internal_id_344R'
        self.special_prov3 = '#pdfjs_internal_id_338R'
        self.other_exp = '#pdfjs_internal_id_346R'
        self.buy_address = '#pdfjs_internal_id_357R'
        self.buy_email = '#pdfjs_internal_id_371R'

        self.prop_add1 = '#pdfjs_internal_id_258R'
        self.prop_add2 = '#pdfjs_internal_id_281R'
        self.prop_add3 = '#pdfjs_internal_id_299R'
        self.prop_add4 = '#pdfjs_internal_id_324R'
        self.prop_add5 = '#pdfjs_internal_id_335R'
        self.prop_add6 = '#pdfjs_internal_id_352R'
        self.prop_add7 = '#pdfjs_internal_id_356R'
        self.prop_add8 = '#pdfjs_internal_id_422R'
        self.prop_add9 = '#pdfjs_internal_id_457R'
        self.prop_add10 = '#pdfjs_internal_id_487R'
                          
        self.init_pg1 = '#pdfjs_internal_id_686R'
        self.init_pg2 = '#pdfjs_internal_id_275R'
        self.init_pg3 = '#pdfjs_internal_id_297R'
        self.init_pg4 = '#pdfjs_internal_id_306R'
        self.init_pg5 = '#pdfjs_internal_id_328R'
        self.init_pg6 = '#pdfjs_internal_id_339R'
        self.init_pg7 = '#pdfjs_internal_id_353R'
        self.init_pg8 = '#pdfjs_internal_id_406R'        

class CheckBoxes:
    def __init__(self):
        self.buyer_pay_title_policy = '#pdfjs_internal_id_270R'
        self.no_amend_or_del = '#pdfjs_internal_id_263R'
        self.buyer_pay_survey = '#pdfjs_internal_id_282R'
        self.yes_hoa = '#pdfjs_internal_id_291R'
        self.no_hoa = '#pdfjs_internal_id_296R'
        self.seller_disclosure = '#pdfjs_internal_id_304R'
        self.as_is = '#pdfjs_internal_id_318R'
        self.buyer_poss = '#pdfjs_internal_id_343R'
        self.hoa_addendum = '#pdfjs_internal_id_367R'
        self.lbp_addendum = '#pdfjs_internal_id_384R'

text_field = TextFields()
check_box = CheckBoxes()
btns = Buttons()

class Elements:
    def __init__(self, browser):
        
        self.seller = browser.find_element(By.CSS_SELECTOR, text_field.seller)
        self.buyer = browser.find_element(By.CSS_SELECTOR, text_field.buyer)
        self.lot = browser.find_element(By.CSS_SELECTOR, text_field.lot)
        self.block = browser.find_element(By.CSS_SELECTOR, text_field.block)
        self.subdivision = browser.find_element(By.CSS_SELECTOR, text_field.subdivision)
        self.city = browser.find_element(By.CSS_SELECTOR, text_field.city)
        self.county = browser.find_element(By.CSS_SELECTOR, text_field.county)
        self.address = browser.find_element(By.CSS_SELECTOR, text_field.address)
        self.exclusions = browser.find_element(By.CSS_SELECTOR, text_field.exclusions)
        self.cash_portion = browser.find_element(By.CSS_SELECTOR, text_field.cash_portion)
        self.finance_portion = browser.find_element(By.CSS_SELECTOR, text_field.finance_portion)
        self.total_price = browser.find_element(By.CSS_SELECTOR, text_field.total_price)
        self.escrow_agent = browser.find_element(By.CSS_SELECTOR, text_field.escrow_agent)
        self.title_address = browser.find_element(By.CSS_SELECTOR, text_field.title_address)
        self.em = browser.find_element(By.CSS_SELECTOR, text_field.em)
        self.om = browser.find_element(By.CSS_SELECTOR, text_field.om)
        self.add_em = browser.find_element(By.CSS_SELECTOR, text_field.add_em)
        self.add_em_days = browser.find_element(By.CSS_SELECTOR, text_field.add_em_days)
        self.op = browser.find_element(By.CSS_SELECTOR, text_field.op)
        self.title_name = browser.find_element(By.CSS_SELECTOR, text_field.title_name)
        self.survey_days = browser.find_element(By.CSS_SELECTOR, text_field.survey_days)
        self.objections = browser.find_element(By.CSS_SELECTOR, text_field.objections)
        self.objection_days = browser.find_element(By.CSS_SELECTOR, text_field.objection_days)
        self.req_notices = browser.find_element(By.CSS_SELECTOR, text_field.req_notices)
        self.sd_days = browser.find_element(By.CSS_SELECTOR, text_field.sd_days)
        self.service_contract = browser.find_element(By.CSS_SELECTOR, text_field.service_contract)
        self.broker_discolsure = browser.find_element(By.CSS_SELECTOR, text_field.broker_discolsure)
        self.closing_date = browser.find_element(By.CSS_SELECTOR, text_field.closing_date)
        self.special_prov1 = browser.find_element(By.CSS_SELECTOR, text_field.special_prov1)
        self.special_prov2 = browser.find_element(By.CSS_SELECTOR, text_field.special_prov2)
        self.special_prov3 = browser.find_element(By.CSS_SELECTOR, text_field.special_prov3)
        self.other_exp = browser.find_element(By.CSS_SELECTOR, text_field.other_exp)
        self.buy_address = browser.find_element(By.CSS_SELECTOR, text_field.buy_address)
        self.buy_email = browser.find_element(By.CSS_SELECTOR, text_field.buy_email)

        self.prop_add1 = browser.find_element(By.CSS_SELECTOR, text_field.prop_add1)
        self.prop_add2 = browser.find_element(By.CSS_SELECTOR, text_field.prop_add2)
        self.prop_add3 = browser.find_element(By.CSS_SELECTOR, text_field.prop_add3)
        self.prop_add4 = browser.find_element(By.CSS_SELECTOR, text_field.prop_add4)
        self.prop_add5 = browser.find_element(By.CSS_SELECTOR, text_field.prop_add5)
        self.prop_add6 = browser.find_element(By.CSS_SELECTOR, text_field.prop_add6)
        self.prop_add7 = browser.find_element(By.CSS_SELECTOR, text_field.prop_add7)
        self.prop_add8 = browser.find_element(By.CSS_SELECTOR, text_field.prop_add8)
        self.prop_add9 = browser.find_element(By.CSS_SELECTOR, text_field.prop_add9)

        self.init_pg1 = browser.find_element(By.CSS_SELECTOR, text_field.init_pg1)
        self.init_pg2 = browser.find_element(By.CSS_SELECTOR, text_field.init_pg2)
        self.init_pg3 = browser.find_element(By.CSS_SELECTOR, text_field.init_pg3)
        self.init_pg4 = browser.find_element(By.CSS_SELECTOR, text_field.init_pg4)
        self.init_pg5 = browser.find_element(By.CSS_SELECTOR, text_field.init_pg5)
        self.init_pg6 = browser.find_element(By.CSS_SELECTOR, text_field.init_pg6)
        self.init_pg7 = browser.find_element(By.CSS_SELECTOR, text_field.init_pg7)
        self.init_pg8 = browser.find_element(By.CSS_SELECTOR, text_field.init_pg8)


        self.buyer_pay_title_policy = browser.find_element(By.CSS_SELECTOR, check_box.buyer_pay_title_policy)
        self.no_amend_or_del = browser.find_element(By.CSS_SELECTOR, check_box.no_amend_or_del)
        self.buyer_pay_survey = browser.find_element(By.CSS_SELECTOR, check_box.buyer_pay_survey)
        self.yes_hoa = browser.find_element(By.CSS_SELECTOR, check_box.yes_hoa)
        self.no_hoa = browser.find_element(By.CSS_SELECTOR, check_box.no_hoa)
        self.sd = browser.find_element(By.CSS_SELECTOR, check_box.sd)
        self.as_is = browser.find_element(By.CSS_SELECTOR, check_box.as_is)
        self.buyer_poss = browser.find_element(By.CSS_SELECTOR, check_box.buyer_poss)
        self.hoa_addendum = browser.find_element(By.CSS_SELECTOR, check_box.hoa_addendum)
        self.lbp_addendum = browser.find_element(By.CSS_SELECTOR, check_box.lbp_addendum)
        

