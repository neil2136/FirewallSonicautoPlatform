from runner.settings import logger
from tools.trafficGen import ScapyPacketSend
import time
import copy


def check_packets(orgpacket, expectpkt):
    flag = False
    logger.info('start search interface')

    for packet in orgpacket.split('Packet comments'):
        # 判断是否元组中所有字符都在字符串中。
        checkres = [x in packet for x in list(expectpkt.values())]
        logger.info(f'check packet result: {checkres}')
        if all(checkres):
            logger.info('packet is found :{}'.format(packet))
            flag = True
            break
    return flag

    #     # it will print a list: [True, True, True, True, True, True]

    # for packet in orgpacket.split('Packet comments'):
    #     if expectpkt['src'] in packet:
    #         if expectpkt['dst'] in packet:
    #             if expectpkt['in'] in packet:
    #                 if expectpkt['out'] in packet:
    #                     if expectpkt['proto'] in packet:
    #                         logger.info(
    #                             '{} packet is found :{}'.format(fwport, packet))
    #                         flag = True
    #                         break
    # return flag


def fw_packet_monitor_run(**kwargs):
    # option_icmp = {
    #     'packetobj': pkgmonitorapi,
    #     'pc1obj': PC1_Login,
    #     'protocol': 'icmp',
    #     'icmp_dict': icmp_dict,
    #     'tos': '0x96'
    # }
    # option_icmpv6 = {
    #     'packetobj': pkgmonitorapi,
    #     'pc1obj': PC1_Login,
    #     'protocol': 'icmpv6',
    #     'pc4obj': PC4_Login,
    #     'tos': 20
    # }

    scapysend = ScapyPacketSend(iface='eth1', count=1)

    logger.info('start run FW packet monitor...')

    clearres = kwargs['packetobj'].clear_packets()
    logger.info(f'clear packets on FW result: {clearres}')

    startres = kwargs['packetobj'].start_capture()
    logger.info(f'start packets on FW result: {startres}')

    if kwargs['protocol'] == 'icmp':
        icmp_dict = copy.deepcopy(kwargs['icmp_dict'])
        icmp_dict['IP']['tos'] = kwargs['tos']
        sendicmpres = scapysend.send_icmp_packet(**icmp_dict)
        logger.info('Send icmp packet result:{}'.format(sendicmpres))
    elif kwargs['protocol'] == 'icmpv6':
        sendres = kwargs['pc4obj'].send_command(
            "python3 {} -tc {}".format('/tmp/send_icmpv6.py', kwargs['tos']))
        logger.info('Send icmpv6 packet result : {}'.format(sendres))

    time.sleep(5)
    stopres = kwargs['packetobj'].stop_capture()
    logger.info(f'stop packets on FW result: {stopres}')

    kwargs['packetobj'].export_captured_packets_pcapng()
    protocol = kwargs['protocol']
    filterdnscmd = f'tshark -R "{protocol}" -r /tmp/packet-c.pcapng -V -T text'
    logger.info(f'filterdnscmd: {filterdnscmd}')

    filteredpackets = kwargs['pc1obj'].send_command(filterdnscmd)
    logger.info('run packet monitor end...')

    return filteredpackets
