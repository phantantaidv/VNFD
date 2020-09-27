import psutil
import time
import requests
from subprocess import check_output

ips = check_output(['hostname', '--all-ip-addresses'])
ip = str(ips)
ip = ip[2:-4]
print(len(ip))
print("Instances's IP:", ip)

        
ACK_message = "ACK"
r = requests.post('http://192.168.1.111:9999/ACKmessage_slice_3', data=ACK_message)
print("<Response [{status_code}] {reason}>".format(status_code=r.status_code, reason=r.reason))
i = 0

while True:
    if i != 0:
        CPU_Pct = round(psutil.cpu_percent()*2,2)
        CPU_Pct = str(CPU_Pct)
        print("*******************************")
        print("CPU Usage = " + CPU_Pct, "%")
        print("*******************************")
        payload = "{ip}, {CPU_Pct}".format(ip=ip, CPU_Pct=CPU_Pct)
        r = requests.post('http://192.168.1.111:9999/Instances_slice_3', data=payload)
        print("<Response [{status_code}] {reason}>".format(status_code=r.status_code, reason=r.reason))
    i += 1
    time.sleep(1)
