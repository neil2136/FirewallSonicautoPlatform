import sys
import os
import re
import subprocess
import paramiko
import threading
from time import sleep

if len(sys.argv) < 2:
    print('ERROR: Please check the parameters!')
    sys.exit()



remote_server_ip = '192.0.1.22'
remote_server_username = 'root'
remote_server_passwd = 'password'
remote_file_path = '/root/iphelper'
interface = 'eth0'
local_ip = '192.168.168.169'
local_broadcast_ip = '192.168.168.255'
server_ip = '13.0.0.5'
TESTCASE_PATH = '/root/iphelper'
server_subnet = '13.0.0.255'
DstPort = sys.argv[1]
SrcPort = 36646
record = '/tmp/record.txt'

record_data = '/tmp/listening_port.txt'
child_output = '/tmp/child_output.txt'
file = '/tmp/ChildReady.txt'


    
    

def remote_action():
    sleep(1)
    try:
        ssh_remote = paramiko.SSHClient()
        ssh_remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_remote.connect(hostname=remote_server_ip, port=22, username=remote_server_username, password=remote_server_passwd)
    except:
        print("failed to connect to remote server")

    cmd1 = 'tcpdump -i {} -A -nn -c 1 udp port {} and dst host \( {} or {} or {}\) > {} &'\
    .format(interface, DstPort, server_ip, local_broadcast_ip, server_subnet, record)
    print('run cmd: {}'.format(cmd1))
    stdin,stdout,stderr = ssh_remote.exec_command(cmd1)
    ssh_remote.close()

def remote2():
    try:
        ssh_remote = paramiko.SSHClient()
        ssh_remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_remote.connect(hostname=remote_server_ip, port=22, username=remote_server_username, password=remote_server_passwd)
    except:
        print("failed to connect to remote server")

    cmd = 'python3 {}/receive.py {} {}'.format(remote_file_path, DstPort, local_broadcast_ip)
    print('Child: run cmd {}'.format(cmd))
    stdin,stdout,stderr = ssh_remote.exec_command(cmd)
    log = stdout.read().decode('utf-8')

    ssh_remote.close()
    output=subprocess.run('ls -l /tmp',shell=True, capture_output=True) 
    output = output.stdout.decode('utf-8')
    sleep(1)
    print('Child: child output content is {}'.format(log))
    if not re.search(r'child_output.txt', str(output), re.S|re.I):
        print('Child: create file {}'.format(child_output))
        os.system('touch {}'.format(child_output))
        fco = open(child_output, 'w')
        fco.write(log)
    else:
        fco = open(child_output, 'w')
        fco.write(log)



def send(DstPort):
    print('remote server ip is :{}'.format(remote_server_ip))

    cmd = 'netcat -u -l -p {} > {} &'.format(SrcPort, record_data)
    print('run cmd {}'.format(cmd))
    os.system(cmd)
    t1 = threading.Thread(target=remote_action, name='remote_action')
    t1.start()

    mac=subprocess.run('ifconfig {}'.format(interface), shell=True, capture_output=True)
    mac = mac.stdout.decode('utf-8')
    print('the interface {} is {}'.format(interface, mac))
    regular = re.search(r'HWaddr\s+([0-9a-f]{2}):([0-9a-f]{2}):([0-9a-f]{2}):([0-9a-f]{2}):([0-9a-f]{2}):([0-9a-f]{2})', str(mac), re.S|re.I)
    if regular:
            mac = regular.group()
            mac = mac.split(" ")[1]
            mac = mac.replace(':', '')
            print('the mac address of {} is {}'.format(interface, mac))
    else:
        print('can not get Mac address, ERROR!')\
    
    t1.join()
    t2 = threading.Thread(target=remote2, name='remote2')
    t2.start()

    print('Parent: send a udp request...')
    for i in range(3):
        if re.search(r'\d+\.\d+\.\d+\.255', str(local_broadcast_ip), re.S|re.I):
            send_udp = '{}/subbroadcast -i {} -m {} -s {}.{} -d {}.{} -p hello_shanghai_automation'\
                .format(TESTCASE_PATH, interface, mac, local_ip, SrcPort, local_broadcast_ip, DstPort)
            print(send_udp)
            os.system(send_udp)
        else:
            send_ip = 'sendip -v -p ipv4 -is {} -id {} -p udp -us {} -ud {} {} -d hello_shanghai_automation'\
                .format(local_ip, local_broadcast_ip, SrcPort, DstPort, local_broadcast_ip)
            print(send_ip) 
            os.system(send_ip)
    
    t2.join()

    # sleep(3)
    pidof = 'pidof netcat'
    pid_netcat=subprocess.run(pidof, shell=True, capture_output=True)
    pid_netcat = pid_netcat.stdout.decode('utf-8')
    if pid_netcat:
        os.system('kill {}'.format(pid_netcat)) 

    for i in range(40):
        output = subprocess.run('ls -l /tmp', shell=True, capture_output=True)
        output = output.stdout.decode('utf-8')
        if re.search(r'child_output.txt', str(output), re.S|re.I) and os.path.getsize(child_output) > 0:
            sleep(2)
            fco = open(child_output, 'r') 
            output = fco.read()
            print('Parent: find the file {}, the remote server\'s log is {}'.format(child_output, output))
            os.system('rm -f {}'.format(child_output))
            break
        else:
            sleep(1)
            print('Parent: wait {} second(s) for the child output file: {}'.format(i, child_output))

        if i == 39:
            print('can not get remote server\'s information!')

    sleep(2)
    with open(record_data, 'r') as f:
        content = f.read()
    print('Parent: client PC received data is {}'.format(content))
    # os.system('rm -f {}'.format(record_data))

    return content
       

if __name__ == '__main__':
    send(DstPort)