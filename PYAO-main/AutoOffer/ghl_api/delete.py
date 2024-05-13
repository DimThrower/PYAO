import requests


def delete_data(url, token):
    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    # Check the response status code and return a result
    if response.status_code == 200:
        print(f'Success: Contact deleted in GHL')
    else:
        raise Exception(
            f"Error with contact deletion: {response.status_code}\n{response.text}")
