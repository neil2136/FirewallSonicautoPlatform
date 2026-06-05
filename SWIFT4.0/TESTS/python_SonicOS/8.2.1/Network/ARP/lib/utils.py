from parameter import * 


def log_testplan(case_id):
    description = show_testcase_info(Parameter.TESTPLAN, 
                                     case_id, description=True)['title']
    testplan = show_testcase_info(Parameter.TESTPLAN, case_id, description=True)
    logger.info(testplan)
    logger.info('*' * 8 + ' title ' + '*' * 8)
    logger.info(testplan['title'])
    logger.info('*' * 8 + ' steps ' + '*' * 8)
    for item in testplan['steps'].split('&'):
        logger.info(item)
    logger.info('*' * 8 + ' result ' + '*' * 8)
    for item in testplan['result'].split('&'):
        logger.info(item)

def get_pc2_mac(iface):
    rc = PC2.send_command(f"ifconfig {iface}")
    iface_mac = re.search("\S{2}:\S{2}:\S{2}:\S{2}:\S{2}:\S{2}", rc).group(0)
    return iface_mac.lower()

def change_pc2_ip(iface, ip):
    rc = PC2.send_command(f"ifconfig {iface} {ip}")
    return rc

def get_pc1_mac(iface):
    rc = os.popen(f"ifconfig {iface}")
    iface_mac = re.search("\S{2}:\S{2}:\S{2}:\S{2}:\S{2}:\S{2}", 
                          rc.read()).group(0)
    return iface_mac.lower()

def sr_ARP(iface):
    conf.iface = iface
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp = ARP(pdst=ip)
    packet = ether/arp
    an, un = srploop(packet, count=3)
    if an:
        logger.info(an.summary())
        return True
    else:
        return False

def get_icmp_reply(iface):
    try:
        packet = sniff(filter=f"icmp and dst host {Parameter.DMZ_HOST}",
                       iface=iface,
                       count=1)
    except Exception:
        logger.info('cannot capture reply packet')
    dst_mac = packet[0].getfield_and_val('dst')[1]
    return dst_mac

def verify_icmp_reply(dst_ip, dst_mac):
    dst_mac = dst_mac.lower()
    packetmonitor = PacketmonitorApi(fw)
    packetmonitor.start_capture()
    packetmonitor.clear_packets()
    pc2_ping(1)
    packetmonitor.stop_capture()
    resp = packetmonitor.export_captured_packets()
    packets = resp.split('Packet number: ')
    for packet in packets:
        logger.info(dst_mac)
        logger.info(dst_ip)
        if f'Dst=[{dst_mac}]' in packet:
            if f'Dst=[{dst_ip}]' in packet:
                if 'ECHO_REPLY' in packet:
                    return True
    else:
        return False


if __name__ == '__main__':
    logger.info(Parameter.DMZ_HOST)
    logger.info(get_pc2_mac('eth0'))
#    packet = verify_icmp_reply('172.17.1.101', '11:22:33:44:55:66')
#    logger.info('*'* 10)
#    if packet:
#        logger.info(packet)

