from definition.global_v import *

def DibblerStart(eth):
    cmd = "dibbler-client status"
    output = os.popen(cmd).read()
    logger.info('dibbler status:' + output)
    
    if re.search(r'Dibbler client: RUNNING, pid=\d+',output, re.I):
        ret = os.system('dibbler-client stop')
        ret = ret + os.system("ps -e | grep dibbler-client | awk '{print $1}' | xargs kill -9")
        logger.info(ret)
       
    cmd = f'\cp -f {confs_path}client.{eth}.conf /etc/dibbler/client.conf'
    logger.info(cmd)
    ret = os.system(cmd)
    time.sleep(2)
    ret += os.system('dibbler-client start')
    time.sleep(2)
    status = os.popen('dibbler-client status').read()
    logger.info(" {} ".center(20, '-').format(status))
    flag = 1
    for i in range(0,5):
        if re.search(r'Dibbler client: RUNNING',status, re.I):
            flag = 0
            break
        else:
            os.system('dibbler-client start')
    print(flag)
    return flag    

def ClearENV(eth):
    # Clear lease on DUT
    leases_status = dhcpserver_obj.get_dhcp_server_leases(version=6)
    logger.info(type(leases_status))
    logger.info(leases_status)
    if leases_status:
        ip_v6 = leases_status[0]["ipv6_address"]
        ret = dhcpserver_obj.delete_target_dhcp_server_lease(ip=ip_v6, version=6)
        logger.info(ret)
    else:
        logger.info("No dhcp server lease found on DUT when stop dibbler...")

    # Clear ipv6 address on interface
    ret = os.popen("ifconfig {}".format(eth)).read()
    logger.info(ret)
    m = re.search(r'inet6 addr: (2003::[6-9])/64', ret, re.I)
    if m:
        os.system("ifconfig eth0 inet6 del {}/64".format(m.group(1)))
        time.sleep(2)
        os.system("ip n flush all")
    ret = os.popen("ifconfig {}".format(eth)).read()
    logger.info(ret)

    return 0

def DibblerStop():

    #cmd = "ps -e | grep dibbler-client | awk '{print $1}' | xargs kill -9"
    cmd = "killall dibbler-client"
    ret = os.system(cmd)

    cmd = f'\cp -f {confs_path}client.conf /etc/dibbler/client.conf'
    logger.info(cmd)
    os.system(cmd)

    return ret
