import os
import sys
import time
import re

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPV6_Interface')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPV6_Interface/lib')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

from runner.settings import logger
from lib.settings import Parameter


conf_path = os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPV6_Interface/confs/radvd.conf'

def setup_network_service_ipv6():
    # restart network service, for some unuseful ipv6 route
    os.system('service network restart')
    time.sleep(4) # waiting for network restart
#eth0
    logger.info("========Delete eth0 ipv6 address...=============")
    cmd = "ifconfig eth0|grep 'inet6'|awk '{print $3}'|grep -v '^fe80'"
    ipv6_eth0_address = ''.join(os.popen(cmd))
    logger.info("ipv6 address of eth0 is: {}".format(ipv6_eth0_address))

    #del
    os.system('ifconfig eth0 inet6 del {}'.format(ipv6_eth0_address))

    #setup
    logger.info("=========set eth0 ipv6 address as 2000:111::100...========")
    os.system('ifconfig eth0 inet6 add {}/64'.format(Parameter.lan_ipv6))

#eth2
    logger.info("====================Delete eth2 ipv6 address...==============")
    cmd2 = "ifconfig eth2|grep 'inet6'|awk '{print $3}'|grep -v '^fe80'"
    ipv6_eth2_address = ''.join(os.popen(cmd2))
    logger.info("ipv6 address of eth2 is: {}".format(ipv6_eth2_address))
    #del
    os.system('ifconfig eth2 inet6 del {}'.format(ipv6_eth2_address))

    #setup
    logger.info("=========set eth0 ipv6 address as 2000:111::100...========")
    os.system('ifconfig eth0 inet6 add {}/64'.format(Parameter.wan_ipv6))

#ip forward
    logger.info("===========Enable ipv6 forwarding...===============")
    os.system("echo '1' >> /proc/sys/net/ipv6/conf/all/forwarding")
    return True


def setup_RA_Server():
    logger.info("=============Open RA Server On PC1====================")
    cmd = '\cp -f {} /tmp/radvd.conf'.format(conf_path)
    os.system(cmd)
    os.system('/usr/sbin/radvd -C /tmp/radvd.conf')
    cmd2 = 'ps aux | grep radvd'
    output = ''.join(os.popen(cmd2))
    logger.info(output)
    if '/usr/sbin/radvd -C /tmp/radvd.conf' in output:
        return True
    return False


def kill_RA_Server():
    logger.info("=============Kill RA Server On PC1====================")
    os.system('/usr/bin/pkill radvd')
    cmd2 = 'ps aux | grep radvd'
    output = ''.join(os.popen(cmd2))
    logger.info(output)
    if '/usr/sbin/radvd -C /tmp/radvd.conf' in output:
        return False
    return True


def checkCapturePacket(address_ip):
    logger.info("=========================check captured packets...=====================")
    # check pc wan ipv6 addr
    cmd = "/sbin/ifconfig eth2 | /bin/grep 'inet6' | /bin/awk '{print $3}' | /bin/grep -v '^fe80'"
    output = ''.join(os.popen(cmd))
    pattern = re.findall('{}::.*/64'.format(address_ip),output,re.S)
    ipv6_addr = ''.join(pattern)
    if ipv6_addr != []:
        # enable ipv6 forwarding to stop autoconf
        os.system('/sbin/sysctl -w net.ipv6.conf.all.forwarding=1')
        # delete all ipv6 addr
        os.system('/sbin/ifconfig eth2 inet6 del {}'.format(ipv6_addr))
        # set pc wan ipv6 static addr
        logger.info("=============set eth2 ipv6 address as 2001:222::100...==============")
        os.system("/sbin/ifconfig eth2 inet6 add {}/64".format(Parameter.wan_ipv6))
        return True
    logger.info("Error:         check captured packets failed!               ")
    return False



def shutDown_network_service_ipv6():
    logger.info("===========================Set PC WAN ipv6 addr to null========================")
    cmd = "/sbin/ifconfig eth2 inet6 del {}/64".format(Parameter.wan_ipv6)
    os.system(cmd)
    logger.info("========================Disable ipv6 forwarding...=============================")
    os.system("/sbin/sysctl -w net.ipv6.conf.all.forwarding=0")
    return True
