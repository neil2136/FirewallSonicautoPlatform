import re
import os
import sys
import time

sys.path.append(os.environ["PYTHON_COMMON_HOME"])

from utm import Firewall,FirewallAPI
from runner.settings import logger
from lib.modules.API.log import LogMonitorApi
from lib.settings import Parameter
from util.enhancedinfo import show_testcase_info

fw = Firewall(Parameter.FIREWALL, user= 'admin', password= 'password', supported_config_mode='api')
log = LogMonitorApi(fw)


def show_log(case_id):
    testplan = show_testcase_info(Parameter.TESTPLAN, case_id, description=True)
    logger.info(testplan)
    logger.info('*' * 8 + ' title ' + '*' * 8)
    logger.info(testplan['title'])
    logger.info('*' * 8 + ' steps ' + '*' * 8)
    for item in testplan['steps'].split('&'):
        logger.info(item)


def get_eth0_macaddr():
    cmd = "arp -a |grep 'eth0'"
    output = ''.join(os.popen(cmd))
    pattern = re.findall('.*at (.*?) ',output,re.S)
    mac_addr = ''.join(pattern)
    return mac_addr
UTM_mac = get_eth0_macaddr()


def get_eth2_ipv6():
    cmd = "ifconfig eth2 |grep 'Scope:Link'"
    output = ''.join(os.popen(cmd))
    pattern = re.findall('fe.*/64', output)
    logger.info("========eth2 inet6: {}===============".format(pattern))
    eth2_inet6 = ''.join(pattern)
    return eth2_inet6
WAN_inet6 = get_eth2_ipv6()


def check_WAN_RA():
    logger.info("==========================Capture RA Packets in WAN========================")
    cmd = '/usr/sbin/tcpdump -i eth2 -c 1 ip6[40]==134'
    output = ''.join(os.popen(cmd))
    pattern = re.findall('.*router advertisement', output, re.S)
    if pattern != []:
        return True
    return False


def check_ipv6_config(config, config_value):
    os.system('rm -f /tmp/dump-file.cap')
    os.system('/usr/sbin/tcpdump -vvv -i eth0 -s 1500 -c 3 -w /tmp/dump-file.cap  ip6 && icmp6 && (ip6[40]==134)')
    cmd = 'tcpdump -v -r /tmp/dump-file.cap'
    output = ''.join(os.popen(cmd))
    count = 0
    while (UTM_mac not in output and count < 4):
        os.system('rm -f /tmp/dump-file.cap')
        logger.info("======={} not in this file, retry to capture......=======================".format(UTM_mac))
        os.system('/usr/sbin/tcpdump -vvv -i eth0 -s 1500 -c 3 -w /tmp/dump-file.cap  ip6 && icmp6 && (ip6[40]==134)')
        count = count + 1
    if config == 'mtu':
        if config_value == '0':
            logger.info(output)
            pattern = re.findall('.*length 24.*{}'.format(UTM_mac), output, re.S)
            if 'mtu option' not in str(pattern):
                return True
        else:
            out = ''.join(os.popen(cmd + ' |grep "mtu option"'))
            logger.info(out)
            pattern = re.findall('.*{}'.format(config_value), out, re.S)
            if pattern != []:
                logger.info(pattern)
                return True
    if config == 'reachable time' or config == 'retrans time':
        out = ''.join(os.popen(cmd + " |grep '{}' ".format(config)))
        logger.info(out)
        pattern = re.findall('.*{}ms'.format(config_value * 1000), out, re.S)
        if pattern != []:
            logger.info(pattern)
            return True
    if config == 'hop limit':
        out = ''.join(os.popen(cmd + " |grep '{}' ".format(config)))
        logger.info(out)
        pattern = re.findall('.*hop limit {}'.format(config_value), out, re.S)
        if pattern != []:
            logger.info(pattern)
            return True
    if config == 'lifetime':
        out = ''.join(os.popen(cmd + " |grep '{}' ".format(config)))
        logger.info(out)
        pattern = re.findall('.*lifetime {}s'.format(config_value), out, re.S)
        if pattern != []:
            logger.info(pattern)
            return True
    if config == 'Flags':
        out = ''.join(os.popen(cmd + " |grep '{}' ".format(config)))
        logger.info(out)
        pattern = re.findall('.*Flags[\s\S].*?{}],'.format(config_value), out, re.S)
        if pattern != []:
            logger.info(pattern)
            return True
    logger.info("Please input right config and config_value, your input: config -> {}, config_value -> {} not match!".format(config,config_value))
    return False


def check_wan_ra_range(ra_min, ra_max):
    cmd = "/usr/sbin/tcpdump -tt -vvv -c 6 -i eth2 ip6[40]==134 | grep -n 'fe80::1ac2'"  # fe80::1ac2 comes from UTM
    count = 0
    while count < 3:
        output = os.popen(cmd).read()
        logger.info("tcpdump output: %s", output)
        pattern = re.findall(r'\d{10}', output)
        logger.info("Found numeric patterns: %s", pattern)
        if len(pattern) < 2:
            logger.error("Not enough numeric patterns found. Expected at least 2, but got: %s", pattern)
            count += 1
            time.sleep(2)
            continue
        
        try:
            interval = int(pattern[1]) - int(pattern[0])
            logger.info("Calculated interval: %d", interval)
        except Exception as e:
            logger.error("Error converting patterns to int: %s", e)
            count += 1
            time.sleep(2)
            continue
        
        if interval < ra_min or interval > ra_max:
            logger.error("ERR: Time interval %d is not in the right range [%d, %d]!", interval, ra_min, ra_max)
            return False
        
        count += 1
    return True


def check_wan_dad():
    tcpdump_log = ''.join(os.popen('/usr/sbin/tcpdump -vvv -r /tmp/dump-file'))
    logger.info(tcpdump_log)
    cmd = "/usr/sbin/tcpdump -vvv -r /tmp/dump-file |grep 'neighbor solicitation'"
    output = ''.join(os.popen(cmd))
    logger.info(output)
    if output == '':
        return False
    return True
