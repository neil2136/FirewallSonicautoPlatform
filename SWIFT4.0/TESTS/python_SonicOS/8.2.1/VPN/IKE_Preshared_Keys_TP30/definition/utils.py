from runner.settings import Params, logger
import time


def check_nbstat_query_in_pcapng(pc_obj, tshark_filter):
    cmd = f'tshark -R "ip.src=={tshark_filter["src"]} and ip.dst=={tshark_filter["dst"]}" ' \
          f'-r /tmp/packet-c.pcapng -V -T text'
    filterpcapng = pc_obj.send_command(cmd)
    logger.info(f'fitter pcapng file result: {filterpcapng}')
    filterlists = [
        'Dst Port: netbios-ns (137)',
        'Response: Message is a response',
        'Type: NBSTAT',
        'Class: IN',
        'Name: WINDOWS7_SSOCLI<00>',
        'Name: WINDOWS7_SSOCLI<20>']
    return all(x in filterpcapng for x in filterlists)


def check_capture_packets(packets, filter_list):
    packets = packets.split('Packet number: ')
    logger.info(f'packet filter list: {filter_list}')
    for packet in packets:
        checkres = [x in str(packet) for x in filter_list]
        logger.info(f'check packet result: {checkres}')
        if all(checkres):
            return True, packet
    return False, ''


def pc_traffic_send(pc_obj, kwargs):
    if kwargs['type'] == 'ping':
        res = pc_obj.ping_from_eth(ip=kwargs['des'], eth=kwargs['eth'], num=10)
        return res
    if kwargs['type'] == 'cmd':
        res = pc_obj.send_command(kwargs['cmd'])
        return res
    if kwargs['type'] == 'http':
        res = requests.get(kwargs['url'])
        return True if res.status_code == 200 else False
    if kwargs['type'] == 'script':
        res = pc_obj.send_command(f'python3 {kwargs["path"]}protocolsend.py -t {kwargs["protocol"]} -u {kwargs["url"]}')
        return res
    if kwargs['type'] == 'nslookup':
        res = pc_obj.send_command(f'python3 {kwargs["path"]}nslookup.py -t {kwargs["protocol"]} -u {kwargs["url"]}')
        return res
    if kwargs['type'] == 'sleep':
        logger.info(f'wait {kwargs["time"]}s to fw capture.')
        time.sleep(kwargs['time'])
        return f'sleep kwargs["time"]'


def fw_packet_monitor_run(packet_obj, pc_obj, kwargs):
    packetres = ''
    logger.info('start run FW packet monitor...')
    clearres = packet_obj.clear_packets()
    logger.info(f'clear packets on FW result: {clearres}')
    startres = packet_obj.start_capture()
    logger.info(f'start packets on FW result: {startres}')

    res = pc_traffic_send(pc_obj, kwargs)
    logger.info(f'pc traffic send result: {res}')

    stopres = packet_obj.stop_capture()
    logger.info(f'start packets on FW result: {stopres}')
    if 'packet' in kwargs.keys():
        if kwargs['packet'] == 'pcapng':
            packetres = packet_obj.export_captured_packets_pcapng()
    else:
        packetres = packet_obj.export_captured_packets()
    logger.info('run packet monitor end...')
    return res, packetres
