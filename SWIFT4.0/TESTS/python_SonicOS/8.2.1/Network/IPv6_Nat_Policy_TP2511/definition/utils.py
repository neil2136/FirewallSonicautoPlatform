from definition.settings import *


def check_pd_in_tsr(pd: str, tsr_info: str):
    m = re.search(r'(IA Prefixes:\s+)(\d.+/64)', tsr_info, re.M)
    if m:
        logger.info(f'get obtained Prefix in TSR file success.\n{m.groups(2)}')
        return pd in m.group(2)
    logger.error('get Prefix failed in tsr')
    return False


def get_IAID_info_in_tsr(tsr_info: str):
    m = re.search(r'Identity Association for Prefix Delegation:\s+(.*)Disable all IPv6 Traffic', tsr_info, re.S | re.M)
    if m:
        logger.info(f'get IAPD message success.\n{m.group(1)}')
        return m.group(1)
    logger.error('get IAID info failed.')
    return ''


def check_interface_v6_addr(interface: str, expect_ip: str):
    resp = if_v6_api.get_interface_address(interface)
    try:
        return expect_ip in resp.get('ip_address')
    except Exception as e:
        logger.error(repr(e))
        return False


def init_packet_capture():
    clear_res = pkt_api.clear_packets()
    logger.info(f'=> clear packet result: {clear_res}')
    start_res = pkt_api.start_capture()
    logger.info(f'=> start capture result: {start_res}')


def get_packet_seq(pkt):
    m = re.search(r'Frame\s+(\d+):', pkt, re.M | re.S)
    logger.info(f'this is the {m.group(1)} packet.')
    return m.group(1)


def get_dhcpv6_packet_type(pkt):
    # seq_num = get_packet_seq(pkt)
    # if not seq_num:
    #     return ''
    if 'DHCPv6' in pkt:
        m = re.search(r'Message type:.*', pkt)
        if m:
            msg_types = ['Solicit', 'Advertise', 'Request', 'Reply', 'Renew', 'Rebind', 'Release']
            for t in msg_types:
                if t in m.group():
                    logger.info(f'this is a {t} type dhcpv6 packet')
                    return t
        logger.info('this is not needed dhcpv6 packet!')
        return False
    logger.info('this packet is not dhcpv6 packet!!!')
    return ''


def get_transaction_id(pkt):
    if 'DHCPv6' in pkt:
        m = re.search(r'Transaction ID:\s+(.*)', pkt)
        if m:
            return m.group(1)
        logger.error('get transaction id in this packet failed.')
        return '0'
    logger.error('this packet is not dhcpv6 packet!!!')
    return '0'


def get_solicit_packet(pkts: list):
    for pkt in pkts:
        get_type = get_dhcpv6_packet_type(pkt)
        if get_type == 'Solicit':
            logger.info(f'found Solicit packet, the whole packet is:\n{pkt}')
            return pkt
    else:
        logger.error('get solicit packet failed.')
        return ''


def get_Client_Identifier_part_from_packet(pkt: str):
    m = re.search(r'Client Identifier\n(.*)Option Request', pkt, re.M | re.S)
    if m:
        logger.info('find Client Identifier part success')
        logger.info(m.group(1))
        return m.group(1)
    logger.error('find Client Identifier part failed')
    return ''


def get_Server_Identifier_part_from_packet(pkt):
    m = re.search(r'Server Identifier\s+(.*)(Option Request)$', pkt, re.M | re.S)
    if m:
        logger.info('get Server Identifier in request message success.')
        return m.group(1)
    logger.error('get Server Identifier in request message failed!!!')
    return False


def get_Elapsed_time_part_from_packet(pkt):
    m = re.search(r'Elapsed time\n.*Elapsed-time.*', pkt, re.M | re.S)
    if m:
        logger.info('find Elapsed-time part success')
        return m.group()
    logger.error('find Elapsed-time part failed')
    return ''


def get_packet_captured_time_from_packet(pkt):
    m = re.search(r'Time delta from previous displayed frame: ([\d\.]+) seconds', pkt, re.M)
    if m:
        logger.info(f'find packet captured time success.\n{m.group(1)}')
        return m.group(1)
    logger.error('find packet captured time failed!!')
    return ''


def get_iapd_part_from_packet(pkt):
    m = re.search(r'Identity Association for Prefix Delegation\n(.*)', pkt, re.M | re.S)
    if m:
        logger.info(f'get iapd info from packet success.\n{m.group(1)}')
        return m.group(1)
    logger.error('get IAPD info from pkt failed.')
    return ''
