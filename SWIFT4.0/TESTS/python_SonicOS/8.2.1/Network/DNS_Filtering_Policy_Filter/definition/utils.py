from definition.settings import Parameter, PC1_LOGIN, packet_api
from runner.settings import logger
import re
import time
import urllib3
urllib3.disable_warnings()


def config_packet_monitor():
    rc1 = packet_api.stop_capture()
    logger.info(f'Stop Capture Packet......{rc1}')
    rc2 = packet_api.clear_packets()
    logger.info(f'Clear Capture Packet for 1 time......{rc2}')
    rc3 = packet_api.clear_packets()
    logger.info(f'Clear Capture Packet for 2 time......{rc3}')
    return rc1 & rc2 & rc3


def do_dig_verify_DNS_query(domain: str, server=Parameter.FIREWALL, host=PC1_LOGIN, opt='', block=False):
    error_1 = 'no servers could be reached'
    error_2 = 'connection timed out'
    error_3 = 'REFUSED'
    out = ''
    if domain:
        logger.info(f'Dig {domain} to verify dns query')
        diag_command = 'dig ' + domain + ' @' + server + ' ' + opt
        for i in range(3):
            time.sleep(3)
            host.send_command(f'ping {Parameter.Neustar_server} -c 5')
            logger.info(f'Query dns for {i+1} times...')
            out = host.send_command(diag_command)
            time.sleep(2)
            rc = re.search(f'{error_1}|{error_2}|{error_3}', str(out))
            if not block and not rc:
                return True, out
            if block and rc:
                return True, out
    else:
        logger.error('Domain cannot be NULL!!')
    return False, out

def check_DNS_reply_from_Server(ifc='X0', server=Parameter.Neustar_server):
    ifc = ifc.upper()
    foundit = False
    res1 = packet_api.stop_capture()
    logger.info(f'Stop Capture Packet......\n{res1}')
    res2 = packet_api.export_captured_packets(format='text')
    logger.info(f'Export capture......\n{res2}')
    match = re.search(r'Packet\snumber:.*?in:X1.*?out:' + ifc + r'.*?Src=\[' + server +
                      '\].*?Dst=\[' + Parameter.X1_IP + '\].*?Packet\snumber', res2, re.I | re.S)
    if match:
        foundit = True
    else:
        logger.error(f'Failed to match echo_request X1-{ifc} packet from {server}')
    return foundit
