import os
import urllib3
import re
from runner.settings import logger
import time
import sys
import urllib3
urllib3.disable_warnings()
from definition.settings import *


def config_packet_monitor():
    result = list()
    found = 0
    result.append(packet_obj.stop_capture())
    time.sleep(3)
    result.append(packet_obj.clear_packets())
    time.sleep(3)
    result.append(packet_obj.clear_packets())
    time.sleep(3)
    for i in result:
        if i == True:
            found += 1
    
    return found

def do_dig_verify_DNS_query(domain):
    rc = None
    logger.info('Clear logs....')
    log_monitor.clear_log()
    logger.info('Dig ' + domain + ' to verify dns query')
    diag_command = 'dig ' + domain +' @'+ Parameter.FIREWALL
    logger.info(diag_command)
    for i in range(15):
        time.sleep(3)
        rc = os.popen(diag_command).read()
        logger.info(rc)

    return rc

def check_DNS_reply_from_Neustar():
    foundit = 0
    packet_obj.stop_capture()
    logger.info('Export capture...')
    ret = packet_obj.export_captured_packets(format='text')
    logger.info(ret)
    Neustar_server = '156.154.54.200'
    match1 = re.search(r'Packet\snumber:.*?in:X1.*?out:X0.*?Src=\[' + Neustar_server +'\].*?Dst=\[' + Parameter.X1_IP + '\].*?Packet\snumber', ret, re.I|re.S) 
    if match1:
        foundit += 1
    else:
        logger.error('Failed to match echo_request X1-X0 packet')

    return foundit