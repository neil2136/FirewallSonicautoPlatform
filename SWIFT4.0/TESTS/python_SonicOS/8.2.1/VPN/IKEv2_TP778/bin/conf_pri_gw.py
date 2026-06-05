from definition.settings import *


def disable_pri_gw():
    logger.info(" {} ".center(20, '-').format('disable primary gw'))
    rc = False
    cmd = "perl /SWIFT4.0/COMMON/bin/swconfig.pl -action portdown -device RemoteGEN7 -port X1 -spec \
        http://osservices-sj.eng.sonicwall.com/topology_details/{}.xml".format(Params.testbed)
    logger.info(cmd)
    resp = os.popen(cmd).read()
    logger.info(resp)
    time.sleep(15)
    for i in range(30):
        out = os.popen("ping {} -c 1".format(Parameter.REMOTEX1)).read()
        if '100% packet loss' in str(out):
            logger.info('Successfully disable primary gw.')
            logger.info(out)
            rc = True
            break
        elif i == 29:
            logger.info('disable primary gw failed')
            logger.info(out)
            rc = False
    return rc


def enable_pri_gw():
    logger.info(" {} ".center(20, '-').format('enable primary gw'))
    rc = False
    cmd = "perl /SWIFT4.0/COMMON/bin/swconfig.pl -action portup -device RemoteGEN7 -port X1 -spec \
        http://osservices-sj.eng.sonicwall.com/topology_details/{}.xml".format(Params.testbed)
    logger.info(cmd)
    resp = os.popen(cmd).read()
    logger.info(resp)
    time.sleep(5)
    for i in range(30):
        resp1 = os.popen(cmd).read()
        logger.info(resp1)
        time.sleep(5)

        out = os.popen("ping {} -c 1".format(Parameter.REMOTEX1)).read()
        logger.info(out)
        if '100% packet loss' not in str(out):
            logger.info('Successfully recover vpn to primary gw.')
            rc = True
            break
        elif i == 29:
            logger.info('recover vpn to primary gw failed')
            rc = False
    return rc

