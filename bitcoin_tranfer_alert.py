import requests
from datetime import  timedelta
import datetime
import time



def gen_linker(coin,hash_value,blochcain_type):
    if coin=='btc':
        linker="https://www.blockchain.com/btc/tx/"+str(hash_value)
        return linker
    elif coin=='eth':
        linker='https://etherscan.io/tx/0x'+str(hash_value)
        return linker
    elif coin=='eos':
        linker = "https://eospark.com/tx/"+str(hash_value)
        return linker
    elif coin=='usdt' and blochcain_type=='ethereum':
        linker = 'https://etherscan.io/tx/0x' + str(hash_value)
        return linker
    elif coin=='usdt' and blochcain_type=='bitcoin':
        linker = 'https://omniexplorer.info/search/' + str(hash_value)
        return linker
    elif coin=='usdt' and blochcain_type=='tron':
        linker = 'https://tronscan.org/#/transaction/' + str(hash_value)
        return linker

def is_trans_alert(coin,btc_number,min):
    '''
    :param coin: 幣種
    :param btc_number:幾顆
    :param min:幾分鐘內
    :return:
    '''
    dtime = datetime.datetime.now() - timedelta(hours=20)
    ans_time = time.mktime(dtime.timetuple())
    my_params = {'api_key': '9eeI8leNbB5fkugC9E1slnlEP9uBewmK', 'min_value': 500000,'start':int(ans_time),'cursor':'2bc7e46-2bc7e46-5c66c0a7','currency':coin}
    r=requests.get('https://api.whale-alert.io/v1/transactions?',params=my_params)
    a=r.json()
    print (a)
    count=int(a['count'])
    print ("count ={}".format(count))
    if count==0:
        print ('no data')
        # sleep(5)
        return 1
    elif count >0:
        alert_list=[]
        for i in range(0,len(a['transactions'])):
            from_value=a['transactions'][i]['from']['owner_type']
            to_value=a['transactions'][i]['to']['owner_type']
            amount_btc = float(a['transactions'][i]['amount'])
            tranfer_time=int(a['transactions'][i]['timestamp'])
            convert_time = datetime.datetime.fromtimestamp(tranfer_time)
            convert_address = str(a['transactions'][i]['hash'])
            blochcain_type=str(a['transactions'][i]['blockchain'])
            if amount_btc>=btc_number:
                if from_value=='exchange' and from_value=='unknown' :
                    amount_usdt = a['transactions'][i]['amount_usd']
                    amount_btc = a['transactions'][i]['amount']
                    from_value_name = a['transactions'][i]['from']['owner']
                    address_full_link = gen_linker(coin,convert_address,blochcain_type)
                    content="\n[ {} ]\n 從 {} 轉到 {} \n 總共 = {:,} {}\n 價值: {:,} usd \n 地址連結: {}".format(convert_time,from_value_name,to_value,amount_btc,coin,amount_usdt,address_full_link)
                    alert_list.append(content)
                elif to_value=='exchange' and from_value=='unknown':
                    amount_usdt = a['transactions'][i]['amount_usd']
                    amount_btc = a['transactions'][i]['amount']
                    to_value_name =a['transactions'][i]['to']['owner']
                    address_full_link = gen_linker(coin,convert_address,blochcain_type)
                    content ="\n[ {} ]\n 從 {} 轉到 {} \n 總共 = {:,} {}\n 價值: {:,} usd \n 地址連結: {}".format(convert_time,from_value, to_value_name,amount_btc,coin,amount_usdt,address_full_link)
                    alert_list.append(content)
                elif from_value=='exchange' and to_value=='exchange' :
                    amount_usdt = a['transactions'][i]['amount_usd']
                    amount_btc = a['transactions'][i]['amount']
                    from_value_name = a['transactions'][i]['from']['owner']
                    to_value_name = a['transactions'][i]['to']['owner']
                    address_full_link = gen_linker(coin,convert_address,blochcain_type)
                    content ="\n[ {} ]\n 從 {} 轉到 {} \n 總共 = {:,} {}\n 價值: {:,} usd \n 地址連結: {}".format(convert_time,from_value_name,to_value_name,amount_btc,coin,amount_usdt,address_full_link)
                    alert_list.append(content)
                elif from_value=='unknown' and to_value=='unknown':
                    amount_usdt=a['transactions'][i]['amount_usd']
                    amount_btc = a['transactions'][i]['amount']
                    address_full_link = gen_linker(coin,convert_address,blochcain_type)
                    content ="\n[ {} ]\n 從 {} 轉到 {} \n 總共 = {:,} {}\n 價值: {:,} usd \n 地址連結: {}".format(convert_time,from_value,to_value,amount_btc,coin,amount_usdt,address_full_link)
                    alert_list.append(content)

        return alert_list


if __name__ == '__main__':
    a=(is_trans_alert(coin='btc',btc_number=10,min=3600))
    for i in a:
        print (i)