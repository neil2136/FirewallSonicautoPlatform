from runner.settings import Params, logger
import re


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


def check_max_routes_packets(packets, filter_list):
    res = {}
    packets = packets.split('Packet comments')
    logger.info(f'packet filter list: {filter_list}')
    for packet in packets:
        checkres = [x in str(packet) for x in filter_list]
        if all(checkres):
            findres = re.findall('IP Address: \d+.\d+.\d+.\d+, Metric: \d+', packet)
            logger.info(f'march ip and metric count: {len(findres)}')
            if len(findres) >= 24:
                logger.info('the first packet include >= 24 RTEs')
                res['first'] = True
            elif len(findres) >= 6:
                logger.info('the second packet include >= 6 RTEs')
                res['second'] = True
                break
    logger.info(f'check first and second rip packet: {res}')
    return res.values()
