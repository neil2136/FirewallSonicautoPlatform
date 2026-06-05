from definition.settings import Parameter, PC1_LOGIN, logMonitor_api, time, re, logger


def do_DNS_query_from_client(domain: str):
    if not domain:
        logger.error('Domain cannot be NULL!!')
        return ''
    cmd = f'dig {domain} @{Parameter.FIREWALL}'
    logger.info(f'start send DIG cmd: {cmd}')
    return PC1_LOGIN.send_command(cmd)


def check_dns_query_no_error(domain: str):
    error_1 = 'no servers could be reached'
    error_2 = 'connection timed out'
    for i in range(3):
        logger.info(f'Query dns for {i+1} times...')
        time.sleep(3)
        output = do_DNS_query_from_client(domain)
        time.sleep(2)
        rc = not re.search(f'{error_1}|{error_2}', str(output))
        if rc:
            return True
    logger.error('Failed to get valid dns reply!')
    return False


def check_related_logs(target=''):
    rc = logMonitor_api.export_log_txt(log_switch=False)
    logger.info(rc)
    return target in rc
