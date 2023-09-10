import requests

def get_data(url, token):
    payload={}
    headers = {
      'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text
