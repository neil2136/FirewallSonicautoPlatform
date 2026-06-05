import os
import sys
import re
import requests
from runner.settings import Params, logger

def check_packet(exportres, filter_tuple, filter_out='none'):
    flag = False
    packets = exportres.split('Packet comments\n ')
    for packet in packets:
        if all(x in packet for x in filter_tuple):
            logger.info(f'packet found : {packet}')
            if filter_out == 'none': 
                flag = True
                break
            else:
                packet_in = packet
                if filter_out not in packet_in:
                    flag = True
                    break
    return flag


def check_dynamic_table(dynamic_table, filter_tuple):
    flag = False
    if all(x in dynamic_table for x in filter_tuple):
        logger.info(f'dynamic route found')
        flag = True  
    return flag


####add in common lib

### API->network.py###
#DynamicRoutingApi
    # default_rip_settings 
    # default_ospf_settings
    # def get_vlan_index(self, name, vlan):
    # def rip_setting(self, msg=False, **kwargs):
    # def ospf_setting(self, msg=False, **kwargs):

### CLI->network.py ###
#RouteCli 
    # def clear_ospf(self):
    #     commands = ['configure', 'routing', 'ospf', 'clear ip ospf process']
    #     result = self.fw.do_cli_commands(commands)
    #     return result

###utm.py###
#FirewallAPI
    #def api_get_header(self, url, params=None, headers=headers1,nologin=False, log_switch=True):

