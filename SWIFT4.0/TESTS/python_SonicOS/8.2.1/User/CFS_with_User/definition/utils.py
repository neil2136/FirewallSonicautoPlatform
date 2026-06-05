import copy

from runner.settings import logger
from definition.settings import (
    BIN_PATH,
    PC4_ETH2_IP,
    PC4_ETH2_IP_V6,
    CaseParms,
    uri_list_obj_dict,
)


# Check http response on the LAN client
def chk_url_resp_cfs(
    pc, expected, url=f"http://{CaseParms.CFS_TEST_URL_1}", is_v4=True
):
    cmds = _get_web_cmds(url, is_v4)
    logger.info("Visit the URL via client.")
    output = pc.send_commands(cmds)
    chk_keys_resp = _get_url_chk_resp(output, expected)
    logger.info(f"Check URL response = {chk_keys_resp}, expected = {expected}")
    res = _chk_expected_resp(chk_keys_resp, expected)
    logger.info(f"URL check result: {res}")
    return res


def _get_web_cmds(url, is_v4):
    SEARCH_WEB_CMD_V4 = [
        'echo " " > /tmp/test.txt',
        f"curl --resolve *:80:{PC4_ETH2_IP} {url} -o /tmp/test.txt",
        "cat /tmp/test.txt",
    ]
    SEARCH_WEB_CMD_V6 = [
        'echo " " > /tmp/test.txt',
        f"curl --resolve *:80:{PC4_ETH2_IP_V6} {url} -o /tmp/test.txt",
        "cat /tmp/test.txt",
    ]
    cmds = SEARCH_WEB_CMD_V4 if is_v4 else SEARCH_WEB_CMD_V6
    logger.info(f"Visit URL cmds = {cmds}")
    return cmds


def _get_url_chk_resp(output, expected):
    keys_dict = {
        "block": [
            "Search Engines and Portals",
            "CFS Default Policy",
            "This site has been blocked",
        ],
        "unblock": ["auto_cfs_html_tag", "6.6.6.6", "test_swf", "test_java"],
        "confirm": ["Confirm needed for the website", "please confirm"],
    }
    chk_keys_resp = [key in output for key in keys_dict.get(expected)]
    logger.info(f"Get URL check response = {chk_keys_resp}")
    return chk_keys_resp if chk_keys_resp else [False]


def _chk_expected_resp(chk_keys_resp, expected):
    return all(chk_keys_resp) if expected == "confirm" else any(chk_keys_resp)


# Get value by key from the CFS object
def get_cfs_value_by_key(cfs_obj, key):
    if key in cfs_obj:
        value = cfs_obj[key]
        logger.info(f"Get value for key {key} = {value}")
        return value
    for _, v in cfs_obj.items():
        if isinstance(v, list):
            for list_element in v:
                return get_cfs_value_by_key(list_element, key)
        if isinstance(v, dict):
            return get_cfs_value_by_key(v, key)
    return None


def upd_cfs_profile_cate(cfs_profile, all_opt="", **kws):
    try:
        categories = cfs_profile["content_filter"]["profile"][0]["category"]
        if all_opt:
            if all_opt not in ["block", "allow", "confirm", "passphrase", "bwm"]:
                logger.error("Incorrect operation settings.")
                raise KeyError("Either all_block or all_allow")
            for cate in categories:
                cate["operation"] = all_opt
            return cfs_profile
        for cate in categories:
            if cate["name"] in kws:
                cate["operation"] = kws[cate["name"]]
        logger.debug(f"Updated CFS profile = {cfs_profile}")
        return cfs_profile
    except Exception as e:
        logger.error(f"Get error when updating categories in the profile: {e}")
        return {}


def gen_url_obj_payload(template=uri_list_obj_dict, **kws):
    payload = upd_cfs_payload(template, **kws)
    logger.info(f"Generate payload for URL object = {payload}")
    return payload


# Update keys/values to CFS payload
def upd_cfs_payload(cfs_obj, **kws):
    logger.info(f"Update {kws} to the CFS object")
    policy_cp = copy.deepcopy(cfs_obj)
    for k, v in kws.items():
        _upd_keys_recur(policy_cp, k, v)
    logger.info(f"Get updated CFS object = {policy_cp}")
    return policy_cp


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


def remote_login_fw(pc_login, user, action, host):
    logger.info(f"Remote {action} to {host} via user {user}")
    cmd = f"python3 {BIN_PATH}/login_logout_dut.py -i {host} -a {action} -u {user}"
    resp = pc_login.send_command(cmd)
    logger.info(f"Login response = {resp}")
    if action == "login":
        return "Successfully login sonincos" in resp
    if action == "logout":
        return "Successfully logout sonincos" in resp


def check_cfs_resp_with_user(
    host, pc_login, user, expected, url=f"http://{CaseParms.CFS_TEST_URL_1}", is_v4=True
):
    logger.info(f"Will check CFS response with user {user}")
    res = False
    try:
        res_login = remote_login_fw(pc_login, user, "login", host)
        res_check = chk_url_resp_cfs(pc_login, expected, url, is_v4)
        res_logout = remote_login_fw(pc_login, user, "logout", host)
    except Exception as e:
        logger.error(f"Error when checking CFS response with user = {e}")
    res = all([res_login, res_check, res_logout])
    logger.info(f"Check CFS response with user {user} = {res}")
    return res
