from runner.settings import Params, logger
from definition.settings import PC1_login, Parameter, statusapi, fwupgradeapi, restartapi
import time
import re


def upgrade_firewall_software(path, bulidtype='old'):
    bootres = False
    logger.info('start upload firmware from api...')
    resp = fwupgradeapi.upload_firmware_by_message(path)
    if resp:
        logger.info('start check uploaded result...')
        if re.search('Firmware uploaded successfully', resp, re.I):
            logger.info('Firmware uploaded successfully...')
            logger.info('start boot fw with configure...')
            bootres = fwupgradeapi.boot_fw(mode=3)
            if bootres:
                logger.info('boot fw with configure successfully...')
                logger.info('wait 200s to make sure fw will auto restart...')
                time.sleep(200)
                try:
                    # force restart fw when boot process has a long response time.
                    output = PC1_login.ping(Parameter.FIREWALL)
                    if output:
                        res = restartapi.restart_now()
                        logger.info(f'force restart result: {res}')
                except Exception as e:
                    logger.info('not need restart beacuse fw is being restart...')
                    logger.info(repr(e))
                retries = 1
                while retries < 31:
                    logger.info(f'retry count: {retries}')
                    logger.info('Sleep 30s waiting for fw up.')
                    time.sleep(30)
                    try:
                        output = PC1_login.ping(Parameter.FIREWALL)
                        if output:
                            checkversion = statusapi.show_version()
                            if checkversion:
                                logger.info("upgrade firmware previous successful...")
                                bootres = True
                                break
                        else:
                            retries += 1
                    except Exception as e:
                        logger.info('check current fw accessed failed, need retry...')
                        logger.info(repr(e))
            else:
                logger.info('boot fw with configure failed...')
        elif re.search('same Firmware already exists', resp, re.I):
            if bulidtype == 'old':
                logger.info('the same Firmware already exists, do not need upgrade version')
                bootres = True
            else:
                logger.info(
                    'error: previous version can not upgrade successful in the steps above.')
                return False
    else:
        logger.info('send upload_firmware_by_message api failed.')
        bootres = False
    return bootres


def get_pc_eth_ip(pc, eth):
    output = pc.send_commands(["ifconfig "+eth+" | grep 'inet 192' | awk '{print $2}'"])
    return output


def get_ip_lease_in_pc(pc_login, eth):
    res = False
    rang_ip_part = '192.168.2.8'
    cmds = [f'ifconfig {eth} 0.0.0.0', 'timeout 20 killall dhclient']
    pc_login.send_commands(cmds)
    for i in range(5):
        time.sleep(3)
        res = pc_login.send_command('timeout 20 dhclient -v {}'.format(eth))
        time.sleep(10)
        logger.info(f'run dhcp client on pc: {res}')
        if f'bound to {rang_ip_part}' in res:
            res = True
            break
        else:
            logger.info(f'pc {eth} failed to get ip address')
    return res
