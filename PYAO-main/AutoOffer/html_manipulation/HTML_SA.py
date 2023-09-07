class PropertyProfile():
    def __init__(self):
        self.location = "Location"
        self.steet_address = "Street_Address"
        self.city = "City"
        self.zip_Code = "Zip_Code"
        self.state = "State"
        self.county = "County"
        self.mls_id = "MLS_ID"
        self.list_price = "List_Price"
        self.dom = "DOM"
        self.agent_first_name = 'Agent_First_Name'
        self.agent_last_name = 'Agent_Last_Name'
        self.agent_email = 'Agent_Email'
        self.agent_cell = 'Agent_Cell'
        self.agent_phone = 'Agent_Phone'
        self.hoa = "HOA"
        self.owner_name = "Owner_Name"
        self.year_built = "Year_Built"
        self.bed = "Bed"
        self.bath = "Bath"
        self.half_bath = "Half_Bath"
        self.sqft = "SQFT"
        self.lot = "Lot"
        self.block = "Block"
        self.mud = "MUD"
        self.arv = "ARV"
        self.repair = "Repair"
        self.offer_price = "Offer_Price"
        self.em = "Earnest_Money"
        self.om = "Option_Money"
        self.option_days = "Option_Days"
        self.close_date = "Closing_Date"
        self.subdivision = "Subdivison"
        self.legal_description = "Legal_Description"
        self.lead_based_paint = "Lead_Based_Paint"
        self.escrow_agent = "Escrow_Agent"
        self.title_company_name = "Title_Company_Name"
        self.title_company_address = "Title_Company_Address"
        self.confidence_score = "Confidence_Score"
        self.forcast_sd = "Forcast_SD"
        self.confidence_score_tolerance_lvl = "CS_Tolerance_LVL"
        self.public_remarks = "Public_Remarks"
        # Default attributes set to none
        self.email_subject = "Email_Subject"
        self.email_body = "Email_Body"
        self.ai_cost = "AI_COST"
        self.offer_sent = "Offer_Sent"
        self.ghl_check = "GHL_Check"
        self.deal_taken = "Deal_Taken"
        self.pdf_offer_path = "Offer_Path"
        self.ghl_offer_made = 'GHL_Offer_Made'
        self.last_updated = "Last_Updated"
        # self.realtor_remarks = 'Realtor_Remarks'
        # self.offer_email = "Offer_Email"
    


# Initialize Property Profile instance
pp = PropertyProfile()

