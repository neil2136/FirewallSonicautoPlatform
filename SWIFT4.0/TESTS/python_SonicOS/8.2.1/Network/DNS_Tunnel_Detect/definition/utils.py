from definition.settings import logger, pc2_login, re


def check_dns_dropped_pkts(pkts):
    flag = []
    packet_list = pkts.split('Packet number:')
    check_list = ['Dst=[53]', "Dropped"]
    for pkt in packet_list:
        if all(x in check_list for x in check_list):
            logger.info(pkt)
            flag.append(True)
        else:
            flag.append(False)
    return all(flag)


def get_pc2_eth1_ip():
    out = pc2_login.send_command('ifconfig eth1 | grep inet')
    m = re.search(r'192.168.168.\d+', out)
    if m:
        ip_addr = m.group()
        logger.info(f'get pc2 eth1 ip addr is: {ip_addr}')
        return ip_addr
    logger.error('find ip addr failed.')
    return ''
