from definition.settings import vpn_api, vpn_rem_api, logger


def del_vpn_policies():
    res1 = vpn_api.del_all_vpn_policies()
    logger.info(f'delete vpn on local result: {res1}')
    res2 = vpn_rem_api.del_all_vpn_policies()
    logger.info(f'delete vpn on remote result: {res2}')
    return res1 and res2
