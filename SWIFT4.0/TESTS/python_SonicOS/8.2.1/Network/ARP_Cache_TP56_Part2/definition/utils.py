import time
import re
from runner.settings import logger
from definition.settings import PC1_login,  diagapi, scripts_path, pkgapi, interfacecli


def get_dut_interface_mac(iface):
    interface_mac = ''
    macres = interfacecli.get_interface_mac(iface)
    for line in macres.split('\n'):
        if 'Runtime MAC' in line:
            interface_mac = line.split(' ')[-1].strip()
            logger.info(f'interface mac is {interface_mac}')
            break
    return interface_mac
    

def get_pc_int_mac(pc_obj, iface):
    rc = pc_obj.send_command(f"ifconfig {iface}")
    iface_mac = re.search("\S{2}:\S{2}:\S{2}:\S{2}:\S{2}:\S{2}", rc).group(0)
    return iface_mac.lower()
            
            
def send_traffic(action='ping_from_pc',**kwargs):   
    if action == 'ping_from_pc':
        output = kwargs['pc_obj'].ping_from_eth(
            kwargs['dest'], 'eth0', num=2)
        logger.info(f"ping {kwargs['dest']} : {output}\n ")

    elif action == 'ping_from_dut':       
        output = diagapi.diag_ping(kwargs['dest'])
        logger.info(f"ping {kwargs['dest']} : {output}\n")
    
    elif action == 'send_arp_from_PC':
        cmd = f'python3 {scripts_path}/scapy_arp_from_PC2.py -srcmac {kwargs["srcmac"]} ' \
                f'-iface {kwargs["iface"]} -psrc {kwargs["psrc"]} -pdst {kwargs["pdst"]}'
        logger.info(cmd)
        output = kwargs["pc_obj"].send_command(cmd)
        logger.info(f"send arp packet from X1 PC : {output}\n")
    
    return output


def fw_packet_monitor_run(action='ping_from_pc', **kwargs):
        logger.info('start run FW packet monitor...')

        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')

        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')

        logger.info(f"action : {action}\n ")

        sendres = send_traffic(action,**kwargs)
        logger.info(f"send traffic result : {sendres}")

        time.sleep(5)
        stopres = pkgapi.stop_capture()
        logger.info(f'start packets on FW result: {stopres}')

        pkgapi.export_captured_packets_pcapng()
        filterdnscmd = 'tshark -R "arp" -r /tmp/packet-c.pcapng -V -T text'
        logger.info(f'filterdnscmd: {filterdnscmd}')

        arpfilteredpackets = PC1_login.send_command(filterdnscmd)
        logger.info(f'arpfilteredpackets: {arpfilteredpackets}')
        logger.info('run packet monitor end...')

        return arpfilteredpackets


def check_arp_packet(exportres, filter_tuple):
    flag = False
    packets = exportres.split('Packet comments\n')
    for packet in packets:
        checkres = [x in packet for x in filter_tuple]
        logger.info(f'check packet result: {checkres}')
        if all(checkres):
            logger.info(f'packet found:\n{packet}')
            flag = True
            break
    return flag

################change in common lib################
# network.api
# arpapi
# add parameter dynamic

#network.cli
# edit
# arpcli
# flush_arp_entry(self, *entries):
# clear arp cache entries

#add 
# interfacecli
# get_interface_mac