class HTML:
    def __init__(self):
        self.webaddress = {
            'har': 'https://matrix.harmls.com/Matrix/SavedSearches.aspx',
            'GHL': 'https://app.gohighlevel.com/',
        }

        self.innerHTML = {}
        self.innerHTML['saved search page'] = {}
        self.innerHTML['saved search page']['saved search name'] = 'PYAO SA'
        self.innerHTML['saved search page']['results'] = 'Results'

        self.innerHTML['listing_page'] = {
            pp.steet_address: 'Address: ',
            pp.city: 'City/Location: ',
            pp.zip_Code: 'Zip Code: ',
            pp.county: 'County: ',
            pp.mls_id: 'ML#: ', 
            pp.list_price: 'List Price: ',
            pp.dom: 'DOM: ', 
            pp.agent_first_name: 'List Agent: ',
            pp.agent_email: 'Agent Email: ',
            pp.agent_cell: 'Agent Cell: ',
            pp.agent_phone: 'Agent Phone:',
            pp.hoa: 'Mgmt Co./HOA Name: ',
            pp.public_remarks: 'Physical Property Description:',
        }

        self.innerHTML['tax_page'] = {
            pp.owner_name: "Owner Name",
            pp.year_built: "Year Built",
            pp.bed: 'Bedrooms',
            pp.bath: 'Full Baths',
            pp.half_bath: 'Half Baths',
            pp.sqft: "Building Sq Ft",
            pp.lot: "Lot #",
            pp.block: "Block #",
            pp.mud: "Water Tax Dist",
            pp.arv: "RealAVM:",
            pp.subdivision: 'Subdivision',
            pp.legal_description: 'Legal Description',
        }

        self.innerHTML['tax_page_cs'] = {
            pp.confidence_score: "Confidence Score:",
            pp.forcast_sd: "Forecast Standard Deviation:",
            pp.confidence_score_tolerance_lvl: 80,
        }
        self.innerHTML['GHL'] = {}

        self.innerHTML['GHL']['Main'] = {
            'Login Page': '#app',
            "Email": "#email",
            "Password": "#password",
            'Login btn': '#app > div:nth-child(1) > div.undefined.flex.v2-open.sidebar-v2-agency > section > div.hl_login--body > div > div > div > div:nth-child(4) > div:nth-child(2) > button',
            'Send Secruity btn': "#app > div:nth-child(1) > div.undefined.flex.v2-open.sidebar-v2-agency > section > div.hl_login--body > div > div > div > div > div.form-group.button-holder > div:nth-child(2) > button",
            'Opportunities': '#sb_opportunities',
            'Locations': '#location-switcher-sidbar-v2',
            'Locations Search': '#location-switcher-sidbar-v2 > div.hl_v2-location_switcher > div.flex.flex-row.items-center.my-3.mx-3.h-7.w-11\/12 > div > input',
            'Houston Location': '#location-list > div:nth-child(1) > div:nth-child(2) > div',
            'New Lead Header': '#data-stage-name-4aca558a-7147-441b-b3cc-f7d236805441',
            'Create Op Window': 'body > div.n-modal-container > div > div > div.n-scrollbar-container > div > div.n-card.n-modal.hl-modal > div.n-card__content',
            'Opportunities Search': "#data-search-opportunities > div.n-input-wrapper > div.n-input__input > input",
            'Card Class': 'borderColor mb-2 hl-card',
            'Card White Space Class':'flex items-center pt-2',
            'New Deal btn': '#data-create-opportunity',
            'Contact Name': '#OpportunityModalContactNameInput > div > div.n-base-selection-label > input',
            'Create Contact': 'body > div.n-modal-container > div > div > div.n-scrollbar-container > div > div.n-card.n-modal.hl-modal > div:nth-child(3) > div > div > div.n-base-select-menu__action',
            #'Create Contact': 'body > div:nth-child(8) > div > div > div.n-scrollbar-container > div > div.n-card.n-modal.hl-modal > div.v-binder-follower-container > div > div > div.n-base-select-menu__action > div',
            'Opportunity Name': "#OpportunityName > div.n-input-wrapper > div > input",
            'Lead Value': "#OpportunityLeadValue > div.n-input-wrapper > div.n-input__input > input",
            'Owner': "#OpportunityOwner > div > div.n-base-selection-label",
            'Owner drpdwn': "body > div.n-modal-container > div > div > div.n-scrollbar-container > div > div.n-card.n-modal.hl-modal > div:nth-child(4) > div > div > div > div > div > div",
            "Opportunity Source": "#OpportunitySource > div.n-input-wrapper > div > input",
            "Stage": "#OpportunityStage > div > div.n-base-selection-label",
            "Offer Made": "body > div.n-modal-container > div > div > div.n-scrollbar-container > div > div.n-card.n-modal.hl-modal > div.v-binder-follower-container > div > div > div > div.n-virtual-list.v-vl > div > div > div:nth-child(3)",
            "My Name": "Charles",
            "Create Button": '#CreateUpdateOpportunity',
            "Close Op Window": '#modal-header-modal-close-btn > span > svg',
            
        }

        self.innerHTML['GHL']['Details'] = {
            'My Name': 'Charles',
            'Lead Source': 'AA MLS Listing',
            'Title Company': ' Title Company Providing Policy ',
            "Class": ".form-group",
            'Contact': "#contact-details > div > div > div > div > div:nth-child(2) > div > span",
            'Contact Check Field': "#contact-details > div > div.hl_contact-details-left.p-0.relative > div > div.h-full.overflow-y-auto > div:nth-child(2) > div.pt-3",
            "General": "#contact-details > div > div > div > div > div:nth-child(3) > div > span",
            'General Check Field': "#contact-details > div > div.hl_contact-details-left.p-0.relative > div > div.h-full.overflow-y-auto > div:nth-child(3) > div.pt-3",
            "General Inputs": {' Street Address ': pp.steet_address, 
                               ' City ': pp.city, 
                               ' State ': pp.state, 
                               ' Postal Code ': pp.zip_Code,
                               },
            "Additional": "#contact-details > div > div > div > div > div:nth-child(4) > div > span",
            "Additional Check Field": "#contact-details > div > div.hl_contact-details-left.p-0.relative > div > div.h-full.overflow-y-auto > div:nth-child(4) > div.pt-3",
            "Additional Inputs": {' Contact Email ': pp.agent_email, 
                                    ' Property Owner Name ': pp.owner_name, 
                                    ' Contact Phone Number ': pp.agent_cell,
                                    ' Property County ': pp.county, 
                                    ' Subdivision/ABST/(The rest of legal description) ': pp.subdivision, 
                                    ' Lot(LT) ': pp.lot, 
                                    ' Block(BLK) ': pp.block, 
                                    ' Address Legal Description ': pp.legal_description, 
                                    ' Square Footage ': pp.sqft, 
                                    ' Year Build ': pp.year_built, 
                                    ' After Repair Value (ARV) ': pp.arv, 
                                    ' Estimated Rehab ': pp.repair, 
                                    ' Sellers Asking Price ': pp.list_price,
                                    ' Offer Amount ': pp.offer_price, 
                                    ' Earnest Money ': pp.em, 
                                    ' Option Fee ': pp.om, 
                                    ' Option Days ': pp.option_days,
                                    ' Which Agent is Managing This Deal? ': 'Manger',
                                    ' Lead Source ': 'Lead Source',
                                    ' Escrow Agent ': pp.escrow_agent,
                                    ' Title Company Address  ': pp.title_company_address,
                                    ' Bed/Bath ': pp.bed,
                                    ' Contact Phone Number ': pp.agent_cell,
                                    ' Property In HOA? ': pp.hoa,
                                    ' Buyer Paying For Title Policy ': "Title Policy",
                                    ' Which Contract Would You Like to Send Out? ': 'TREC',
                                    ' Title Company Providing Policy ': pp.title_company_name,
                                    }, 
             # Define Last Additional Check Field by a style to get the very botom                            
            "Last Additional Check Field": "#contact-details > div > div.hl_contact-details-left.p-0.relative > div > div.h-full.overflow-y-auto > div:nth-child(4) > div.pt-3 > div > div[style='height: 10px;']",
            "Scroll Window": "#contact-details > div > div.hl_contact-details-left.p-0.relative > div > div.h-full.overflow-y-auto",
            "Option Ends": "#contact\.option_end_on > div.vdp-datepicker.mt-1 > div:nth-child(1) > input", # This is used to better located the Title policy button
            "Title Policy": "div.mb-2:nth-child(26) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > label:nth-child(2)",
            "Yes HOA": "#contact\.property_in_hoa > div.contact\.property_in_hoa > div:nth-child(1) > label",
            "No HOA": "#contact\.property_in_hoa > div.contact\.property_in_hoa > div:nth-child(2) > label",
             "TREC": "#contact\.which_contract_would_you_like_to_send_out > div.contact\.which_contract_would_you_like_to_send_out > div:nth-child(1) > label",
            "Save btn": "#contact-details > div > div.hl_contact-details-left.p-0.relative > div > div.h-full.overflow-y-auto > div.form-footer.save.absolute.bottom-0.left-0.bg-white.flex.w-full.justify-between.border-t.p-2.z-\[999\] > div:nth-child(2) > div > button",

        }

        self.offer_details = {
            pp.repair: None,
            pp.offer_price: None,
            pp.close_date: None,
            pp.em: None,
            pp.om: 50,
            pp.option_days: 10,
            pp.offer_sent: None,

            # Set the default values for these
            pp.escrow_agent: 'Sally Schopp',
            pp.title_company_address: '2915 W. Bitters Rd. Ste 301, 78248',
            pp.title_company_name: 'Alamo Title (Sally)',                  
        }

        ##pendo-close-guide-f0df2a63

        ##__next > div > main

        self.selectors = {}
        self.selectors['har'] = {
            'user': '#username',
            'password': '#password',
            'login_btn': '#login_btn',
            'matrix': 'body > div.pageContent > div.pc_content.color_carbon > div:nth-child(2) > div.col-md-4.col-12.order-md-2.order-0 > div:nth-child(1) > a',
            'first_mls_link': '#wrapperTable > td:nth-child(8) > span',
            'listing_link': '#wrapperTable > div > div > div:nth-child(3) > div > span > div.mtx-containerNavTabs > ul > li:nth-child(1)',
            'tax_link': '#wrapperTable > tbody > tr > td > table > tbody > tr:nth-child(3) > td:nth-child(6) > span > a > img',
            'next_btn': '#m_lblPagingSummary > span > a:nth-child(2)',
            'current_num': '#m_lblPagingSummary > b:nth-child(2)',
            'final_num': '#m_lblPagingSummary > b:nth-child(3)',  
            'listing_dom_check': '#wrapperTable',
            'tax_dom_check': 'body > rlst-root > rlst-reports > mat-sidenav-container > mat-sidenav-content > div > main > rlst-property-details-report > rlst-base-report > article > div > rlst-property-details-body > section > img',
            'mls_id_html': '#wrapperTable > tbody > tr > td > span > table > tbody > tr:nth-child(5) > td.display.d48m10 > table > tbody > tr.d48m11 > td.d48m15 > table > tbody > tr:nth-child(3) > td.d48m27 > span',
        }

        self.credentials = {}
        self.credentials['har'] = {
            'user': 'josephdavis',
            'password': 'Rwhsorange12'
        }