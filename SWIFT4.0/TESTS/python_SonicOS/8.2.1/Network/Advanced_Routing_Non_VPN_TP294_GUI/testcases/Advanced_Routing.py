from definition.settings import *
from definition.utils import *


# make sure G7+ routeing mode must be advanced.
class TestGUI_TC01(Test):
    uuid = "SOSAIOT-TC-55642"
    description = show_testcase_info(TESTPLAN, 'GUI_TC01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_routing_mode_must_advanced(self):
        output = dynaroutingapi.show_routing_settings()
        try:
            res = True if output['routing']['mode']=='advanced' else False
        except Exception as e:
            res = False
            logger.info(repr(e))
        Assertion.assert_equal(res, True, "ERR: check routing mode failed")


# check config routing mode not need restart.
class TestGUI_TC02(Test):
    uuid = "SOSAIOT-TC-55672"
    description = show_testcase_info(TESTPLAN, 'GUI_TC02', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_routing_mode_to_off(self):
        output = dynaroutingapi.set_advanced_routing_mode(**{'advanced': 'off'})
        Assertion.assert_equal(output, True, "ERR: set routing mode failed")

    def test_02_set_routing_mode_to_on(self):
        output = dynaroutingapi.set_advanced_routing_mode(**{'advanced': 'on'})
        Assertion.assert_equal(output, True, "ERR: set routing mode failed")

    def test_03_check_routing_mode_must_advanced(self):
        TestGUI_TC01().test_01_check_routing_mode_must_advanced()


# check RIP and OSPF are configurable.
class TestGUI_TC03(Test):
    uuid = "SOSAIOT-TC-55683"
    description = show_testcase_info(TESTPLAN, 'GUI_TC03', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_rip_for_x1(self):
        rip_dict = {
            'interface': 'X1',
            'mode': 'send_and_receive',
        }
        output = dynaroutingapi.set_rip(**rip_dict)
        Assertion.assert_equal(output, True, "ERR: set routing mode failed")

    def test_02_check_rip_config_must_enable_in_x1(self):
        rip_configure = {
            'ifName': 'X1',
            'rip': 'RIP Enabled',
        }
        output = dynaroutingapi.get_rip_list_data()
        res = check_routing_config(output, **rip_configure)
        Assertion.assert_equal(res, True, "ERR: check rip config failed")

    def test_03_config_ospf_for_x1(self):
        ospf_dict = {
            'interface': 'X1',
            'mode': 'enable',
            'hello_interval': '5',
            'dead_interval': '20',
            'cost': 'on',
        }
        output = dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: set routing mode failed")

    @repeat_method(5)
    def test_04_check_ospf_config_must_enable_in_x1(self):
        time.sleep(10)
        ospf_configure = {
            'ifName': 'X1',
            'ospf': 'OSPF Enabled',
        }
        output = dynaroutingapi.get_ospf_list_data()
        res = check_routing_config(output, **ospf_configure)
        Assertion.assert_equal(res, True, "ERR: check ospf config failed")

    def test_05_init_rip_and_ospf_settings(self):
        rip_dict = {
            'interface': 'X1',
            'mode': 'disable',
        }
        output1 = dynaroutingapi.set_rip(**rip_dict)
        ospf_dict = {
            'interface': 'X1',
            'mode': 'disable',
            'cost': 'on',
        }
        output2 = dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: init rip and ospf settings failed")


# check RIP configure must disable in all ports.
class TestGUI_TC05(Test):
    uuid = "SOSAIOT-TC-55701"
    description = show_testcase_info(TESTPLAN, 'GUI_TC05', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC05')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_rip_config_must_disable_in_all(self):
        rip_configure = {
            'ifName': 'ALL',
            'rip': 'RIP Disabled',
        }
        output = dynaroutingapi.get_rip_list_data()
        res = check_routing_config(output, **rip_configure)
        Assertion.assert_equal(res, False, "ERR: check rip config failed")


# check Default Metric 1-15
class TestGUI_TC10(Test):
    uuid = "SOSAIOT-TC-55643"
    description = show_testcase_info(TESTPLAN, 'GUI_TC10', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_default_metric_rip(self):
        validres = []
        valid_list = ['1', '5', '15']
        for metric in valid_list:
            output = dynaroutingapi.rip_config(**{'DefaultMetric': metric})
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid default metric failed")

    def test_02_check_invalid_default_metric_rip(self):
        invalidres = []
        invalid_list = ['-1', '0', '16']
        for metric in invalid_list:
            output, msg = dynaroutingapi.rip_config(msg=True, **{'DefaultMetric': metric})
            if 'Data out of bounds' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 3, "ERR: config invalid default metric failed")

    def test_03_init_defalut_metric(self):
        output = dynaroutingapi.rip_config(**{'DefaultMetric': '1'})
        Assertion.assert_equal(output, True, "ERR: init default metric failed")


# check Administrative Distance field boundaries(1~255)
class TestGUI_TC11(Test):
    uuid = "SOSAIOT-TC-55649"
    description = show_testcase_info(TESTPLAN, 'GUI_TC11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_admin_distance_rip(self):
        validres = []
        valid_list = ['1', '100', '255']
        for metric in valid_list:
            output = dynaroutingapi.rip_config(**{'AdministrativeDistance': metric})
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid admin distance failed")

    def test_02_check_invalid_admin_distance_rip(self):
        invalidres = []
        invalid_list = ['-1', '0', '256']
        for metric in invalid_list:
            output, msg = dynaroutingapi.rip_config(msg=True, **{'DefaultMetric': metric})
            if 'Data out of bounds' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 3, "ERR: config invalid admin distance failed")

    def test_03_init_admin_distance(self):
        output = dynaroutingapi.rip_config(**{'AdministrativeDistance': '120'})
        Assertion.assert_equal(output, True, "ERR: init admin distance failed")


# boundaries for Advertise Static Routes Metric (1~15)
class TestGUI_TC12(Test):
    uuid = "SOSAIOT-TC-55658"
    description = show_testcase_info(TESTPLAN, 'GUI_TC12', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_static_routes_rip(self):
        validres = []
        valid_list = ['1', '5', '15']
        for metric in valid_list:
            output = dynaroutingapi.rip_config(**{'StaticsMetric': metric})
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid static routes failed")

    def test_02_check_invalid_static_routes_rip(self):
        invalidres = []
        invalid_list = ['-1', '0', '16']
        for metric in invalid_list:
            output, msg = dynaroutingapi.rip_config(msg=True, **{'StaticsMetric': metric})
            if 'Data out of bounds' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 3, "ERR: config invalid static routes failed")

    def test_03_init_static_routes(self):
        output = dynaroutingapi.rip_config(**{'AdministrativeDistance': '1'})
        Assertion.assert_equal(output, True, "ERR: init admin distance failed")


# boundaries for Redistribute Connected Networks Metric (1 - 16777214)
class TestGUI_TC13(Test):
    uuid = "SOSAIOT-TC-55662"
    description = show_testcase_info(TESTPLAN, 'GUI_TC13', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_connected_networks_metric(self):
        validres = []
        valid_list = ['1', '6666', '16777214']
        for metric in valid_list:
            ospf_dict = {
                'connect_network': 'on',
                'connect_metric': metric,
            }
            output = dynaroutingapi.ospf2_config(**ospf_dict)
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        CaseParams.tc13_test_result.append(all(validres))
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid Connected Networks Metric failed")

    def test_02_check_invalid_connected_networks_metric(self):
        invalidres = []
        invalid_list = ['-1', '0', '16777215']
        for metric in invalid_list:
            ospf_dict = {
                'connect_network': 'on',
                'connect_metric': metric,
            }
            output, msg = dynaroutingapi.ospf2_config(msg=True, **ospf_dict)
            if 'Data out of bounds' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        CaseParams.tc13_test_result.append(all(invalidres))
        Assertion.assert_equal(invalidres.count(True), 3, "ERR: config invalid Connected Networks Metric failed")

    def test_03_init_connected_networks_metric(self):
        ospf_dict = {
            'connect_network': 'on',
            'connect_metric': '1',
        }
        output= dynaroutingapi.ospf2_config(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: init OSPF Connected Networks Metric failed")


# boundaries for Redistribute OSPF Routes Metric (1~15)
class TestGUI_TC14(Test):
    uuid = "SOSAIOT-TC-55663"
    description = show_testcase_info(TESTPLAN, 'GUI_TC14', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_redistribute_ospf_rip(self):
        validres = []
        valid_list = ['1', '5', '15']
        for metric in valid_list:
            output = dynaroutingapi.rip_config(**{'ConnectedMetric': metric})
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid Redistribute OSPF Routes failed")

    def test_02_check_invalid_redistribute_ospf_rip(self):
        invalidres = []
        invalid_list = ['-1', '0', '16']
        for metric in invalid_list:
            output, msg = dynaroutingapi.rip_config(msg=True, **{'ConnectedMetric': metric})
            if 'Data out of bounds' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 3, "ERR: config invalid Redistribute OSPF Routes failed")

    def test_03_init_redistribute_ospf(self):
        output = dynaroutingapi.rip_config(**{'AdministrativeDistance': '1'})
        Assertion.assert_equal(output, True, "ERR: init Redistribute OSPF Routes failed")


# check OSPF configure must disable in all ports.
class TestGUI_TC16(Test):
    uuid = "SOSAIOT-TC-55668"
    description = show_testcase_info(TESTPLAN, 'GUI_TC16', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_ospf_config_must_disable_in_all(self):
        ospf_configure = {
            'ifName': 'ALL',
            'ospf': 'OSPF Disabled',
        }
        output = dynaroutingapi.get_ospf_list_data()
        res = check_routing_config(output, **ospf_configure)
        Assertion.assert_equal(res, False, "ERR: check rip config failed")


# ospf boundaries for Dead Interval Metric (1~65535)
class TestGUI_TC18(Test):
    uuid = "SOSAIOT-TC-55670"
    description = show_testcase_info(TESTPLAN, 'GUI_TC18', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_dead_interval(self):
        validres = []
        valid_list = ['11', '6666', '65535']
        for metric in valid_list:
            ospf_dict = {
                'interface': 'X1',
                'mode': 'enable',
                'dead_interval': metric,
                'cost': 'on',
            }
            output = dynaroutingapi.set_ospf2(**ospf_dict)
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid Dead Interval failed")

    def test_02_check_invalid_dead_interval(self):
        invalidres = []
        invalid_list = ['-1', '0', '65536']
        for metric in invalid_list:
            ospf_dict = {
                'interface': 'X1',
                'mode': 'enable',
                'dead_interval': metric,
            }
            output, msg = dynaroutingapi.set_ospf2(msg=True, **ospf_dict)
            if 'Data out of bounds' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 3, "ERR: config invalid Dead Interval failed")

    def test_03_init_dead_interval_ospf(self):
        ospf_dict = {
            'interface': 'X1',
            'mode': 'enable',
            'dead_interval': '40',
            'cost': 'on',
        }
        output= dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: init Dead Interval failed")


# ospf boundaries for Interface Cost Metric (1~65535)
class TestGUI_TC19(Test):
    uuid = "SOSAIOT-TC-55671"
    description = show_testcase_info(TESTPLAN, 'GUI_TC19', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_interface_cost(self):
        validres = []
        valid_list = ['11', '6666', '65535']
        for metric in valid_list:
            ospf_dict = {
                'interface': 'X1',
                'mode': 'enable',
                'cost': metric,
            }
            output = dynaroutingapi.set_ospf2(**ospf_dict)
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid Interface Cost failed")

    def test_02_check_invalid_interface_cost(self):
        invalidres = []
        invalid_list = ['-1', '0', '65536']
        for metric in invalid_list:
            ospf_dict = {
                'interface': 'X1',
                'mode': 'enable',
                'cost': metric,
            }
            output, msg = dynaroutingapi.set_ospf2(msg=True, **ospf_dict)
            if 'Data out of bounds' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 3, "ERR: config invalid Interface Cost failed")

    def test_03_init_interface_cost(self):
        ospf_dict = {
            'interface': 'X1',
            'mode': 'enable',
            'cost': 'on',
        }
        output= dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: init Interface Cost failed")


# OSPF Area field and its boundaries <0-4294967295>
class TestGUI_TC21(Test):
    uuid = "SOSAIOT-TC-55674"
    description = show_testcase_info(TESTPLAN, 'GUI_TC21', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_area(self):
        validres = []
        valid_list = ['1', '666666', '4294967295', '12.12.12.12']
        for metric in valid_list:
            ospf_dict = {
                'interface': 'X1',
                'mode': 'enable',
                'area': metric,
                'cost': 'on'
            }
            output = dynaroutingapi.set_ospf2(**ospf_dict)
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 4, "ERR: config valid area failed")

    def test_02_check_invalid_area(self):
        invalidres = []
        invalid_list = ['-1', '256.256.256.256', '4294967296']
        for metric in invalid_list:
            ospf_dict = {
                'interface': 'X1',
                'mode': 'enable',
                'area': metric,
                'cost': 'on'
            }
            output, msg = dynaroutingapi.set_ospf2(msg=True, **ospf_dict)
            if 'Data is incorrectly formatted' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 3, "ERR: config invalid area failed")

    def test_03_init_area(self):
        ospf_dict = {
            'interface': 'X1',
            'mode': 'enable',
            'area': '0',
            'cost': 'on'
        }
        output= dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: init area failed")


# Hello Interval field boundaries <0-65536>
class TestGUI_TC22(Test):
    uuid = "SOSAIOT-TC-55675"
    description = show_testcase_info(TESTPLAN, 'GUI_TC22', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_hello_interval(self):
        validres = []
        valid_list = ['1', '6666', '65535']
        for metric in valid_list:
            ospf_dict = {
                'interface': 'X1',
                'mode': 'enable',
                'hello_interval': metric,
                'dead_interval': metric,
                'cost': 'on'
            }
            output = dynaroutingapi.set_ospf2(**ospf_dict)
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid hello interval failed")

    def test_02_check_invalid_hello_interval(self):
        invalidres = []
        invalid_list = ['-1', '0', '65536']
        for metric in invalid_list:
            ospf_dict = {
                'interface': 'X1',
                'mode': 'enable',
                'hello_interval': metric,
                'dead_interval': metric,
                'cost': 'on'
            }
            output, msg = dynaroutingapi.set_ospf2(msg=True, **ospf_dict)
            if 'Data out of bounds' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 3, "ERR: config invalid hello interval failed")

    def test_03_init_hello_interval(self):
        ospf_dict = {
            'interface': 'X1',
            'mode': 'enable',
            'hello_interval': '10',
            'dead_interval': '10',
            'cost': 'on'
        }
        output= dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: init hello interval failed")


# Router Priority field boundaries <0-255>
class TestGUI_TC23(Test):
    uuid = "SOSAIOT-TC-55676"
    description = show_testcase_info(TESTPLAN, 'GUI_TC23', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_router_priority(self):
        validres = []
        valid_list = ['2', '66', '255']
        for metric in valid_list:
            ospf_dict = {
                'interface': 'X1',
                'mode': 'enable',
                'router_priority': metric,
                'cost': 'on'
            }
            output = dynaroutingapi.set_ospf2(**ospf_dict)
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid router priority failed")

    def test_02_check_invalid_router_priority(self):
        invalidres = []
        invalid_list = ['-1', 'FF', '256']
        for metric in invalid_list:
            ospf_dict = {
                'interface': 'X1',
                'mode': 'enable',
                'router_priority': metric,
                'cost': 'on'
            }
            output, msg = dynaroutingapi.set_ospf2(msg=True, **ospf_dict)
            if 'Data out of bounds' in json.dumps(msg) or 'Invalid Interface Priority' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 3, "ERR: config invalid router priority failed")

    def test_03_init_router_priority(self):
        ospf_dict = {
            'interface': 'X1',
            'mode': 'enable',
            'router_priority': '1',
            'cost': 'on'
        }
        output= dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: init router priority failed")


# format of data in the OSPF Router-ID
class TestGUI_TC24(Test):
    uuid = "SOSAIOT-TC-55677"
    description = show_testcase_info(TESTPLAN, 'GUI_TC24', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC24')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_router_id(self):
        validres = []
        valid_list = ['192.168.168.1', '12.12.12.254', '172.0.0.10']
        for metric in valid_list:
            ospf_dict = {
                'router_id': metric,
            }
            output = dynaroutingapi.ospf2_config(**ospf_dict)
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid OSPF Router-ID failed")

    def test_02_check_invalid_router_id(self):
        invalidres = []
        invalid_list = ['-1', '0', '192.168.168.256', '0.0.0.0']
        for metric in invalid_list:
            ospf_dict = {
                'router_id': metric,
            }
            output, msg = dynaroutingapi.ospf2_config(msg=True, **ospf_dict)
            if 'Data is incorrectly formatted' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 4, "ERR: config invalid OSPF Router-ID failed")

    def test_03_init_router_id(self):
        ospf_dict = {
            'router_id': Parameter.FIREWALL,
        }
        output= dynaroutingapi.ospf2_config(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: init OSPF Router-ID failed")


# Default Metric field boundaries (1 - 16777214)
class TestGUI_TC26(Test):
    uuid = "SOSAIOT-TC-55679"
    description = show_testcase_info(TESTPLAN, 'GUI_TC26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_default_metric(self):
        validres = []
        valid_list = ['1', '6666', '16777214']
        for metric in valid_list:
            ospf_dict = {
                'metric': metric,
            }
            output = dynaroutingapi.ospf2_config(**ospf_dict)
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid Default Metric failed")

    def test_02_check_invalid_default_metric(self):
        invalidres = []
        invalid_list = ['-1', '0', '16777215']
        for metric in invalid_list:
            ospf_dict = {
                'metric': metric,
            }
            output, msg = dynaroutingapi.ospf2_config(msg=True, **ospf_dict)
            if 'Data out of bounds' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 3, "ERR: config invalid Default Metric failed")

    def test_03_init_default_metric(self):
        ospf_dict = {
            'metric': '1',
        }
        output= dynaroutingapi.ospf2_config(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: init OSPF Default Metric failed")


# Verify that the Metric and Metric Type become available
class TestGUI_TC27(Test):
    uuid = "SOSAIOT-TC-55680"
    description = show_testcase_info(TESTPLAN, 'GUI_TC27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_original_default_route(self):
        res = []
        org_list = ['never', 'wan-up', 'always']
        for originate in org_list:
            ospf_dict = {
                'default_route': originate,
                'metric': '10',
                'metric_type': '2',
            }
            output = dynaroutingapi.ospf2_config(**ospf_dict)
            res.append(output)
        logger.info(f'config original result: {res}')
        Assertion.assert_equal(res.count(True), 3, "ERR: config original default route failed")

    def test_02_init_original_default_route(self):
        ospf_dict = {
            'default_route': 'never',
            'metric': '11',
            'metric_type': '1',
        }
        output = dynaroutingapi.ospf2_config(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: init original default route failed")


# boundaries of the Metric for Original Default Route (1 - 16777214)
class TestGUI_TC28(Test):
    uuid = "SOSAIOT-TC-55681"
    description = show_testcase_info(TESTPLAN, 'GUI_TC28', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC28')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_original_default_metric(self):
        validres = []
        valid_list = ['1', '6666', '16777214']
        for metric in valid_list:
            ospf_dict = {
                'default_route': 'wan-up',
                'metric': metric,
            }
            output = dynaroutingapi.ospf2_config(**ospf_dict)
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid original Default Metric failed")

    def test_02_check_invalid_original_default_metric(self):
        invalidres = []
        invalid_list = ['-1', '0', '16777215']
        for metric in invalid_list:
            ospf_dict = {
                'default_route': 'wan-up',
                'metric': metric,
            }
            output, msg = dynaroutingapi.ospf2_config(msg=True, **ospf_dict)
            if 'Data out of bounds' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 3, "ERR: config invalid original Default Metric failed")

    def test_03_init_original_default_metric(self):
        ospf_dict = {
            'default_route': 'never',
            'metric': '11',
        }
        output= dynaroutingapi.ospf2_config(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: init OSPF original Default Metric failed")


# boundaries of the Metric for Redistribute Static Routes (1 - 16777214)
class TestGUI_TC31(Test):
    uuid = "SOSAIOT-TC-55685"
    description = show_testcase_info(TESTPLAN, 'GUI_TC31', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC31')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_static_routes_metric(self):
        validres = []
        valid_list = ['1', '6666', '16777214']
        for metric in valid_list:
            ospf_dict = {
                'static_route': 'on',
                'static_metric': metric,
            }
            output = dynaroutingapi.ospf2_config(**ospf_dict)
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid static routes Metric failed")

    def test_02_check_invalid_static_routes_metric(self):
        invalidres = []
        invalid_list = ['-1', '0', '16777215']
        for metric in invalid_list:
            ospf_dict = {
                'static_route': 'on',
                'static_metric': metric,
            }
            output, msg = dynaroutingapi.ospf2_config(msg=True, **ospf_dict)
            if 'Data out of bounds' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 3, "ERR: config invalid static routes Metric failed")

    def test_03_init_static_routes_metric(self):
        ospf_dict = {
            'static_route': 'on',
            'static_metric': '1',
        }
        output= dynaroutingapi.ospf2_config(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: init OSPF static routes Metric failed")


# boundaries of the Tag for Advertise Static Routes (1 - 4294967295)
class TestGUI_TC32(Test):
    uuid = "SOSAIOT-TC-55686"
    description = show_testcase_info(TESTPLAN, 'GUI_TC32', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC32')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_static_routes_tag(self):
        validres = []
        valid_list = ['0', '6666', '4294967295']
        for metric in valid_list:
            ospf_dict = {
                'static_route': 'on',
                'static_tag': metric,
            }
            output = dynaroutingapi.ospf2_config(**ospf_dict)
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid static routes tag failed")

    def test_02_check_invalid_static_routes_tag(self):
        invalidres = []
        invalid_list = ['-1', '4294967296']
        for metric in invalid_list:
            ospf_dict = {
                'static_route': 'on',
                'static_tag': metric,
                'cost': 'on',
            }
            output, msg = dynaroutingapi.ospf2_config(msg=True, **ospf_dict)
            if ' OSPF Internal Error' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 2, "ERR: config invalid static routes tag failed")

    def test_03_init_static_routes_tag(self):
        ospf_dict = {
            'static_route': 'on',
            'static_tag': '1',
        }
        output= dynaroutingapi.ospf2_config(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: init OSPF static routes tag failed")


# boundaries of the Metric for Redistribute Connected Networks (1 - 16777214)
class TestGUI_TC35(Test):
    uuid = "SOSAIOT-TC-55689"
    description = show_testcase_info(TESTPLAN, 'GUI_TC35', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC35')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_connected_networks_metric(self):
        res = CaseParams.tc13_test_result
        logger.info(f'use tc13 test result: {res}')
        Assertion.assert_equal(res.count(True), 2, "ERR: check connected networks metric failed")


# boundaries for Redistribute Connected Networks Tag (1 - 4294967295)
class TestGUI_TC36(Test):
    uuid = "SOSAIOT-TC-55690"
    description = show_testcase_info(TESTPLAN, 'GUI_TC36', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC36')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_connected_networks_tag(self):
        validres = []
        valid_list = ['0', '6666', '4294967295']
        for metric in valid_list:
            ospf_dict = {
                'connect_network': 'on',
                'connect_tag': metric,
            }
            output = dynaroutingapi.ospf2_config(**ospf_dict)
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid Connected Networks tag failed")

    def test_02_check_invalid_connected_networks_tag(self):
        invalidres = []
        invalid_list = ['-4294967295', '-1', '4294967296']
        for metric in invalid_list:
            ospf_dict = {
                'connect_network': 'on',
                'connect_tag': metric,
            }
            output, msg = dynaroutingapi.ospf2_config(msg=True, **ospf_dict)
            if 'OSPF Internal Error' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 3, "ERR: config invalid Connected Networks tag failed")

    def test_03_init_connected_networks_tag(self):
        ospf_dict = {
            'connect_network': 'on',
            'connect_tag': '1',
        }
        output= dynaroutingapi.ospf2_config(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: init OSPF Connected Networks tag failed")


# boundaries of the Metric for Redistribute RIP Routes (1 - 16777214)
class TestGUI_TC39(Test):
    uuid = "SOSAIOT-TC-55693"
    description = show_testcase_info(TESTPLAN, 'GUI_TC39', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC39')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_rip_routes_metric(self):
        validres = []
        valid_list = ['1', '6666', '16777214']
        for metric in valid_list:
            ospf_dict = {
                'rip_route': 'on',
                'rip_metric': metric,
            }
            output = dynaroutingapi.ospf2_config(**ospf_dict)
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid rip routes Metric failed")

    def test_02_check_invalid_rip_routes_metric(self):
        invalidres = []
        invalid_list = ['-1', '0', '16777215']
        for metric in invalid_list:
            ospf_dict = {
                'rip_route': 'on',
                'rip_metric': metric,
            }
            output, msg = dynaroutingapi.ospf2_config(msg=True, **ospf_dict)
            if 'Data out of bounds' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 3, "ERR: config invalid rip routes Metric failed")

    def test_03_init_rip_routes_metric(self):
        ospf_dict = {
            'rip_route': 'on',
            'rip_metric': '1',
        }
        output= dynaroutingapi.ospf2_config(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: init OSPF rip routes Metric failed")


# boundaries of the tag for Redistribute RIP Routes (1 - 4294967295)
class TestGUI_TC40(Test):
    uuid = "SOSAIOT-TC-55694"
    description = show_testcase_info(TESTPLAN, 'GUI_TC40', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'GUI_TC40')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_valid_rip_routes_metric(self):
        validres = []
        valid_list = ['0', '6666', '4294967295']
        for metric in valid_list:
            ospf_dict = {
                'rip_route': 'on',
                'rip_tag': metric,
            }
            output = dynaroutingapi.ospf2_config(**ospf_dict)
            validres.append(output)
        logger.info(f'config valid values: {validres}')
        Assertion.assert_equal(validres.count(True), 3, "ERR: config valid rip routes tag failed")

    def test_02_check_invalid_rip_routes_metric(self):
        invalidres = []
        invalid_list = ['-4294967295', '-1', '4294967296']
        for metric in invalid_list:
            ospf_dict = {
                'rip_route': 'on',
                'rip_tag': metric,
            }
            output, msg = dynaroutingapi.ospf2_config(msg=True, **ospf_dict)
            if 'OSPF Internal Error' in json.dumps(msg):
                invalidres.append(True)
            else:
                invalidres.append(False)
        logger.info(f'config invalid values: {invalidres}')
        Assertion.assert_equal(invalidres.count(True), 3, "ERR: config invalid rip routes tag failed")

    def test_03_init_rip_routes_metric(self):
        ospf_dict = {
            'rip_route': 'on',
            'rip_tag': '1',
        }
        output= dynaroutingapi.ospf2_config(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: init OSPF rip routes tag failed")




