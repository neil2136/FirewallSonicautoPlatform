from runner.settings import logger
import time
import copy
import re


def start_dibbler_server(pc_obj):
    dibbler_log = ''
    cmd_list = [
        'killall -9 dibbler-server',
        'rm -rf /var/lib/dibbler/*',
        'rm -rf /var/log/dibbler.log',
        'touch /var/log/dibbler.log',
        'dibbler-server run >> /var/log/dibbler.log &',
        'timeout 5 cat /var/log/dibbler.log',
    ]
    for cmd in cmd_list:
        dibbler_log += pc_obj.send_command(cmd)
    if 'Interface ppp0/-1 is not present in the system' in dibbler_log:
        return False
    elif 'Accepting connections' in dibbler_log:
        return True
    else:
        return False


def get_interface_part_in_tsr(tsr_info, checklist):
    logger.info(checklist)
    interface_partten = "Blade_1_INTERFACES_START(.*)#Blade_1_INTERFACES_END"
    interface_rex = re.compile(interface_partten, re.DOTALL)
    mo1 = interface_rex.search(tsr_info)
    if mo1:
        interface_part = mo1.group(1)
        interface_list = interface_part.split('-----------------------------------------------------------------')
        for interface_info in interface_list:
            checkres = [x in interface_info for x in checklist]
            logger.info(f'check packet result: {checkres}')
            if all(checkres):
                pppoe_parttern = "\[IPv6 Settings\].*?IPv6 Addresses:(.*)?\[PPPOEv6 : Address Assignment Setting start\](.*)?\[PPPOEv6 : Address Assignment Setting end\]"
                pppoe_rex = re.compile(pppoe_parttern, re.DOTALL)
                mo2 = pppoe_rex.search(interface_info)
                if mo2:
                    ipv6_address_part = mo2.group(1)
                    logger.info(ipv6_address_part)
                    pppoe_setting_part = mo2.group(2)
                    return pppoe_setting_part
    else:
        logger.info("can't find interface part in tsr")
        return ''




