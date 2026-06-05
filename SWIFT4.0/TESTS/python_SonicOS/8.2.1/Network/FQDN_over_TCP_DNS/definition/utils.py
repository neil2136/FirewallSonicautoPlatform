import copy
import json
import time

from runner.settings import logger
from definition.settings import SCRIPTS_PATH, packetmonitorapi


def send_dns_query_via_lan(
    pc_login, host, domain, port=53, opt="query", via="udp", loop=3
):
    try:
        cmds = f"python3 {SCRIPTS_PATH}/dnstest.py -o {opt} -i {host} -p {port} -d {domain} -t {via} -l {loop}"
        out = pc_login.send_command(cmds)
        res = True if "done" in out else False
        logger.info(f"Send DNS {opt} for {domain} to {host} via {via} success.")
        return res
    except Exception as e:
        logger.error(f"Error when sending DNS {opt} = {e}")
        return False


def _chk_data_in_resp(resp, *kws, is_json=True):
    chk_data = json.dumps(resp) if is_json else resp
    logger.info(f"Check data in response = {chk_data}")
    return all(kw in chk_data for kw in kws)


def confirm_dns_settings(resp, *keys):
    chk_res = _chk_data_in_resp(resp, *keys)
    logger.info(f"Confirm dns settings result = {chk_res}")
    return chk_res


def upd_dns_settings_payload(dns_settings, **kws):
    logger.info(f"Update {kws} to the DNS settings")
    settings_cp = copy.deepcopy(dns_settings)
    for k, v in kws.items():
        _upd_keys_recur(settings_cp, k, v)
    logger.info(f"Get updated the DNS settings = {settings_cp}")
    return settings_cp


def _upd_keys_recur(data, key, value):
    for k, v in data.items():
        if k == key:
            _upd_keys(data, key, value)
        else:
            if isinstance(v, list):
                for list_element in v:
                    _upd_keys_recur(list_element, key, value)
            if isinstance(v, dict):
                _upd_keys_recur(v, key, value)


def _upd_keys(data, key, value):
    logger.info(f"Update key = {key} to {value}")
    if isinstance(value, dict):
        for dict_k, dict_v in value.items():
            data[key][dict_k] = dict_v
    else:
        data[key] = value


def start_cap_pkts(wait_time=5):
    logger.info("Start run FW packet monitor...")
    clearres = packetmonitorapi.clear_packets()
    logger.info(f"Clear packets from FW result: {clearres}")
    startres = packetmonitorapi.start_capture()
    logger.info(f"Start capture from FW result: {startres}")
    logger.info(f"Sleep {wait_time}s before capturing packets")
    time.sleep(wait_time)
    res = {"clear": clearres, "start": startres}
    logger.info(f"Start capture results = {res}")
    return res


def chk_cap_results(wait_time=20, **filters):
    logger.info(f"Sleep {wait_time}s for capturing packets.")
    time.sleep(wait_time)
    packets = packetmonitorapi.export_captured_packets()
    stopres = packetmonitorapi.stop_capture()
    logger.info(f"Stop capture from FW result: {stopres}")
    chk_res = {
        name: _check_cap_pkts(packets, filter) for name, filter in filters.items()
    }
    logger.info(f"Check packets results = {chk_res}")
    return all(chk_res.values()), chk_res


def _check_cap_pkts(packets, filter_list):
    packets = packets.split("Packet number: ")
    logger.info(f"Packet filter list: {filter_list}")
    for packet in packets:
        checkres = [x in str(packet) for x in filter_list]
        logger.info(f"Packet = {packet}")
        logger.info(f"Check packet result: {checkres}")
        if all(checkres):
            logger.info(f"Check DNS over TCP result = {True}, packet = {packet}")
            return True
    logger.info(f"Check DNS over TCP result: {False}")
    return False


def check_case_result(res, wait_time=15):
    if not res:
        logger.info(f"Sleep {wait_time}s before the next retry")
        time.sleep(wait_time)
