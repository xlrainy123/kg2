# encoding=utf8
import urllib3
import json
access_token = '24.5b454a3cbef9f05ff57c4a98dfc41298.2592000.1545901385.282335-14954286'

url_template = 'https://aip.baidubce.com/rpc/2.0/kg/v1/cognitive/entity_annotation?access_token={}'

def get_baidu_url(name):
    http = urllib3.PoolManager()
    data = {'data': name}
    encoded_data = json.dumps(data)
    url = url_template.format(access_token)
    response = http.request('POST', url, body=encoded_data, headers={'Content-Type': 'application/json'})
    attrs = response.data.decode('utf-8')
    params = json.loads(attrs)
    print(params['entity_annotation'][0]['_bdbkUrl'])
    return params['entity_annotation'][0]['_bdbkUrl']

if __name__ == '__main__':
    get_baidu_url('图灵')