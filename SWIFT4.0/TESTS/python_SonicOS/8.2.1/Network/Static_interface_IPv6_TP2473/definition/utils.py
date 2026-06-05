import time
from runner.settings import logger
from definition.settings import iface_v6_api, localhost, iface_v4_api, rm_ifacev4_api, fw, rem_fw, pkt_api, iface_cli


def check_RA_packet(packets, in_if, src_ip=None, dst_ip='ff02::1', status='Received'):
    packet_list = packets.split("\n\n")
    packet_in = f'in:{in_if.upper()}*'
    packet_info = 'ROUTER_ADVERTISEMENT'
    for packet in packet_list:
        if src_ip:
            if all(x in packet for x in (src_ip, dst_ip, packet_in, packet_info, status)) and 'DROPPED' not in packet:
                logger.info('found the RA packet')
                return True, packet
        else:
            if all(x in packet for x in (packet_in, dst_ip, packet_info, status)) and 'DROPPED' not in packet:
                logger.info('found the RA packet')
                return True, packet
    else:
        logger.error('not found RA packet')
    return False, ''


def get_interface_ipv6_addr(interface):
    if_status = iface_v6_api.get_interface_address(interface)
    v6_addr = ''
    try:
        ips = if_status['ip_address']
        if ips.startswith('fe80'):
            logger.error('get v6 address failed.')
        else:
            addr = ips.split(',')[0]
            for key in addr:
                if key == '/':
                    break
                else:
                    v6_addr += key
            logger.info(f'x1 ipv6 address is: {v6_addr}')
    except Exception as e:
        logger.error(repr(e))
    return v6_addr


def get_FW_inteface_mac(unit, interface):
    mac = ''
    if unit == fw:
        mac = iface_v4_api.get_interface_mac(interface)
    elif unit == rem_fw:
        mac = rm_ifacev4_api.get_interface_mac(interface)
    logger.info(f'=====get fw interface <{interface}> mac addr is: {mac.lower()}=======')
    return mac.lower()


def check_forwarded_mac(packets_info, src_ip, trs_src_ip, dst_ip):
    pc1_eth1_mac = get_pc_eth_mac(localhost, 'eth1')
    if not pc1_eth1_mac:
        return False
    x0_mac = get_FW_inteface_mac(fw, 'x0')
    x2_mac = get_FW_inteface_mac(fw, 'x2')
    if not x0_mac or not x2_mac:
        return False
    remx2_mac = get_FW_inteface_mac(rem_fw, 'x2')
    if not remx2_mac:
        return False
    packets = packets_info.split('*Packet number:')
    for packet in packets:
        if f'Src=[{src_ip}]' in packet and f'Dst=[{dst_ip}]' in packet:
            if f'Src=[{pc1_eth1_mac}]' in packet and f'Dst=[{x0_mac}]' in packet:
                logger.info('FW received packet from client.')
                logger.info(packet)
                break
    else:
        logger.error('check packet received from LAN failed')
        return False

    for packet in packets:
        if f'Src=[{trs_src_ip}]' in packet and f'Dst=[{dst_ip}]' in packet:
            if f'Src=[{x2_mac}]' in packet and f'Dst=[{remx2_mac}]' in packet:
                logger.info('FW forward packet from WAN.')
                logger.info(packet)
                return True
    else:
        logger.error('check forward packet from WAN failed')
        return False


def get_pc_eth_mac(pc_login, eth):
    cmd = "ifconfig " + eth + " | grep ether | awk '{print $2}'"
    output = pc_login.send_command(cmd)
    mac = output.strip()
    if len(mac) == 17:
        logger.info('=' * 10 + 'get mac address successfully' + '=' * 10)
        logger.info(f'pc1 {eth} mac address is: {mac}')
        return mac.lower()
    else:
        logger.info('=' * 10 + 'get mac adddress failed' + '=' * 10)
        return ''


def init_packet_capture():
    clear_res = pkt_api.clear_packets()
    logger.info(f'=> clear packet result: {clear_res}')
    start_res = pkt_api.start_capture()
    logger.info(f'=> start capture result: {start_res}')


def packets_process_for_RA(iface):
    time.sleep(30)
    packets = pkt_api.export_captured_packets()
    logger.info(packets)
    return packets


def packets_process_for_ping6(addr):
    init_packet_capture()
    logger.info('=> send traffic from LAN to WAN')
    localhost.ping6(addr, num=2)
    time.sleep(10)
    stop_res = pkt_api.stop_capture()
    logger.info(f'=> start capture result: {stop_res}')
    packets = pkt_api.export_captured_packets()
    return packets


def generate_temporary_ipv6_addr(iface):
    iface_mac = get_FW_inteface_mac(fw, iface)
    logger.info(iface_mac)
    ip_list = iface_mac.split(':')
    return "2000::" + ip_list[0]+ip_list[1]+":"+ip_list[2]+ip_list[3]+":"+ip_list[4]+ip_list[5]
