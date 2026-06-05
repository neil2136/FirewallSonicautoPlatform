import re
from definition.settings import logger
from definition.settings import packetobj
from definition.settings import PC1_host
from definition.settings import Assertion


def start_capture():
    logger.info('start run FW packet monitor...')
    clearres = packetobj.clear_packets()
    logger.info(f'clear packets on FW result: {clearres}')
    startres = packetobj.start_capture()
    logger.info(f'start packets on FW result: {startres}')
    Assertion.assert_equal(clearres & startres, True, "ERR: change hostname Fail")


def stop_capture(protocol):
    port = 25 if protocol == "smtp" else 110
    stopres = packetobj.stop_capture()
    logger.info(f'stop packets on FW result: {stopres}')
    packetobj.export_captured_packets_pcapng()
    filterdnscmd = f'tshark -r /tmp/packet-c.pcapng -Y "tcp.dstport=={port}" -V -T text'
    logger.info(f'filterdnscmd: {filterdnscmd}')
    filteredpackets = PC1_host.send_command(filterdnscmd)
    # logger.info(f'run packet monitor end...,filterpackets is {filteredpackets}')
    return filteredpackets


def verify_packet_in_capture(protocol):
    rc = False
    try:
        rc_new = []
        packets = stop_capture(protocol)
        packet_list = packets.split('Packet comments')
        packet_list.pop(0)
        for packet in packet_list:
            if "Dst:" in packet:
                idenf_pattern = "(?<=Identification: )(.*?)(?=\s\()"
                des_ip_pattern = "(?<=Dst: )(\d+\.\d+\.\d+\.\d+)(?=\s\()"
                des_port_pattern = "(?<=Destination port: )(.*?)(?=\s\()"
                idenf = re.search(idenf_pattern, packet).group(0)
                logger.info(f"idenf is {idenf}")
                des_ip = re.search(des_ip_pattern, packet).group(0)
                logger.info(f"des_ip is {des_ip}")
                des_port = re.search(des_port_pattern, packet).group(0)
                logger.info(f"des_port is {des_port}")
                if (
                        des_ip == "10.6.0.69"
                        and des_port == protocol
                        and ("Consumed" in packet or "Forwarded" in packet)
                        and "in:X4*(interface),out:X1" in packet
                ):
                    new_pattern = f"(?<=Packet comments)((?!Packet comments).)*in:--,out:X1\\*((?!Packet comments).)*172.17.1.10((?!Packet comments).)*{idenf}((?!Packet comments).)*{protocol}"
                    logger.info(f"new_parttern is  {new_pattern}")
                    packet_result = re.search(new_pattern, packets, re.I | re.S | re.M)
                    #logger.info(f"match packet is {packet_result.group(0)}")
                    if packet_result:
                        rc_new.append(True)
                    else:
                        logger.info(f"false packet is {packet}")
                        rc_new.append(False)
        logger.info(f"rc_new is {rc_new}")
        if rc_new:
            rc = all(rc_new)
    except:
        pass
    logger.info(f"rc is {rc}")
    return rc
