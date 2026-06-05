from runner.settings import logger
from definition.settings import Parameter


def start_L2TP_Client(pc_obj):
    connectcmds = [
        'systemctl restart strongswan',
        'systemctl restart xl2tpd',
        'sleep 3',
        'strongswan up myvpn',
        'echo "c myvpn" > /var/run/xl2tpd/l2tp-control',
        'sleep 5',
        'grep xl2tpd /var/log/messages | tail -5'
    ]
    connectres = pc_obj.send_commands(connectcmds)
    filter_tuple = [
        "connection 'myvpn' established successfully",
        "Connection established"
    ]
    checkres = [x in str(connectres) for x in filter_tuple]
    logger.info(checkres)
    flag = True if all(checkres) else False
    logger.info(f"check if groupvpn and L2TP connected: {flag}")
    return flag


def get_ppp_address(pc_obj):
    pppaddr = ''
    ifconfigres = pc_obj.send_command("ifconfig ppp")
    if 'ppp' in str(ifconfigres):
        res = pc_obj.send_command("ifconfig ppp | awk 'NR==2{print $2}'")
        pppaddr = res.rstrip()
        logger.info(f"client ip is {pppaddr}")
    else:
        logger.info("L2TP client can't be connect")
    return pppaddr


def check_route(pc_obj):
    rtres = pc_obj.send_command("ip -4 r")
    routecheck1 = f'{Parameter.FIREWALL} dev ppp'
    flag = True if routecheck1 in str(rtres) else False
    return flag
