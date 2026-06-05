import json

from runner.settings import logger


def _chk_data_in_resp(resp, *kws, is_json=True):
    chk_data = json.dumps(resp) if is_json else resp
    logger.info(f"Check data in response = {chk_data}")
    return all(kw in chk_data for kw in kws)


def confirm_port_servs(port_info, servs):
    chk_res = _chk_data_in_resp(port_info, *servs)
    logger.info(f"Caonfirm port services status = {chk_res}")
    return chk_res


def chk_tsr_port_info(tsr, port_info):
    chk_res = _chk_data_in_resp(tsr, *port_info, is_json=False)
    logger.info(f"Check port infomation in TSR result = {chk_res}")
    return chk_res


# Filter policies by keywords
def _filter_nat_poli_unnumber(polis, chk_kws):
    ipv4_polis = polis.get("ipv4")
    if ipv4_polis:
        return _chk_data_in_resp(ipv4_polis, *chk_kws)


def chk_unnumber_nat_polis(polis_info, ppp_port="X1", unnum_port="X2"):
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
        return len(filtered_polis) == 2

