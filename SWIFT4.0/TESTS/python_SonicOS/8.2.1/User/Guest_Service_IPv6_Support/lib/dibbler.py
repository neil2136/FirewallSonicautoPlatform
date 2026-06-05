import re
from networkdevice import Host


def dibblerstart(host,filepath,interface):
    cmd = 'dibbler-client status'
    target_host = Host(host)
    out = target_host.send_command(cmd)
    if re.search(r'Dibbler client: RUNNING, pid=\d+', out, re.M):
        cmd = "dibbler-client stop";
        output = target_host.send_command(cmd)
        print(output)
    filename = filepath+ '/client.'+interface+'.conf'
    cmd = 'cp -f '+ filename + ' /etc/dibbler/client.conf'
    print(cmd)
    target_host.send_command(cmd)
    cmd = 'dibbler-client start >  /tmp/dibbler.log  2>&1  &'
    target_host.send_command(cmd)


def dibblerstop(host,filepath):
    target_host = Host(host)
    cmd = 'dibbler-client stop'
    target_host.send_command(cmd)
    file_name = filepath + '/client.conf'
    cmd = 'cp -f ' + file_name+' /etc/dibbler/client.conf'
    target_host.send_command(cmd)


