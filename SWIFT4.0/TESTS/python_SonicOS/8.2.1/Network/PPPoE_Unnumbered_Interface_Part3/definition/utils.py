import json
import time

from runner.settings import logger
from definition.settings import SCRIPTS_PATH


def _chk_data_in_resp(resp, *kws, is_json=True):
    chk_data = json.dumps(resp) if is_json else resp
    logger.info(f"Check data in response = {chk_data}")
    return all(kw in chk_data for kw in kws)


def confirm_port_servs(port_info, servs):
    chk_res = _chk_data_in_resp(port_info, *servs)
    logger.info(f"Confirm port services status = {chk_res}")
    return chk_res


def is_port_disabled(port_info):
    chk_res = _chk_data_in_resp(port_info, '"shutdown_port": true')
    logger.info(f"Confirm port disabled = {chk_res}")
    return chk_res


def is_dyn_dhcps_enabled(dhcp_info, chk_kws):
    if '"dhcp_server": {"ipv4": {"scope": {"dynamic":' not in json.dumps(dhcp_info):
        logger.info("No dynamic DHCP scope found.")
        return False
    dyn_dhcps = dhcp_info["dhcp_server"]["ipv4"]["scope"]["dynamic"]
    enabled_dyn_dhcps = [scope for scope in dyn_dhcps if scope.get("enable")]
    chk_res = _chk_data_in_resp(enabled_dyn_dhcps, *chk_kws)
    logger.info(f"Confirm dynamic DHCP scope enabled = {chk_res}")
    return chk_res


# Filter policies by keywords
def _filter_nat_poli_unnumber(polis, chk_kws):
    ipv4_polis = polis.get("ipv4")
    if ipv4_polis:
        return _chk_data_in_resp(ipv4_polis, *chk_kws)


def chk_unnumber_nat_polis(polis_info, ppp_port="X1", unnum_port="X2", chk_exist=True):
    polis = polis_info.get("nat_policies")
    if polis:
        rule_kws_out = [
            f'"inbound": "{unnum_port}"',
            f'"outbound": "{ppp_port}"',
            '"destination": {"any": true}',
            f'"source": {{"name": "{unnum_port} Subnet"}}',
        ]

        rule_kws_in = [
            f'"inbound": "{ppp_port}"',
            f'"outbound": "{unnum_port}"',
            f'"destination": {{"name": "{unnum_port} Subnet"}}',
            '"source": {"any": true}',
        ]
        # Filter out inbound and outbound NAT policies by rules
        filtered_polis = [
            poli
            for poli in polis
            if _filter_nat_poli_unnumber(poli, rule_kws_out)
            or _filter_nat_poli_unnumber(poli, rule_kws_in)
        ]
        logger.info(
            f"Filter {len(filtered_polis)} NAT policy for unnumbered = {filtered_polis}"
        )
        return len(filtered_polis) == 2 if chk_exist else len(filtered_polis) == 0


def _pc_traffic_send(kwargs):
    if kwargs["type"] == "ping":
        res = kwargs["pc_login"].ping(ip=kwargs["des"])
        return res


def fw_packet_monitor_run(**kwargs):
    if "path" not in kwargs.keys():
        kwargs["path"] = SCRIPTS_PATH
    logger.info("Start run FW packet monitor...")
    clearres = kwargs["packet_obj"].clear_packets()
    logger.info(f"Clear packets from FW result: {clearres}")
    startres = kwargs["packet_obj"].start_capture()
    logger.info(f"Start capture from FW result: {startres}")
    res = _pc_traffic_send(kwargs)
    time.sleep(5)
    logger.info(f"PC traffic send result: {res}")
    if "packet" in kwargs.keys() and kwargs["packet"] == "pcapng":
        packetres = kwargs["packet_obj"].export_captured_packets_pcapng()
    else:
        packetres = kwargs["packet_obj"].export_captured_packets()
    stopres = kwargs["packet_obj"].stop_capture()
    logger.info(f"Stop capture from FW result: {stopres}")
    return res, packetres


def check_capture_packets(packets, filter_list):
    packets = packets.split("Packet number: ")
    logger.info(f"Packet filter list: {filter_list}")
    for packet in packets:
        checkres = [x in str(packet) for x in filter_list]
        logger.info(f"check packet result: {checkres}")
        if all(checkres):
            return True, packet
    return False, ""
