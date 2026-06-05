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


def check_test_log():
    logger.info(" {} ".center(20, '-').format('Test log'))
    time.sleep(2)
    log = str(LogObj.export_log_txt(log_switch=False))
    flag = 0
    reg1 = re.search('Tunnel\s+Up.*GW\s+{}.*Negotiation\s+Done'.format(Parameter.REMOTEX1), log, re.I|re.M)
    reg2 = re.search('VPN\s+Policy.*IKEv2\s+Peer\s+is\s+not\s+responding', log, re.I|re.M)
    reg3 = re.search('Tunnel\s+Up.*GW\s+{}.*Negotiation\s+Done'.format(Parameter.REMOTEX2), log, re.I|re.M)

    if reg1:
        flag = 1
        logger.info(reg1.group())
        if reg2:
            flag = 2
            logger.info(reg2.group())
            if reg3:
                flag = 3
                logger.info(reg3.group())
    if flag == 3:
        logger.info('Test log passed.')
        logger.info("flag={}".format(flag))
        logger.info(log)
        rc = True
    else:
        logger.info('Test log failed.')
        logger.info(log)
        logger.info("flag={}".format(flag))
        rc = False
    return rc


def ping_traffic_blocked():
    logger.info(" {} ".center(20, '-').format('Initiate pings'))
    rc = False
    for i in range(10):
        out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
        if '100% packet loss' not in str(out):
            logger.info('Ping from local to remote failed')
            rc = True
            break
        elif i == 9:
            logger.info('Ping from local to remote passed')
            logger.info(out)
            rc = False
    return rc


def check_test_log_after_pri_gw_down():
    logger.info(" {} ".center(20, '-').format('Test log'))
    time.sleep(2)
    log = str(LogObj.export_log_txt(log_switch=False))
    flag = 0
    reg1 = '{}.*IKE\s+negotiation\s+complete'.format(Parameter.REMOTEX1)
    reg2 = 'IKE\s+negotiation\s+aborted\s+due\s+to\s+Timeout'
    reg3 = 'Using\s+secondary\s+gateway\s+to\s+negotiate'
    reg4 = '{}.*IKE\s+negotiation\s+complete'.format(Parameter.REMOTEX2)
    for reg in [reg1, reg2, reg3, reg4]:
        resp = re.search(reg, log, re.I | re.M)
        if resp:
            flag += 1
            logger.info("flag={}".format(flag))
            logger.info(resp.group())
    if flag == 4:
        logger.info('Test log passed.')
        rc = True
    else:
        logger.info('Test log failed.')
        logger.info(log)
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