from runner.settings import logger
import time
# import os
# import sys


def get_site_to_site_vpn_policy_by_name(vpnbase_settingapi, policy_name):
    output = vpnbase_settingapi.show_s2svpnpolicy()
    logger.info(f'output is:{output}')
    vpnpolicies = output['vpn']['policy']
    try:
        for vpn_policy in vpnpolicies:
            if f"'name': '{policy_name}'" in str(vpn_policy):
                return vpn_policy
    except Exception as e:
        logger.error(repr(e))
        return ''
