from runner.settings import Params, logger


# Check whether x2 client can get ip or not
def check_ip_in_pc_eth1(pc_login, ip_inet='192.168.2.'):
    logger.info("Confirm whether x2 client can get ip or not... ")
    cmds = [
        "ifconfig eth1 0.0.0.0",
        "dhclient eth1 -r",
        "dhclient eth1 -v",
    ]
    pc_login.send_commands(cmds)
    output = pc_login.send_command(f"ip -4 a")
    return True if f'inet {ip_inet}' in output else False
