import re
import time
from runner.settings import logger


def check_packet_requery(dnsserver, exportres, ao_value):
    query_count = 0
    packets = exportres.split('Packet comments\n ')
    filter_tuple = (dnsserver, ao_value, 'type A,',
                    'Domain Name System (query)')
    for packet in packets:
        if all(x in packet for x in filter_tuple):
            query_count += 1
    logger.info(f'query_count to {dnsserver} is {query_count}')
    return query_count


def check_packet_response_udp(exportres, ao_value):
    lesshosts = ''
    packets = exportres.split('Packet comments\n ')
    filter_tuple = (ao_value, 'type A,', 'UDP',
                    'Domain Name System (response)')
    for packet in packets:
        if all(x in packet for x in filter_tuple):
            hostspart = re.search(r'Answers\n(.*)\n',
                                  packet, re.I | re.S | re.M)
            if hostspart:
                lesshosts = hostspart.group(1)
                break
    if not lesshosts:
        logger.info('cannot get dns response\n')
    return lesshosts


def check_packet_response_tcp(exportres, ao_value):
    morehosts = ''
    packets = exportres.split('Packet comments\n')
    filter_tuple = (ao_value, 'type A,', 'TCP',
                    'Domain Name System (response)')
    for packet in packets:
        if all(x in packet for x in filter_tuple):
            hostspart = re.search(r'Answers\n(.*)\n',
                                  packet, re.I | re.S | re.M)
            if hostspart:
                morehosts = hostspart.group(1)
                break
    if not morehosts:
        logger.info('cannot get dns response\n ')
    return morehosts


def fw_packet_monitor_run(packet_obj, pc_obj, ao_obj, ao_name, sleeptime=15):
    logger.info('start run FW packet monitor...')
    ao_obj.purge_ao_by_name(ao_name, 'fqdn')
    logger.info('------purge fqdn------')
    pkt_setting_dict = {
        'display_filter': {
            'bidirectional': True,
            'destination_ips': '',
            'destination_ports': '53',
        }
    }
    confpkgres = packet_obj.conf_packmon(**pkt_setting_dict)
    logger.info('start capture result:{}'.format(confpkgres))

    clearres = packet_obj.clear_packets()
    logger.info(f'clear packets on FW result: {clearres}')
    startres = packet_obj.start_capture()
    logger.info(f'start packets on FW result: {startres}')

    ao_obj.resolve_ao_by_name(ao_name, 'fqdn')
    logger.info('------resolve fqdn-------')
    time.sleep(sleeptime)
    stopres = packet_obj.stop_capture()
    logger.info(f'start packets on FW result: {stopres}')

    packet_obj.export_captured_packets_pcapng()
    filterdnscmd = 'tshark -R "dns" -r /tmp/packet-c.pcapng -V -T text'
    dnsfilteredpackets = pc_obj.send_command(filterdnscmd)
    logger.info('run packet monitor end...')

    return dnsfilteredpackets


def check_TSR(diagnostic_obj, table, aoname):
    aopart = ''
    # table is 'Address Object Table' or 'Address Group Table'
    tsr = diagnostic_obj.get_tsr_part(
        'Network', 'Address Objects', table)
    pattern = '-------' + aoname + '-------\n(.*?)Time Created'
    aopartres = re.search(pattern, tsr, re.M | re.I | re.S)
    if aopartres:
        aopart = aopartres.group(0)
        logger.info(f'{aoname} TSR Part is found:\n{aopart}\n')
    else:
        logger.info(f'{aoname} TSR Part is not found:{aopart}\n')
    return aopart


def get_pc_mac(pc_obj, eth_name):
    mac_org = ''
    mac = ''
    if eth_name == 'eth0':
        mac_org = pc_obj.send_command(
            "ifconfig eth0|grep HWaddr|awk '{print $5}'").strip('\n')
    elif eth_name == 'eth2':
        mac_org = pc_obj.send_command(
            "ifconfig eth2|grep HWaddr|awk '{print $5}'").strip('\n')
    else:
        logger.info('Please specify interface name of pc')
    b = mac_org.split(':')
    mac = ''.join(b)
    return mac_org, mac


def get_pc_linklocal(pc_obj, eth_name):
    linklocal = ''
    if eth_name == 'eth0':
        linklocal = pc_obj.send_command(
            "ifconfig eth0|grep fe80|awk '{print $3}'").split('/')[0]
    elif eth_name == 'eth2':
        linklocal = pc_obj.send_command(
            "ifconfig eth2|grep fe80|awk '{print $3}'").split('/')[0]
    else:
        logger.info('Please specify interface name of pc')
    return linklocal


def search_log(base_time, log, search_filters):
    time_array = time.strptime(
        log['time'], '%m/%d/%Y %H:%M:%S')
    logger.info(f'time_array in log is : {time_array}')
    if time_array >= base_time:
        logger.info(
            'fw log time is : {}'.format(log['time']))
        if all(filter in str(log) for filter in search_filters):
            return True
    else:
        return False


def check_log_by_time(fw_time, fw_logs, search_filters):
    flag = False
    if type(fw_time) is dict:
        part_time = fw_time['time']['date'].replace(
            ':', '/') + ' ' + fw_time['time']['time']
        base_time = time.strptime(part_time, '%Y/%m/%d %H:%M:%S')
        logger.info(f'fw system base_time is : {part_time}')
        if type(fw_logs) is list:
            for log in fw_logs:
                if search_log(base_time, log, search_filters):
                    logger.info(f'the match log event in : {log}')
                    flag = True
        elif type(fw_logs) is dict:
            if search_log(base_time, fw_logs, search_filters):
                logger.info(f'the match log event in : {fw_logs}')
                flag = True
        else:
            logger.info('fw_logs is not list or dict.')
    else:
        logger.info('fw_time is not dict.')
    return flag


def wait_arp_timeout(arp_obj, mac):
    flag = False
    sleep_time = 30
    keylist = [f"'mac_address': {mac}",
               "'timeout': 'Expires in 0 minutes'"]
    try:
        for each in range(0, 8):
            time.sleep(sleep_time)
            arpcaches = arp_obj.show_arp_caches()
            if mac in str(arpcaches):
                for arpcache in arpcaches:
                    if all(x in arpcache for x in keylist):
                        logger.info("arp entry is :{}".format(arpcache))
                        flag = True
            else:
                flag = True

            if flag:
                logger.info(
                    f'{mac} in arp is detele after {(each + 1)*sleep_time}s')
                break
            else:
                logger.info(
                    f'{mac} in arp is still existed after {(each + 1)*sleep_time}s')
        return flag
    except Exception as e:
        logger.info("expected arpcache not found with error {}".format(repr(e)))
