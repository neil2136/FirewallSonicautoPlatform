from settings import Parameter, fw, localhost
from settings import logger, Params, re, parse


def verify_ip1_in_ip2_network(ip1, ip2):
    ## verify x2_ip is in server network
    try:
        for i in range(0, 2):
            if ip1.split('.')[i] == ip2.split('.')[i]:
                i += 1
            else:
                return False
        return True
    except BaseException:
        logger.error("ERR: failed to get pppoe IP")
    return False


def ping_from_client(dst='0.0.0.0', num=5, repeat=5):
    rc = False
    try:
        for i in range(repeat):
            res = localhost.send_command(f'ping {dst} -c {num}')
            logger.info(res)
            rc = False if re.search("100% packet loss", res, re.I) else True
            if rc:
                break
    except BaseException:
        logger.error(f"ERR: failed to ping pppoe server {dst}")
    return rc


def time_difference(time_pre, time_new):
    rc = False
    try:
        if time_pre and time_new:
            pre = parse(time_pre)
            new = parse(time_new)
            difference = (new - pre).seconds
            logger.info(f"time difference is {difference}")
            rc = True if 0 < difference <= 125 else False
        else:
            logger.error("ERR: input time can not be null!")
    except BaseException:
        logger.error("ERR: failed to get time difference")
    return rc
