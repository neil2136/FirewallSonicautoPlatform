import re
import time
from runner.settings import logger


def get_pc_eth_mac(pc, eth):
    out = pc.send_command("ifconfig " + eth +
                          " | grep HWaddr | awk '{print $5}'")
    mac = ''.join(out.strip().split(':'))
    return mac


def pc_get_ip_lease(pc, eth):
    res = False
    ip_addr = ''
    for i in range(10):
        pc.send_command('ifconfig {} 0.0.0.0'.format(eth))
        pc.send_command('timeout 20 killall dhclient')
        out = pc.send_command('timeout 20 dhclient -v {}'.format(eth))
        time.sleep(60)
        logger.info(out)
        m = re.search(
            r'bound to ([23]\.[23]\.[23]\.\d+).*renewal in', out, re.I)
        if m:
            ip_addr = m.group(1)
            logger.info(f'pc {eth} successfully get ip address')
            res = True
            break
        else:
            logger.info(f'pc {eth} failed to get ip address')   
    return res, ip_addr


def pc_release_ip(pc, eth):
    pc.send_command('killall dhclient')
    pc.send_command(f'timeout 20 dhclient -r {eth}')
    pc.send_command(f'timeout 5 ifconfig {eth} 0.0.0.0')
    time.sleep(3)
    logger.info('check if pc eth ip is released...')
    output = pc.send_command(f'ifconfig {eth}')
    if 'inet addr' not in output:
        logger.info(f"pc {eth} release successfully")
        return True
    else:
        logger.info(f"pc {eth} release failed")
        return False

def check_dhcp_ack_packet(packets, src_ip, dst_ip, dst_if):
    packets = packets.split('Packet number: ')
    ackinfo = f"out:{dst_if}*, Generated (Sent Out)"
    src = f"Src=[{src_ip}]"
    dst = f"Dst=[{dst_ip}]"
    for packet in packets:
        if src in packet and dst and ackinfo in packet:
            if "Src=[67], Dst=[68]" in packet:
                return True, packet
    return False, None