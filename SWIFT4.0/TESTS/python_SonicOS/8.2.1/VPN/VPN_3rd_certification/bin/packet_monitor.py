from definition.settings import *


def start_packet_monitor():
    rc = Lpacket_obj.stop_capture()
    time.sleep(3)
    rc &= Lpacket_obj.clear_packets()
    time.sleep(3)
    pc_info = {
        'monitor_filter': {
            'ip_types': 'ICMP',
            # 'source_ips': PC1_eth0,
            # 'source_ports': PC2_eth0,
            'status': {
                'consumed': False,
                'dropped': False,
                'forwarded': True
            }

        }
    }
    rc &= Lpacket_obj.conf_packmon(**pc_info)
    time.sleep(3)
    rc &= Lpacket_obj.start_capture()
    return rc


def check_captured_monitor():
    Lpacket_obj.stop_capture()
    resp = Lpacket_obj.export_captured_packets()
    logger.info(resp)
    match = re.search(r'VPN policy: vpn1', str(resp), re.I|re.M)
    if match:
        rc = True
    else:
        rc = False
    return rc