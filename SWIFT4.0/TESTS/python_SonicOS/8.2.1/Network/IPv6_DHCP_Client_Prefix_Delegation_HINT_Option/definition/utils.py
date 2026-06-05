from definition.settings import *


def init_packet_capture():
    clear_res = pkt_mon_api.clear_packets()
    logger.info(f'=> clear packet result: {clear_res}')
    start_res = pkt_mon_api.start_capture()
    logger.info(f'=> start capture result: {start_res}')


def check_interface_v6_addr(iface, expect_ip):
    resp = if_v6_api.get_interface_address(iface)
    try:
        return expect_ip in resp.get('ip_address')
    except Exception as e:
        logger.error(repr(e))
        return False


def get_iapd_part_from_packet(pkt):
    m = re.search(r'Identity Association for Prefix Delegation\n(.*)', pkt, re.M | re.S)
    if m:
        logger.info(f'get iapd info from packet success.\n{m.group(1)}')
        return m.group(1)
    logger.error('get IAPD info from pkt failed.')
    return ''


def get_dhcpv6_packet_type(pkt):
    if 'DHCPv6' in pkt:
        m = re.search(r'Message type:.*', pkt)
        if m:
            msg_types = ['Solicit', 'Advertise', 'Request', 'Reply', 'Renew', 'Rebind', 'Release']
            for t in msg_types:
                if t in m.group():
                    logger.info(f'this is a {t} type dhcpv6 packet')
                    return t
        logger.error('this is not needed dhcpv6 packet!')
        return False
    logger.error('this packet is not dhcpv6 packet!!!')
    return ''
