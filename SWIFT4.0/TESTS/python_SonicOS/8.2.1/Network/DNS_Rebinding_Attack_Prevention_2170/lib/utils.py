import sys
import os
import re
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/DNS_Rebinding_Attack_Prevention_2170')
from definition.settings import *

def start_dns_server(ip_addr):
    dns_server.send_command("pkill named")
    ip_addr = ip_addr.split(',')
    test_com_zone_msg = \
    "\$TTL 1D\n" + \
    "@    IN    SOA     test.com.      root (\n" + \
    "                 2007042801\n" + \
    "                 1H\n" + \
    "                 15M\n"+ \
    "                 1W\n"+ \
    "                 1D )\n"+ \
    "              IN   NS      ns.test.com.\n"+ \
    "              IN   MX  10  mail.test.com.\n"
    for ip in ip_addr:
        test_com_zone_msg += '              IN   A       ' + f"{ip}\n"
    test_com_zone_msg += \
    "www           IN   A       10.1.1.60\n" + \
    "ns            IN   A       10.1.1.60\n" + \
    "mail          IN   A       10.1.1.60\n" + \
    "db            IN   A       10.1.1.60\n"
    logger.info(f'The message is:{test_com_zone_msg}')
    dns_server.send_command(f'echo "{test_com_zone_msg}" > /var/named/test.com.zone' )
    dns_server.send_command('named -c /etc/named.conf &')
    out = dns_server.send_command('cat /var/named/test.com.zone')
    if ip_addr[0] in out:
        rc = True
    else:
        rc = False
        logger.error('start dns server failed...')
        logger.info(out)
    return rc

def start_dns_server_X2(ip_addr):
    PC3.send_command("pkill netwox")
    cmd = f"netwox 104 -h test.com -H {ip_addr} -a ns.test.com -A 127.0.0.1 </dev/null >/dev/null 2>/dev/null &"
    for i in range(5):
        out = PC3.send_command(cmd)
        if not out:
            rc = True
            break
        else:
            rc = False
            logger.error('netwox config dns failed...')
            logger.info(out)
    return rc

def get_ip_of_name(dns_server, action, domain):
    cmd1 = f'dig @{dns_server} {domain} +short +time=2'
    if action == 'return-query-refused':
        cmd = f"dig @{dns_server} {domain} +time=2 +noquestion +nostats " + \
             "+noauthority +noadditional"
        out = PC1.send_command(cmd)
        if 'status: REFUSED' in out:
            logger.info("DNS lookup refused\n")
            return ''
    out = PC1.send_command(cmd1)
    rsp = chomppy(out[0])
    logger.info(rsp)
    if rsp:
        logger.info(f'----rsp is {rsp}------')
    return rsp

def chomppy(k):
    if k=="" or k=="\n" or k=="\r\n" or k=="\r": return ""
    if len(k)==1: return k #depends on above case being not true
    if len(k)==2 and (k[-1]=='\n' or k[-1]=='\r'): return k[0]
    #done with weird cases, now deal with average case
    lastend=k[-2:] #get last two pieces
    if lastend=='\r\n':
        outstr=k[:-2]
        return outstr
    elif (lastend[1]=="\n" or lastend[1]=="\r"):
        outstr=k[:-1]
        return outstr
    return k

def check_packet(pkt_path,filter,key_word):
    # cmd = f"tshark -r {pkt_path} -R '{filter}' -V -w /tmp/filter.pcapng"
    cmd = f"tshark -r {pkt_path} -Y '{filter}' -V -w /tmp/filter.pcapng"
    logger.info(f'send command {cmd}')
    packets_info = os.popen(cmd).read()
    logger.info(f"filter packet info is {packets_info}")
    rc = False
    for packet in re.split('Packet comments', packets_info):
        logger.info(f"--------{packet}")
        if key_word in  packet :
            logger.info(f' {key_word} in packets_info  ')
            rc = True
            break
    return rc

    
