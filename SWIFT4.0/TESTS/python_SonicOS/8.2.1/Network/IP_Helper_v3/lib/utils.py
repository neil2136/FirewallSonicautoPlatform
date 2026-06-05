from definition.initial_param import *
from scapy.all import *


def test_dhcp_traffic():
    logger.info('ifconfig eth1 down')
    os.system('ifconfig eth1 down')
    cmd = 'dhclient {} &'.format(Parameter.INTERFACE_LAN)
    logger.info(cmd)
    os.system(cmd)
    for i in range(1, 15):
        sleep(30)
        logger.info(i)
        logger.info('ifconfig eth0')
        output = ''.join(os.popen('ifconfig eth0'))
        logger.info(output)
        # dhcp server: 192.168.168.20-22
        pattern = re.search(r'192\.168\.168\.2[0-2]', output, re.M)
        if pattern:
            logger.info("Got DHCP ip: {}".format(pattern.group()))
            return True
    return False


def show_case_info(case_id):
    testplan = show_testcase_info(Parameter.TESTPLAN, case_id, description=True)
    logger.info(testplan)
    logger.info('*' * 8 + ' title ' + '*' * 8)
    logger.info(testplan['title'])
    logger.info('*' * 8 + ' steps ' + '*' * 8)
    for item in testplan['steps'].split('&'):
        logger.info(item)


def kill_dhclient():
    # restore eth0 ip and up eth1
    os.system('ifconfig {} {}'.format(Parameter.INTERFACE_LAN, Parameter.PC1_LAN_IP))
    os.system('ifconfig eth1 up')
    out = ''.join(os.popen('pidof dhclient'))
    logger.info("kill {}".format(out))
    os.system("kill {}".format(out))


def dns_traffic():
    logger.info(" ****  I'm scapy, sending dns trafic...  **** ")
    data = 'shanghai_automation'
    pkt = IP(src='192.168.168.169', dst='192.168.168.255')/UDP()/DNS(qr=0)/data
    send(pkt, inter=1, count=10, iface="eth0")
    sleep(3)
