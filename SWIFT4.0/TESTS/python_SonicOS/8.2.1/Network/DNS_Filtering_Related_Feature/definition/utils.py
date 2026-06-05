from definition.settings import Parameter, PC1_LOGIN, packet_api, time, re
from runner.settings import logger


def initial_packet_monitor():
    rc_stop = packet_api.stop_capture()
    logger.info(f'Stop Capture Packet......{rc_stop}')
    rc_clear1 = packet_api.clear_packets()
    logger.info(f'Clear Capture Packet for 1 time......{rc_clear1}')
    rc_clear2 = packet_api.clear_packets()
    logger.info(f'Clear Capture Packet for 2 time......{rc_clear2}')
    return rc_stop & rc_clear1 & rc_clear2


def do_DNS_query_from_client(domain: str):
    if not domain:
        logger.error('Domain cannot be NULL!!')
        return ''
    cmd = f'dig {domain} @{Parameter.FIREWALL}'
    logger.info(f'start send DIG cmd: {cmd}')
    return PC1_LOGIN.send_command(cmd)


def check_dns_query_no_error(domain: str):
    packet_api.start_capture()
    error_1 = 'no servers could be reached'
    error_2 = 'connection timed out'
    for i in range(3):
        logger.info(f'Query dns for {i+1} times...')
        time.sleep(3)
        output = do_DNS_query_from_client(domain)
        time.sleep(2)
        rc = not re.search(f'{error_1}|{error_2}', str(output))
        if rc:
            return True
    logger.error('Failed to get valid dns reply!')
    return False


def check_dns_packets_in_wireshark(tCmd: str, target: tuple or str):
    res1 = packet_api.stop_capture()
    logger.info(f'Stop Capture Packet...... {res1}')
    res2 = packet_api.export_captured_packets_pcapng()
    logger.info(f'Export capture...... {res2}')
    cmd = f'tshark -R "{tCmd}" -r /tmp/packet-c.pcapng -V -T text'
    tsRes = PC1_LOGIN.send_command(cmd)
    if isinstance(target, tuple):
        found = [x in tsRes for x in target]
        rc = all(found)
    else:
        rc = target in tsRes
    logger.info(f'check packet result...... {rc}')
    return rc
