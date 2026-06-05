import time
from definition.settings import logger, zone_api, pc1_login, pc2_login, syslog_file


def syslog_check(file, match_content):
    logger.info(f'match_content:\n{match_content}')
    with open(file, 'r', encoding="utf-8") as f:
        logger.info(f'syslogfile:\n{f}')
        for line in f:
            logger.info(f'syslog:\n{line}')
            checkres = [x in line for x in match_content]
            if all(checkres):
                logger.info(f'find matched syslog:\n{line}')
                return True
        logger.error('not found matched syslog.'.center(40, '*'))
        return False


def send_udp_traffic():
    logger.info("initial udp server")
    pc2_login.send_command(f'killall python3')
    pc2_login.send_command(
        f'nohup python3 /tmp/udpserver.py > /tmp/udpserver.log 2>&1 &')
    time.sleep(2)
    logger.info("clear the syslog file")
    pc1_login.send_command(f'echo "" > {syslog_file}')
    logger.info("initial udp client")
    res = pc1_login.send_command("python3 /tmp/udpclient.py")
    flag = True if 'udp traffic test' in res else False
    return flag
