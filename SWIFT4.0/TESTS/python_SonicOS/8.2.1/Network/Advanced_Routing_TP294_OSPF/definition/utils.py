from runner.settings import Params, logger
from definition.settings import Parameter
import re
import csv


def check_pcapng_packets(packets, filter_list):
    packets = packets.split('Packet comments')
    logger.info(f'packet filter list: {filter_list}')
    for packet in packets:
        checkres = [x in str(packet) for x in filter_list]
        logger.info(f'check packet result: {checkres}')
        if all(checkres):
            logger.info(packet)
            return True, packet
    return False, ''


def check_interval_packets(packets, filter_list):
    x2counts = 0
    x3counts = 0
    packets = packets.split('Packet comments')
    logger.info(f'packet filter list: {filter_list}')
    for packet in packets:
        checkres = [x in str(packet) for x in filter_list]
        logger.info(f'check packet result: {checkres}')
        if all(checkres):
            if 'Source: ' + Parameter.X2_IP in packet:
                x2counts += 1
            elif 'Source: ' + Parameter.X3_IP in packet:
                x3counts += 1
            else:
                logger.info('source ip not march x2 or x3.')
    logger.info(f'check x2 counts: {x2counts}, check x3 counts: {x3counts}')
    return x2counts, x3counts


def get_route_list_in_type(rtype='rip'):
    route_list_url = 'api/sonicos/dynamic-file/getRouteList.json?reqType='
    if rtype == 'rip':
        url = route_list_url + '4096'
    elif rtype == 'ospfv2':
        url = route_list_url + '256'
    elif rtype == 'ospfv3':
        url = route_list_url + '65536'
    elif rtype == 'riping':
        url = route_list_url + '1048576'
    else:
        logger.info('Please input a vaild route type: rip/ospfv2/ospfv3/riping')
        return ''
    response = self.fw.api_get(url)
    return response


def str_2_csv(text, decimal="|"):
    lines = csv.reader(text.split(decimal))
    return [line for line in lines][1:]


# def set_ospf2(self, msg=False, **kwargs):
#     if 'priority' in kwargs.keys():
#         cgi += 'ZOspfIfPriority=' + kwargs['priority'] + '&'
#     else:
#         cgi += 'ZOspfIfPriority=1&'

# class RouteCli():
    # def show_nsm_database(self):
    #     commands = ['show routing nsm database']
    #     result = self.fw.do_cli_commands(commands, tag=1)[1]
    #     return result
