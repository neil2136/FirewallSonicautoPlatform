from runner.settings import Params, logger
import time
from definition.settings import packetmonitorapi, PC1_login, PC4_ETH1_IP


def fw_packet_monitor_run():
    logger.info('start run FW packet monitor...')
    clearres =packetmonitorapi.clear_packets()
    logger.info(f'clear packets from FW result: {clearres}')
    startres = packetmonitorapi.start_capture()
    logger.info(f'start capture from FW result: {startres}')
    res = PC1_login.ping_from_eth(ip=PC4_ETH1_IP, eth='eth1')
    time.sleep(5)
    logger.info(f'pc traffic send result: {res}')
    packetres = packetmonitorapi.export_captured_packets()
    stopres = packetmonitorapi.stop_capture()
    logger.info(f'stop capture from FW result: {stopres}')
    return res, packetres


def check_capture_packets(filter_list):
    res, packets = fw_packet_monitor_run()
    packets = packets.split('Packet number: ')
    # logger.info(packets)
    logger.info(f'packet filter list: {filter_list}')
    for packet in packets:
        checkres = [x in str(packet) for x in filter_list]
        logger.info(f'check packet result: {checkres}')
        if all(checkres):
            logger.info(packet)
            return True, packet
    return False, ''
