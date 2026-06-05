from settings import *
import copy
import os
import re
import time

def check_result(check_list, output, mode=None):
    ret = False
    rc = []
    try:
        if check_list:
            for i, check_str in enumerate(check_list):
                original_pattern = check_str
                if mode and mode.lower() == 'snmp':
                    if not check_str.startswith("5609"):
                        check_str = r"5609.*?Configuration succeeded.*?" + check_str
                elif mode and mode.lower() == 'syslog':
                    if not check_str.lstrip().startswith("m=1382"):
                        check_str = (r'm=1382.*?msg="Configuration succeeded:.*?'+ check_str +r'.*?"')

                if re.search(check_str, output, re.M | re.S):
                    rc.append(1)
                    logger.info(f'✅ Pattern {i+1} matched: {original_pattern}')
                else:
                    rc.append(0)
                    logger.info(f'❌ Pattern {i+1} failed: {original_pattern}')
                    logger.info(f'   Full pattern used: {check_str}')
                    
            ret = all(rc)
            logger.info(f'Overall result: {ret} ({sum(rc)}/{len(rc)} patterns matched)')
    except Exception as e:
        logger.error(f'Error when execute function check_result: {repr(e)}')
    return ret


def verify_result(mode, checklist=None):
    rc = False
    if mode == 'syslog':
        time.sleep(3)
        with os.popen('cat /var/log/messages', 'r') as file:
            syslog = file.read()
        logger.info(syslog)
        rc = check_result(checklist, output=syslog, mode='syslog')
    elif mode == 'snmp':
        output = PC2_login.send_command(
            'cat /var/log/messages | grep snmptrapd')
        logger.info(output)
        rc = check_result(checklist, output=output, mode='snmp')
    elif mode == 'audit':
        output = audit_log_api.export_audit_log_txt()
        logger.info(output)
        rc = check_result(checklist, output=output)
    elif mode == 'log':
        output = log_api.export_log_txt()
        logger.info('output')
        logger.info(output)
        logger.info('output')
        rc = check_result(checklist, output=output)
    return rc


def clear_log_message():
    PC2_login.send_command("echo '' > /var/log/messages")
    os.system("echo '' > /var/log/messages")
    log_api.clear_log()


def check_smpt_packet(srcip, dstip, exportres):
    service = "Dst=[25]"
    packets = exportres.split('Packet number: ')
    result_packet = []
    dstip = f"Dst=[{dstip}]"
    srcip = f"Src=[{srcip}]"
    content = 'Generated'
    for packet in packets:
        if dstip in packet:
            if srcip in packet:
                if service in packet:
                    if content in packet:
                        return True, packet
    return False, False

def get_syslog():
    with open('/var/log/messages', 'r', encoding='gb2312', errors='ignore') as file:
            syslog = file.read()
    logger.info(syslog)
    return syslog
