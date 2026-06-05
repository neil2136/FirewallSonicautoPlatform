import os
from time import sleep

print('chdir /root/iphelper/')
os.chdir('/root/iphelper/')
path = os.getcwd()
print('current working directory:'.format(path))
cmd = 'tar zxvf netcat-0.7.1.tar.gz'
# print('run cmd:{}'.format(cmd))
os.system(cmd)
sleep(1)
print('chdir /root/iphelper/netcat-0.7.1')
os.chdir('/root/iphelper/netcat-0.7.1/')
sleep(1)
cmds = (
    './configure',
    'make',
    'make install'
)
for cmd in cmds:
    sleep(1)
    os.system(cmd)