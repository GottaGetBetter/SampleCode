import sqlite3
import datetime
import pandas as pd
import json
import urllib.request

#Convert hex string to int
def hexStringToInteger(s):
    return int(s,0)

#Fetch data from scratch
def fetchData(oracle, start =0 ,end=99999999):
    with urllib.request.urlopen("http://api.etherscan.io/api?module=account&action=txlist&address="+oracle+"&startblock="+str(start)+"&endblock="+str(end)+"&sort=asc&apikey=3NGYJJHWUWDWVJUCXWXEF1PKJERK15IZ6B") as url:
        transactionData = json.loads(url.read().decode())

        start = int(transactionData['result'][-1]['blockNumber'])+1
        if len(str(start)) == 7:
            end = 2000000+ start
        elif len(str(start)) == 8:
            end = 20000000+ start



    transactionResult = transactionData['result']
    count = 0
    for result in transactionResult:
        inputString = result['input']
        blockNumber = result['blockNumber']
        timeStamp = int(result['timeStamp'])
        transactionH = result['hash']
        gasUsed = int(result['gasUsed'])

        methodID = inputString[0:10]
        if methodID != "0x5a686699":
            continue
        priceHex = inputString[10:74]
        zzzHex = inputString[74:138]


        priceETH = hexStringToInteger('0x'+priceHex)/10**18
        zzzValue = (hexStringToInteger('0x'+zzzHex)-int(result['timeStamp']))/3600
        fee = gasUsed * 0.000000001 * priceETH

        dbInsertQuerry(oracle, blockNumber, transactionH, inputString, timeStamp, priceETH, zzzValue, fee)




    fetchData(oracle, start, end)


#Insert function
def dbInsertQuerry(oracle, block, transaction, inputString, time, price, zzz, fee):
    connection = sqlite3.connect("MakerOracle.db")
    cursor = connection.cursor()

    oracle = str(oracle)


    cursor.execute(f'''INSERT INTO transactions VALUES('{oracle}', {block}, '{transaction}', '{inputString}', {fee})''')
    cursor.execute(f'''INSERT INTO inputs VALUES('{transaction}', {time}, {price}, {zzz})''')


    connection.commit()
    connection.close()

#Update database function
def dbUpdateQuerry(oracle):
    connection = sqlite3.connect("MakerOracle.db")
    cursor = connection.cursor()

    oracle = str(oracle)

    cursor.execute(f'''SELECT MAX(block) FROM transactions WHERE oracle = '{oracle}' ''')
    start = cursor.fetchone()[0] + 1
    end = 20000000+ start

    with urllib.request.urlopen("http://api.etherscan.io/api?module=account&action=txlist&address="+oracle+"&startblock="+str(start)+"&endblock="+str(end)+"&sort=asc&apikey=3NGYJJHWUWDWVJUCXWXEF1PKJERK15IZ6B") as url:
        transactionData = json.loads(url.read().decode())

    transactionResult = transactionData['result']
    if len(transactionResult) == 0:
        return None
    count = 0
    for result in transactionResult:
        inputString = result['input']
        blockNumber = result['blockNumber']
        timeStamp = int(result['timeStamp'])
        transactionH = result['hash']
        gasUsed = int(result['gasUsed'])

        methodID = inputString[0:10]
        if methodID != "0x5a686699":
            continue
        priceHex = inputString[10:74]
        zzzHex = inputString[74:138]


        priceETH = hexStringToInteger('0x'+priceHex)/10**18
        zzzValue = (hexStringToInteger('0x'+zzzHex)-int(result['timeStamp']))/3600
        fee = gasUsed *0.000000001*priceETH

        dbInsertQuerry(oracle, blockNumber, transactionH, inputString, timeStamp, priceETH, zzzValue, fee)

    local_time = time.asctime( time.localtime(time.time()) )
    print(f"New updates for {oracle} {local_time}")
    connection.close()

#Get Stats
def getStats():
    connection = sqlite3.connect("MakerOracle.db")
    connection.row_factory = lambda cursor, row: row[0]
    c = connection.cursor()

    c.execute('''SELECT time-LAG(time) OVER (ORDER BY time) FROM inputs ''')
    update_time_list = sorted(c.fetchall()[1:])


    average_update_time = sum(update_time_list)/len(update_time_list)/60
    max_update_time = update_time_list[-1]
    min_update_time = update_time_list[0]
    med_update_time = statistics.median(update_time_list)


    c.execute('''SELECT zzz FROM inputs''')
    live_time_list = sorted(c.fetchall())


    average_live_time = sum(live_time_list)/len(live_time_list)
    max_live_time = live_time_list[-1]
    min_live_time = live_time_list[0]
    med_live_time = statistics.median(live_time_list)


    c.execute('''SELECT fee FROM transactions''')
    fee_list = sorted(c.fetchall())

    average_fee = sum(fee_list)/len(fee_list)
    max_fee = fee_list[-1]
    min_fee = fee_list[0]
    med_fee = statistics.median(fee_list)
    return f"(In hour) \nAverage time to live: {average_live_time}\n Max time to live: {max_live_time} \n Min time to live: {min_live_time} \n Med time to live: {med_live_time}\n (In minutes)\n Average update time: {average_update_time} \n Max update time :{max_update_time} \n Min update time: {min_update_time}\n Med update time: {med_update_time}\n (In USD) \n Average fee : {average_fee}\n Min fee : {min_fee}\n Max fee: {max_fee}\n Med fee : {med_fee}"

    connection.close()





#SAMPLE
connection = sqlite3.connect("MakerOracle.db")
c = connection.cursor()

c.execute('''SELECT * FROM oracles''')
for oracle in c.fetchall():
    oracle = oracle[0]
    try:
        fetchData(oracle)
    except IndexError as error:
        continue

print("Completed")

connection.close()
