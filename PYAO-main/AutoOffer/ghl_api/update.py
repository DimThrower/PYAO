from AutoOffer.ghl_api.deal_lookup import deal_lookup
import requests, json

def opp_update(token, street_address, days_back, stage_id, status="open", pipeline_id=None):

     # Spit the address for query
    words = street_address.split()

    # Take the first two words (if they exist)
    deal_query = ' '.join(words[:2])

    print([deal_query])

    deal_taken, opp = deal_lookup(pipeline_id=pipeline_id, deal_query=deal_query, days_back=days_back, token=token)
    print(opp)
    deal_id = opp[0].get("id")
    title = opp[0].get("name")

    # print(deal_id)

    import requests

    url = f"https://rest.gohighlevel.com/v1/pipelines/{pipeline_id}/opportunities/{deal_id}"

    payload_keys = ["pipelineId", "stageId", "status", "title"]
    payload_values = [pipeline_id, stage_id, status, title]

    payload = {payload_key: payload_value 
               for payload_key, payload_value 
               in zip(payload_keys, payload_values)
               if payload_value
               }

    #print(f" PAYLOAD {payload}")

    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.request("PUT", url, headers=headers, data=payload)


    # Check the response status code and return a result
    if response.status_code == 200:
        # Extract the contact ID
        print("Deal updated")
       # print(f"After Update {response.text}")
    else:
        print(f"Error: {response.status_code}\n{response.text}")
        return f"Error: {response.status_code}\n{response.text}"
    