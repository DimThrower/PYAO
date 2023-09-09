from datetime import datetime
from AutoOffer import settings
import requests, json
from get import get_data
from get_time import get_time

def deal_taken_check(pipeline_id, deal_query, days_back=45, token=settings.GHL_HOU_API_KEY):
    # set time for when deals are still viable
    time_cutoff = get_time(days_back=days_back)

    url = f"https://rest.gohighlevel.com/v1/pipelines/{pipeline_id}/opportunities?query={deal_query}"
    json_response = get_data(url=url, token=token)

    if json_response:
        # Parse the JSON response
        response_data = json.loads(json_response)   
        #print(response_data)

        opportunities = response_data.get("opportunities", [])

        # Filter opportunities
        filtered_opportunities = [opp for opp in opportunities if datetime.strptime(opp['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ') > time_cutoff]

        if filtered_opportunities:
            if len(filtered_opportunities) == 0:
                return "No"
            else:
                print(filtered_opportunities)
                return "Yes"

    return "No"