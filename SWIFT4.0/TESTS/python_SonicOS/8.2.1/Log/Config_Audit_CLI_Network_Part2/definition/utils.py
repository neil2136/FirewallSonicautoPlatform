from definition.settings import *


def check_result(check_list, output, mode=None):
    ret = False
    rc = []
    try:
        if check_list:
            for check_str in check_list:
                if mode and mode.lower() == 'snmp':
                    check_str = r"5609.*?Configuration succeeded.*?" + check_str
                elif mode and mode.lower() == 'syslog':
                    check_str = r"m=1382 msg=\"Configuration succeeded.*?" + check_str

                if re.search(check_str, output, re.M):
                    rc.append(1)
                else:
                    rc.append(0)
                    logger.info('check fail: {}'.format(check_str))
            ret = all(rc)
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


def get_syslog_via_pc1():
    with open('/var/log/messages', 'r', encoding='gb2312', errors='ignore') as file:
            syslog = file.read()
    logger.info(syslog)
    return syslog


