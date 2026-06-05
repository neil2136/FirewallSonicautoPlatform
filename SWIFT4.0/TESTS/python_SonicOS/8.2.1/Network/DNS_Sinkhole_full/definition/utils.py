from definition.settings import PC2_LOGIN, logMonitor_api, time, re, logger, packet_api


def do_DNS_query_from_client(domain: str, opt):
    if not domain:
        logger.error('Domain cannot be NULL!!')
        return ''
    cmd = f'dig {domain} {opt}'
    logger.info(f'start send DIG cmd: {cmd}')
    return PC2_LOGIN.send_command(cmd)


def check_dns_query_result(domain: str, block=False, opt=''):
    error_1 = 'no servers could be reached'
    error_2 = 'connection timed out'
    for i in range(3):
        logger.info(f'Query dns for {i+1} times...')
        time.sleep(3)
        output = do_DNS_query_from_client(domain, opt)
        time.sleep(1)
        rc = re.search(f'{error_1}|{error_2}', str(output))
        if not block and not rc:
            logger.info('The query is successful.')
            return True, output
        if block and rc:
            logger.info('The query is blocked.')
            return True, output
    logger.error('Failed to get correct dns reply!')
    return False, output


def check_related_logs(target: tuple):
    res = logMonitor_api.export_log_txt(log_switch=False)
    logger.info(res)
    found = [x in res for x in target]
    rc = all(found)
    logger.info(f'Check logs result...... {rc}')
    return rc


def initial_packet_monitor():
    rc1 = packet_api.stop_capture()
    logger.info(f'Stop Capture Packet......{rc1}')
    rc2 = packet_api.clear_packets()
    logger.info(f'Clear Capture Packet for 1 time......{rc2}')
    rc3 = packet_api.clear_packets()
    logger.info(f'Clear Capture Packet for 2 time......{rc3}')
    return rc1 & rc2 & rc3


def check_dns_packets_in_wireshark(tCmd: str, ekey: tuple or str):
    res1 = packet_api.stop_capture()
    logger.info(f'Stop Capture Packet......\n{res1}')
    res2 = packet_api.export_captured_packets_pcapng()
    logger.info(f'Export capture......\n{res2}')
    cmd = f'tshark -R "{tCmd}" -r /tmp/packet-c.pcapng -V -T text'
    tsRes = PC2_LOGIN.send_command(cmd)
    if isinstance(ekey, tuple):
        found = [x in tsRes for x in ekey]
        rc = all(found)
    else:
        rc = ekey in tsRes
    logger.info(f'Check packet result: {rc}')
    return rc

def check_dns_packets_not_in_wireshark(tCmd: str, ekey: tuple or str):
    res1 = packet_api.stop_capture()
    logger.info(f'Stop Capture Packet...... {res1}')
    res2 = packet_api.export_captured_packets_pcapng()
    logger.info(f'Export capture...... {res2}')
    cmd = f'tshark -R "{tCmd}" -r /tmp/packet-c.pcapng -V -T text'
    tsRes = PC2_LOGIN.send_command(cmd)
    if isinstance(ekey, tuple):
        found = [x not in tsRes for x in ekey]
        rc = all(found)
    else:
        rc = ekey not in tsRes
    logger.info(f'Check key not in packet result: {rc}')
    return rc
