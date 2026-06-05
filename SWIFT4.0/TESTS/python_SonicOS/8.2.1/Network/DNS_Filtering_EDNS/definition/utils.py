from definition.settings import Parameter, PC1_LOGIN, packet_api, dnspxy_api, time, re
from runner.settings import logger


def initial_packet_monitor_and_flush_dns_cache():
    rc1 = packet_api.stop_capture()
    logger.info(f'Stop Capture Packet......{rc1}')
    rc2 = packet_api.clear_packets()
    logger.info(f'Clear Capture Packet for 1 time......{rc2}')
    rc3 = packet_api.clear_packets()
    logger.info(f'Clear Capture Packet for 2 time......{rc3}')
    flush_rc = dnspxy_api.flush_caches('ipv4')
    logger.info(f'Flush dns proxy caches......{flush_rc}')
    return rc1 & rc2 & rc3 & flush_rc


def do_DNS_query_from_client(domain: str, opt='dig'):
    if not domain:
        logger.error('Domain cannot be NULL!!')
        return ''
    if opt == 'nslookup':
        cmd = f'nslookup {domain} {Parameter.FIREWALL}'
        logger.info(f'start send NSLOOKUP cmd: {cmd}')
    else:
        cmd = f'dig {domain} @{Parameter.FIREWALL}'
        logger.info(f'start send DIG cmd: {cmd}')
    return PC1_LOGIN.send_command(cmd)


def check_dns_query_no_error(domain: str, opt='dig'):
    packet_api.start_capture()
    error_1 = 'no servers could be reached'
    error_2 = 'connection timed out'
    error_3 = 'REFUSED'
    for i in range(3):
        logger.info(f'Run for {i} times...')
        time.sleep(3)
        PC1_LOGIN.send_command(f'ping {Parameter.Neustar_server} -c 5')
        output = do_DNS_query_from_client(domain, opt)
        time.sleep(2)
        rc = not re.search(f'{error_1}|{error_2}|{error_3}', str(output), re.I)
        if rc:
            break
    else:
        logger.error('Failed to get valid dns reply!')
    return rc, output


def check_dns_packets_in_wireshark(tCmd: str, ekey: tuple or str):
    res1 = packet_api.stop_capture()
    logger.info(f'Stop Capture Packet......\n{res1}')
    res2 = packet_api.export_captured_packets_pcapng()
    logger.info(f'Export capture......\n{res2}')
    cmd = f'tshark -R "{tCmd}" -r /tmp/packet-c.pcapng -V -T text'
    tsRes = PC1_LOGIN.send_command(cmd)
    if isinstance(ekey, tuple):
        foundit = [x in tsRes for x in ekey]
        rc = all(foundit)
    else:
        rc = ekey in tsRes
    logger.info(f'check packet result: {rc}')
    return rc
