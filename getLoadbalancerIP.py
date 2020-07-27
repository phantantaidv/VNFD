import requests
import json

TACKER_URL = 'http://192.168.2.59'


def get_token():
    # print("\nGet token:")
    get_token_result = ''
    get_token_url = TACKER_URL + ':5000/v3/auth/tokens'
    get_token_body = {
        'auth': {
            'identity': {
                'methods': [
                    'password'
                ],
                'password': {
                    'user': {
                        'domain': {
                            'name': 'Default'
                        },
                        'name': 'admin',
                        'password': 'admin'
                    }
                }
            },
            'scope': {
                'project': {
                    'domain': {
                        'name': 'Default'
                    },
                    'name': 'admin'
                }
            }
        }
    }
    get_token_response = requests.post(get_token_url, data=json.dumps(get_token_body))
    # print("Get Tacker token status: " + str(get_token_response.status_code))
    get_token_result = get_token_response.headers['X-Subject-Token']
    return get_token_result

def findLoadbalancerIp():
    getNetworkListUrl = TACKER_URL + ':9890/v1.0/vnfs'
    token = get_token()
    headers = {'X-Auth-Token': token}
    getResponse = requests.get(getNetworkListUrl, headers=headers)
    # print("Server Response status:" + str(getResponse.status_code))
    getServerListResult = str(getResponse.json())
    markPoint = getServerListResult.find('Balancer')
    LoadbalancerIp = getServerListResult[markPoint + 300: markPoint + 315]
    return LoadbalancerIp

def writeFile(filename, content):
    f = open(filename, 'w')
    f.write(content)
    f.close()

def extractIp():
    Content = "LOAD_BALANCER_IP = '{ip}'".format(ip = findLoadbalancerIp())
    writeFile('param.py', Content)
