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

# getServerListResult = """{'vnfs': [{'status': 'ACTIVE', 'description': 'Load Balancer', 'name': 'hybrid_VNF_fb83e4f9-7326-4c15-8ed4-47e7613f4d04', 'tenant_id': 'dd5a48e68066451082ef80f8f0a91d12', 'created_at': '2020-07-27 03:45:04', 'updated_at': None, 'id': '625ae8c6-f5d4-4f9c-8cc8-44f81aa44baa', 'instance_id': 'c861116a-0775-49a5-b8c7-7e18c4d04613', 'mgmt_url': '{"VDU1": "192.168.233.173"}', 'placement_attr': {'vim_name': 'openstack'}, 'error_reason': None, 'attributes': {'heat_template': 'heat_template_version: 2013-05-23\ndescription: \'Load Balancer\n\n  \'\nparameters: {}\nresources:\n  CP1:\n    type: OS::Neutron::Port\n    properties:\n      port_security_enabled: true\n      network: shared\n      security_groups: [default]\n  FIP1:\n    type: OS::Neutron::FloatingIP\n    properties:\n      floating_network: public\n      port_id: {get_resource: CP1}\n  VDU1:\n    type: OS::Nova::Server\n    properties:\n      user_data_format: RAW\n      availability_zone: nova\n      key_name: MyKey\n      image: xenial-server-cloudimg-amd64\n      user_data: \'#!/bin/sh\n\n        HOSTNAME=$hostname\n\n        sudo -i\n\n        sudo chmod 777 /etc/hosts\n\n        sudo echo "127.0.1.1 ${HOSTNAME}" >> /etc/hosts\n\n        sudo chmod 644 /etc/hosts\n\n        sudo apt-get update && sudo apt-get install -y rabbitmq-server python3-pip\n\n        sudo pip3 install pika && pip3 install request && pip3 install flask\n\n        sudo pip3 install uuid\n\n        wget https://raw.githubusercontent.com/phantantaidv/VNFD/master/producer.py\n\n        -P /home/ubuntu\n\n        ################### Short link###########\n\n        wget -O /home/ubuntu/producer.py https://bit.ly/2XPJE1W\n\n        sudo rabbitmqctl add_user openstack rabbit\n\n        sudo rabbitmqctl set_permissions openstack ".*" ".*" ".*"\n\n        python3 /home/ubuntu/producer.py\n\n        #screen -d -m -S producer python3 /home/ubuntu/producer.py\n\n        \'\n      flavor: m1.medium\n      networks:\n      - port: {get_resource: CP1}\n      config_drive: false\noutputs:\n  mgmt_ip-VDU1:\n    value:\n      get_attr: [CP1, fixed_ips, 0, ip_address]\n'}, 'vim_id': '555b2df1-1df2-4954-8877-ad58751757f1', 'vnfd_id': 'fb83e4f9-7326-4c15-8ed4-47e7613f4d04'}, {'status': 'ACTIVE', 'description': 'lowCapaciity', 'name': 'Om2mVnf467', 'tenant_id': 'dd5a48e68066451082ef80f8f0a91d12', 'created_at': '2020-07-27 03:47:51', 'updated_at': None, 'id': 'bcde78b4-9c7f-443f-b014-69abbe632a81', 'instance_id': '36a1d04e-5a5f-497e-9a95-c4a1e1b34e0a', 'mgmt_url': '{"VDU1": "192.168.233.24"}', 'placement_attr': {'vim_name': 'openstack'}, 'error_reason': None, 'attributes': {'heat_template': 'heat_template_version: 2013-05-23\ndescription: \'lowCapaciity\n\n  \'\nparameters: {}\nresources:\n  CP1:\n    type: OS::Neutron::Port\n    properties:\n      port_security_enabled: true\n      network: shared\n      security_groups: [default]\n  FIP1:\n    type: OS::Neutron::FloatingIP\n    properties:\n      floating_network: public\n      port_id: {get_resource: CP1}\n  VDU1:\n    type: OS::Nova::Server\n    properties:\n      user_data_format: RAW\n      availability_zone: nova\n      key_name: MyKey\n      image: xenial-server-cloudimg-amd64\n      user_data: \'#!/bin/sh\n\n        HOSTNAME=$hostname\n\n        sudo -i\n\n        sudo chmod 777 /etc/hosts\n\n        sudo echo "127.0.1.1 ${HOSTNAME}" >> /etc/hosts\n\n        sudo chmod 644 /etc/hosts\n\n        sudo apt-get update && sudo apt-get install -y default-jre unzip python3-pip\n\n        sudo pip3 install pika && pip3 install requests\n\n        ########## Shour link to download ############3\n\n        wget -O /home/ubuntu/MonitorInstances.py https://bit.ly/2ASthc4\n\n        wget -O /home/ubuntu/consumer.py https://bit.ly/2AXSsd7\n\n        ##################################################\n\n        screen -d -m -S monitor python3 /home/ubuntu/MonitorInstances.py\n\n        screen -d -m -S consumer python3 /home/ubuntu/consumer.py\n\n        git clone https://github.com/phantantaidv/om2m.git /home/ubuntu/testing\n\n        cd /home/ubuntu/testing\n\n        unzip in-cse.zip\n\n        sudo chmod 766 in-cse/*\n\n        cd in-cse\n\n        screen -d -m -S om2m ./start.sh\n\n        \'\n      flavor: ds1G\n      networks:\n      - port: {get_resource: CP1}\n      config_drive: false\noutputs:\n  mgmt_ip-VDU1:\n    value:\n      get_attr: [CP1, fixed_ips, 0, ip_address]\n'}, 'vim_id': '555b2df1-1df2-4954-8877-ad58751757f1', 'vnfd_id': 'e8a6443b-72fa-4cb3-96e5-7b5c04428dd4'}]}"""
#
# # a = """Balancer', 'name': 'hybrid_VNF_fb83e4f9-7326-4c15-8ed4-47e7613f4d04', 'tenant_id': 'dd5a48e68066451082ef80f8f0a91d12', 'created_at': '2020-07-27 03:45:04', 'updated_at': None, 'id': '625ae8c6-f5d4-4f9c-8cc8-44f81aa44baa', 'instance_id': 'c861116a-0775-49a5-b8c7-7e18c4d04613', 'mgmt_url': '{"VDU1": """
# # print(len(a))
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

extractIp()