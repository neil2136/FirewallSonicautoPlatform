from definition.settings import *


def ping_from_local_to_remote():
    logger.info(" {} ".center(20, '-').format('Initiate pings'))
    rc = False
    for i in range(10):
        out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
        logger.info(out)
        if '100% packet loss' not in str(out):
            logger.info('Successfully initiated continuous traffic from remote to local NAT.')
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
        logger.info(out)
        if re.search('100% packet loss', str(out)):
            logger.info('block ping from local to remote passed')
            rc = True
            break
        elif i == 9:
            logger.info('block ping from local to remote failed')
            logger.info(out)
            rc = False
    return rc


def check_test_log():
    logger.info(" {} ".center(20, '-').format('Test log'))
    time.sleep(2)
    log = LogObj.export_log_txt(log_switch=False)
    if re.search('IKE\s+negotiation\s+complete', log, re.I):
        rc = True
        logger.info('Test log passed.')
    else:
        logger.info(log)
        rc = False
    return rc


def check_test_log_regotiation():
    logger.info(" {} ".center(20, '-').format('Clear log'))
    ret = LogObj.clear_log()
    if ret == None:
        rc1 = True
    else:
        rc1 = False
    logger.info(" {} ".center(20, '-').format('Test log'))
    time.sleep(320)
    log = LogObj.export_log_txt(log_switch=False)
    if re.search('negotiation\s+complete', log, re.I):
        logger.info(log)
        rc2 = False
        logger.info('Test log mismatch passed.')
    else:
        rc2 = True
    rc = rc1 & rc2
    return rc
