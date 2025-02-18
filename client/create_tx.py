import base64
import subprocess
import os
import json

def blockreader(file):
        
    with open(file, 'r') as b:
        blockfile = json.load(b)
        data = []


        #transactions = blockfile['data']['data'][0]['payload']['data']['actions'][0]['payload']['action']['proposal_response_payload']['extension']['results']['ns_rwset'][1]['rwset']['writes'] #transaction data (transaction value in base64)
        limit = len(blockfile['data']['data'])
        transactions = []
        i = 0
        while i < limit:
            transactions.append(blockfile['data']['data'][i]['payload']['data']['actions'][0]['payload']['action']['proposal_response_payload']['extension']['results']['ns_rwset'][1]['rwset']['writes'])
            i+=1
        
        tx_list = []
        z = 0
        while z < limit:
            for x in transactions[z]:
                if 'value' in x:
                    tx_list.append(str({'key': x['key'], 'value': x['value']}))
            z+=1

        #for x in transactions:
        #    if 'value' in x:
        #        tx_list.append(str({'key': x['key'], 'value': x['value']}))
                #tx_list.append(str({'key': x['key'], 'value': base64.b64decode(x['value']).decode()}))
        
        #data.append(blockfile['data']['data'][0]['payload']['header']['channel_header']['channel_id'])
        #print(data)
        #data[0] = blockfile['data']['data'][0]['payload']['data']['actions'][0]['payload']['action']['proposal_response_payload']['extension']['results']['ns_rwset'][1]['rwset']['writes'] #transaction data (transaction value in base64)
        tranx = ','.join(str(e) for e in tx_list)
        #tranx = tranx_s.translate(str.maketrans({"'": r"\'", ",": r"\,"}))
        data.append(tranx)
        data.append(len(tx_list))
        data.append(blockfile['data']['data'][0]['payload']['header']['channel_header']['channel_id']) #channel ID
        data.append(blockfile['data']['data'][0]['payload']['header']['channel_header']['timestamp']) #timestamp for transaction
        data.append(blockfile['data']['data'][0]['payload']['header']['channel_header']['tx_id']) #transaction ID
        data.append(blockfile['data']['data'][0]['payload']['header']['signature_header']['creator']['id_bytes']) #transaction creator certificate base64
        
        header = []
        header.append(blockfile['header']['data_hash']) #blockdata hash
        header.append(int(blockfile['header']['number'])) #Block number
        header.append(blockfile['header']['previous_hash']) #previous block header hash
    
        return header, data

    

def prep(directory):
    blocks=os.listdir(directory)
    for file in sorted(blocks):
        if file.endswith('.json'):
            blockreader(directory+file)
            head, body = blockreader(directory+file)
            txnfile = 'blocks_folder/transactions.js'
            prev_txnfile = 'blocks_folder/prev_transactions.js'
            try:
                open(txnfile, 'x')
            except FileExistsError:
                if os.path.exists(prev_txnfile):
                    os.remove(prev_txnfile)
                    os.rename(txnfile, prev_txnfile)
                    open(txnfile, 'x')
                else:
                    os.rename(txnfile, prev_txnfile)
                    open(txnfile, 'x')
            #print(f"updater.set({body[0]}, {body[1]}, {body[2]}, {body[3]}, {body[4]}, {body[5]}, {head[0]}, {head[1]}, {head[2]})")
            with open(txnfile, 'w') as file:
                #file.write("updater.set("+repr(body[0])+"," +repr(body[1])+"," +repr(body[2])+"," +repr(body[3])+"," +repr(body[4])+"," +repr(body[5])+"," +repr(head[0])+"," +repr(head[1])+"," +repr(head[2])+")")
                #file.write("`"+repr(body[0])+"," +repr(body[1])+"," +repr(body[2])+"," +repr(body[3])+"," +repr(body[4])+"," +repr(body[5])+"," +repr(head[0])+"," +repr(head[1])+"," +repr(head[2])+"`")
                file.write("var data1 = "+repr(body[0])+"\n"+"var data2 = "+repr(body[1])+"\n"+"var data3 = "+repr(body[2])+"\n"+"var data4 = "+repr(body[3])+"\n"+"var data5 = "+repr(body[4])+"\n"+"var data6 = "+repr(body[5])+"\n"+"var data7 = "+repr(head[0])+"\n""var data8 = "+repr(head[1])+"\n"+"var data9 = "+repr(head[2]))
            #print(body[0])
            #Create transaction and submit
            cmd = '''geth --exec 'loadScript("call_contract.js")' attach ../eth-blockchain/data/geth.ipc'''
            subprocess.run(cmd, shell=True)

    
        
loc = "blocks_folder/"
prep(loc)
