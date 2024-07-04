import requests
import json
from datetime import datetime, timezone

def get_latest_pairs(url,headers):

    params = {
        'sort': 'name',  # Set the sort parameter to 'name'
        'order': 'asc'   # Set the order parameter to 'asc' or 'desc' as needed
    }

    response = requests.get(url + 'v2/blockchain',headers=headers,params=params)

    print(response.text)




def get_pool(url, headers, chain):
    # Get the current timestamp with timezone information
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    # Calculate the timestamp for the start of today with timezone information
    start_of_today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    params = {
        'sort': 'creationTime',  # Set the sort parameter to 'creationTime'
        'order': '0',  # Set the order parameter to '0'
        'from': start_of_today,
        'to': now
    }

    response = requests.get(url + f'v2/pool/{chain}', headers=headers, params=params)
    formatted_response = json.dumps(response.json(), indent=2)
    print(formatted_response)

def get_token(url, headers, chain):
    # Get the current timestamp with timezone information
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    # Calculate the timestamp for the start of today with timezone information
    start_of_today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    params = {
        'sort': 'creationTime',  # Set the sort parameter to 'creationTime'
        'order': '0',  # Set the order parameter to '0'
        'from': start_of_today,
        'to': now
    }

    response = requests.get(url + f'v2/token/{chain}', headers=headers, params=params)
    formatted_response = json.dumps(response.json(), indent=2)
    print(formatted_response)

#get_pool(url,headers,'solana')
#get_latest_pairs(url,headers=headers)
#get_token(url,headers,'solana')

