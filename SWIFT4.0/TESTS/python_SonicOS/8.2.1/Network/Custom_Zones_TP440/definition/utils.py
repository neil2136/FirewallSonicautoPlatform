from runner.settings import Params, logger


def check_custom_zones(base_dict, source_dict):
    output = True
    try:
        for key, value in base_dict.items():
            if source_dict['zones'][0][key] == value:
                logger.info(f'set general settings {key} to {value} success')
            else:
                output = False
                logger.error(f'set general settings {key} to {value} fail')
    except BaseException as f:
        logger.error(f)
    return output


def icmp_drop_check(resp, src_ip, dst_ip):
    packets = resp.split('Packet number: ')
    icmptype = 'ICMP Type = 8'
    srcip = f"Src=[{src_ip}]"
    dstip = f"Dst=[{dst_ip}]"
    for packet in packets:
        if icmptype in packet:
            if srcip in packet and dstip in packet:
                if 'Packet dropped' in packet:
                    return True, packet
    return False, False
