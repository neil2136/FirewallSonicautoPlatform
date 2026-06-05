from definition.settings import *

def clear_log_and_snmp_msg():
    
    log_obj.clear_log()
    out1 =PC2.send_commands(["echo '' > /var/log/messages","cat /var/log/messages"])
    out2 = PC1.send_commands(["echo '' > /var/log/messages","cat /var/log/messages"])
    out1,out2 = out1.replace(' ','').replace('\n',''),out2.replace(' ','').replace('\n','')
    if out1 == '' and out2 == '':
        rc = True
        logger.info('clear log and snmp server message successful!')
    else:
        rc = False
        logger.info(f'out1:{out1}')
        logger.info(f'out2:{out2}')
        logger.info('clear log and snmp server message Failed!')
    return rc

def check_msg_list(check_list,output,mode):
    rc = True
    try:
        if check_list:
            for check_str in check_list:
                if mode and mode.lower() == 'snmp':
                    check_str = r"5609.*?Configuration succeeded.*?" + check_str
                elif mode and mode.lower() == 'syslog':
                    check_str = r"m=1382 msg=\"Configuration succeeded.*?" + check_str
                if re.search(check_str, output, re.M):
                    rc &= True
                else:
                    rc &= False
                    logger.info('check fail: {}'.format(check_str))
    except Exception as e:
        logger.error(f'Error when execute function check_result: {repr(e)}')
    return rc

def check_log_msg(mode,check_list):
    logger.info(f'check log {check_list} in {mode}')
    if mode == 'syslog':
        time.sleep(3)
        with os.popen('cat /var/log/messages', 'r') as file:
            syslog = file.read()
            s= syslog.replace(' ','').replace('\n','')
        logger.info(f'----------{s}-------------------')
        logger.info(syslog)
        rc = check_msg_list(check_list=check_list,output=syslog,mode=mode)
    elif mode == 'snmp':
        output = PC2.send_command('cat /var/log/messages | grep snmptrapd')
        logger.info(output)
        rc = check_msg_list(check_list=check_list,output=output,mode=mode)
    elif mode == 'audit':
        output = audit_logobj.export_audit_log_txt()
        logger.info(output)
        rc = check_msg_list(check_list=check_list,output=output,mode=mode)
    elif mode == 'log':
        output = log_obj.export_log_txt()
        logger.info(output)
        rc = check_msg_list(check_list=check_list,output=output,mode=mode)
    return rc

