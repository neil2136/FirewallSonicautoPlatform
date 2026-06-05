import json
from runner.settings import logger


def get_dynamic_protocol_status_on_ti(dynamic_routingapi, ti, d_protocol='all_d_protocol'):
    output = dynamic_routingapi.get_route_advanced_data()
    logger.info(f'output is:{output}')
    ospfv2info = ''
    ripinfo = ''
    ospfv3info = ''
    ripnginfo = ''
    if f'"name": "{ti}"' not in json.dumps(output):
        logger.error(f'there is no tunnel interface {ti}')
        return ''
    else:
        ipv4interfaceinfo = output['data']['ipv4']['interfaces']
        ipv6interfaceinfo = output['data']['ipv6']['interfaces']
        for ipv4_interface in ipv4interfaceinfo:
            if f'"name": "{ti}"' in json.dumps(ipv4_interface):
                logger.info(f'niipv4info is :{ipv4_interface}')
                ripinfo = ipv4_interface['RIP']
                ospfv2info = ipv4_interface['OSPFv2']
        for ipv6_interface in ipv6interfaceinfo:
            if f'"name": "{ti}"' in json.dumps(ipv6_interface):
                logger.info(f'niipv6info is :{ipv6_interface}')
                ripnginfo = ipv6_interface['RIPng']
                ospfv3info = ipv6_interface['OSPFv3']
        logger.info(f'ospfv2info is {ospfv2info}')
        logger.info(f'ripinfo is {ripinfo}')
        logger.info(f'ospfv3info is {ospfv3info}')
        logger.info(f'ripnginfo is {ripnginfo}')
        if d_protocol == 'rip':
            return ripinfo
        if d_protocol == 'ripng':
            return ripnginfo
        if d_protocol == 'ospfv2':
            return ospfv2info
        if d_protocol == 'ospfv3':
            return ospfv3info
        if d_protocol == 'all_d_protocol':
            return ospfv2info, ripinfo, ospfv3info, ripnginfo


def check_droute_learned_from_ti_in_route_policy(route_policyapi, **check_dict):
    metric = ''
    if check_dict['d_protocol'] == 'ospfv2':
        metric = '110'
    if check_dict['d_protocol'] == 'rip':
        metric = '120'
    if check_dict['d_protocol'] == 'ebgp':
        metric = '20'
    droutoutput = route_policyapi.get_dynamic_route_policy()
    logger.info(f'drouteoutput is:{droutoutput}')
    reslist = []
    if droutoutput:
        for droute in droutoutput:
            for check_route in check_dict['route']:
                if check_route in str(droute):
                    routelist = [f"'destination': '{check_route}'", f"'interface': '{check_dict['interface']}'",
                                 f"'gateway': '{check_dict['gw']}'",
                                 f"'metric': {metric}"]
                    res = [i in str(droute) for i in routelist]
                    reslist += res

    return reslist


def get_interface_status(interface_v4api, inter_name):
    inter_status = ''
    statuslist = interface_v4api.get_interface_report_status()
    for status in statuslist:
        if f"'name': '{inter_name}'" in str(status):
            logger.info(f'{inter_name} output is :{status}')
            inter_status = status["status"]
            logger.info(f'interface status is:{inter_status}')
            break
    return inter_status


