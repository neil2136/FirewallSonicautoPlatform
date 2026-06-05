from definition.settings import *


def start_packet_monitor(ip_type):
    rc = Lpacket_obj.stop_capture()
    time.sleep(3)
    rc &= Lpacket_obj.clear_packets()
    time.sleep(3)
    pak_filter = {
        'monitor_filter': {
            'ip_types': ip_type,
        }
    }
    rc &= Lpacket_obj.conf_packmon(**pak_filter)
    time.sleep(3)
    rc &= Lpacket_obj.start_capture()
    return rc


def check_captured_monitor(spe_ip):
    Lpacket_obj.stop_capture()
    resp = Lpacket_obj.export_captured_packets()
    logger.info(resp)
    match1 = re.search('ICMP.*Src=\[12.12.1.200\], Dst=\[{}\]'.format(spe_ip), str(resp), re.I|re.M)
    match2 = re.search('VPN policy: vpn1', str(resp), re.I|re.M)
    if match1 or match2:
        rc = True
    else:
        rc = False
        logger.info(resp)
    return rc
