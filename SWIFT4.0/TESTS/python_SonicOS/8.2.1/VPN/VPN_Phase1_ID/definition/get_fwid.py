from definition.settings import *


def get_fw_id(dut='local'):
    logger.info('show fw status')
    fw_id = None
    rc = False
    fw_cli = Firewall(Parameter.DUT, user='admin', password='password', supported_config_mode='cli-ssh')
    rm_cli = Firewall(Parameter.REMOTEX1, user='admin', password='password', supported_config_mode='cli-ssh')
    res, sta_info = fw_cli.do_cli_commands(['show status'], 1)
    if dut == 'remote':
        res, sta_info = rm_cli.do_cli_commands(['show status'], 1)
    sta_list = sta_info.split('\n')
    for reg in sta_list:
        if re.search('Serial Number.*', reg, re.I|re.M):
            fw_id = reg.replace(' ', '').split(':')[1]
            logger.info(fw_id)
            rc = True
            break
    if rc == False:
        logger.info('cannot get fw id, define it as NONE')
    return fw_id
