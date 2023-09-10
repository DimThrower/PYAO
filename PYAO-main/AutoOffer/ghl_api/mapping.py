import json, re

from AutoOffer import settings
from AutoOffer.ghl_api.get import get_data

def create_stage_map(token):
    try:
        json_response = get_data(url="https://rest.gohighlevel.com/v1/pipelines/", token=token)
        #print(json_response)

        # Parse the JSON response
        response_data = json.loads(json_response)

        # Extract the contact ID
        pipeline_id = response_data.get("pipelines")[0].get("id")  
        #print(pipeline_id)

        # Extract the list of stages from the JSON data
        stages = response_data.get("pipelines", [])[0].get("stages", [])

        # Create a dictionary to store the stage name to stage ID mapping
        stage_map = {}

        # Iterate through the stages and create the mapping
        for stage in stages:
            stage_name = stage.get("name", "")
            formatted_stage_name = re.sub(r'\s+', '', stage_name)
            stage_id = stage.get("id", "")
            stage_map[formatted_stage_name] = stage_id

        return [pipeline_id, stage_map]

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def create_custom_fields_map(token):
    # Get the json for all the custom fields
    json_response = get_data(url="https://rest.gohighlevel.com/v1/custom-fields/", token=token)

    # Parse the JSON response
    response_data = json.loads(json_response)   
    #print(json_response)

    custom_fields_map = {}
    custom_fields = response_data.get("customFields", [])
    for field in custom_fields:
        field_key = field.get("fieldKey")
        formatted_field_key = re.sub(r'\.', '_', field_key)
        field_id = field.get("id")
        if formatted_field_key and field_id:
            custom_fields_map[formatted_field_key] = field_id

    #print(custom_fields_map)
    return custom_fields_map

def create_users_map(token):
    json_response = get_data(url="https://rest.gohighlevel.com/v1/users/", token=token)

    # Parse tne JSON response
    response_data = json.loads(json_response)

    users_map = {}
    users = response_data.get("users", [])
    for user in users:
        user_key = user.get("name")
        formatted_user_key = re.sub(r'\s+', '', user_key)
        user_id = user.get("id")
        if formatted_user_key and user_id:
            users_map[formatted_user_key] = user_id

    # print(users_map)
    return users_map

