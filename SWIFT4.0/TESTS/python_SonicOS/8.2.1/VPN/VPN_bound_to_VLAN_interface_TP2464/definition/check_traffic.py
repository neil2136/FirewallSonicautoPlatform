from definition.settings import *


def ping_traffic(ip):
    logger.info(" {} ".center(20, '-').format('Initiate pings'))
    rc = False
    for i in range(10):
        time.sleep(2)
        out = PC1.send_command("ping {} -c 1 ".format(ip))
        if '100% packet loss' not in str(out):
            logger.info('Successfully initiated continuous traffic from remote to local NAT.')
            rc = True
            break
        elif i == 9:
            logger.info('Ping failed')
            logger.info(out)
            rc = False
    return rc

