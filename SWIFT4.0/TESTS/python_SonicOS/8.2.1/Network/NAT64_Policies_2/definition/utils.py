from definition.settings import pkt_api, logger, script_file, pc3_login, pc1_login, pc2_login, PC1_ETH1_V6, Parameter, \
    PC2_ETH1_IP
import re
from time import sleep


def init_packet_capture():
    cls_res = pkt_api.clear_packets()
    logger.info(f'clear packet result: {cls_res}')
    start_res = pkt_api.start_capture()
    logger.info(f'start packet capture result: {start_res}')


def get_IP_Header_part_from_icmp_packet(packet: str):
    m = re.search(r'(Internet Protocol Version.*)Internet Control Message Protocol', packet, re.M | re.S)
    return m.group() if m else ''


def get_icmp_packt_from_packet(packets, target=''):
    check_dict = {
        'icmp_request': ('ICMP', 'Src: 12.12.1.168', 'Dst: 12.12.1.169', 'Type: 8 (Echo (ping) request)'),
        'icmp_reply': ('ICMP', 'Src: 12.12.1.168', 'Dst: 12.12.1.169', 'Type: 8 (Echo (ping) request)'),
        'icmpv6_request': ('ICMPv6', 'Src: 2000::169', 'Dst: 64:ff9b::c0c:1a9', 'Type: Echo (ping) request'),
        'icmpv6_reply': ('ICMPv6', 'Src: 64:ff9b::c0c:1a9', 'Dst: 2000::169', 'Type: Echo (ping) reply')
    }
    if not packets:
        logger.error('\033[1;31mnot capture any packet on firewall!!\033[0m')
        return ''
    if target not in check_dict:
        logger.error("\033[1;31mplease specify correct packet type\033[0m")

    pkt_list = packets.split('\n\n')
    for packet in pkt_list:
        # if ver == 'v4':
        #     if pkt_type == 'request':
        #         if all(x in packet for x in
        #                ('ICMP', 'Src: 12.12.1.168', 'Dst: 12.12.1.169', 'Type: 8 (Echo (ping) request)')):
        #             logger.info(f'icmp packet details:\n{packet}')
        #             return packet
        #     else:
        #         if all(x in packet for x in
        #                ('ICMP', 'Src: 12.12.1.168', 'Dst: 12.12.1.169', 'Type: 8 (Echo (ping) request)')):
        #             logger.info(f'icmp packet details:\n{packet}')
        #             return packet
        # else:
        #     if pkt_type == 'request':
        #         if all(x in packet for x in
        #                ('ICMPv6', 'Src: 2000::169', 'Dst: 64:ff9b::c0c:1a9', 'Type: Echo (ping) request')):
        #             logger.info(f'icmpv6 packet details:\n{packet}')
        #             return packet
        #     else:
        #         if all(x in packet for x in
        #                ('ICMPv6', 'Src: 64:ff9b::c0c:1a9', 'Dst: 2000::169', 'Type: Echo (ping) reply')):
        #             logger.info(f'icmpv6 packet details:\n{packet}')
        #             return packet
        if all(x in packet for x in check_dict.get(target)):
            logger.info(f'find {target} packet successfully, details:\n{packet}')
            return packet
    logger.error('\033[1;31mnot found icmp packet!!\033[0m')
    return False


def check_ip_header_from_packet(version='6_to_4'):
    if version not in ('6_to_4', '4_to_6'):
        logger.error('please specify correct value for param verison')
        return False
    pkt_api.export_captured_packets_pcapng()
    pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng -V')
    if version == '6_to_4':
        icmpv6_pkt = get_icmp_packt_from_packet(pkts, target='icmpv6_request')
        icmp_pkt = get_icmp_packt_from_packet(pkts, target='icmp_request')
    else:
        icmpv6_pkt = get_icmp_packt_from_packet(pkts, target='icmpv6_reply')
        icmp_pkt = get_icmp_packt_from_packet(pkts, target='icmp_reply')
    icmpv6_ip_header = get_IP_Header_part_from_icmp_packet(icmpv6_pkt)
    icmp_ip_header = get_IP_Header_part_from_icmp_packet(icmp_pkt)

    logger.info('check payload length update...')
    try:
        len_icmpv6 = re.search(r'Payload length: (\d+)', icmpv6_ip_header, re.M).group(1)
        logger.info(f'icmpv6 payload length: {len_icmpv6}')
        len_icmp = re.search(r'Total Length: (\d+)', icmp_ip_header, re.M).group(1)
        logger.info(f'icmp payload length: {len_icmp}')
        res1 = int(len_icmpv6) + 20 == int(len_icmp)
        if not res1:
            logger.error(f'\033[1;31mpayload length updated failed\033[0m')
            return False
        logger.info(f'\033[1;31mcheck payload length result: {res1}\033[0m')
    except Exception as e:
        logger.error(f'\033[1;31m{repr(e)}\033[0m')
        return False

    if version == '6_to_4':
        check_dict = {
            'Version: 6': 'Version: 4',
            'Hop limit': 'Time to live',
            'Next header': 'Protocol',
            f'Src: {PC1_ETH1_V6}': f'Src: {Parameter.X1_IP}',
            f'Dst: {Parameter.X1_NAT64_IP}': f'Dst: {PC2_ETH1_IP}'
        }
    else:
        check_dict = {
            'Version: 6': 'Version: 4',
            'Hop limit': 'Time to live',
            'Next header': 'Protocol',
            f'Src: {Parameter.X1_NAT64_IP}': f'Src: {Parameter.X1_IP}',
            f'Dst: {PC1_ETH1_V6}': f'Destination: {PC2_ETH1_IP}'
        }
    logger.info('check other details...')
    for x, y in check_dict.items():
        if x not in icmpv6_ip_header or y not in icmp_ip_header:
            if version == '6_to_4':
                logger.error(f'\033[1;31mcheck {x} update to {y} failed!\033[0m')
            else:
                logger.error(f'\033[1;31mcheck {y} update to {x} failed!\033[0m')
            return False
    return True


