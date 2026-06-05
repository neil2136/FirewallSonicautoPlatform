from definition.initial_parameter import *


class TestNatPolicies_26(Test):
    uuid = "SOSAIOT-TC-58623"
    description= show_testcase_info(Parameter.TESTPLAN, '26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_default_nat_policy_by(self):
        logger.info("check ping traffic from lanpc to wanpc")
        rc = not os.system('ping ' + PC1_ETH0_IP + ' -c 1 -w 1')
        Assertion.assert_equal(rc, True, "ERR: check default nat policy failed")

class TestNatPolicies_27(Test):
    uuid = "SOSAIOT-TC-58624"
    description = show_testcase_info(Parameter.TESTPLAN, '27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_03_add_nat_policy(self):
        nat_json = {
            "nat_policies": [
            {
                "ipv4": {
                    "uuid": "00000000-0000-0001-0800-2cb8ed6d8008",
                    "name": "my_nat_policy",
                    "enable": True,
                    "comment": "",
                    "dns_doctoring": False,
                    "inbound": "X1",
                    "outbound": "any",
                    "source": {
                        "any": True
                    },
                    "translated_source": {
                        "original": True
                    },
                    "destination": {
                        "name": "X1 IP"
                    },
                    "translated_destination": {
                        "name": "lanpc"
                    },
                    "service": {
                        "any": True
                    },
                    "translated_service": {
                        "original": True
                    }
                }
                }
            ]
        }
        rc = natpolicy_obj.add_nat_policy(**nat_json)
        Assertion.assert_equal(rc, True, "ERR:add nat policy failed")

    def test_05_add_access_rule(self):
        access_rules = {
            "uuid": "00000000-0000-0001-0700-22222",
            "name": "my_access_rule",
            "enable": True,
            "from": "WAN",
            "to": "LAN",
            "action": "allow",
            "source": {
                "address": {
                    "any": True
                },
                "port": {
                    "any": True
                }
            },
            "service": {
                "name": "HTTPS"
            },
            "destination": {
                "address": {
                    "any": True
                }
            },
            "schedule": {
                "always_on": True
            },
            "users": {
                "included": {
                    "all": True
                },
                "excluded": {
                    "none": True
                }
            },
            "comment": "",
            "fragments": True,
            "logging": True,
            "sip": False,
            "h323": False,
            "flow_reporting": False,
            "botnet_filter": False,
            "geo_ip_filter": {
                "enable": False,
                "global": True
            },
            "priority": {
                "auto": True
            }
        }
        rc = access_rules_obj.config_accessrule(**access_rules)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: add access rule from LAN to WAN failed")

    def test_06_check_https_traffic(self):
        out = httpserver.send_command('curl -k https://' + Parameter.X1_IP + '/test_file.txt')
        if re.search('this file is for nat policy test', out, re.M):
            logger.info('get file by https successfully')
            rc = True
        else:
            logger.error('error: failed to get file by https')
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check https traffic failed")

    def test_06_teardown(self):
        rc1 = access_rules_obj.delete_accessrule_by_name(name = 'my_access_rule')
        rc2 = natpolicy_obj.del_nat_policy_by_name(name = 'my_nat_policy')
        Assertion.assert_equal(rc1 & rc2, True, "ERR: remove config failed")


class TestNatPolicies_35(Test):
    uuid = "SOSAIOT-TC-58633"
    description = show_testcase_info(Parameter.TESTPLAN, '35', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '35')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_access_rule_ftp(self):
        access_rules = {
            "uuid": "00000000-0000-0001-0700-2cb8ed691d4c",
            "name": "my_access_rule1",
            "enable": True,
            "from": "WAN",
            "to": "LAN",
            "action": "allow",
            "source": {
                "address": {
                    "any": True
                },
                "port": {
                    "any": True
                }
            },
            "service": {
                "name": "FTP"
            },
            "destination": {
                "address": {
                    "any": True
                }
            },
            "schedule": {
                "always_on": True
            },
            "users": {
                "included": {
                    "all": True
                },
                "excluded": {
                    "none": True
                }
            },
            "comment": "",
            "fragments": True,
            "logging": True,
            "sip": False,
            "h323": False,
            "flow_reporting": False,
            "botnet_filter": False,
            "geo_ip_filter": {
                "enable": False,
                "global": True
            },
            "priority": {
                "auto": True
            }
        }
        rc = access_rules_obj.config_accessrule(**access_rules)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: add access rule from LAN to WAN failed")

    def test_03_add_nat_policy(self):
        nat_json = {
            "nat_policies": [
            {
                "ipv4": {
                    "uuid": "00000000-0000-0001-0800-2cb8ed6d8008",
                    "name": "my_nat_policy",
                    "enable": True,
                    "comment": "",
                    "dns_doctoring": False,
                    "inbound": "X1",
                    "outbound": "any",
                    "source": {
                        "any": True
                    },
                    "translated_source": {
                        "original": True
                    },
                    "destination": {
                        "name": "X1 IP"
                    },
                    "translated_destination": {
                        "name": "lanpc"
                    },
                    "service": {
                        "any": True
                    },
                    "translated_service": {
                        "original": True
                    }
                }
                }
            ]
        }
        rc = natpolicy_obj.add_nat_policy(**nat_json)
        Assertion.assert_equal(rc, True, "ERR:add nat policy failed")

    def test_04_check_ftp_traffic(self):
        # check ftp traffic from wanpc
        tc_path = os.environ["PYTHON_SONICOS_HOME"] + '/Network/NAT_Policies-TP167/testcases'
        rc = httpserver.send_command('python3 ' + tc_path + '/get_file_by_ftp.py -host ' + Parameter.X1_IP +
                                ' -user ftpuser -password password')
        Assertion.assert_regular(rc, r'Login successful', "check ftp traffic failed")


    def test_05_add_access_rule_https(self):
        access_rules = {
            "uuid": "00000000-0000-0001-0700-22222",
            "name": "my_access_rule2",
            "enable": True,
            "from": "WAN",
            "to": "LAN",
            "action": "allow",
            "source": {
                "address": {
                    "any": True
                },
                "port": {
                    "any": True
                }
            },
            "service": {
                "name": "HTTPS"
            },
            "destination": {
                "address": {
                    "any": True
                }
            },
            "schedule": {
                "always_on": True
            },
            "users": {
                "included": {
                    "all": True
                },
                "excluded": {
                    "none": True
                }
            },
            "comment": "",
            "fragments": True,
            "logging": True,
            "sip": False,
            "h323": False,
            "flow_reporting": False,
            "botnet_filter": False,
            "geo_ip_filter": {
                "enable": False,
                "global": True
            },
            "priority": {
                "auto": True
            }
        }
        rc = access_rules_obj.config_accessrule(**access_rules)
        Assertion.assert_equal(rc, True, "ERR: add access rule from LAN to WAN failed")

    @repeat_method(3)
    def test_06_check_https_traffic(self):
        out = httpserver.send_command('curl -k https://' + Parameter.X1_IP + '/test_file.txt')
        if re.search('this file is for nat policy test', out, re.M):
            logger.info('get file by https successfully')
            rc = True
        else:
            logger.error('error: failed to get file by https')
            rc = False
        Assertion.assert_equal(rc, True, "check https traffic failed")

    def test_07_teardown(self):
        rc1 = access_rules_obj.delete_accessrule_by_name(name = 'my_access_rule1')
        rc2 = access_rules_obj.delete_accessrule_by_name(name='my_access_rule2')
        rc3 = natpolicy_obj.del_nat_policy_by_name(name = 'my_nat_policy')
        Assertion.assert_equal(rc1 & rc2 & rc3, True, "ERR: remove config failed")


class TestNatPolicies_38(Test):
    uuid = "SOSAIOT-TC-58636"
    description = show_testcase_info(Parameter.TESTPLAN, '38', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '38')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_service_object(self):
        service_object_tcp = {"object_type": "tcp",
                              "name": "http_8888",
                              "tcp": {
                                  "begin": 8888,
                                  "end": 8888
                              }
                              }
        (rc, uuid) = service_obj.config_service_object(**service_object_tcp)
        Assertion.assert_equal(rc, True, "ERR: add service object failed")

    def test_03_add_nat_policy(self):
        nat_json = {
            "nat_policies": [
            {
                "ipv4": {
                    "uuid": "00000000-0000-0001-0800-2cb8ed6d8008",
                    "name": "my_nat_policy",
                    "enable": True,
                    "comment": "",
                    "dns_doctoring": False,
                    "inbound": "X1",
                    "outbound": "any",
                    "source": {
                        "any": True
                    },
                    "translated_source": {
                        "original": True
                    },
                    "destination": {
                        "name": "X1 IP"
                    },
                    "translated_destination": {
                        "name": "lanpc"
                    },
                    "service": {
                        "name": "http_8888"
                    },
                    "translated_service": {
                        "name": "HTTP"
                    }
                }
                }
            ]
        }
        rc = natpolicy_obj.add_nat_policy(**nat_json)
        Assertion.assert_equal(rc, True, "ERR:add nat policy failed")

    def test_05_add_access_rule_http(self):
        access_rules = {
            "uuid": "00000000-0000-0001-0700-22222",
            "name": "my_access_rule",
            "enable": True,
            "from": "WAN",
            "to": "LAN",
            "action": "allow",
            "source": {
                "address": {
                    "any": True
                },
                "port": {
                    "any": True
                }
            },
            "service": {
                "name": "http_8888"
            },
            "destination": {
                "address": {
                    "name": 'X1 IP'
                }
            },
            "schedule": {
                "always_on": True
            },
            "users": {
                "included": {
                    "all": True
                },
                "excluded": {
                    "none": True
                }
            },
            "comment": "",
            "fragments": True,
            "logging": True,
            "sip": False,
            "h323": False,
            "flow_reporting": False,
            "botnet_filter": False,
            "geo_ip_filter": {
                "enable": False,
                "global": True
            },
            "priority": {
                "auto": True
            }
        }
        rc = access_rules_obj.config_accessrule(**access_rules)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: add access rule from LAN to WAN failed")

    @repeat_method(3)
    def test_06_check_https_traffic(self):
        out = httpserver.send_command('curl -k http://' + Parameter.X1_IP + ':8888/test_file.txt')
        if re.search('this file is for nat policy test', out, re.M):
            logger.info('get file by https successfully')
            rc = True
        else:
            logger.error('error: failed to get file by https')
            rc = False
        Assertion.assert_equal(rc, True, "check http traffic failed")



