import sys
import re
import time

from utm import Firewall
from lib.modules.CLI import system
from settings import Parameter
from tools.trafficGen import MyHttpClinet
from runner.settings import logger


fw = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')

def capture_packet(dst_ip=False, proto_type=False):
    packet_obj = system.PacketmonitorCli(fw)
    cap_info = {
        'dis_dest_ips': dst_ip,
        'dis_ip_types': proto_type,
    }
    logger.info('Configure Capture Filter Destination Ip to {}'.format(dst_ip))
    packet_obj.conf_capture(**cap_info)
    logger.info('start capture....')
    packet_obj.start_capture()
    http = MyHttpClinet('http://' + Parameter.WEB_SERVER + '/wiki')
    http.Http_get()
    time.sleep(20)
    logger.info('stop capture....')
    packet_obj.stop_capture()
    return analyze_packet(dst_ip, proto_type)

def analyze_packet(dst_ip, proto_type):
    forwarded = 0
    packet_obj = system.PacketmonitorCli(fw)
    packets = packet_obj.show_packet()
    if re.search(r''+ dst_ip +'\D*'+ proto_type +'.*forwarded', packets, re.I):
        forwarded += 1
    return forwarded
