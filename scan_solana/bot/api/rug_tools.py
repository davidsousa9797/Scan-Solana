import json
import requests
from bot.credentials.creds import *

def get_rug_token_report(address):
    headers = {
        'accept': 'application/json'
    }

    response = requests.get(url_rug + f'/tokens/{address}/report', headers=headers)

    response_json = json.loads(response.text)

    pretty_json = json.dumps(response_json, indent=4)

    return response_json


def rug_select_new_pairs_for_new_coins(address):
    headers = {
        'accept': 'application/json'
    }

    response = requests.get(url_rug + f'/tokens/{address}/report/summary', headers=headers)

    response_json = json.loads(response.text)

    pretty_json = json.dumps(response_json, indent=4)

    return pretty_json


def check_security_report_json(data_json):

    if data_json is not None:

        token_freeze = data_json["token"]["freezeAuthority"]
        top_holders = data_json["topHolders"]
        freeze_authority = data_json["freezeAuthority"]
        risk = data_json["risks"]
        markets = data_json["markets"]

        holders_pct_values = [round(item['pct'], 2) for item in top_holders]
        risk_name_level_values = [(item['name'], item['level']) for item in risk]
        lp_data = [{'pubkey': entry['pubkey'], 'lpLockedUSD': entry['lp']['lpLockedUSD'],
                    'lpLockedPct': entry['lp']['lpLockedPct']} for entry in markets]

        # Check if any risk name matches the specified conditions
        if any(name in ["Freeze Authority still enabled", "Single holder ownership", "High ownership"] for name, level
               in risk_name_level_values):
            return "Invalid"

        # Check if token_freeze or freeze_authority is not None
        if token_freeze is not None or freeze_authority is not None:
            return "Invalid"

        # Check if any lpLockedUSD value is higher than 30000
        for entry in lp_data:
            if entry['lpLockedUSD'] > 30000:
                return "Valid"

        # If none of the conditions are met, return valid
        return "Missing"


#json = get_rug_token_report('CBKrfiMps488bguKrn1mhrx1TW9A4ievYjTw6eQp6rWV')
#check_indicator = check_security_report_json(json)

#x = 5
