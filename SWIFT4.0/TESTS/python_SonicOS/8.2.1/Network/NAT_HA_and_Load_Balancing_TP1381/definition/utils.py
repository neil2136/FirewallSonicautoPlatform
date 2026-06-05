from definition.settings import pkt_api, logger, Parameter, pc1_login, pc2_login
from time import sleep
import re


def init_packet_capture():
    cls_res = pkt_api.clear_packets()
    logger.info(f'clear packet result: {cls_res}')
    start_res = pkt_api.start_capture()
    logger.info(f'start packet capture result: {start_res}')


def check_probe_packet(pro_type='icmp', iface=Parameter.FIREWALL):
    if pro_type not in ('icmp', 'tcp', 'tcp_port'):
        logger.error('\033[1;31mplease specify correct probe type\033[0m')
        return False
    init_packet_capture()
    sleep(10)
    stop_res = pkt_api.stop_capture()
    logger.info(f'stop capture result: {stop_res}')
    pkts = pkt_api.export_captured_packets()
    pkt_list = pkts.split('\n\n')
    check_info = {'icmp': ('IP Type: ICMP(0x1)', f'Src=[{iface}]'),
                  'tcp': ('IP Type: TCP(0x6)', f'Src=[{iface}]'),
                  'tcp_port': ('IP Type: TCP(0x6)', f'Src=[{iface}]', 'Dst=[443]')
                  }
    for pkt in pkt_list:
        if all(x in pkt for x in check_info[pro_type]):
            logger.info(f'get the matched packet:\n{pkt}')
            return True
    logger.error('\033[1;31mnot found the probe packet!\033[0m')
    return False


def get_reply_packet(pc):
    init_packet_capture()
    pc.send_command(f'ping {Parameter.X1_NAT_IP} -c 2')
    stop_res = pkt_api.stop_capture()
    logger.info(f'stop capture result: {stop_res}')
    pkt_api.export_captured_packets_pcapng(filepath='/tmp/packet-c.pcapng')
    pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng')
    logger.info(pkts)
    if pc is pc2_login:
        pattern = r'12.12.1.169 -> 192.168.168.\d+\s+ICMP.*request'
    else:
        pattern = r'12.12.1.170 -> 192.168.168.\d+\s+ICMP.*request'
    rc = re.search(pattern, pkts)
    if rc:
        logger.info(f'found matched request packet:\n{rc.group()}')
        return rc.group()
    logger.error('\033[1;31mnot found matched translated request\033[0m')
    return ''


def get_dst_ip_from_packet(pc):
    pkt_info = get_reply_packet(pc)
    if pkt_info:
        dst_ip = re.search(r'192.168.168.\d+', pkt_info)
        logger.info(f'dst ip is: {dst_ip.group()}')
        return dst_ip.group() if dst_ip else ''
    return ''
