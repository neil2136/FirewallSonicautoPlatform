from runner.settings import logger
import time


def get_tunnel_id(dyroute_obj, tunnel_name):
    tunnel_id = ''
    res = dyroute_obj.get_ospf_list_data()
    logger.info(res)
    for item in res['routedIfs'].split('|'):
        if 'VPN' in item and tunnel_name in item:
            logger.info(item)
            tunnel_id = item.split(',')[2]
            logger.info(f"tunnel id is {tunnel_id}")
            break
    return tunnel_id


def check_packet(exportres, filter_tuple):
    count = 0
    packets = exportres.split('Packet comments\n ')
    for packet in packets:
        if all(x in packet for x in filter_tuple):
            logger.info(f'packet found : {packet}')
            count = count + 1
    return count


def filter_packet(pkg_obj, pc_obj, protocol):
    logger.info(f'delete packet file')
    pc_obj.send_command("rm - f /tmp/packet-c.pcapng")
    clearres = pkg_obj.clear_packets()
    logger.info(f'clear packets on FW result: {clearres}')
    startres = pkg_obj.start_capture()
    logger.info(f'start packets on FW result: {startres}')
    time.sleep(30)
    stopres = pkg_obj.stop_capture()
    logger.info(f'stop packets on FW result: {stopres}')
    pkg_obj.export_captured_packets_pcapng()
    filterripcmd = f'tshark -R "{protocol}" -r /tmp/packet-c.pcapng -V -T text'
    filteredpackets = pc_obj.send_command(filterripcmd)
    return filteredpackets
