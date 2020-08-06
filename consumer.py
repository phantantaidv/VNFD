#!/usr/bin/env python
import pika
import requests
import time
import socket
import json
# import getLoadbalancerIP
# loadBalancerIp = getLoadbalancerIP.findLoadbalancerIp()

TACKER_URL = 'http://192.168.1.111'


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
    markPoint = getServerListResult.find("""'{"VDU5""")
    LoadbalancerIp = getServerListResult[markPoint + 11: markPoint + 26]
    return LoadbalancerIp

while 1:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1',8080))
    if result == 0:
        print("Port is open")
        time.sleep(1)
        break
    else:
        print("Port is not open")
        time.sleep(1)
credentials = pika.PlainCredentials('openstack', 'rabbit')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(findLoadbalancerIp(), 5672, '/', credentials))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def send_to_om2m(payload):
    headers = {"X-M2M-Origin":"admin:admin", "Content-Type": "application/xml;ty=2"}
    response = requests.post('http://localhost:8080/~/in-cse/in-name/SENSOR/DATA', data=payload, headers=headers)

    return response

def on_request(ch, method, props, body):
    print(" [.] request(%s)" % body)
    response = send_to_om2m(body)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
#channel.basic_consume(on_request, queue='rpc_queue')
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
