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
    for i in range(5):
        time.sleep(3)
        rc = os.popen(diag_command).read()

    return rc

def do_dig_verify_DNS_query_block(domain):
    rc = None
    logger.info('Clear logs....')
    log_monitor.clear_log()
    logger.info('Dig ' + domain + ' to verify dns query')
    diag_command = 'dig ' + domain +' @'+ Parameter.FIREWALL
    logger.info(diag_command)
    for i in range(5):
        time.sleep(5)
        rc = os.popen(diag_command).read()

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

def check_related_logs(domain):
    flag_log = False
    rc = log_monitor.export_log_txt(log_switch=False)
    logger.info(rc)
    start = "DNS Packet AllowedStandard Message String"
    end ='DNS Packet Allowed'
    match1 = re.search(r'' + start + '(.*?)' + end + '', rc, re.I|re.S)
    if match1:
        output1 = match1.group(0)
        logger.info(output1)
        match2 = re.search(domain, output1, re.I|re.S)
        if match2:
            flag_log = True
        else:
            logger.error('No related logs.')
    else:
        logger.error('Related logs were not included.')
        
    return flag_log

def check_related_logs_block(domain):
    flag_log = False
    rc = log_monitor.export_log_txt(log_switch=False)
    logger.info(rc)
    start = "DNS Packet DroppedStandard Message String"
    end ='DNS Packet Blocked'
    match1 = re.search(r'' + start + '(.*?)' + end + '', rc, re.I|re.S)
    if match1:
        output1 = match1.group(0)
        logger.info(output1)
        match2 = re.search(domain, output1, re.I|re.S)
        if match2:
            flag_log = True
        else:
            logger.error('No related logs.')
    else:
        logger.error('Related logs were not included.')
        
    return flag_log

def check_related_logs_reply(domain):
    flag_log = False
    rc = log_monitor.export_log_txt(log_switch=False)
    logger.info(rc)
    start = "DNS Packet DroppedStandard Message String"
    end ='DNS Packet Negatively Replied'
    match1 = re.search(r'' + start + '(.*?)' + end + '', rc, re.I|re.S)
    if match1:
        output1 = match1.group(0)
        logger.info(output1)
        match2 = re.search(domain, output1, re.I|re.S)
        if match2:
            flag_log = True
        else:
            logger.error('No related logs.')
    else:
        logger.error('Related logs were not included.')
        
    return flag_log

def check_DNS_reply_flag():
    flag_log = False
    cmd = 'rm -rf /tmp/packet-c.pcapng'
    os.system(cmd)
    packet_obj.stop_capture()
    time.sleep(2)
    logger.info('Export capture...')
    packet_obj.export_captured_packets_pcapng()
    cmd = "tshark -R 'dns.flags.rcode == 2' -r /tmp/packet-c.pcapng -V -T text"
    logger.info(cmd)
    rc = os.popen(cmd).read()
    logger.info(rc)
    start = '0010 = Reply code: Server failure'
    match1 = re.search(start, rc, re.S|re.DOTALL)
    if match1:
        flag_log = True
    else:
        logger.error('Related dns response were not included.')
        
    return flag_log

def check_DNS_reply_the_answer_address(domain):
    flag = False
    logger.info('Clear logs....')
    log_monitor.clear_log()
    logger.info('config packet monitor...')
    packet_obj.stop_capture()
    packet_obj.clear_packets()
    packet_obj.start_capture()
    logger.info('Dig ' + domain + ' to verify dns query')
    diag_command = 'dig a ' + domain +' @'+ Parameter.FIREWALL
    logger.info(diag_command)
    rc = os.popen(diag_command).read()
    logger.info(rc)
    fored_ip_v4 = '127.0.0.2'
    if fored_ip_v4 in rc:
        flag = True
    else:
        logger.error('the answer address in DNS Reply is wrong')

    return flag

def check_related_logs_fored_ip(domain):
    flag_log = False
    rc = log_monitor.export_log_txt(log_switch=False)
    logger.info(rc)
    start = "DNS Packet DroppedStandard Message String"
    end ='DNS Filtering - DNS Packet IP Forged'
    match1 = re.search(r'' + start + '(.*?)' + end + '', rc, re.I|re.S)
    if match1:
        output1 = match1.group(0)
        logger.info(output1)
        match2 = re.search(domain, output1, re.I|re.S)
        if match2:
            flag_log = True
        else:
            logger.error('No related logs.')
    else:
        logger.error('Related logs were not included.')
        
    return flag_log

def check_DNS_reply_the_answer_address_v6(domain):
    flag = False
    logger.info('Clear logs....')
    log_monitor.clear_log()
    logger.info('config packet monitor...')
    packet_obj.stop_capture()
    packet_obj.clear_packets()
    packet_obj.start_capture()
    logger.info('Dig ' + domain + ' to verify dns query')
    diag_command = 'dig aaaa ' + domain +' @'+ Parameter.FIREWALL
    logger.info(diag_command)
    fored_ip_v6 = '1001::2'
    for _ in range(5):
        rc = os.popen(diag_command).read()
        logger.info(rc)
        if fored_ip_v6 in rc:
            flag = True
            break
        time.sleep(2)
    else:
        logger.error('the answer address in DNS Reply is wrong')

    return flag
