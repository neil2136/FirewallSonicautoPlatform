import re
import json
from csv import DictReader
from io import StringIO
from runner.settings import logger


def get_dynamic_route_hit_time_in_tsr(tsr_routing, range_begin):
    hittime = ''
    route_sp = tsr_routing.split('\n\n\n')
    for route in route_sp:
        if f'rangeBegin: {range_begin}' in route:
            logger.info(f'get ipv6 pbr from tsr is {route}')
            hittime = re.search('(?<=Time Last Hit:   )\d+/\d+/\d+\s+\d+:\d+:\d+.\d+', route, re.I | re.S).group()
            return hittime
    return hittime


def get_d_route_interface(routepolres, route_dst):
    routepolstring = routepolres.replace("|", "\n\n")
    csv_file = StringIO(routepolstring)
    csv_dict_reader = DictReader(csv_file)
    # Iterate over each row in the CSV file
    for row in csv_dict_reader:
        routepolicy = json.loads(json.dumps(row))
        # logger.info(f'routepolicy is:{routepolicy}')
        if 'Dynamic_Route' in routepolicy['name'] and routepolicy['dst'] == route_dst:
            logger.info(f'routepolicy is :{routepolicy}')
            return routepolicy['ifName']


def icmp_traffic_check(resp, **kwargs):
    request = False
    packets = resp.split('Packet number: ')
    packetin = f"in:{kwargs['iface_in']}"
    packetout = f"out:{kwargs['iface_out']}"
    icmptype = 'ICMP Type = 128'
    srcip = f"Src=[{kwargs['src_ip']}]"
    dstip = f"Dst=[{kwargs['dst_ip']}"
    status = 'Forwarded'
    tuples = (packetin, packetout, icmptype, srcip, dstip, status)
    for packet in packets:
        if all(x in packet for x in tuples):
            request = True
    logger.info(f'resuest is {request}')
    logger.info(f'request is {request}')
    if request:
        repacketin = f"in:{kwargs['iface_out']}"
        repacketout = f"out:{kwargs['iface_in']}"
        reicmptype = 'ICMP Type = 129'
        resrcip = f"Src=[{kwargs['dst_ip']}]"
        redstip = f"Dst=[{kwargs['src_ip']}]"
        retuples = (repacketin, repacketout, reicmptype, resrcip, redstip, status)
        for packet in packets:
            if all(x in packet for x in retuples):
                return True, packet
    else:
        return False,


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
                    if "X" in check_dict["interface"] or "TI" in check_dict["interface"]:
                        routelist = [f"'destination': '{check_route}'", f"'gateway': '{check_dict['gw']}'",
                                     f"'metric': {metric}",
                                     f"'interface': '{check_dict['interface']}'"]
                    else:
                        routelist = [f"'destination': '{check_route}'", "'gateway': '0.0.0.0'",
                                     f"'metric': {metric}",
                                     f"'interface': None", f"'interface': None"]
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


# # add by JLian
# def delete_router_bgp(self, AS):
#     # AS: 1-4294967295>
#     commands = ['configure', 'routing', 'bgp', 'configure terminal', 'no router bgp' + ' ' + str(AS)]
#     res, output = self.fw.do_cli_commands(commands, tag=1)
#     return res, output

# # add by JLian
# def show_in_routing_bgp(self, cmd):
#     commands = ['configure', 'routing', 'bgp', 'configure terminal', cmd]
#     res, output = self.fw.do_cli_commands(commands, tag=1)
#     return res, output

# # need to add into api/policy
# def get_route_pol_list(self):
#     logger.info(f'getObjectList get url: {self.getobject_url}')
#     objectlist = self.fw.api_get(self.getobject_url)
#     if isinstance(objectlist, dict) and "routePolArray" in objectlist.keys():
#         return objectlist["routePolArray"]
#     else:
#         return ''