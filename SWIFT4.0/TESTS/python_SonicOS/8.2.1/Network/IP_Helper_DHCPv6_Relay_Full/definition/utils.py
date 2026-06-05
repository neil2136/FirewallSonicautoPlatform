from definition.settings import *


def check_specified_dhcpv6_packet(pkt_type, dhcpv6_type, pkt):
    if 'DHCPv6' in pkt:
        m = re.findall(r'Message type:.*', pkt)
        if len(m) == 2:
            logger.info(m)
            return pkt_type in m[0] and dhcpv6_type in m[1]
    logger.info('this is not a dhcpv6 packet')
    return False


