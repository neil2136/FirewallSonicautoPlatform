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
    logger.info(f'dynamic_table:{dynamic_table}')
    logger.info(f'expected filter:{filter_tuple}')
    if all(x in dynamic_table for x in filter_tuple):
        logger.info(f'dynamic route found')
        flag = True
    return flag


def compare_ospf_info(conf1, conf2):
    x2_conf1 = re.search("interface X2(.*?)!", conf1, re.S).group(1)
    logger.info(f"X2 configuration before reboot is {x2_conf1}")
    x2_conf2 = re.search("interface X2(.*?)!", conf1, re.S).group(1)
    logger.info(f"X2 configuration after reboot is {x2_conf2}")
    ospf_conf1 = re.search("router ospf(.*?)!", conf2, re.S).group(1)
    logger.info(f"ospf configuration before reboot is {ospf_conf1}")
    ospf_conf2 = re.search("router ospf(.*?)!", conf2, re.S).group(1)
    logger.info(f"ospf configuration after reboot is {ospf_conf1}")
    flag = True if x2_conf1 == x2_conf2 and ospf_conf1 == ospf_conf2 else False
    return flag
