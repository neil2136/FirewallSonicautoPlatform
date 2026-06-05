from definition.settings import Parameter, PC1_LOGIN, re, time
from runner.settings import logger


def query_category_result(domain_list: list):
    rc = True
    for domain in domain_list:
        logger.info(f"{f' Do Dig Query For {domain} ':.^70}")
        digRes = check_dns_query_no_error(domain)
        if not digRes:
            logger.error(f'Failed to dig {domain}')
            rc = False
        logger.info(f'{rc} \n')
    return rc


def check_dns_query_no_error(domain: str, opt=""):
    if not domain:
        logger.error('Domain cannot be NULL!!')
        return False

    cmd = f'dig {domain} @{Parameter.FIREWALL} {opt}'
    error_1 = 'no servers could be reached'
    error_2 = 'connection timed out'
    for i in range(3):
        logger.info(f'Run for {i+1} times...')
        time.sleep(3)
        output = PC1_LOGIN.send_command(cmd)
        time.sleep(2)
        rc = not re.search(f'{error_1}|{error_2}', str(output))
        if rc:
            return True
    else:
        logger.error('Failed to get valid dns reply!')
        return False
