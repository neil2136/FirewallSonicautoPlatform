import subprocess
from definition.settings import logger, pkg_api, Parameter

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


def fw_packet_monitor_clear_start():
    logger.info('start run FW packet monitor...')
    clear_res = pkg_api.clear_packets()
    logger.info(f'clear packets on FW result: {clear_res}')
    start_res = pkg_api.start_capture()
    logger.info(f'start packets on FW result: {start_res}')
    return clear_res & start_res


def fw_packet_monitor_stop_export(pc_login, cmd):
    stop_res = pkg_api.stop_capture()
    logger.info(f'stop packets on FW result: {stop_res}')
    pkg_api.export_captured_packets_pcapng()
    dns_cmd = f'tshark -R "{cmd}" -r /tmp/packet-c.pcapng -V -T text'
    logger.info(f'filter dns cmd: {dns_cmd}')
    filtered_packets = pc_login.send_command(dns_cmd)
    logger.info('run packet monitor end...')
    return filtered_packets

def failed_queries():
    logger.info('Start queries to dns server ......')
    domains = [
        'pc2.baidu.com',
        'pc3.baidu.com',
        'pc4.baidu.com',
        'pc5.baidu.com',
        'pc6.baidu.com',
        'www.baidu.com',
        '1.baidu.com',
        '2.baidu.com',
        '3.baidu.com',
        '4.baidu.com',
        '5.baidu.com',
        '6.baidu.com',
        '7.baidu.com',
        '8.baidu.com',
        '9.baidu.com',
        '10.baidu.com',
        '11.baidu.com',
        '12.baidu.com',
        '13.baidu.com',
        '14.baidu.com',
        '15.baidu.com',
        '16.baidu.com',
        '17.baidu.com',
        '18.baidu.com',
        '19.baidu.com',
        '20.baidu.com',
        '21.baidu.com',
        '22.baidu.com',
        '23.baidu.com',
        '24.baidu.com',
        '25.baidu.com',
        '26.baidu.com',
        '27.baidu.com',
        '28.baidu.com',
        '29.baidu.com',
        '30.baidu.com',
        '31.baidu.com',
        '33.baidu.com',
        '32.baidu.com'
    ]
    for domain in domains:
        domain = domain.strip()
        with subprocess.Popen(
            ["dig", "+short", "+retry=0", domain, f"@{Parameter.FIREWALL}"], stdout=subprocess.DEVNULL):
            pass
    logger.info('END')
