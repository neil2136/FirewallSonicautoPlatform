from definition.settings import fw, logger, pc1_ssh, pc2_ssh, pc3_ssh, pc4_ssh, pc5_ssh, Parameter, interface_obj, packetmonitor_obj, time

#start fw capture with command
def fw_packet_monitor_run(**kwargs):
    logger.info('start run FW packet monitor...')
    clearres = kwargs['packet_obj'].clear_packets()
    logger.info(f'clear packets from FW result: {clearres}')
    startres = kwargs['packet_obj'].start_capture()
    logger.info(f'start capture from FW result: {startres}')
    #time.sleep(10)
    time.sleep(5)
    if 'click_dhcp_renew' in kwargs['cmd']:
        res = kwargs['runner_obj'].click_dhcp_renew('x1')
    elif 'click_dhcp_release' in kwargs['cmd']:
        res = kwargs['runner_obj'].click_dhcp_release('x1')
    else:
        res = kwargs['runner_obj'].send_command(kwargs['cmd'])
    #time.sleep(5)
    time.sleep(2)
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

#get x1 ppp ip address
def get_ppp_ip_address(interface):
    Parameter.X1_PPP_IP = ''
    resp = interface_obj.get_interface_address(name=interface)
    logger.info(f"Get X1 interface address info = {resp}")
    Parameter.X1_PPP_IP = resp.get("ip_address")
    if not Parameter.X1_PPP_IP or Parameter.X1_PPP_IP == '0.0.0.0':
        return False
    return True

#get x3 ppp ip address
def get_ppp_ip_address_x3(interface):
    Parameter.X3_PPP_IP = ''
    resp = interface_obj.get_interface_address(name=interface)
    logger.info(f"Get X3 interface address info = {resp}")
    Parameter.X3_PPP_IP = resp.get("ip_address")
    if not Parameter.X3_PPP_IP or Parameter.X3_PPP_IP == '0.0.0.0':
        return False
    return True

def get_interface_ip_mode(interface) :
    interface_resp = interface_obj.get_interface_report()
    try:
        for i in interface_resp:
            for key,value in i.items():
                if value == interface:
                    return i['ip_mode']
    except Exception:
        logger.error("can not find interface ip mode")
        return None

def ping_wan_ip(ip, pc_ssh):
    if pc_ssh not in [pc3_ssh, pc4_ssh, pc5_ssh] :
        return False
    result = pc_ssh.ping(ip)
    return result



