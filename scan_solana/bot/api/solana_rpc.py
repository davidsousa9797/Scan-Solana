import requests
from bot.credentials.creds import headers_alchemy as headers
import pandas as pd
import json

url = "https://solana-mainnet.g.alchemy.com/v2/alcht_osJ3bVr8Pp8UQtryOadQ11Pje6FlBL"

def get_block(block_number):

    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "getBlock",
        "params": [
            257210959,
            {
                "encoding": "jsonParsed",
                "transactionDetails": "full",
                "rewards": True,
                "commitment": "finalized",
                "maxSupportedTransactionVersion": 0
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)

    json_response = response.json()
    pretty_response = json.dumps(json_response, indent=4)
    #data = json.loads(response)

    # Convert the list of dictionaries to a DataFrame
    #df = pd.DataFrame(response)
    #print(response.text)
    #x =4

#TODO - Need to find a way to retrive the first transactions (signatures) of the Token
def get_signatures_for_token():

    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "getSignaturesForAddress",
        "params": ["A5nvoNHLmJ4ydL5KroxphCX4umFwcn8VWb4kXm7L6sXn"]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)


    json_response = response.json()
    pretty_response = json.dumps(json_response, indent=4)

    return pretty_response

#TODO - for each signature get the transaction details and check if the swap was more than 60% of the supply
def get_transaction_details():

    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "getTransaction",
        "params": [
            "hLY4HFCFWH6QoyJdYnFDZX8hNnWPBz29nvTtcq3LnezHtYWnckkciSgy7kmotE4mSeU4jwZrp9LppcdQ234FUuF",
            {
                "encoding": "jsonParsed",
                "commitment": "finalized",
                "maxSupportedTransactionVersion": 10
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    json_response = response.json()
    pretty_response = json.dumps(json_response, indent=4)

    return pretty_response


sign = get_signatures_for_token()
trx = get_transaction_details()

x = 4