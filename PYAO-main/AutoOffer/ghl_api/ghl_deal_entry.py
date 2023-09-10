from AutoOffer.ghl_api.fields import createCustomFieldDict#, build_stage_class, build_users_class
from AutoOffer.ghl_api.mapping import create_custom_fields_map, create_stage_map
from AutoOffer import settings
from AutoOffer.ghl_api.get import get_data
from AutoOffer.ghl_api.get_time import get_time
from AutoOffer.ghl_api.deal_lookup import deal_lookup
from AutoOffer.ghl_api.create import create_contact, create_opp, create_note

def enter_deal(
                #for contact
                first_name, last_name, contact_source, 
                street_address, city, state, 
                postal_code, location,

                #for opporutunity
                assigned_to, stage,
                monetary_value, source, pipeline_id,

                #for additional details
                number_value, email_value, owner_value,
                source_value, seller_value, county_value,
                subdivision_value, lot_value, block_value,
                legal_value, sqft_value, bedbath_value,
                yrbuilt_value, hoa_value, arv_value,
                rehab_value, fee_value, sale_price_value,
                asking_value, offer_value, close_value,
                em_value, om_value, option_days_value,
                title_policy_value, escrow_value, title_address_value,
                title_company_value, provisions_value, lbp_value,
                trec_value,

                users_map, stages_map,

                days_back, notes,

                token=settings.GHL_HOU_API_KEY,
               ):

    # Spit the address for query
    words = street_address.split()

    # Take the first two words (if they exist)
    deal_query = ' '.join(words[:2])


    # Check to see if the deal is taken
    deal_taken, opp = deal_lookup(pipeline_id=pipeline_id, deal_query=deal_query, days_back=days_back, token=token)
    print(f"Is the deal taken? {deal_taken}")

    if deal_taken == "No":
        fields = createCustomFieldDict(token=token, location=location,
                                        number_value = number_value,
                                        email_value = email_value,
                                        owner_value = owner_value,
                                        source_value = source_value,
                                        seller_value = seller_value,
                                        county_value = county_value,
                                        subdivision_value = subdivision_value,
                                        lot_value = lot_value,
                                        block_value = block_value,
                                        legal_value = legal_value,
                                        sqft_value = sqft_value,
                                        bedbath_value = bedbath_value,
                                        yrbuilt_value = yrbuilt_value,
                                        hoa_value = hoa_value,
                                        arv_value = arv_value,
                                        rehab_value = rehab_value,
                                        fee_value = fee_value,
                                        sale_price_value = sale_price_value,
                                        asking_value = asking_value,
                                        offer_value = offer_value,
                                        close_value = close_value,
                                        em_value = em_value,
                                        om_value = om_value,
                                        option_days_value = option_days_value,
                                        title_policy_value = title_policy_value,
                                        escrow_value = escrow_value,
                                        title_address_value = title_address_value,
                                        title_company_value = title_company_value,
                                        provisions_value = provisions_value,
                                        lbp_value = lbp_value,
                                        trec_value = trec_value,
            )

        #print(fields)

        contact_id = create_contact(first_name = first_name,
                                    last_name = last_name,
                                    contact_source = contact_source,
                                    street_address = street_address,
                                    city = city,
                                    state = state,
                                    postal_code = postal_code,
                                    custom_field=fields,
                                    token=token)


        if contact_id:
           # users = build_users_class(token=token)
            create_opp(title = f"{street_address}, {city}, {state} {postal_code}",
                       pipeline_id=pipeline_id,
                       contact_id=contact_id,
                        assigned_to = users_map.get(f"{assigned_to}"),
                        stage_id = stages_map.get(f"{stage}"),
                        monetary_value = monetary_value,
                        source = source,
                        token = token,
            )

            # Create notes
            create_note(contact_id=contact_id, notes=notes, token=token, user_id=users_map.get(f"{assigned_to}"))

    return deal_taken
    '''
        fields = createCustomFieldDict(token=token, location=location,
            number_value='9012308338', email_value='test@email.com', owner_value='Charles', source_value='AA Realtor Email', 
            seller_value='Joe Chris', county_value='Harris', subdivision_value='Shotgun', lot_value='5',
            block_value='2', legal_value='Lock and Key', sqft_value='5264', bedbath_value='3/4/5',
            yrbuilt_value='1346', hoa_value='Yes', arv_value='11111', rehab_value='44444',
            fee_value='10000', sale_price_value='245555', asking_value='77777', offer_value='525252',
            close_value='2023-09-19', em_value='799', om_value='99', option_days_value='10',
            title_policy_value='No', escrow_value="Carrie Morrison", title_address_value="1111 N Loop W Suite 1100, 77008(Carrie)",
            title_company_value='StarTex Title (Carrie)', provisions_value='Closing Cost', lbp_value='Yes', trec_value="TREC 1-4"
            )
        
        #print(fields)

        contact_id = create_contact(first_name="Test", last_name="Working", contact_source="test source", 
                      street_address="123 Smith Street", city="Houston", state="TX", postal_code="77077",
                       custom_field=fields,token=token)

        if contact_id:
            users = build_users_class()
            create_opp(title= f"{street_address}, {city}, {state} {postal_code}", pipeline_id=pipeline_id,contact_id=contact_id, 
                       assigned_to=users.CharlesWatkins, stage_id=stages.NewLead, monetary_value=10000, source="Test-MLS/PYAO",
                       token=token,
            )
        '''

'''
location = "SA"
api_key = ghl_api(location)

users = create_users_map(token=api_key)
pipeline_id, stages = create_stage_map(token=api_key)

opp_update(
    token=api_key,
    street_address="123 Smith Sts",
    days_back=100,
    pipeline_id=pipeline_id,
    stage_id=stages.get('1stOfferMade/FollowUp')
)

enter_deal(
    # Contact Information
    first_name="Test",
    last_name="Working",
    contact_source="test source",
    street_address="123 Smith Street",
    city="Houston",
    state="TX",
    postal_code="77077",

    # Opportunity Details
    assigned_to="CharlesWatkins",
    stage="NewLead",
    monetary_value=10000,
    source="Test-MLS/PYAO",
    pipeline_id=pipeline_id,

    # Additional Details
    number_value='9012308338',
    email_value='test@email.com',
    owner_value='Charles',
    source_value='AA Realtor Email',
    seller_value='Joe Chris',
    county_value='Harris',
    subdivision_value='Shotgun',
    lot_value='5',
    block_value='2',
    legal_value='Lock and Key',
    sqft_value='5264',
    bedbath_value='3/4/5',
    yrbuilt_value='1346',
    hoa_value='Yes',
    arv_value='11111',
    rehab_value='44444',
    fee_value='10000',
    sale_price_value='245555',
    asking_value='77777',
    offer_value='525252',
    close_value='2023-09-19',
    em_value='799',
    om_value='99',
    option_days_value='10',
    title_policy_value='Yes',
    escrow_value="Carrie Morrison",
    title_address_value="1111 N Loop W Suite 1100, 77008(Carrie)",
    title_company_value='StarTex Title (Carrie)',
    provisions_value='Closing Cost',
    lbp_value='Yes',
    trec_value="TREC 1-4",

    # Other Parameters
    users_map=users,
    stages_map=stages,
    days_back=45,
    token=api_key,
    location=location,
)

'''
