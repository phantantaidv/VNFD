import pika
import uuid
import json
import os
from flask import Flask, request
app = Flask(__name__)

# def getHostIp():
#     lines = str(os.popen('ifconfig').read())
#     markIP = lines.index('inet addr:')
#     ip = lines[markIP + 10: markIP + 27]
#     return ip


lines = str(os.popen('ifconfig').read())
markIP = lines.index('inet addr:')
#print(markIP)

ip = lines[markIP + 10: markIP + 27]
@app.route("/")
def hello():
    return "Hello World!"

@app.route('/api/post_data', methods=['GET', 'POST'])
def post_data():
    http_post_rpc = RpcClient()
    print(" [x] Requesting http post to om2m")
    data = request.data
    print(data)
    response = http_post_rpc.call(data)
    print(" [.] Got %r" % response)
    return response
    #return uuid

class RpcClient(object):
    def __init__(self):
        self.credentials = pika.PlainCredentials('openstack', 'rabbit')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.033.104', 5672, '/', self.credentials))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        #self.channel.basic_consume(self.on_response, auto_ack=True,
        #                           queue=self.callback_queue)
        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=n)
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response)

if __name__=="__main__":
    app.run(host='0.0.0.0')

#http_post_rpc = RpcClient()

#print(" [x] Requesting http post to om2m")
#data = '<om2m:cin xmlns:om2m="http://www.onem2m.org/xml/protocols"><cnf>message</cnf><con>&lt;obj&gt;&lt;str name=&quot;appId&quot; val=&quot;SENSOR&quot;/&gt;&lt;str name=&quot;category&quot; val=&quot;temperature &quot;/&gt;&lt;int name=&quot;data&quot; val=&quot;27&quot;/&gt;&lt;int name=&quot;unit&quot; val=&quot;celsius&quot;/&gt;&lt;/obj&gt;</con></om2m:cin>'
#data = '<m2m:ae xmlns:m2m="http://www.onem2m.org/xml/protocols" rn="MY_SENSOR3"><api>app-sensor</api><lbl>Type/sensor Category/temperature Location/home</lbl><rr>false</rr></m2m:ae>'
#response = http_post_rpc.call(data)
#print(" [.] Got %r" % response)
