
import time

from bot.api.dex_tools import *
from bot.credentials.creds import *
from bot.db.mongodb import *
from datetime import datetime
from bot.api.rug_tools import *



adb = get_localhost_mongo_client()

today_date = datetime.now().strftime('%Y%m%d')
now_time = datetime.now().strftime('%H%M%S')

def new_pairs_engine(adb):
    # engine to get new pairs and write to the db

    pairs_data = get_pairs_data(url, headers)
    time.sleep(4)
    get_new_pairs_df = extract_pairs_main_tokens(pairs_data)

    library = adb['new_pairs']
    reader = library.read('new_pairs')
    new_pairs_db_df = reader.data

    # Filter rows in get_new_pairs_df with address not in new_pairs_db_df['address']
    get_new_pairs_df = get_new_pairs_df[~get_new_pairs_df['address'].isin(new_pairs_db_df['address'])]

    # Add new column "Status" with the value "Valid"
    get_new_pairs_df['Status'] = "Valid"

    library.write('new_pairs', get_new_pairs_df, metadata={"time": now_time, "date": today_date})

    print(f'Writing new pairs data to database: {today_date} - {now_time}')
    print(get_new_pairs_df)

#Test function
#new_pairs_engine(adb)
#library = adb['new_pairs']
##item = library.read('new_pairs')
#new_pairs_df = item.data
#metadata = item.metadata
#x = 4
#json = check_security_audit_token(url=url,headers=headers,address='Cnt95TJZ7rAdipweik4iv6gefEHQt28P19hK1ycEJ1R7')
#check = check_security_audit_json(json)
#y = 54
#retrive new pairs from database funtion3
def get_new_pairs_db():

    if adb.library_exists('new_pairs') == False:  # check if 'buy_tokens' library exists
        adb.initialize_library('new_pairs')

    db_lib = adb['new_pairs']

    # To avoid LibraryNotFoundException, check if 'buy_tokens' exists in the library
    if 'new_pairs' in db_lib.list_symbols():
        reader = db_lib.read('new_pairs')
        new_pairs_df = reader.data
    else:
        new_pairs_df = pd.DataFrame()  # return an empty DataFrame, or handle accordingly

    return new_pairs_df

def get_buy_tokens_db():

    if adb.library_exists('buy_tokens') == False:  # check if 'buy_tokens' library exists
        adb.initialize_library('buy_tokens')  # initialize library if not exists

    db_lib = adb['buy_tokens']

    # To avoid LibraryNotFoundException, check if 'buy_tokens' exists in the library
    if 'buy_tokens' in db_lib.list_symbols():
        reader = db_lib.read('buy_tokens')
        buy_tokens_df = reader.data
    else:
        buy_tokens_df = pd.DataFrame()  # return an empty DataFrame, or handle accordingly

    return buy_tokens_df
#x = get_new_pairs_db()
#x = 4

#signal engine with security checks / keep writing to the buy_tokens db df (create a column where they have staged until boughted and if boughted set them as 
def security_audit_engine():
    new_pairs_df = get_new_pairs_db()
    valid_rows_df = new_pairs_df[new_pairs_df['Status'] == 'Valid']
    buy_token_db = adb['buy_tokens']
    symbol_name = 'buy_tokens'

    # Check if the symbol exists, if not write an empty DataFrame to it
    existing_symbols = buy_token_db.list_symbols()
    if symbol_name not in existing_symbols:
        buy_token_db.write(symbol_name, pd.DataFrame())

    for token_address in valid_rows_df['address']:
        # check the security measures
        json_security = check_security_audit_token(url=url, headers=headers, address=token_address)
        dex_security_indicator = check_security_audit_json(json_security)

        if dex_security_indicator == 'Invalid':
            # change new_pairs_df[Status] for position where address = token_address to Invalid
            new_pairs_df.loc[new_pairs_df['address'] == token_address, 'Status'] = 'Invalid'

        if dex_security_indicator == 'Pass':
            # change new_pairs_df[Status] for position where address = token_address to Pass
            new_pairs_df.loc[new_pairs_df['address'] == token_address, 'Status'] = 'Pass'
            # get the row from newpair_address and append(write) it to the buy_token_db
            row = new_pairs_df[new_pairs_df['address'] == token_address]
            buy_token_db.append(symbol_name, row, metadata={"time": now_time, "date": today_date})
            print(f'SEND BUY ORDER FOR {row}')

        time.sleep(3)


####rug check
def lp_lock_rug_engine():
    buy_tokens_df = get_buy_tokens_db()

    check_tokens_df = buy_tokens_df[buy_tokens_df['Status'] == 'Pass']

    for token_address in check_tokens_df['address']:
        json_rug = get_rug_token_report(address=token_address)
        indicator = check_security_report_json(json_rug)

        if indicator == 'Invalid':
            buy_tokens_df.loc[buy_tokens_df['address'] == token_address, 'Status'] = 'Rug'
            adb['buy_tokens'].write('buy_tokens', buy_tokens_df, metadata={"time": now_time, "date": today_date})
            print('updated to Rug')
        if indicator == 'Valid':
            buy_tokens_df.loc[buy_tokens_df['address'] == token_address, 'Status'] = 'Buy'
            adb['buy_tokens'].write('buy_tokens', buy_tokens_df, metadata={"time": now_time, "date": today_date})
            print('updated to Buy')
        if indicator == 'Missing':
            print('still missing')
            pass
        # You may add more conditions for other indicators if needed

        time.sleep(3)

    return buy_tokens_df


#df = get_buy_tokens_db()
#report = get_rug_token_report(address='947tEoG318GUmyjVYhraNRvWpMX7fpBTDQFBoJvSkSG3')

#TODO - check why is the buy_tokens adb returning only 1 row / new pairs are over writing instead of appending / some new pairs are from exisitend coins so we just want new created/ use rugcheck api
while True:
     new_pairs_engine(adb)
     time.sleep(3)
     security_audit_engine()
     lp_lock_rug_engine()

#list = adb.list_libraries()
#check = adb.library_exists('buy_tokens')
#adb.initialize_library('buy_tokens')

#db_lib = adb['buy_tokens']
#reader = db_lib.read('buy_tokens')
#data = reader.data

#db_lib2 = adb['buy_tokens']
# reader = db_lib.read('buy_tokens')
# buy_tokens_df = reader.data

#pools = check_pools_token(url=url,headers=headers,address='947tEoG318GUmyjVYhraNRvWpMX7fpBTDQFBoJvSkSG3')
#m = check_pools_json(pools)
#time.sleep(3)
#pooos = check_pool_locks(url=url,headers=headers, address='6hKhvYoNf67nftegCm85PWwr6Pt8sBrxK7RUCvigFmcH')
x = 4