def check_packet(traffic_type, fragment=True):
    if traffic_type not in ('udp', 'tcp', 'ftp', 'icmpv6_f', 'tcp_f', 'udp_f', 'icmpv6_from_wan'):
        logger.error(
            '\033[1;31mplease specify the traffic_type as udp, tcp, ftp, icmpv6_f, tcp_f, udp_f, icmpv6_from_wan!\033[0m')
        return False
    pkt_api.monitor_default()
    init_packet_capture()
    if traffic_type == 'ftp':
        pc1_login.send_command(f'ftp 64:ff9b::c0c:1a9 &')
    elif traffic_type == 'icmpv6_from_wan':
        pc2_login.send_command(f'python3 {script_file} {traffic_type}')
    else:
        pc3_login.send_command(f'python3 {script_file} {traffic_type}')
    sleep(10)
    stop_res = pkt_api.stop_capture()
    logger.info(f'\033[1;31mstop capture result: {stop_res}.\033[0m')
    pkt_api.export_captured_packets_pcapng(f'/tmp/packet-{traffic_type}-fragment.pcapng')
    pkts = pc1_login.send_command(f'tshark -r /tmp/packet-{traffic_type}-fragment.pcapng -V')
    non_fragment_check_dict = {
        'udp': ('Src: 12.12.1.168', 'Dst: 12.12.1.169 ', 'Dst Port: italk (12345)'),
        'tcp': ('Src: 12.12.1.168', 'Dst: 12.12.1.169 ', 'Dst Port: ezmeeting-2 (10101)'),
        'ftp': ('Src: 12.12.1.168', 'Dst: 12.12.1.169 ', 'Dst Port: ftp (21)')
    }
    fragment_check_dict = {
        'icmpv6_f': {'src_check': ('Src: 2002::169', 'Dst: 64:ff9b::c0c:1a9', 'Next header: IPv6 fragment'),
                     'dst_check': ('Src: 12.12.1.168', 'Dst: 12.12.1.169', 'Fragment offset', 'Protocol: ICMP')},
        'udp_f': {'src_check': (
            'Src: 2002::169', 'Dst: 64:ff9b::c0c:1a9', 'Next header: IPv6 fragment', 'Dst Port: 22222'),
            'dst_check': ('Src: 12.12.1.168', 'Dst: 12.12.1.169', 'Dst Port: 22222')},
        'tcp_f': {'src_check': (
            'Src: 2002::169', 'Dst: 64:ff9b::c0c:1a9', 'Next header: IPv6 fragment',
            'Dst Port: ezmeeting-2 (10101)'),
            'dst_check': ('Src: 12.12.1.168', 'Dst: 12.12.1.169', 'Dst Port: ezmeeting-2 (10101)')},
        'icmpv6_from_wan': ('Src: 2001::169', 'Dst: 64:9999::c0c:1a9', 'Fragmentation Header')
    }
    if pkts:
        pkt_list = pkts.split('\n\n')
        if not fragment:
            for pkt in pkt_list:
                if all(x in pkt for x in non_fragment_check_dict.get(traffic_type)):
                    logger.info(f'find the nat64 pkt:\n{pkt}')
                    return True
            else:
                logger.error('\033[1;31mnot found the nat64 pkt!\033[0m')
                return False

        if traffic_type == 'icmpv6_from_wan':
            for pkt in pkt_list:
                if all(x in pkt for x in fragment_check_dict.get(traffic_type)):
                    logger.info('after translated into ipv6 packet, find ipv6 fragment header successfully!')
                    return True
            else:
                logger.info('\033[1;31mnot find ipv6 fragment header after translated!\033[0m')
                return False

        for pkt in pkt_list:
            if all(x in pkt for x in fragment_check_dict.get(traffic_type).get('src_check')):
                logger.info(f'find the source ipv6 fragment packet.\n {pkt}')
                res1 = True
                if res1:
                    break
        else:
            logger.error('\033[1;31mnot find the source ipv6 fragment packet!\033[0m')
            return False

        for pkt in pkt_list:
            if all(x in pkt for x in fragment_check_dict.get(traffic_type).get('dst_check')):
                logger.info(f'find the translated ipv4 fragment packet.\n{pkt}')
                res2 = True
                if res2:
                    break
        else:
            logger.error('\033[1;31mnot find the translated ipv4 fragment packet!\033[0m')
            return False
        return res1 & res2
    logger.error('\033[1;31mnot capture any packtes!!\033[0m')
    return False
