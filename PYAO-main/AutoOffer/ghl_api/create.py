import requests, json, uuid
from AutoOffer import settings
from AutoOffer.ghl_api.delete import delete_data

def generate_email_guid():
    random_guid = str(uuid.uuid4())
    formatted_guid = f"{random_guid}@python.com"
    return formatted_guid

def create_contact(first_name, token,contact_source=None,
                   email=generate_email_guid(), phone=None, last_name=None,
                   street_address=None, city=None, state=None, 
                   country=None,postal_code=None, custom_field=None,  tags=None,  website=None,
                   date_of_birth=None, company_name=None, url="https://rest.gohighlevel.com/v1/contacts/"):

    # Create the payload as a dictionary
    payload = {
        "email": email,
        "phone": phone,
        "firstName": first_name,
        "lastName": last_name,
        "name": f"{first_name} {last_name}",
        "address1": street_address,
        "city": city,
        "state": state,
        "country": country,
        "postalCode": postal_code,
        "companyName": company_name,
        "website": website,
        "tags": tags,
        "source": contact_source,
        "customField": custom_field
    }

    # Define the headers with the API token
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Make the POST request with JSON payload
    response = requests.post(url, headers=headers, json=payload)

    # Parse the respnse JSON
    response_json = json.loads(response.text)

    #print(custom_field)

    # Check the response status code and return a result
    if response.status_code == 200:
        # Extract the contact ID
        contact_id = response_json.get("contact", {}).get("id", None)
       # print (response_json.get("contact", {}).get("customField", None))
        print(contact_id)
        return contact_id
    else:
        print(f"Error: {response.status_code}\n{response.text}")
        return f"Error: {response.status_code}\n{response.text}"

def create_opp(title, contact_id, assigned_to, monetary_value, pipeline_id, stage_id, source, token, location_id=None, status="open"):
    url = f"https://rest.gohighlevel.com/v1/pipelines/{pipeline_id}/opportunities/"

    payload = {
        "pipelineId": pipeline_id,
        "locationId": location_id,
        "title": title,
        "stageId": stage_id,
        "status":status,
        "contactId":contact_id,
        "monetaryValue": monetary_value,
        "assignedTo": assigned_to,
        "source": source,
    }
    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.post(url, json=payload, headers=headers)

    # Check the response status code and return a result
    if response.status_code == 200:
        print("Opportunity created")
        pass
       # print(response.json())
    else:
        # Delete Opp if contact was not properly saved
        delete_data(url=f"https://rest.gohighlevel.com/v1/contacts/{contact_id}", token=token)
        print(f'Opportunity creation error. Deleted Contact')

        print(f"Error: {response.status_code}\n{response.text}")
        return f"Error: {response.status_code}\n{response.text}"

def create_note(contact_id, notes, token, user_id):
    url = f"https://rest.gohighlevel.com/v1/contacts/{contact_id}/notes/"

    payload = {
        "body": notes,
        "userId":  user_id,
    }

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # Check the response status code and return a result
    if response.status_code == 200:
        print("Note created")
        pass
        #print(response.json())
    else:
        print(f"Error: {response.status_code}\n{response.text}")
        return f"Error: {response.status_code}\n{response.text}"

