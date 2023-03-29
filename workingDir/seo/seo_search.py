import time
from xml import dom

from requests import Response
import requests
from urllib.parse import urlencode
import random
import string
import time
from fake_useragent import UserAgent
import json

chrome_ua:list = UserAgent().data_browsers['chrome']

# id是地区元组 
    # 21577777:广东(电信) 21577778:贵州(电信) 21577775:安徽(电信) 21577786:云南(电信) 
    # 21577789:山东(联通) 21577776:吉林(联通) 21577781:江苏(联通) 21577784:黑龙江(联通)  21577785:河北(联通)
ids = ('21577777','21577778','21577775','21577786','21577789','21577776','21577781','21577784','21577785')

# 服务器列表 
servers = {
    '21577777': '7Z6X7eM6XQrDAtec|gMpag==',
    '21577778': 'sQKV8kYp|wNxvbSknkjuSg==',
    '21577775': 'PkmI7hqapd6vjB4xWLNQYw==',
    '21577786': '~MY5RoSlZThPg2FWU95GxA==',
    '21577789': 'Rv90~Ksj1L43o1paEdFlPw==',
    '21577776': '60Nalf4AeB6unlRqEv7KxQ==',
    '21577781': '|ob45Dk5IfqMwqRk1xcWPw==',
    '21577784': 'FVPBtDll6C4AirNQXcl~fg==',
    '21577785': 'B0tT1sgLvByXqUFTs~TzIA=='
}

random_callback = 'jQuery'+''.join(random.sample(string.digits,10))+''.join(random.sample(string.digits,10))+ \
''.join(random.sample(string.digits,2))+'_'+str(int(round(time.time() * 1000)))


# 根据域名和地区 查询ip
def get_ip(domain,id,server):
    query_data = {
        't': 'dns',
        'server': server,
        'id': id,
        'callback': random_callback
    }
    data = {
        'host': domain,
        'type': '1',
        'total': '9',
        'process': '0',
        'right': '0'
    }
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': random.choice(chrome_ua),
        'Host': 'tool.chinaz.com',
        'origin': 'https://tool.chinaz.com',
        'pragma': 'no-cache',
        'referer': 'https://tool.chinaz.com/DNS?type=1',
        'x-requested-with': 'XMLHttpRequest'
    }
    response:Response = requests.api.post(url='https://tool.chinaz.com/AjaxSeo.aspx?'+urlencode(query_data),data=data,headers=headers)
    return response

# 查询域名最快的ip
def find_fastest_ip(domain):
    ttl = 0
    final_ip = None
    for id in ids:
        response = get_ip(domain,id,servers[id])
        res = json.loads(response.text[42:].replace('(', '').replace(')', ''))
        if res['list'] != None and res['list'].__len__() != 0:
            list_data:list = res['list']
            for item in list_data:
                item_ttl = item['ttl']
                # 判断此ttl是否为最小值 
                if ttl == 0:
                    ttl = int(item_ttl)   
                    final_ip = item['result']
                elif int(item_ttl) < int(ttl):
                    # 更新ttl
                    ttl = int(item_ttl)
                    final_ip = item['result']
        time.sleep(0.2)
    return final_ip

if __name__=='__main__':
    ip = find_fastest_ip('www.github.com')
    if ip is not None:
        print('解析结果:'+ip)
    else:
        print('域名无法解析!')


