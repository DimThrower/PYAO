import token
from mapping import create_custom_fields_map, create_stage_map, create_users_map
from get import get_data
from AutoOffer import settings

def createCustomFieldDict(token,
    number_value=None, email_value=None, owner_value=None, source_value=None, 
    seller_value=None, county_value=None, subdivision_value=None, lot_value=None,
    block_value=None, legal_value=None, sqft_value=None, bedbath_value=None,
    yrbuilt_value=None, hoa_value=None, arv_value=None, rehab_value=None,
    fee_value=None, sale_price_value=None, asking_value=None, offer_value=None,
    close_value=None, em_value=None, om_value=None, option_days_value=None,
    title_policy_value=None, escrow_value=None, title_address_value=None,
    title_company_value=None, provisions_value=None, lbp_value=None, trec_value=None, 
    location="HOU",):

    cf = build_custom_fields_class(token=token)

    if location == "HOU":
        custom_fields_dict = [
            {"id":cf.contact_contact_phone_number, "value":number_value},
            {"id":cf.contact_contact_email, "value":email_value},
            {"id":cf.contact_which_agent_is_managing_this_deal, "value":owner_value},
            {"id":cf.contact_lead_source, "value":source_value},
            {"id":cf.contact_owner_name, "value":seller_value},
            {"id":cf.contact_property_county, "value":county_value},
            {"id":cf.contact_subdivisionabstthe_rest_of_legal_description, "value":subdivision_value},
            {"id":cf.contact_lotlt, "value":lot_value},
            {"id":cf.contact_blockblk, "value":block_value},
            {"id":cf.contact_address_legal_description, "value":legal_value},
            {"id":cf.contact_square_footage, "value":sqft_value},
            {"id":cf.contact_bedbath, "value":bedbath_value},
            {"id":cf.contact_year_build, "value":yrbuilt_value},
            {"id":cf.contact_property_in_hoa, "value":hoa_value},
            {"id":cf.contact_after_repair_value_arv, "value":arv_value},
            {"id":cf.contact_after_repair_value_arv, "value":rehab_value},
            {"id":cf.contact_deal_fee, "value":fee_value},
            {"id":cf.contact_potential_investor_sales_price, "value":sale_price_value},
            {"id":cf.contact_sellers_asking_price, "value":asking_value},
            {"id":cf.contact_offer_amount, "value":offer_value},
            {"id":cf.contact_expected_close_date, "value":close_value},
            {"id":cf.contact_earnest_money, "value":em_value},
            {"id":cf.contact_option_fee, "value":om_value},
            {"id":cf.contact_contract_option_days, "value":option_days_value},
            {"id":cf.contact_seller_paying_for_title_policy, "value":[title_policy_value]},
            {"id":cf.contact_escrow_agent, "value":escrow_value},
            {"id":cf.contact_title_company_address_1, "value":title_address_value},
            {"id":cf.contact_title_company, "value":title_company_value},
            {"id":cf.contact_trec_special_provisionsamendment, "value":provisions_value},
            {"id":cf.contact_house_built_before_1978, "value":[lbp_value]},
            {"id":cf.contact_which_contract_would_you_like_to_send_out, "value":trec_value}
       ]
    else:
         custom_fields_dict = [
            {"id":cf.contact_contact_phone_number, "value":number_value},
            {"id":cf.contact_contact_email, "value":email_value},
            {"id":cf.contact_which_agent_is_managing_this_deal, "value":owner_value},
            {"id":cf.contact_lead_source, "value":source_value},
            {"id":cf.contact_owner_name, "value":seller_value},
            {"id":cf.contact_property_county, "value":county_value},
            {"id":cf.contact_subdivisionabstthe_rest_of_legal_description, "value":subdivision_value},
            {"id":cf.contact_lotlt, "value":lot_value},
            {"id":cf.contact_blockblk, "value":block_value},
            {"id":cf.contact_address_legal_description, "value":legal_value},
            {"id":cf.contact_square_footage, "value":sqft_value},
            {"id":cf.contact_bedbath, "value":bedbath_value},
            {"id":cf.contact_year_build, "value":yrbuilt_value},
            {"id":cf.contact_property_in_hoa, "value":hoa_value},
            {"id":cf.contact_after_repair_value_arv, "value":arv_value},
            {"id":cf.contact_after_repair_value_arv, "value":rehab_value},
            {"id":cf.contact_deal_fee, "value":fee_value},
            {"id":cf.contact_potential_investor_sales_price, "value":sale_price_value},
            {"id":cf.contact_sellers_asking_price, "value":asking_value},
            {"id":cf.contact_offer_amount, "value":offer_value},
            {"id":cf.contact_expected_close_date, "value":close_value},
            {"id":cf.contact_earnest_money, "value":em_value},
            {"id":cf.contact_option_fee, "value":om_value},
            {"id":cf.contact_contract_option_days, "value":option_days_value},
            {"id":cf.contact_seller_paying_for_title_policy, "value":[title_policy_value]},
            {"id":cf.contact_escrow_agent, "value":escrow_value},
            {"id":cf.contact_title_company_address_1, "value":title_address_value},
            {"id":cf.contact_title_company, "value":title_company_value},
            {"id":cf.contact_trec_special_provisionsamendment, "value":provisions_value},
            {"id":cf.contact_house_built_before_1978, "value":[lbp_value]},
            {"id":cf.contact_which_contract_would_you_like_to_send_out, "value":trec_value}
       ]

    return custom_fields_dict

def build_custom_fields_class(token):
    class CustomFields:
        pass

    custom_fields_map = create_custom_fields_map(token=token)

    cf = CustomFields()

    # Iterate oves the attributes ant set them to the new values
    for custom_field_key, custom_field_value in custom_fields_map.items():
        setattr(cf, custom_field_key, custom_field_value)
            
    #print(cf.contact_deal_fee)

    return(cf)

def build_stage_class(token):
    class Stages:
        pass

    # Get the pipeline and stage mapping
    pipeline_id, stage_map = create_stage_map(token=token)

    stages = Stages()

    # Iterate over the attributes and set them to the new values
    for stage_key, stage_value in stage_map.items():
        setattr(stages, stage_key, stage_value)    
    print(stages.Closed)

    return [pipeline_id, stages]

def build_users_class(token):
    class Users:
        pass

    users_map = create_users_map(token=token)
    #print(users_map)

    users = Users()

    for user_name, user_id in users_map.items():
        setattr(users, user_name, user_id)

    print(users.CharlesWatkins)
    return users
