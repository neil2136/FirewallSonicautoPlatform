from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'

    def test_00_edit_x1_interface_to_wan(self):
        logger.info("config x1 interface... ")
        x1_wan_dict = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': False,
            'mgmt_ping': True,
            'user_https': False,
            'mgmt-snmp': False,
        }
        rc = interface_api.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_01_add_guest_user(self):
        guest_user = {
            'action': 'add',
            'accountname': 'guest',
            'password': 'password',
        }
        rc = guest_api.user_guest_account(**guest_user)
        Assertion.assert_equal(rc, True, "ERR: create guest user failed")

    def test_02_add_custom_trusted_zone(self):
        base_dict = {
            'name': "cus_trust",
            'security_type': 'trusted'
        }
        trusted_dict = {"zones": [base_dict]}
        zoneres = zone_api.add_zone_object(**trusted_dict)
        Assertion.assert_equal(zoneres, True, "ERR: Add Zone Failed")

    def test_03_add_custom_public_zone(self):
        base_dict = {
            'name': "cus_public",
            'security_type': 'public'
        }
        trusted_dict = {"zones": [base_dict]}
        zoneres = zone_api.add_zone_object(**trusted_dict)
        Assertion.assert_equal(zoneres, True, "ERR: Add Zone Failed")

    def test_04_create_full_admin_local_user(self):
        user_json = {
            'action': 'add',
            'username': Parameter.custom_admin_name,
            'userpassword': Parameter.custom_admin_password,
            'member_of': ['Trusted Users', 'Everyone', 'SonicWALL Administrators']

        }
        post_resp = localuser_api.local_user(**user_json)
        get_resp = localuser_api.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), '"name": "test_user1"', 'err: user_test1 not created')

    def test_05_add_disabled_guest_account(self):
        guest_user = {
            'action': 'add',
            'accountname': 'disable_guest',
            'password': 'password',
            "enable_guest_service_privilege": False
        }
        rc = guest_api.user_guest_account(**guest_user)
        Assertion.assert_equal(rc, True, "ERR: create guest user failed")

    def test_06_add_expired_guest_account(self):
        guest_user = {
            "name": "expire_guest",
            "password": "password",
            "prune_on_expiry": False,
            "account_lifetime": {
                "minutes": 1
            },
            "idle_timeout": {
                "minutes": 1
            },
            "quota_cycle": {},
            "session_lifetime": {
                "minutes": 1
            },
            "limit": {
                "receive": 0,
                "transmit": 0
            }
        }
        rc = guest_api.add_guest_account(**guest_user)
        Assertion.assert_equal(rc, True, "ERR: create guest user failed")

    def test_07_create_non_guest_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'notguest',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'Everyone']

        }
        post_resp = localuser_api.local_user(**user_json)
        get_resp = localuser_api.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), '"name": "notguest"', 'err: create local user failed')

    def test_08_create_guest_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'localguest',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'Everyone', 'Guest Services']

        }
        post_resp = localuser_api.local_user(**user_json)
        get_resp = localuser_api.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), '"name": "localguest"', 'err: local guest user not created')

    def test_09_add_ao_group_for_10103202200(self):
        host_dns = {
            "object_type": "host",
            "name": "dns_ip_host",
            "zone": "WAN",
            "value": "10.103.202.200"
        }
        range_dns = {
            "object_type": "range",
            "name": "dns_ip_range",
            "zone": "WAN",
            "value": '10.103.202.150,10.103.202.210'
        }
        subnet_dns = {
            "object_type": "network",
            "name": "dns_ip_network",
            "zone": "WAN",
            "value": '10.103.202.0,255.255.255.0'
        }
        group_dns = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "dns_ip_host"
                                }
                            ]
                        },
                        "name": "dns_group"
                    }
                }
            ]
        }
        smtp_redirect = {
            "object_type": "host",
            "name": "smtp_redirect",
            "zone": "WAN",
            "value": "172.17.1.10"
        }
        rc1 = addressobjects_api.config_addressobject(**host_dns)
        rc2 = addressobjects_api.config_addressobject(**range_dns)
        rc3 = addressobjects_api.config_addressobject(**subnet_dns)
        rc4 = addressobjectgroup_api.add_addressgroup(**group_dns)
        rc5 = addressobjects_api.config_addressobject(**smtp_redirect)
        Assertion.assert_equal(rc1 & rc2 & rc3 & rc4 & rc5, True, "ERR: add ao failed")

    def test_10_set_guest_deny_network_log(self):
        eventconf = {
            "log": {
                "event": [
                    {
                        "id": 724,
                        "name": "Guest Services Deny Network",
                        "priority_level": "warning",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {},
                        "syslog": {},
                        "trap": {},
                        "ipfix": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "log_digest": False,
                        "alert_email": {}
                    }
                ]
            }
        }
        eventres = logsettings_api.edit_event(event_id='724', **eventconf)
        Assertion.assert_equal(eventres, True, "ERR: set log failed")

    @repeat_method(10)
    def test_11_Register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
