import psutil
import time
import requests
from subprocess import check_output

ips = check_output(['hostname', '--all-ip-addresses'])
ip = str(ips)
ip = ip[2:-4]
print(len(ip))
print("Instances's IP:", ip)

i = 0
while True:
    if i != 0:
        CPU_Pct = str(psutil.cpu_percent())
        print("*******************************")
        print("CPU Usage = " + CPU_Pct, "%")
        print("*******************************")
        payload = "{ip}, {CPU_Pct}".format(ip=ip, CPU_Pct=CPU_Pct)
        r = requests.post('http://192.168.1.111:9999/Instances_slice_2', data=payload)
        print("<Response [{status_code}] {reason}>".format(status_code=r.status_code, reason=r.reason))
    i += 1
    time.sleep(1)
