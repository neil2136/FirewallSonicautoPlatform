from definition.settings import pkt_api, logger


def init_packet_capture():
    clear_res = pkt_api.clear_packets()
    logger.info(f'clear packet capture result: {clear_res}')
    start_res = pkt_api.start_capture()
    logger.info(f'clear packet capture result: {start_res}')
