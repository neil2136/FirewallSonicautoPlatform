from definition.settings import *


def disable_x1_port(device):
    logger.info(" {} ".center(20, '-').format('disable remote x1 port'))
    rc = False
    cmd = "perl /SWIFT4.0/COMMON/bin/swconfig.pl -action portdown -device {} -port X1 -spec \
        http://osservices-sj.eng.sonicwall.com/topology_details/{}.xml".format(device, Params.testbed)
    logger.info(cmd)
    resp = os.popen(cmd).read()
    logger.info(resp)    
    time.sleep(15)
    
    for i in range(30):
        out = os.popen("ping {} -c 1".format(Parameter.REMOTEX1)).read()
        if '100% packet loss' in str(out):
            logger.info('Successfully disable remote x1 port.')
            logger.info(out)
            rc = True
            break
        elif i == 29:
            logger.info('disable remote x1 port failed')
            logger.info(out)
            rc = False
    return rc


def enable_x1_port(device):
    logger.info(" {} ".center(20, '-').format('enable remote x1 port'))
    rc = False
    cmd = "perl /SWIFT4.0/COMMON/bin/swconfig.pl -action portup -device {} -port X1 -spec \
        http://osservices-sj.eng.sonicwall.com/topology_details/{}.xml".format(device, Params.testbed)
    logger.info(cmd)
    resp = os.popen(cmd).read()
    logger.info(resp)
    time.sleep(15)

    for i in range(30):
        out = os.popen("ping {} -c 1".format(Parameter.REMOTEX1)).read()
        logger.info(out)
        if '100% packet loss' not in str(out):
            logger.info('Successfully recover remote x1 port.')
            rc = True
            break
        elif i == 29:
            logger.info('recover remote x1 port failed')
            rc = False
    return rc
