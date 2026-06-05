from definition.settings import *


class TestInitFW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        rc = interface_api.config_interface(**x1_static_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    @repeat_method(10)
    def test_02_Register_fw(self):
        time.sleep(20)
        rc = license_cli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    # def test_02_Config_X2(self):
    #     res = interface_api.config_interface(**x2_wan_dict)
    #     Assertion.assert_equal(res, True, "ERR: Config remote X2 to static failed")

    # def test_03_enable_IPS(self):
    #     ips_global = {
    #         'intrusion_prevention': {
    #             'enable': True,
    #             'signature_group': {
    #                 'high_priority': {
    #                     'prevent_all': True,
    #                     'detect_all': True,
    #                     'log_redundancy': {}
    #                 },
    #                 'medium_priority': {
    #                     'prevent_all': True,
    #                     'detect_all': True,
    #                     'log_redundancy': {}
    #                 },
    #                 'low_priority': {
    #                     'prevent_all': True,
    #                     'detect_all': True,
    #                     'log_redundancy': {}
    #                 }
    #             }
    #         }
    #     }
    #     rc = ips_api.config_IPS_global(**ips_global)
    #     Assertion.assert_equal(rc, True, "ERR: enable ips failed")
    #
    # def test_03_enable_dpi_ssl_client(self):
    #     client_dict = {
    #         'enable': True,
    #         'intrusion_prevention': True,
    #     }
    #     res = clientssl_api.config_general_settings(**client_dict)
    #     Assertion.assert_equal(res, True, "ERR: enable dpi ssl client failed")

    def test_04_Conifg_log_settings(self):
        output = logcategory_api.logging_level(level='debug')
        Assertion.assert_equal(output, True, "ERR: Config log settings failed")

    # def test_05_disable_ips_signature_4698(self):
    #     # 4698 will block the low level test
    #     signature_json = {
    #         "intrusion_prevention": {
    #             "policy": [
    #                 {
    #                     "id": 4698,
    #                     "included": {
    #                         "ip": {
    #                             "category": True
    #                         },
    #                         "users": {
    #                             "category": True
    #                         }
    #                     },
    #                     "excluded": {
    #                         "ip": {
    #                             "category": True
    #                         },
    #                         "users": {
    #                             "category": True
    #                         }
    #                     },
    #                     "schedule": {
    #                         "category": True
    #                     },
    #                     "log_redundancy": {
    #                         "category": True
    #                     },
    #                     "category": "WEB-CLIENT",
    #                     "name": "ActiveX Object Obfuscated Instantiation 2",
    #                     "prevention": {},
    #                     "detection": {}
    #                 }
    #             ]
    #         }
    #     }
    #     output = ips_api.config_ips_signatures(id=4698, **signature_json)
    #     Assertion.assert_equal(output, True, "ERR: disable ips signature failed")
