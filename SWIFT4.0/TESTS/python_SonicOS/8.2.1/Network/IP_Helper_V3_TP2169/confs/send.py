import sys
import os
import re
import paramiko
import subprocess
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


def send(DstPort):
    print('remote server ip is :{}'.format(remote_server_ip))
    pid = os.fork()
    print('==================')
    print(pid)
    print('----------------')
    if pid == 0:
        print('Child ID: {}'.format(os.getpid()))
       
        output=subprocess.run('ls -l /tmp',shell=True, capture_output=True) 
        output = output.stdout.decode('utf-8')
        if not re.search(r'ChildReady.txt', str(output), re.S|re.I):
            print('Child: create file {}'.format(file))
            os.system('touch {}'.format(file))
            with open(file, 'w') as f:
                f.write('Child ID: {} \n'.format(os.getpid()))
        else:
            os.system('rm -f {}'.format(file))
            os.system('touch {}'.format(file))
            with open(file, 'w') as f:
                f.write('Child ID: {} \n'.format(os.getpid()))
        # sleep(2)
        try:
            ssh_remote = paramiko.SSHClient()
            ssh_remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_remote.connect(hostname=remote_server_ip, port=22, username=remote_server_username, password=remote_server_passwd)
        except:
            print("Child: failed to connect to remote server")
        
        sleep(3)
        cmd = 'python3 {}/receive.py {} {}'.format(remote_file_path, DstPort, local_broadcast_ip)
        print('Child: run cmd {}'.format(cmd))
        stdin,stdout,stderr = ssh_remote.exec_command(cmd)
        log = stdout.read().decode('utf-8')

        ssh_remote.close()
        # sleep(1)
        print('Child: child output content is {}'.format(log))
        if not re.search(r'child_output.txt', str(output), re.S|re.I):
            print('Child: create file {}'.format(child_output))
            os.system('touch {}'.format(child_output))
            fco = open(child_output, 'w')
            fco.write(log)
        else:
            fco = open(child_output, 'w')
            fco.write(log)

        print('Child: finish')
    else:
        print('Parent ID: {}'.format(os.getpid()))
        cmd = 'nc -u -l -p {} > {} &'.format(SrcPort, record_data)
        print('Parent: run cmd {}'.format(cmd))
        os.system(cmd)
        print('Parent: wait for {}'.format(file))

        mac=subprocess.run('ifconfig {}'.format(interface), shell=True, capture_output=True)
        mac = mac.stdout.decode('utf-8')
        print('Parent: the interface {} is {}'.format(interface, mac))
        regular = re.search(r'ether\s+([0-9a-f]{2}):([0-9a-f]{2}):([0-9a-f]{2}):([0-9a-f]{2}):([0-9a-f]{2}):([0-9a-f]{2})', str(mac), re.S|re.I)
        if regular:
                mac = regular.group()
                mac = mac.split(" ")[1]
                mac = mac.replace(':', '')
                print('Parent: the mac address of {} is {}'.format(interface, mac))
        else:
            print('Parent: can not get Mac address, ERROR!')\
        
        # sleep(1)
        for i in range(32):
            output = subprocess.run('ls -l /tmp', shell=True, capture_output=True)
            output = output.stdout.decode('utf-8')
            if re.search(r'ChildReady.txt', str(output), re.S|re.I) and os.path.getsize(file) > 0 :
                print('Parent: find child process login remote PC successfully...')
                sleep(1)
                os.system('rm -f {}'.format(file))
                break
            else:
                print('Parent: wait {} second(s)'.format(i))
                sleep(1)

            if i == 31:
                print('Parent: can not find {}'.format(file))

        sleep(2)
        print('Parent: send a udp request...')
        
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