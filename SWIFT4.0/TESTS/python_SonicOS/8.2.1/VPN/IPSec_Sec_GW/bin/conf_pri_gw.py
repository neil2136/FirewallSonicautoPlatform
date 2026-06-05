from definition.settings import *


def disable_pri_gw():
    logger.info(" {} ".center(20, '-').format('disable primary gw'))
    rc = False
    cmd = "perl /SWIFT4.0/COMMON/bin/swconfig.pl -action portdown -device RemoteGEN7 -port X1 -spec \
        http://osservices-sj.eng.sonicwall.com/topology_details/{}.xml".format(Params.testbed)
    resp = os.system(cmd)
    time.sleep(15)
    for i in range(30):
        out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
        if '100% packet loss' not in str(out):
            logger.info('Successfully change vpn to secondary gw.')
            logger.info(out)
            rc = True
            break
        elif i == 30:
            logger.info('change vpn to secondary gw failed')
            logger.info(out)
            rc = False
    return rc


def enable_pri_gw():
    logger.info(" {} ".center(20, '-').format('enable primary gw'))
    rc = False
    cmd = "perl /SWIFT4.0/COMMON/bin/swconfig.pl -action portup -device RemoteGEN7 -port X1 -spec \
        http://osservices-sj.eng.sonicwall.com/topology_details/{}.xml".format(Params.testbed)
    resp = os.system(cmd)
    time.sleep(15)
    for i in range(30):
        out = os.popen("ping {} -c 1".format(Parameter.REMOTEX1)).read()
        if '100% packet loss' not in str(out):
            logger.info('Successfully recover vpn to primary gw.')
            logger.info(out)
            rc = True
            break
        elif i == 30:
            logger.info('recover vpn to primary gw failed')
            logger.info(out)
            rc = False
    return rc