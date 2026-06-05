import re
from definition.settings import scapyobj, logger, packetapi


def pc_send_tcp_packets(src_ip, dst_ip):
    tcp_packet = {
        'IP': {
            'src': src_ip,  # '192.168.168.169'
            'dst': dst_ip,  # '12.12.1.169'
        },
        'TCP': {
            'sport': 5555,
            'dport': 8888,
        },
        'data': 'automation',
    }
    scapyobj.send_tcp_packet(**tcp_packet)

def fw_config_capture_monitor():
    packetapi.monitor_default()
    packetapi.clear_packets()
    packetapi.start_capture()



def get_tcp_packet_port_number(packets, src_ip, dst_ip):
    src_port = ''
    dst_port = ''
    packet_list = packets.split('Packet number:')
    check_list = [f'Src=[{src_ip}]', f'Dst=[{dst_ip}]', 'TCP(0x6)']
    for packet in packet_list:
        if all(x in packet for x in check_list):
            logger.info(
                'get tcp packet, check the scr_port and dst_port')
            logger.info(packet)
            try:
                src_port = re.search('Src=\[\d{4,}\]', packet, re.I | re.M).group()
                dst_port = re.search('Dst=\[\d{4,}\]', packet, re.I | re.M).group()
            except Exception as e:
                logger.error(repr(e))
            break
    else:
        logger.info("get tcp packet failed.")
    logger.info(f'source port: {src_port}')
    logger.info(f'dst port: {dst_port}')
    return src_port, dst_port


def get_icmp_identifer(file_name, src_ip, dst_ip, verison='ipv4'):
    identifer = ''
    f = open(file_name, 'r', encoding='utf-8')
    packet_list = f.readlines()
    check_list = [src_ip, dst_ip, 'Echo (ping) request']
    for packet in packet_list:
        if all(x in packet for x in check_list):
            logger.info(f'get {verison} icmp request success, check the ICMP identifer')
            logger.info(packet)
            try:
                identifer = re.search('id=0x[0-9a-f]+', packet, re.I | re.M).group()
            except Exception as e:
                logger.error(repr(e))
            break
    else:
        logger.info('get icmp request packet failed.')
    f.close()
    logger.info(f"identifer is: {identifer}")
    return identifer

