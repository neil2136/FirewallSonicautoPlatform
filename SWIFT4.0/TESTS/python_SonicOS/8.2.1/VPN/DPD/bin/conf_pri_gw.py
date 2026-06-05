from definition.settings import *


def disable_device_port(port):
    logger.info('disable remote {}'.format(port))
    rc = False
    cmd = "perl /SWIFT4.0/COMMON/bin/swconfig.pl -action portdown -device RemoteGEN7 -port {} -spec \
        http://osservices-sj.eng.sonicwall.com/topology_details/{}.xml".format(port, Params.testbed)
    if port == 'X1':
        target = Parameter.REMOTEX1
    else:
        target = Parameter.REMOTEX2
    for i in range(10):
        logger.info(cmd)
        resp = os.popen(cmd).read()
        logger.info(resp)
        out = os.popen("ping {} -c 1".format(target)).read()
        logger.info(out)
        time.sleep(10)
        if '100% packet loss' in str(out):
            logger.info('Successfully disable remote {}.'.format(port))
            rc = True
            break
        elif i == 9:
            logger.info('failed disable remote {}'.format(port))
            rc = False
    return rc


def enable_device_port(port):
    logger.info(" {} ".center(20, '-').format('enable primary gw'))
    rc = False
    cmd = "perl /SWIFT4.0/COMMON/bin/swconfig.pl -action portup -device RemoteGEN7 -port {} -spec \
        http://osservices-sj.eng.sonicwall.com/topology_details/{}.xml".format(port, Params.testbed)

    time.sleep(10)
    if port == 'X1':
        target = Parameter.REMOTEX1
    else:
        target = Parameter.REMOTEX2
    for i in range(10):
        logger.info(cmd)
        resp = os.popen(cmd).read()
        logger.info(resp)
        time.sleep(10)
        out = os.popen("ping {} -c 1".format(target)).read()
        if '100% packet loss' not in str(out):
            logger.info('Successfully recover remote x1.')
            logger.info(out)
            rc = True
            break
        elif i == 9:
            logger.info('Successfully recover remote x1')
            logger.info(out)
            rc = False
    return rc
