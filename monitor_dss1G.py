import psutil
import time
import requests
from subprocess import check_output

ips = check_output(['hostname', '--all-ip-addresses'])
ip = str(ips)
ip = ip[2:-4]
print(len(ip))
print("Instances's IP:", ip)

condition = True	
while condition == True:	
    time.sleep(1)	
    CPU_Pct = str(psutil.cpu_percent())
    if float(CPU_Pct) <= 35:	
        condition = False	
    else:	
        condition = True

ACK_message = "ACK"
r = requests.post('http://192.168.1.111:9999/ACKmessage', data=ACK_message)
print("<Response [{status_code}] {reason}>".format(status_code=r.status_code, reason=r.reason))
i = 0

while True:
    if i != 0:
        CPU_Pct = str(psutil.cpu_percent())
        print("*******************************")
        print("CPU Usage = " + CPU_Pct, "%")
        print("*******************************")
        payload = "{ip}, {CPU_Pct}".format(ip=ip, CPU_Pct=CPU_Pct)
        r = requests.post('http://192.168.1.111:9999/Instances', data=payload)
        print("<Response [{status_code}] {reason}>".format(status_code=r.status_code, reason=r.reason))
    i += 1
    time.sleep(1)
