from definition.settings import logger, pc1_ssh, pc2_ssh, pc3_ssh, pc4_ssh, packetmonitor_obj, time
import copy

# check no_nat policy
def check_no_nat_policy(allpolicies, lan_port='X0', wan_port='X1'):
    inbound_flag = False
    outbound_flag = False
    no_nat_inbound_std = {
            'name': 'Default NAT Policy',
            'inbound': wan_port,
            'outbound': lan_port,
            'translated_source': {'original': True},
            'translated_destination': {'original': True},
            'enable': True,
            'comment': 'Auto-added No-NAT Policy for Inbound to ' + lan_port,
            }

    no_nat_outbound_std = {
             'name': 'Default NAT Policy',
            'inbound': lan_port,
            'outbound': wan_port,
            'translated_source': {'original': True},
            'translated_destination': {'original': True},
            'enable': True,
            'comment': 'Auto-added No-NAT Policy for Outbound from ' + lan_port,
                }
    try:
        for i in allpolicies["nat_policies"]:
            i_backup = copy.deepcopy(i)
            if all([i["ipv4"].get(key) == value for key, value in no_nat_inbound_std.items()]):
                logger.info(
                    'Find Auto-added No-NAT Policy for Inbound to ' + lan_port + f' is.......{i_backup}')
                inbound_flag = True
            if all([i["ipv4"].get(key) == value for key, value in no_nat_outbound_std.items()]):
                logger.info(
                    'Find Auto-added No-NAT Policy for Outbound from ' + lan_port + f' is.......{i_backup}')
                outbound_flag = True
        return inbound_flag & outbound_flag

    except Exception as e:
        logger.info('!!!!can not find Auto-added No-NAT Policy!!!!')

# start fw capture
def fw_packet_monitor_run(**kwargs):
    logger.info('start run FW packet monitor...')
    clearres = kwargs['packet_obj'].clear_packets()
    logger.info(f'clear packets from FW result: {clearres}')
    startres = kwargs['packet_obj'].start_capture()
    logger.info(f'start capture from FW result: {startres}')
    res = kwargs['pc_login'].send_command(kwargs['cmd'])
    time.sleep(5)
    logger.info(f'pc traffic send result: {res}')
    if 'packet' in kwargs.keys() and kwargs['packet'] == 'pcapng':
        packetres = kwargs['packet_obj'].export_captured_packets_pcapng()
    else:
        packetres = kwargs['packet_obj'].export_captured_packets()
    stopres = kwargs['packet_obj'].stop_capture()
    logger.info(f'stop capture from FW result: {stopres}')
    return res, packetres

# analysis capture packets
def check_capture_packets(packets, filter_list):
    packets = packets.split('Packet number: ')
    logger.info(f'packet filter list: {filter_list}')
    for packet in packets:
        logger.info(f'packet show list: {packet}')
        checkres = [x in str(packet) for x in filter_list]
        if all(checkres):
            return True, packet
    return False, ''

