from definition.settings import pkt_api, logger, if_v6_api, if_v6_cli, Parameter, pc1_login
import re
from time import sleep


def init_packet_capture():
    clear_res = pkt_api.clear_packets()
    logger.info(f'=> clear packet result: {clear_res}')
    start_res = pkt_api.start_capture()
    logger.info(f'=> start capture result: {start_res}')


def get_v6_addr(iface):
    for i in range(3):
        logger.info(f'run for {i + 1} time')
        resp = if_v6_api.get_interface_address(iface)
        v6_addr = resp.get('ip_address') if resp else ''
        if v6_addr:
            m = re.search(r'200[12]:1:2:4::\w+', v6_addr)
            if m:
                logger.info(f'{iface} get ipv6 addr is: {m.group()}')
                return m.group()
            if_v6_cli.click_dhcpv6_renew(iface)
            sleep(10)
        else:
            logger.error(f'get interface {iface} ipv6 json failed')
    return ''


def click_dhcp_release_renew(iface):
    r1 = if_v6_cli.click_dhcpv6_release(iface)
    sleep(3)
    logger.info(f'click interface {iface} relesae result: {r1}')
    r2 = if_v6_cli.click_dhcpv6_renew(iface)
    sleep(3)
    logger.info(f'click interface {iface} relesae result: {r2}')


def capture_packets_from_fw(iface='x1', renewd=True, init=True):
    if init:
        init_packet_capture()
    if renewd:
        if not iface:
            logger.error('param <iface> must be specified!')
            return ''
        click_dhcp_release_renew(iface)
    sleep(60)
    stop_res = pkt_api.stop_capture()
    logger.info(f'=> stop capture result: {stop_res}')
    pkt_api.export_captured_packets_pcapng('/tmp/packet-c.pcapng')
    pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng -V')
    pkt_list = pkts.split('\n\n')
    return pkt_list


def get_dhcpv6_packet_type(pkt):
    if 'DHCPv6' in pkt:
        m = re.search(r'Message type:.*', pkt)
        if m:
            msg_types = ['Solicit', 'Advertise', 'Request', 'Reply', 'Renew', 'Rebind', 'Release']
            for t in msg_types:
                if t in m.group():
                    logger.info(f'this is a {t} type dhcpv6 packet')
                    return t
        logger.info('this is not needed dhcpv6 packet!')
        return ''
    logger.info('this packet is not dhcpv6 packet!!!')
    return ''
