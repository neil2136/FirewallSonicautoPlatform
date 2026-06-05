from runner.settings import logger, re, time
import paramiko

def pc_get_ip_lease(pc, eth):
    res = False
    ip_addr = ''
    for i in range(3):
        pc.send_command('ifconfig {} 0.0.0.0'.format(eth))
        pc.send_command('timeout 10 killall dhclient')
        out = pc.send_command('timeout 10 dhclient -v {}'.format(eth))
        time.sleep(20)
        m = re.search(
            r'bound to (12\.12\.2\.\d+).*renewal in', out, re.I)
        if m:
            ip_addr = m.group(1)
            logger.info(f'pc {eth} successfully get ip address')
            res = True
            break
        else:
            logger.info(f'pc {eth} failed to get ip address')   
    return res, ip_addr

                
def get_pc_mac(pc, eth):
    cmd = "ifconfig " + eth + " | grep HWaddr | awk '{print $5}'"
    output = pc.send_command(cmd)
    mac = output.strip()
    if len(mac) == 17:
        logger.info('='*10+'get mac address successfully'+'='*10)
        logger.info(f' mac address is: {mac}')
        return mac.lower()
    else:
        logger.info('='*10+'get mac adddress failed'+'='*10)
        return ''
