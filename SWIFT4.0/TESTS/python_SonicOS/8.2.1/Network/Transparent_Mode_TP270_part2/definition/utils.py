from runner.settings import Params, logger
import time


def get_ip_lease_in_pc(pc_login, eth):
    res = False
    rang_ip_part = '12.12.1.9'
    cmds = [f'ifconfig {eth} 0.0.0.0', 'timeout 20 killall dhclient']
    pc_login.send_commands(cmds)
    for i in range(5):
        time.sleep(3)
        res = pc_login.send_command('timeout 20 dhclient -v {}'.format(eth))
        time.sleep(10)
        logger.info(f'run dhcp client on pc: {res}')
        if f'bound to {rang_ip_part}' in res:
            res = True
            break
        else:
            logger.info(f'pc {eth} failed to get ip address')
    return res


def release_ip_in_pc(pc_login, eth):
    cmds = ['killall dhclient', f'timeout 20 dhclient -r {eth}', f'timeout 5 ifconfig {eth} 0.0.0.0']
    pc_login.send_commands(cmds)
    time.sleep(3)
    logger.info('check if pc eth ip is released...')
    output = pc_login.send_command(f'ifconfig {eth}')
    if 'inet addr' not in output:
        logger.info(f"pc {eth} release successfully")
        return True
    else:
        logger.info(f"pc {eth} release failed")
        return False
