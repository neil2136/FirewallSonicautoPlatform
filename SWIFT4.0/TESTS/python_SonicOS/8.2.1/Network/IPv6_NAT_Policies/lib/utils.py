from definition.initial_param import *


def delete_default_ipv6_route(PC='PC1'):
    host = localhost
    if PC == 'PC2':
        host = pc2_ssh
    cmd = 'ip -6 r |grep ^default| wc -l'
    count = int(host.send_command(cmd))
    logger.info("Do 'ip -6 r d default' {} times".format(count))
    while count:
        host.send_command('ip -6 r d default')
        count = count - 1


def configure_ipv6_address_of_PC(config, ipv6_address, eth, PC='PC1'):
    # input:
    # 1. config = a (add)/ d(delete)
    # 2. ipv6 address
    # 3. eth
    cmd = "ip -6 a {} {}/64 dev {}".format(config, ipv6_address, eth)
    logger.info(cmd)
    if PC == 'PC2':
        rc = pc2_ssh.send_command(cmd)
    else:
        rc = localhost.send_command(cmd)
    return rc


# input : ip address to check
def check_NATed_source_ip(ip, eth='eth1', ping_ip=Parameter.wan_host1):
    # delete exist file
    del_cmd = '\cp -f /tmp/tcpdump.file'
    pc2_ssh.send_command(del_cmd)
    pc2_ssh.send_command("tcpdump -i {} -v icmp6 > /tmp/tcpdump.file 2>&1 &".format(eth))
    sleep(2)
    ping_cmd = 'ping6 -c 4 -i 3 -I {} {}'.format(eth, ping_ip)
    localhost.send_command(ping_cmd)
    sleep(10)
    pc2_ssh.send_command("pkill tcpdump")
    output = pc2_ssh.send_command("cat /tmp/tcpdump.file")
    logger.info(output)
    pc2_ssh.send_command("exit")
    # check packet with/without input IP
    if ip in output:
        logger.info(" The ICMP packets with your checking IP! ")
        return False
    else:
        logger.info(" Your private IP is hidden by UTM NAT policy! ")
        return True


# input : list of translated ip & ip pool to check
def check_NATed_destination_ip(trans_ips, ip_pool):
    # delete exist file
    del_cmd = '\cp -f /tmp/tcpdump.file'
    pc2_ssh.send_command(del_cmd)
    pc2_ssh.send_command("tcpdump -i eth1 -v icmp6 > /tmp/tcpdump.file 2>&1 &")
    for trans_ip in trans_ips:
        ping_cmd = 'ping6 -c 3 -i 3 -I eth1 ' + trans_ip
        localhost.send_command(ping_cmd)
        sleep(3)
    pc2_ssh.send_command("pkill tcpdump")
    output = pc2_ssh.send_command("cat /tmp/tcpdump.file")
    logger.info(output)
    pc2_ssh.send_command("exit")
    # check the packet file without translated ips but with ip addr in ip pool
    for trans_ip in trans_ips:
        if trans_ip in output:
            logger.info(" Warning: ICMP packet with your translated IP!")
            return False
        for ip in ip_pool:
            if ip in output:
                logger.info(" Your translated IP is hidden by UTM NAT policy, and ip now is: {} !".format(ip))
                return True
        logger.info(" Translated ip is not changed into any ip addresses in your ip pools!")
        return False


