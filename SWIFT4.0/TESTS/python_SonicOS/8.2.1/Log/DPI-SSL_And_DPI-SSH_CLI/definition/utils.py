from definition.settings import *

def clear_log_and_snmp_msg():
    log_obj.clear_log()
    out1 =PC2.send_commands(["echo '' > /var/log/messages","cat /var/log/messages"])
    out2 = PC1.send_commands(["echo '' > /var/log/messages","cat /var/log/messages"])
    out1, out2 = out1.replace(' ','').replace('\n',''), out2.replace(' ','').replace('\n','')
    if out1 == '' and out2 == '':
        rc = True
        logger.info('Clear log and snmp server message successful!')
    else:
        rc = False
        logger.info(f'out1: {out1}')
        logger.info(f'out2: {out2}')
        logger.info('Clear log and snmp server message failed!')
    return rc

def check_msg_list(mode, check_list, output):
    try:
        for check_str in check_list:
            if mode == 'syslog':
                check_str = r"m=1382 msg=\"Configuration succeeded:.*?" + check_str
            elif mode == 'snmp':
                check_str = r"5609.*?Configuration succeeded:.*?" + check_str
            if re.search(check_str, output, re.M):
                rc = True
            else:
                rc = False
                logger.info(f'check fail: {check_str}')
    except Exception as e:
        logger.error(f'Error when execute function check_result: {repr(e)}')
    return rc

def check_log_msg(mode, check_list):
    logger.info(f'check log {check_list} in {mode}')
    if mode == 'syslog':
        time.sleep(3)
        with open('/var/log/messages', 'r') as file:
            syslog = file.read()
            logger.info(syslog)
        rc = check_msg_list(mode, check_list, syslog)
    elif mode == 'snmp':
        output = PC2.send_command('cat /var/log/messages | grep snmptrapd')
        logger.info(output)
        rc = check_msg_list(mode, check_list, output)
    elif mode == 'audit':
        output = audit_logobj.export_audit_log_txt()
        logger.info(output)
        rc = check_msg_list(mode, check_list, output)
    elif mode == 'system':
        output = log_obj.export_log_txt()
        logger.info(output)
        rc = check_msg_list(mode, check_list, output)
    return rc
