import re
from runner.settings import Params, logger
from definition.settings import scripts_path, PC3_login, snmpapi, Parameter


def login_fw_in_pc(ip, action='login', msg='Successfully login'):
    command = f'python3 {scripts_path}LoginDUTFromInterface.py -i {ip} -a {action}'
    res = PC3_login.send_command(command)
    result = True if re.search(msg, res) else False
    return result


def add_snmp_group_auth(**snmp_option):
    # Add a snmp group, a user and an access
    try:
        group_res = snmpapi.add_snmp_group(name=snmp_option['user_group'])
        if group_res:
            user_res = snmpapi.snmp_user_add(**snmp_option)
            if user_res:
                access_res = snmpapi.snmp_access_add(**snmp_option)
                if access_res:
                    return True
                else:
                    logger.info('ERR: Add snmp access failed!')
            else:
                logger.info('ERR: Add snmp user failed!')
        else:
            logger.info('ERR: Add snmp group failed!')
        return False
    except BaseException:
        logger.error("ERR: fail to add snmp configurations!")
    return False


def nat_icmp_check(resp, src_ip, dst_ip):
    packets = resp.split('Packet number: ')
    icmptype = 'ICMP Type = 8'
    srcip = f"Src=[{src_ip}]"
    dstip = f"Dst=[{dst_ip}]"
    for packet in packets:
        if icmptype in packet:
            if srcip in packet:
                if dstip in packet:
                    return True, packet
    return False, False


# need add to lib api class file
# from modules.API.network import FailoverLbApi
# class FailoverLbApi(FailoverLbApi):
#     '''DynamicRoutingApi class'''




