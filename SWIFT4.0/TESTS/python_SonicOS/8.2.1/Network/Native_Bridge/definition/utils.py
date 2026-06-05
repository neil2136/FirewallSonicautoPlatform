from runner.settings import logger
from tools.trafficGen import ScapyPacketSend
import time
import copy
import re


def check_packets(orgpacket, expectpkt, packet_from = "dut"):
    flag = False
    logger.info(f"expectpkt is {expectpkt}")
    if packet_from == "dut":
        split_words = "Packet comments"
    elif packet_from == "pc":
        split_words = "\n\nFrame "
    else:
        logger.info("you should specify the packet_from ")
        return flag
    for packet in orgpacket.split(split_words):
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
    filterdnscmd = 'tshark -r /tmp/packet-c.pcapng -V -T text'
    logger.info(f'filterdnscmd: {filterdnscmd}')

    filteredpackets = pcobj.send_command(filterdnscmd)
    logger.info('run packet monitor end...')

    return filteredpackets


def get_pc_int_mac(pc_obj, iface):
    iface_mac = pc_obj.send_command("ifconfig " + iface + " | grep ether | awk '{print $2}'")
    return iface_mac[:-1].lower()


def pc_get_ip_lease(pc, eth):
    res = False
    ip_addr = ''
    for i in range(10):
        pc.send_command('ifconfig {} 0.0.0.0'.format(eth))
        pc.send_command('timeout 20 killall dhclient')
        out = pc.send_command('timeout 20 dhclient -v {}'.format(eth))
        time.sleep(10)
        logger.info(out)
        m = re.search(
            r'bound to (13\.1\.1\.\d+).*renewal in', out, re.I)
        if m:
            ip_addr = m.group(1)
            logger.info(f'pc {eth} successfully get ip address {ip_addr}')
            res = True
            break
        else:
            logger.info(f'pc {eth} failed to get ip address')
    return res, ip_addr
