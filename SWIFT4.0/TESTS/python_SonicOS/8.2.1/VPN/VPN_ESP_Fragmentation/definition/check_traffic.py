from definition.settings import *


def ping_traffic(pc,ip,length):
    logger.info(" {} ".center(20, '-').format('Initiate pings'))
    rc = False
    for i in range(20):
        time.sleep(5)
        out = pc.send_command("ping {} -c 1 -s {}".format(ip,length))
        if '100% packet loss' not in str(out):
            logger.info('Successfully initiated continuous traffic from remote to local NAT.')
            rc = True
            break
        elif i == 9:
            logger.info('Ping failed')
            logger.info(out)
            rc = False
    return rc

