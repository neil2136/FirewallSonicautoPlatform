from runner.settings import logger
import time
import copy


def check_packets(orgpacket, expectpkt):
    flag = False
    logger.info(f"expectpkt is {expectpkt}")
    for packet in orgpacket.split("Packet comments"):
        checkres = [x in packet for x in expectpkt]
        logger.info(f'check packet result: {checkres}')
        if all(checkres):
            logger.info('packet is found :{}'.format(packet))
            flag = True
            break
    return flag


def fw_packet_monitor_clear_start(packetobj):
    logger.info('start run FW packet monitor...')

    clearres = packetobj.clear_packets()
    logger.info(f'clear packets on FW result: {clearres}')

    startres = packetobj.start_capture()
    logger.info(f'start packets on FW result: {startres}')

    return clearres & startres


def fw_packet_monitor_stop_export(packetobj, pcobj):
    stopres = packetobj.stop_capture()
    logger.info(f'stop packets on FW result: {stopres}')

    packetobj.export_captured_packets_pcapng()
    filterdnscmd = 'tshark -R "dns" -r /tmp/packet-c.pcapng -V -T text'
    logger.info(f'filterdnscmd: {filterdnscmd}')

    filteredpackets = pcobj.send_command(filterdnscmd)
    logger.info('run packet monitor end...')

    return filteredpackets