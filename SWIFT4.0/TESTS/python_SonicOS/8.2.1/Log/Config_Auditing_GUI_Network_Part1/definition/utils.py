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
                    rc &= True
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

def DibblerStart():
    cmd = "dibbler-client status"
    output = os.popen(cmd).read()
    logger.info('dibbler status:' + output)
    
    if re.search(r'Dibbler client: RUNNING, pid=\d+',output, re.I):
        ret = os.system('dibbler-client stop')
        ret = ret + os.system("ps -e | grep dibbler-client | awk '{print $1}' | xargs kill -9")
        logger.info(ret)
       
    cmd = f'\cp -f {CONFS_PATH}client.eth0.conf /etc/dibbler/client.conf'
    logger.info(cmd)
    ret = os.system(cmd)
    time.sleep(2)
    ret += os.system('dibbler-client start')
    time.sleep(2)
    status = os.popen('dibbler-client status').read()
    logger.info(" {} ".center(20, '-').format(status))
    flag = 1
    for i in range(0,5):
        if re.search(r'Dibbler client: RUNNING',status, re.I):
            flag = 0
            break
        else:
            os.system('dibbler-client start')
    print(flag)
    return flag  


def DibblerStop():
    #cmd = "ps -e | grep dibbler-client | awk '{print $1}' | xargs kill -9"
    # cmd = "killall dibbler-client"
    cmd = "dibbler-client stop"
    ret = os.system(cmd)
    cmd = f'\cp -f {CONFS_PATH}client.conf /etc/dibbler/client.conf'
    logger.info(cmd)
    os.system(cmd)
    return ret
    
