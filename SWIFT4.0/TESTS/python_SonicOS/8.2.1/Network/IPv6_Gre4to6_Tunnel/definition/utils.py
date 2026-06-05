from definition.settings import *


def init_packet_capture():
    pkt_api.clear_packets()
    pkt_api.clear_packets()
    pkt_api.start_capture()

