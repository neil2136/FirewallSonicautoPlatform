from definition.settings import *


def ping_from_remote_to_baidu():
    spe_ip = '0.0.0.0'
    url_list = ['www.baidu.com','www.google.com','www.bing.com','www.jd.com']
    for url in url_list:
        cmd = f'curl {url} -k -s -o /tmp/output.html' + " -w '%{http_code}'"
        logger.info(cmd)
        resp = PC2_login.send_command(cmd)
        logger.info(resp)
        if resp in ['200','201','301','302']:
            rc = True
            spe_ip = get_speip(url)
            logger.info(spe_ip)
            break
        else:
            rc = False
            logger.info("access to www.baidu.com from DUT failed")
            logger.info("ping local host from remote")
            ping_info = PC2_login.send_command("ping {} -c 5".format(PC1_eth0))
            logger.info(ping_info)
    return rc, spe_ip

def get_speip(url):
    try:
        # Run ping command and capture output
        cmd = f"ping -c 1 {url} | grep -oE '([0-9]{{1,3}}\.){{3}}[0-9]{{1,3}}' | head -1"
        ip_addr = PC2_login.send_command(cmd).strip()
        
        if ip_addr and len(ip_addr.split('.')) == 4:
            logger.info(f"Resolved IP for {url}: {ip_addr}")
            return ip_addr
            
        logger.error(f"Failed to extract IP from ping output for {url}")
        return "0.0.0.0"
        
    except Exception as e:
        logger.error(f"Error pinging {url}: {str(e)}")
        return "0.0.0.0"

def ping_from_remote_to_spe_ip(spe_ip):
    logger.info(" {} ".center(20, '-').format('Initiate pings'))
    rc = False
    for i in range(10):
        out = PC2_login.send_command("ping {} -c 1".format(spe_ip))
        if ' 0% packet loss' in str(out):
            logger.info('Successfully initiated continuous traffic from remote to local NAT.')
            logger.info(out)
            rc = True
            break
        elif i == 9:
            logger.info('Ping failed')
            logger.info(out)
            rc = False
    return rc


def ping_traffic_blocked():
    logger.info(" {} ".center(20, '-').format('Initiate pings'))
    rc = False
    for i in range(10):
        out = PC2_login.send_command("ping {} -c 1".format(PC1_eth0))
        if '100% packet loss' in str(out):
            logger.info('Ping from remote to local failed')
            rc = True
            break
        elif i == 9:
            logger.info('Ping from remote to local passed')
            logger.info(out)
            rc = False
    return rc


def ping_from_local_to_remote():
    logger.info(" {} ".center(20, '-').format('Initiate pings'))
    rc = False
    for i in range(10):
        out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
        if '100% packet loss' not in str(out):
            logger.info('Successfully initiated continuous traffic from remote to local NAT.')
            logger.info(out)
            rc = True
            break
        elif i == 9:
            logger.info('Ping failed')
            logger.info(out)
            rc = False
    return rc


def ping_from_remote_to_local():
    logger.info(" {} ".center(20, '-').format('Initiate pings'))
    rc = False
    for i in range(10):
        out = PC2_login.send_command("ping {} -c 1".format(PC1_eth0))
        if '100% packet loss' not in str(out):
            logger.info('Successfully initiated continuous traffic from remote to local NAT.')
            logger.info(out)
            rc = True
            break
        elif i == 9:
            logger.info('Ping failed')
            logger.info(out)
            rc = False
    return rc


def check_test_log(dut, ref1):
    logger.info(" {} ".center(20, '-').format('Test log'))
    time.sleep(2)
    log = str(LLogObj.export_log_txt(log_switch=False))
    if dut == "remote":
        log = str(RLogObj.export_log_txt(log_switch=False))

    flag = 0
    reg1 = re.search('{} Mode complete'.format(ref1['ike_exchange']), log, re.I|re.M)
    reg2 = re.search('IKE negotiation complete', log, re.I|re.M)
    reg3 = re.search('IKEv2 negotiation complete', log, re.I|re.M)

    if reg1:
        flag = 1
        logger.info(reg1.group())
    if reg2:
        flag += 1
        logger.info(reg2.group())

    if flag == 2:
        logger.info('Test log passed.')
        logger.info("flag={}".format(flag))
        rc = True
    elif reg3:
        logger.info('Test log passed.')
        logger.info(reg3.group())
        rc = True
    else:
        logger.info('Test log failed.')
        logger.info("Test log show:{}".format(log))
        rc = False
    return rc


def check_failure_test_log():
    logger.info(" {} ".center(20, '-').format('Test log'))
    time.sleep(2)
    log = str(LLogObj.export_log_txt(log_switch=False))
    reg = re.search('IPsec proposal does not match \(Phase 2\)', log, re.I|re.M)
    if reg:
        logger.info(reg.group())
        logger.info('Test log passed.')
        rc = True
    else:
        logger.info('Test log failed.')
        logger.info("Test log show:{}".format(log))
        rc = False
    return rc
