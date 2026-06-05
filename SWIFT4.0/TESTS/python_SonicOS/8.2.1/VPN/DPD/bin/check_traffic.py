from definition.settings import *


def ping_from_local_to_remote():
    logger.info(" {} ".center(20, '-').format('Initiate pings'))
    rc = False
    for i in range(10):
        out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
        if '100% packet loss' not in str(out):
            logger.info('Successfully initiated continuous traffic from remote to local NAT.')
            logger.info(out)
            rc = True
            break
        elif i == 9:
            logger.info('Ping failed')
            logger.info(out)
            rc = False
    return rc


def ping_from_remote_to_local():
    logger.info(" {} ".center(20, '-').format('Initiate pings'))
    rc = False
    for i in range(10):
        out = PC2_login.send_command("ping {} -c 1".format(PC1_eth0))
        if '100% packet loss' not in str(out):
            logger.info('Successfully initiated continuous traffic from remote to local NAT.')
            logger.info(out)
            rc = True
            break
        elif i == 9:
            logger.info('Ping failed')
            logger.info(out)
            rc = False
    return rc


def ping_from_PC4_to_PC5():
    logger.info(" {} ".center(20, '-').format('Initiate pings'))
    rc = False
    for i in range(10):
        out = PC4_login.send_command("ping {} -c 1".format(PC5_eth0))
        if '100% packet loss' not in str(out):
            logger.info('Successfully initiated continuous traffic from remote to local NAT.')
            logger.info(out)
            rc = True
            break
        elif i == 9:
            logger.info('Ping failed')
            logger.info(out)
            rc = False
    return rc


def ping_traffic_blocked():
    logger.info(" {} ".center(20, '-').format('Initiate pings'))
    rc = False
    for i in range(10):
        out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
        if '100% packet loss' in str(out):
            logger.info('Ping from local to remote failed')
            rc = True
            break
        elif i == 9:
            logger.info('Ping from local to remote passed')
            logger.info(out)
            rc = False
    return rc


def ping_traffic2_blocked():
    logger.info(" {} ".center(20, '-').format('Initiate pings'))
    rc = False
    for i in range(10):
        out = PC4_login.send_command("ping {} -c 3".format(PC5_eth0))
        if '100% packet loss' in str(out):
            logger.info('Ping from local to remote failed')
            rc = True
            break
        elif i == 9:
            logger.info('Ping from local to remote passed')
            logger.info(out)
            rc = False
    return rc


def check_test_log():
    logger.info(" {} ".center(20, '-').format('Test log'))
    time.sleep(2)
    log = str(LogObj.export_log_txt(log_switch=False))
    reg = re.search('IKE negotiation complete', log, re.I|re.M)
    if reg:
        logger.info(reg.group())
        rc = True
    else:
        logger.info('Test log failed.')
        logger.info(log)
        rc = False
    return rc


def check_test_log_with_dis_dpd():
    logger.info("check no info1: NOTIFY: R_U_THERE")
    logger.info("check no info2: Tunnel Down")
    time.sleep(2)
    log = str(LogObj.export_log_txt(log_switch=False))
    logger.info(log)
    reg1 = re.search('NOTIFY: R_U_THERE', log, re.I|re.M)
    reg2 = re.search('Tunnel Down', log, re.I|re.M)
    if reg1 or reg2:
        logger.info('Test no matched log failed.')
        if reg1:
            logger.info("match info1: NOTIFY: R_U_THERE")
        if reg2:
            logger.info("match info2: Tunnel Down")
        rc = False
    else:
        logger.info('Test no specified log passed.')
        rc = True
    return rc


def check_test_log_with_enable_dpd():
    logger.info("check appears info1: NOTIFY: R_U_THERE")
    logger.info("check appears info2: Tunnel Down")
    time.sleep(2)
    log = str(LogObj.export_log_txt(log_switch=False))
    logger.info(log)
    reg1 = re.search('NOTIFY: R_U_THERE', log, re.I|re.M)
    reg2 = re.search('Remove IPSec SaNode', log, re.I|re.M)
    if reg1 and reg2:
        logger.info('Test log passed.')
        rc = True
    else:
        logger.info('Test log failed.')
        if not reg1:
            logger.info('no matched info1: NOTIFY: R_U_THERE')
        if not reg2:
            logger.info('no matched info2: Tunnel Down')
        rc = False
    return rc


def check_test_log_after_expire():
    logger.info(" {} ".center(20, '-').format('Test log'))
    time.sleep(2)
    log = str(LogObj.export_log_txt(log_switch=False))
    flag = 0
    reg1 = '{}.*IKE\s+SA\s+lifetime\s+expired'.format(Parameter.REMOTEX2)
    reg2 = '{}.*IKE\s+negotiation\s+complete'.format(Parameter.REMOTEX1)
    for reg in [reg1, reg2]:
        resp = re.search(reg, log, re.I | re.M)
        if resp:
            flag += 1
            logger.info("flag={}".format(flag))
            logger.info(resp.group())
    if flag == 2:
        logger.info('Test log passed.')
        rc = True
    else:
        logger.info('Test log failed.')
        logger.info(log)
        rc = False
    return rc