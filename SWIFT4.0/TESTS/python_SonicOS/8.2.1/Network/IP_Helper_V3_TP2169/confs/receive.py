import sys
from time import sleep
import os
import re
import subprocess



if len(sys.argv) < 3:
    print('ERROR: Please check the parameters!')
    sys.exit()



SrcPort = sys.argv[1]
DstPort = sys.argv[2]
server_ip = '13.0.0.5'
server_subnet = '13.0.0.255'
interface = 'eth0'
record = '/tmp/record.txt'
remote_server_ip = '192.0.1.22'

def receive(SrcPort, DstPort):
    cmd = 'tcpdump -i {} -A -nn -c 1 udp port {} and dst host \( {} or {} or {}\) > {} &'\
        .format(interface, SrcPort, server_ip, DstPort, server_subnet, record)
    print('run cmd: {}'.format(cmd))
    output = subprocess.run(cmd, shell=True, capture_output=True)
    output = output.stdout.decode('utf-8')
    print(output)
    sleep(6)
    with open(record, 'r') as f:
        content = f.read()
        content = ''.join(content)
    print('Server: the tcpdump\'s content is: {}'.format(content))
    regular = re.search(r'IP ((?:\d{1,3})\.(?:\d{1,3})\.(?:\d{1,3})\.(?:\d{1,3}))\.(\d+)', str(content), re.S|re.I)
    if regular:
        if regular.group(1) == '13.0.0.168' or regular.group(1) == '192.168.168.169':
            print('Server: get a unicast, it\'s from {}. Send a reply...'.format(regular.group(1)))
            cmd = 'sendip -v -p ipv4 -is {server} -id {g1} -p udp -us {port} -ud {g2} {g1} -d shanghai_automation_are_the_best'\
                .format(server=server_ip,port=SrcPort, g1=regular.group(1), g2=regular.group(2))
            print(cmd)
            output = subprocess.run(cmd, shell=True, capture_output=True)
            output = output.stdout.decode('utf-8')
            print(output)
        else:
            print('receive a multicast...')
    else:
        print('can not get dst port')


    pid_td =  subprocess.run('pidof tcpdump', shell=True, capture_output=True)
    pid_td = pid_td.stdout.decode('utf-8')

    if pid_td:
        os.system('kill {}'.format(pid_td))
    os.system('rm -f {}'.format(record))


if __name__ == '__main__':
    receive(SrcPort, DstPort)