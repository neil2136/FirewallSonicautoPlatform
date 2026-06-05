from definition.settings import *


def test_dhcp_traffic(PC):
    sleep(10)  # wait for UTM configuring
    pc_ssh = ''
    if PC == 'PC1':
        pc_ssh = Host('localhost')
    if PC == 'PC3':
        pc_ssh = Host(Params.testbed + '-PC3')
    pc_ssh.send_command('ifconfig eth2 down')
    cmd = 'dhclient {} &'.format(Parameter.INTERFACE_LAN)
    pc_ssh.send_command(cmd)
    for i in range(1, 15):
        sleep(30)
        logger.info("Trying to get dhcp ip....{}".format(i))
        output = pc_ssh.send_command('ifconfig eth0')
        logger.info(output)
        pattern = re.search(r'3\.3\.3\.1[0-2]', output, re.M)
        if PC == 'PC1' and pattern:
            logger.info("PC1 client got DHCP ip: {}".format(pattern.group()))
            # restore
            kill_dhclient(PC='PC1')
            pc_ssh.send_command('ifconfig eth0 192.168.168.169')
            cmd = "service network restart"
            pc_ssh.send_command(cmd)
            sleep(20)
            return True
        if PC == 'PC3' and pattern:
            logger.info("PC3 client got DHCP ip: {}".format(pattern.group()))
            # restore
            kill_dhclient(PC='PC3')
            pc_ssh.send_command('ifconfig eth0 3.3.3.22')
            return True
    return False


def kill_dhclient(PC):
    pc_ssh = ''
    if PC == 'PC1':
        pc_ssh = Host('localhost')
    if PC == 'PC3':
        pc_ssh = Host(Params.testbed + '-PC3')
    pc_ssh.send_command('ifconfig eth2 up')
    output = pc_ssh.send_command('pidof dhclient')
    logger.info(output)
    cmd = 'kill {}'.format(output)
    pc_ssh.send_command(cmd)
    pass
