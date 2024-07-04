import json
import requests
import datetime  # Change this line
import pandas as pd
from bot.api.solana_price import solana_usd_price
#from raydium_tx import *
from bot.credentials.creds import *




def get_token_basic_info(url, headers,address):

    params = {
        'chain': 'solana',
        'address': address
    }

    response = requests.get(url + f'/token/solana/{address}/info', headers=headers, params=params, verify=False)

    # Parse the response as JSON
    response_json = json.loads(response.text)

    print(json.dumps(response_json, indent=4, sort_keys=True))

    return response_json


#get_token_basic_info(url,headers,address='947tEoG318GUmyjVYhraNRvWpMX7fpBTDQFBoJvSkSG3')
#latest coins created
def get_pairs_data(url, headers):
    # Set 'from' to the start of the day in ISO format
    from_time = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

    # Set 'to' to the current time in ISO format
    to_time = datetime.datetime.now().isoformat()

    params = {
        'sort': 'creationTime',
        'order': 0,
        'from': from_time,
        'to': to_time,
        'pageSize': 50
    }
    response = requests.get(url + f'/pool/solana', headers=headers, params=params, verify=False)


    # Parse the response as JSON
    response_json = json.loads(response.text)

    print(json.dumps(response_json, indent=4, sort_keys=True))

    return response_json

#get the token basic information from the json into a df
def extract_pairs_main_tokens(data):
    main_tokens_list = []

    for result in data["data"]["results"]:
        main_token_info = {
            "address": result["mainToken"]["address"],
            "name": result["mainToken"]["name"],
            "symbol": result["mainToken"]["symbol"]
        }
        #check if address is from a new token
        main_tokens_list.append(main_token_info)

    df = pd.DataFrame(main_tokens_list)
    return df



def check_security_audit_token(url,headers,address):

    params = {
        'chain': 'solana',
        'address': address
    }

    response = requests.get(url + f'/token/solana/{address}/audit', headers=headers, params=params, verify=True)

    # Parse the response as JSON
    response_json = json.loads(response.text)

    print(json.dumps(response_json, indent=4, sort_keys=True))

    return response_json



def check_security_audit_json(data_json):
    data = data_json.get("data")

    if data is not None:
        is_open_source = data.get("isOpenSource", "")
        is_honeypot = data.get("isHoneypot", "")
        is_mintable = data.get("isMintable", "")
        is_proxy = data.get("isProxy", "")
        slippage_modifiable = data.get("slippageModifiable", "")
        is_blacklisted = data.get("isBlacklisted", "")
        sell_tax = data.get("sellTax", {})
        buy_tax = data.get("buyTax", {})
        is_contract_renounced = data.get("isContractRenounced", "")
        is_potentially_scam = data.get("isPotentiallyScam", "")

        #ok
        if is_open_source in ["yes", ""] and \
                is_honeypot in ["no", ""] and \
                is_mintable in ["no", ""] and \
                is_proxy in ["unknown", ""] and \
                slippage_modifiable in ["no", ""] and \
                is_blacklisted in ["unknown", ""] and \
                sell_tax.get("min") is None and \
                sell_tax.get("max") is None and \
                buy_tax.get("min") is None and \
                buy_tax.get("max") is None and \
                is_contract_renounced == "yes" and \
                is_potentially_scam == "no":
            return 'Pass'
        #not ok
        elif is_honeypot in ["yes", ""] or \
                is_mintable in ["yes", ""] or \
                slippage_modifiable in ["yes", ""] or \
                sell_tax.get("min") is not None or \
                sell_tax.get("max") is not None or \
                buy_tax.get("min") is not None or \
                buy_tax.get("max") is not None or \
                is_potentially_scam == "yes":
            return 'Invalid'
        else:
            return 'Valid'
    else:
        return 'Missing'


def check_pools_token(url, headers, address):
    # Set 'from' to the start of the day in ISO format
    from_time = '2023-05-05T00:00:00'

    # Set 'to' to the current time in ISO format
    to_time = datetime.datetime.now().isoformat()

    params = {
        'chain': 'solana',
        'address': address,
        'sort': 'creationTime',
        'order': 0,
        'from': from_time,
        'to': to_time
    }


    response = requests.get(url + f'/token/solana/{address}/pools', headers=headers, params=params)

    # Parse the response as JSON
    response_json = json.loads(response.text)

    print(json.dumps(response_json, indent=4, sort_keys=True))

    return response_json


def check_pools_json(data_json):

    results = data_json.get('data', {}).get('results', [])

    for result in results:
        side_token = result.get('sideToken', {})
        if side_token.get('address') == 'So11111111111111111111111111111111111111112' \
                and side_token.get('name') == 'Wrapped SOL' and side_token.get('symbol') == 'SOL':
            return [result.get('address')]
    return ['not_available']

def check_pool_locks(url,headers, address):

    params = {
        'chain': 'solana',
        'address': address,

    }

    response = requests.get(url + f'/pool/solana/{address}/locks', headers=headers, params=params)

    # Parse the response as JSON
    response_json = json.loads(response.text)

    print(json.dumps(response_json, indent=4, sort_keys=True))

    return response_json
def get_sol_amount(amount):

    sol_price_usd = solana_usd_price()

    token_amount =(amount * 1) / sol_price_usd

    #amount in USD
    return token_amount

