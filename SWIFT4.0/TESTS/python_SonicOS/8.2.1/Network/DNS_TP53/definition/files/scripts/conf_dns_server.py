#!/usr/bin/python3
import os
import sys
import re
import pexpect
from optparse import OptionParser


prompts = '[$#>:]'
usage = '--- how to use this program -- \n' \
        'python3 /SWIFT4.0/TESTS/python_SonicOS/7.0.1/Network/DNS_TP53/definition/files/LoginDUTFromInterface.py ' \
        '-i 10.11.1.30 -p /SWIFT4.0/TESTS/python_SonicOS/7.0.1/Network/DNS_TP53/definition/files/'
parser = OptionParser(usage)
parser.add_option('-i', '--ip', dest='ip', action='store', type='string', help='pc eth ip')
parser.add_option('-p', '--path', dest='path', action='store', type='string', help='script path')

(options, args) = parser.parse_args()
ip = options.ip
path = options.path
print(f'shot parameter value print: -i: {ip}, -p: {path}')


def ssh_login():
    try:
        myssh = pexpect.spawn('ssh %s@%s' % ('root', ip),timeout=60, encoding="utf-8")
        myssh.logfile = sys.stdout
        index = myssh.expect([
                "(?i)are you sure.*",
                "(?i)password:",
                "[#\$] ",
                pexpect.EOF,
                pexpect.TIMEOUT
            ])
        #ssh_newkey = 'Are you sure you want to continue connecting'
        #index = myssh.expect(["password", ssh_newkey, pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
                myssh.sendline("yes")
                myssh.expect("(?i)password:")
                myssh.sendline('password')
        elif index == 1:
            myssh.sendline('password')
        elif index == 2:
            return myssh
        else:
            print("ssh login failed: EOF or TIMEOUT")
            myssh.close(force=True)
            return None
        myssh.expect("[#\$] ")
        return myssh
    except Exception as e:
        print(f"Login PC {ip} failed,ssh login exception: {e}")
        return None


def dns_server_file_cp():
    try:
        cp_list = [
            {'source': 'named.conf', 'dest': '/etc/named.conf'},
            {'source': 'named.rfc1912.zones', 'dest': '/etc/named.rfc1912.zones'},
            {'source': 'test.com.zone', 'dest': '/var/named/test.com.zone'},
            {'source': '1.16.172.zone', 'dest': '/var/named/1.16.172.zone'},
        ]
        child = ssh_login()
        for file in cp_list:
            cmd = f'\cp -rf {path}/dnsconf/{file["source"]} {file["dest"]}'
            print(f'cmd run: {cmd}')
            child.sendline(cmd)
            child.expect("[#\$] ")
        child.sendline('find /var/named/ -name 1.16.172.zone')
        child.expect("[#\$] ")
        findres = child.before
        if cp_list[0]['dest'] in findres:
            print('config base dns server file successful !')
        else:
            print('config base dns server file fail.')
    except Exception as e:
        print(f"copy server file failed exception: {e}")
        return None


def dnssec_server_config():
    child = ssh_login()
    child.sendline('cd /var/named')
    child.expect("[#\$] ")
    # check dnssec service configure
    child.sendline('find . -name "*.key"')
    child.expect("[#\$] ")
    lsres = child.before
    if 'Ktest' in lsres:
        print('check test.com.zone configure')
        child.sendline(f'cat test.com.zone')
        child.expect("[#\$] ")
        catres = child.before
        if 'Ktest.com' not in catres:
            findres = re.findall('Ktest.com\S+', lsres)
            print(f'the ksk zsk key is: {findres}')
            if len(findres) == 2:
                child.sendline(f'echo "\$INCLUDE {findres[0]}" >> test.com.zone')
                child.expect("[#\$] ")
                child.sendline(f'echo "\$INCLUDE {findres[1]}" >> test.com.zone')
                child.expect("[#\$] ")
        else:
            print(lsres)
            print('dnssec service inuse, do not need create again !')
    else:
        print('start dnssec configure...')
        # 1. gen the ksk key
        child.sendline('dnssec-keygen -f KSK -r /dev/urandom -a NSEC3RSASHA1 -b 768 -n ZONE test.com')
        child.expect("[#\$] ")
        # 2. gen the zsk key
        child.sendline('dnssec-keygen -r /dev/urandom -a NSEC3RSASHA1 -b 768 -n ZONE test.com')
        child.expect("[#\$] ")
        # 3. edit test.com.zone and assigned key
        child.sendline('find *.key')
        child.expect("[#\$] ")
        lsres = child.before
        findres = re.findall('Ktest.com\S+', lsres)
        print(f'the ksk zsk key is: {findres}')
        if len(findres) == 2:
            child.sendline(f'echo "\$INCLUDE {findres[0]}" >> test.com.zone')
            child.expect("[#\$] ")
            child.sendline(f'echo "\$INCLUDE {findres[1]}" >> test.com.zone')
            child.expect("[#\$] ")
            # get the NSEC3 salt
            child.sendline(f'head -c 1000 /dev/urandom | sha1sum | cut -b 1-16')
            child.expect("[#\$] ")
            sumres = child.before
            headsum = sumres.split('\r\n')
            print(f'head sum is: {headsum}')
            if len(headsum) == 3:
                # gen test.com.zone.signed file
                child.sendline(f'dnssec-signzone -3 {headsum[1]} -o test.com test.com.zone')
                child.expect("[#\$] ")
                # 4. deploy assigned to /etc/named.rfc1912.zones
                # change test.com.zone to test.com.zone.signed.
                # already finished in cp file.
                print('finished dnssec configure...')
            else:
                print('can not get NSEC3\'s salt')
                print(sumres)
        else:
            print('can not get the public key')
            print(lsres)
    child.close(force=True)


def restart_named_service():
    child = ssh_login()
    child.sendline('service named restart')
    child.expect("[#\$] ")
    namedres = child.before
    restartres = re.findall('OK', namedres)
    if len(restartres) >= 2:
        print('restart dns server successful.')
    else:
        print('restart dns server failed.')
        print(namedres)


if __name__ == '__main__':
    print('.................start config base dns server file...................')
    dns_server_file_cp()
    print('.................end config base dns server file...................')
    print('.................start config dns sec service...................')
    dnssec_server_config()
    print('.................end config dns sec service...................')
    print('.................start restart dns service...................')
    restart_named_service()
    print('.................end restart dns service...................')