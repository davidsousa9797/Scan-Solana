import json
import requests
from bot.credentials.creds import *
import datetime  # Change this line


#latest coins created
def get_solana_price_json(url, headers):

    solana_adress = 'So11111111111111111111111111111111111111112'
    # Set 'from' to the start of the day in ISO format
    from_time = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

    # Set 'to' to the current time in ISO format
    to_time = datetime.datetime.now().isoformat()


    response = requests.get(url + f'/token/solana/{solana_adress}/price', headers=headers, verify=True)


    # Parse the response as JSON
    response_json = json.loads(response.text)

    #print(json.dumps(response_json, indent=4, sort_keys=True))

    return response_json

def solana_usd_price():

    data_json = get_solana_price_json(url, headers)
    data = data_json["data"]

    SOL_USD = data.get("price", "")

    return SOL_USD



solana_usd_price()