import requests

def delete_data(url, token):
    payload={}
    headers = {
      'Authorization': f'Bearer {token}'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)
    return response.text

