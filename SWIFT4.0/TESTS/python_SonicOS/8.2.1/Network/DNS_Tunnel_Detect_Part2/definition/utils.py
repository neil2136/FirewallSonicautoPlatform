from definition.settings import *


def check_dns_pkts(status):
    cls_res = pktapi.clear_packets()
    logger.info(f'clear packet monitor result: {cls_res}')
    start_res = pktapi.start_capture()
    logger.info(f'start packet monitor result: {start_res}')
    pc1_login.send_command(f'python3 {script_file} dns_query')
    time.sleep(3)
    stop_res = pktapi.stop_capture()
    logger.info(f'stop packet monitor result: {stop_res}')
    packets = pktapi.export_captured_packets()

    flag = []
    packet_list = packets.split('Packet number:')
    check_list = ['Dst=[53]', status]
    for pkt in packet_list:
        if all(x in check_list for x in check_list):
            logger.info(pkt)
            flag.append(True)
        else:
            flag.append(False)
    res = all(flag) if flag else False
    return res


def run_iodine_on_client(pc=pc1_login):
    for i in range(5):
        pc.send_command('killall iodine')
        time.sleep(5)
        client_path = f'{install_iodine_path}/bin/iodine'
        pc.send_command(f'chmod u+x {client_path}')
        logger.info("start iodline client on pc...")
        out1 = pc.send_command(f'{client_path} -P password -r {PC3_ETH1_IP} test.com')
        time.sleep(10)
        if 'Connection setup complete' in out1:
            break
    else:
        logger.error('dns tunnel setup failed.')
        return False

    out2 = pc.send_command('ifconfig')
    m = re.search('10.0.0.\d', out2, re.M | re.I)
    if m:
        logger.info(f'{pc} dns tunnel established succeed.\ngot tunnel ip address is {m.group()}')
        logger.info(f'ping from {pc}...')
        res = pc.ping(ip=Parameter.DNS_IP, num=10)
        return res
    else:
        logger.error('pc not got dns tunnel ip address')
        return False


def check_client_not_detected(client=PC1_ETH1_IP):
    for i in range(6):
        time.sleep(60)
        resp = dnssecurityapi.show_detected_client()
        check_res = client not in json.dumps(resp)
        if not check_res:
            return False
    logger.info('client is not in the detection list')
    return True
