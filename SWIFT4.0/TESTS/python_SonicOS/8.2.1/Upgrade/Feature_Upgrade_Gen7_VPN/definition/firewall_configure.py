from definition.settings import *


class FWFunctionConfigure:

    def wlb_configure(self):
        wlb_conf_dict = {
            "failover_lb": {
                "group": [
                    {
                        "final_backup": "",
                        "interface": [
                            {
                                "name": "X1",
                                "probe_condition": "always",
                                "probe_type": "physical",
                                "rank": 1
                            },
                            {
                                "name": "X2",
                                "probe_condition": "always",
                                "probe_type": "physical",
                                "rank": 2
                            }
                        ],
                        "name": " Default LB Group",
                        "preempt": True,
                        "probing": {
                            "global_responder": False,
                            "health_check": 5,
                            "missed_intervals": 3,
                            "successful_intervals": 3
                        },
                        "type": "basic"
                    }
                ]
            }
        }
        output = failoverapi.config_failover_groups_by_multi(**wlb_conf_dict)
        return output

    def numbered_ti_configure(self):
        res1, msg1 = vpnapi.add_vpn_policy(msg=True, **l_tunnel_dict)
        if 'Already exists' in str(msg1):
            res1 = True
        res2, msg2 = r_vpnapi.add_vpn_policy(msg=True, **r_tunnel_dict)
        if 'Already exists' in str(msg2):
            res2 = True

        res3, msg3 = interfaceapi.add_interface(msg=True, **l_ti_dict)
        if 'Already exists' in str(msg3):
            res3 = True
        res4, msg4 = r_interfaceapi.add_interface(msg=True, **r_ti_dict)
        if 'Already exists' in str(msg4):
            res4 = True

        res5, msg5 = routepolicyapi.add_route_policy(msg=True, **route_policy_dict)
        if 'Already exists' in str(msg5):
            res5 = True
        route_base_dict.update(
            {
                "name": 'auto_remote_ti_route1',
                "destination": {
                    "name": 'local_vpn_net'
                },
            }
        )
        res6, msg6 = r_routepolicyapi.add_route_policy(msg=True, **route_policy_dict)
        if 'Already exists' in str(msg6):
            res6 = True
        logger.info(f'tunnel configure result: {res1}, {res2}, {res3}, {res4}, {res5}, {res6}')
        return res1 & res2 & res3 & res4 & res5 & res6

    def s2s_vpn_configure(self):
        res1, msg1 = vpnapi.add_vpn_policy(msg=True, **l_s2s_vpn_dict)
        if 'Already exists' in str(msg1):
            res1 = True
        res2, msg2 = r_vpnapi.add_vpn_policy(msg=True, **r_s2s_vpn_dict)
        if 'Already exists' in str(msg2):
            res2 = True
        logger.info(f'add s2s vpn result: {res1, res2}')
        return res1 & res2

    def wan_groupvpn_configure(self):
        l_group_vpn_dict = {
            'enable': True,
            'secret': 'password',
            'auth_mode': 'shared_secret',
            'ike_encryption': 'triple-des',
            'ike_auth': 'sha-384',
            'ipsec_encryption': 'triple_des',
            'ike_lifetime': 240,
            'ipsec_auth': 'sha_384',
            'ipsec_lifetime': 240,
            'client_authentication': 'allow_unauthenticated',
            'unauthenticated_group': 'Firewalled Subnets',
            'management_https': True,
            'management_ssh': True,
        }
        res, msg = vpnapi.edit_wangroup_vpn_policy(msg=True, **l_group_vpn_dict)
        if 'Already exists' in str(msg):
            res = True
        return res

    def ula_configure(self):
        user_dict = {
            'action': 'add',
            'username': CaseParams.ula_user_name,
            'userpassword': 'password',
            'vpn_client_access': ['LAN Subnets'],
            'member_of': ['Everyone'],
        }
        res, msg = userLocalapi.local_user(msg=True, **user_dict)
        if 'Already exists' in str(msg):
            res = True
        return res






