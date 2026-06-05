import unittest
from settings import *
cdrouter = cdrouter_test.CDRTest(Parameter.CDROUTER,path=Parameter.TESTPATH, case=Parameter.CASE, conf=Parameter.CONF, log=Parameter.LOG, ver='cdr2.6')


class Test_22_Add_NM_Policy(Test):
    description= show_testcase_info(Parameter.TESTPLAN, '22', description=True)['title']
    uuid = "SOSAIOT-TC-58714"

    def test_22_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_22_01_add_network_monitor_policy(self):
        nm_dict={
            "network_monitors": [{
                "policy": {
                    "ipv4": {
                        "name": 'tc22',
                        'probe': {'target': {'name': 'remotehost'}, 'type':{"tcp":{"port":1234,"explicit":True}}, 'interval': 5,},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'outbound_interface':'X0',
                        'next_hop':{'name':'wanhost'},
                        'comment':'nm for tc22'
                    }
                }
            }]
        }
        rc = nm.add_network_monitor(**nm_dict)
        Assertion.assert_equal(rc, True, "ERR: add nm policy failed")

    def test_22_02_add_route_with_probe(self):
        route_dict = {"route_policies":
            [{"ipv4":
                {
                    "name":"tc22-route",
                    "comment":"",
                    "interface":"X0",
                    "metric":3,
                    "service":{"any":True},
                    "gateway":{"default":True},
                    "source":{"group":"LAN Subnets"},
                    "destination":{"group":"WAN Subnets"},
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"tc22",
                    "distance":{"auto":True},
                    "disable_when_probes_succeed":False,
                    "default_probe_state_up":False,
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]}
        rc = route.add_route_policy(**route_dict)
        Assertion.assert_equal(rc, True, "ERR: add route policy with probe failed")

    def test_22_03_del_route_policy(self):
        rc = route.del_route_policy_by_name(name='tc22-route')
        Assertion.assert_equal(rc, True, "ERR: delete nm policy failed")

    def test_22_04_del_network_monitor_policy(self):
        rc = nm.del_network_monitor(name='tc22')
        Assertion.assert_equal(rc, True, "ERR: delete nm policy failed")


class Test_23_Edit_NM_Policy(Test):
    description= show_testcase_info(Parameter.TESTPLAN, '23', description=True)['title']
    uuid = "SOSAIOT-TC-58715"

    def test_23_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_23_02_add_AO(self):
        pc1 = Host('localhost')
        output = pc1.send_command("ifconfig eth1|sed -n '2p'")
        match = re.search(r'inet addr:(\d*.\d*.\d*.\d*)',output)
        lan_ip = '192.168.168.100'
        if match.group(1) == '192.168.168.100':
            lan_ip = '192.168.168.200'
        ao_opt = {
            "object_type":"host",
            "name": 'PC1_eth0',
            "zone": 'LAN',
            "value":  lan_ip
        }
        rc = ao.config_addressobject(**ao_opt) 
        Assertion.assert_equal(rc, True, "ERR: add ao failed")

    def test_23_03_add_NM(self):
        nm_dict={
            "network_monitors": [{
                "policy": {
                    "ipv4": {
                        'name': 'tc23',
                        'probe': {'target': {'name':'PC1_eth0'}, 'type': {'ping': 'explicit'}, 'interval': 5},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'comment': ''
                    }
                }
            }]
        }
        rc = nm.add_network_monitor(**nm_dict)
        Assertion.assert_equal(rc, True, "ERR: add nm policy failed")
        
    def test_23_03_edit_NM(self):
        nm_dict={
            "network_monitors": [{
                "policy": {
                    "ipv4": {
                        'name': 'tc23',
                        'probe': {'target': {'name':'PC1_eth0'}, 'type': {'tcp': {'port':1234,'explicit':True}}, 'interval': 5},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'comment': ''
                    }
                }
            }]
        }
        rc = nm.edit_network_monitor(**nm_dict)
        Assertion.assert_equal(rc, True, "ERR: add nm policy failed")
        
    def test_23_04_del_network_monitor_policy(self):
        rc = nm.del_network_monitor(name='tc23')
        Assertion.assert_equal(rc, True, "ERR: delete nm policy failed")


class Test_24_Delete_NM_Policy(Test):
    description= show_testcase_info(Parameter.TESTPLAN, '24', description=True)['title']
    uuid = "SOSAIOT-TC-58716"

    def test_24_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_24_01_add_NM(self):
        nm_dict={
            "network_monitors": [{
                "policy": {
                    "ipv4": {
                        'name': 'tc24',
                        'probe': {'target': {'name':'PC1_eth0'}, 'type': {'ping': 'explicit'}, 'interval': 5},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'comment': ''
                    }
                }
            }]
        }
        rc = nm.add_network_monitor(**nm_dict)
        Assertion.assert_equal(rc, True, "ERR: add nm policy failed")
           
    def test_24_04_del_network_monitor_policy(self):
        rc = nm.del_network_monitor(name='tc24')
        Assertion.assert_equal(rc, True, "ERR: delete nm policy failed")

    def test_24_05_delete_aos(self):
        rc = ao.del_addressobject(**{'ip_type':'ipv4','name':'PC1_eth0'})
        Assertion.assert_equal(rc, True, "ERR: delete ao failed")

        
class Test_30_Check_NAT(Test):
    description= show_testcase_info(Parameter.TESTPLAN, '30', description=True)['title']
    uuid = "SOSAIOT-TC-58721"

    def test_30_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '30')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_30_01_add_AO(self):
        ao_opt1 = {
            "object_type":"host",
            "name": 'wan_host',
            "zone": 'WAN',
            "value":  '3.3.3.3'
        }
        ao_opt2 = {
            "object_type":"range",
            "name": 'lan_range',
            "zone": 'LAN',
            "value":  '192.168.168.10,192.168.168.20'
        }
        rc = ao.config_addressobject(**ao_opt1) 
        rc &= ao.config_addressobject(**ao_opt2) 
        Assertion.assert_equal(rc, True, "ERR: add ao failed")

    def test_30_02_add_nat_policy(self):
        natpolicy_dict = {
            "nat_policies":[
                { 
                    "ipv4":{ 
                        "name":"tc30",
                        "inbound": "X1",
                        "outbound": "any",
                        "source": {
                            "any": True
                        },
                        "translated_source": {
                            "original": True
                        },
                        "destination": {
                            "name": "wan_host"
                        },
                        "translated_destination": {
                            "name":"lan_range"
                        },
                        "high_availability":{
                            "probing":{
                                "probe_type":{
                                    "icmp_ping":True
                                },
                                "probe_every":5,
                            }
                        }
                        #"source_port_remap": True  ###this option can be enabled only when "translated source" is not Original
                    }
                }
            ]
        }
        rc = nat.add_nat_policy(**natpolicy_dict)
        Assertion.assert_equal(rc, True, "ERR: add nat policy failed")

    def test_30_03_check_nm_policy(self):
        rc = nm.get_network_monitor()
        logger.info(rc)
        Assertion.assert_regular(rc['network_monitors'][0]['policy']['ipv4']['name'], 'NAT', "ERR: verify network monitor name failed")
        Assertion.assert_equal(rc['network_monitors'][0]['policy']['ipv4']['probe']['target']['name'], 'lan_range', "ERR:verify network monitor target failed")
        Assertion.assert_equal(rc['network_monitors'][0]['policy']['ipv4']['probe']['type']['ping'], 'non-explicit', "ERR: verify network monitor type failed")
        Assertion.assert_equal(rc['network_monitors'][0]['policy']['ipv4']['comment'], 'Auto-added from configured NAT Policy probe', "ERR: verify network monitor comment failed")

    def test_30_04_delete_nat_policy(self):
        rc = nat.del_nat_policy_by_name(name='tc30')
        Assertion.assert_equal(rc, True, "ERR: delete nat policy failed")

    def test_30_05_delete_aos(self):
        rc = ao.del_addressobject(**{'ip_type':'ipv4','name':'wan_host'})
        rc &= ao.del_addressobject(**{'ip_type':'ipv4','name':'lan_range'})
        Assertion.assert_equal(rc, True, "ERR: delete aos failed")


@paramunittest.parametrized(
    {"check": 'tsr', 'tcid':'37','uuid':'1514774','description':show_testcase_info(Parameter.TESTPLAN, '37', description=True)['title']},
    {"check": 'pref','tcid':'64','uuid':'1514793','description':show_testcase_info(Parameter.TESTPLAN, '64', description=True)['title']},
)

class Test_37_64_TSR_PREF_Check(Test):
    def setParameters(self,check, tcid, uuid, description):
        '''parameter check,tcid,uuid must be same with the dict above'''
        self.check = check
        self.tcid = tcid
        self.uuid = uuid
        self.description = description

    def test_37_64_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '37')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")    

    def test_37_64_01_add_AO(self):
        ao_opt1 = {
            "object_type":"host",
            "name": 'lan_host',
            "zone": 'LAN',
            "value":  '192.168.168.100'
        }
        ao_opt2 = {
            "object_type":"range",
            "name": 'lan_range',
            "zone": 'LAN',
            "value":  '192.168.168.129,192.168.168.130'
        }
        ao_opt3= {
            "object_type":"host",
            "name": 'wan_host',
            "zone": 'WAN',
            "value":  '3.3.3.3'
        }
        ao_opt4= {
            "object_type":"host",
            "name": 'wan_gw',
            "zone": 'WAN',
            "value":  '1.2.3.4'
        }
        ao_opt5= {
            "object_type":"host",
            "name": 'lan_gw',
            "zone": 'LAN',
            "value":  '192.168.168.102'
        }
        rc = ao.config_addressobject(**ao_opt1) 
        rc &= ao.config_addressobject(**ao_opt2) 
        rc &= ao.config_addressobject(**ao_opt3) 
        rc &= ao.config_addressobject(**ao_opt4) 
        rc &= ao.config_addressobject(**ao_opt5) 
        Assertion.assert_equal(rc, True, "ERR: add ao failed")

    def test_37_64_02_add_NM(self):
        nm_dict1={
            "network_monitors": [{
                "policy": {
                    "ipv4": {
                        'name': 'LAN-Host',
                        'probe': {'target': {'name':'lan_host'}, 'type': {'tcp': {'port':1234}}, 'interval': 5},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'comment': ''
                    }
                }
            }]
        }
        nm_dict2={
            "network_monitors": [{
                "policy": {
                    "ipv4": {
                        'name': 'LAN-Range',
                        'probe': {'target': {'name':'lan_range'}, 'type': {'ping': 'explicit'}, 'interval': 5,'next_hop':{'name':'lan_gw'},'outbound_interface':'X0'},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'comment': ''
                    }
                }
            }]
        }
        nm_dict3={
            "network_monitors": [{
                "policy": {
                    "ipv4": {
                        'name': 'WAN-GW',
                        'probe': {'target': {'name':'wan_gw'}, 'type': {'ping': 'non-explicit'}, 'interval': 5},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'comment': ''
                    }
                }
            }]
        }
        nm_dict4={
            "network_monitors": [{
                "policy": {
                    "ipv4": {
                        'name': 'WAN-Host',
                        'probe': {'target': {'name':'wan_host'}, 'type': {'ping': 'explicit'}, 'interval': 5,'next_hop':{'name':'wan_gw'},'outbound_interface':'X1'},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'comment': ''
                    }
                }
            }]
        }
        rc = nm.add_network_monitor(**nm_dict1)
        rc &= nm.add_network_monitor(**nm_dict2)
        rc &= nm.add_network_monitor(**nm_dict3)
        rc &= nm.add_network_monitor(**nm_dict4)
        Assertion.assert_equal(rc, True, "ERR: add nm policy failed")

    def test_37_64_03_get_tsr_or_pref(self):
        if self.check == 'pref':
            setting.export_setting_exp('/tmp/pepbr.exp')
            setting.boot_fw(2)
            setting.import_setting_exp('/tmp/pepbr.exp')
        rc = tsr.get_tsr_part('Network','Network Monitor')
        logger.info(rc)
        Assertion.assert_regular(rc,'LAN-Host', "ERR:check nm policy1 in tsr failed")
        Assertion.assert_regular(rc, 'LAN-Range', "ERR:check nm policy2 in tsr failed")
        Assertion.assert_regular(rc, 'WAN-GW', "ERR:check nm policy3 in tsr failed")
        Assertion.assert_regular(rc, 'WAN-Host', "ERR:check nm policy3 in tsr failed")

    def test_37_64_04_delete_nm(self):
        rc = nm.del_network_monitor(name='LAN-Host')
        rc &= nm.del_network_monitor(name='LAN-Range')
        rc &= nm.del_network_monitor(name='WAN-GW')
        rc &= nm.del_network_monitor(name='WAN-Host')
        Assertion.assert_equal(rc, True, "ERR: delete nm policy failed")
   
    def test_37_64_05_delete_aos(self):
        rc = ao.del_addressobject(**{'ip_type':'ipv4','name':'lan_host'})
        rc &= ao.del_addressobject(**{'ip_type':'ipv4','name':'lan_range'})
        rc &= ao.del_addressobject(**{'ip_type':'ipv4','name':'wan_gw'})
        rc &= ao.del_addressobject(**{'ip_type':'ipv4','name':'wan_host'})
        rc &= ao.del_addressobject(**{'ip_type':'ipv4','name':'lan_gw'})
        Assertion.assert_equal(rc, True, "ERR: delete aos failed")


@paramunittest.parametrized(
    {"probe_type": 'tcp+explicit', 'target':'remotehost', 'port': '1234','testvar':'swl_remoteHostTcpPort','tcid':'41','uuid':'1514779','description':show_testcase_info(Parameter.TESTPLAN, '41', description=True)['title']},
    {"probe_type": 'ping+non-explicit', 'target':'wanhost', 'port': '','testvar':'','tcid':'38','uuid':'1514775','description':show_testcase_info(Parameter.TESTPLAN, '38', description=True)['title']},
    {"probe_type": 'tcp+non_explicit', 'target':'wanhost', 'port': '1234','testvar':'swl_wanTcpPort','tcid':'39','uuid':'1514776','description':show_testcase_info(Parameter.TESTPLAN, '39', description=True)['title']},
    {"probe_type": 'ping+explicit', 'target':'remotehost', 'port': '','testvar':'','tcid':'40','uuid':'1514778','description':show_testcase_info(Parameter.TESTPLAN, '40', description=True)['title']},
)

class Test_38_39_40_41_Probe_Type_Test(Test):
    # cdrouter = cdrouter_test.CDRTest(Parameter.CDROUTER,path=Parameter.TESTPATH, case=Parameter.CASE, conf=Parameter.CONF, log=Parameter.LOG, ver='cdr2.6')

    def setParameters(self, probe_type, target, port, testvar, tcid, uuid, description):
        '''parameter probe_type,port,target,tcid,uuid must be same with the dict above'''
        self.probe_type = probe_type
        self.target = target
        self.port = port
        self.testvar=testvar
        self.tcid = tcid
        self.uuid = uuid
        self.description = description

    def test_38_39_40_41_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_38_39_40_41_01_add_network_monitor_policy(self):
        self.nm_dict={
            "network_monitors": [{
                "policy": {
                    "ipv4": {
                        'name': 'tc' + str(self.tcid),
                        'probe': {'target': {'name': self.target}, 'type': {self.probe_type.split('+')[0]: self.probe_type.split('+')[1]}, 'interval': 5},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'comment': ''
                    }
                }
            }]
        }
        if self.probe_type == 'ping+explicit' or self.probe_type == 'tcp+explicit':
            self.nm_dict['network_monitors'][0]['policy']['ipv4']['outbound_interface'] = 'X1'
            self.nm_dict['network_monitors'][0]['policy']['ipv4']['next_hop'] = {'name': 'wanhost'}
        if 'tcp' in self.probe_type:
            self.nm_dict['network_monitors'][0]['policy']['ipv4']['probe']['type']['tcp']={}
            self.nm_dict['network_monitors'][0]['policy']['ipv4']['probe']['type']['tcp']['port'] = int(self.port)
            self.nm_dict['network_monitors'][0]['policy']['ipv4']['probe']['type']['tcp'][self.probe_type.split('+')[1]] = True
       
# {"network_monitors":[{"policy":{"ipv4":{"name":"explicit","probe":{"target":{"group":"WAN Interface IP"},"type":{"tcp":{"port":1233,"explicit":true}},"interval":5},"reply_timeout":1,"interval":{"missed":3,"successful":3},"must_respond":false,"comment":"","next_hop":{"name":"X1 IP"},"outbound_interface":"X1","rst_as_miss":false}}}]}
# {"network_monitors":[{"policy":{"ipv4":{"name":"ddd","probe":{"target":{"group":"LAN Interface IP"},"type":{"ping":"explicit"},"interval":5},"reply_timeout":1,"interval":{"missed":3,"successful":3},"must_respond":false,"comment":"","next_hop":{"name":"X0 IP"},"outbound_interface":"X0"}}}]}
            
        rc = nm.add_network_monitor(**self.nm_dict)
        Assertion.assert_equal(rc, True, "ERR: add nm policy failed")

    def test_38_39_40_41_02_check_network_monitor_policy_before_traffic(self):
        output = nm.get_network_monitor_status()
        # {"data":{"resourceType":"netmon-status","dataType":"current","netMonArray":[{"name":"netMonProbes-0","policy_name":"ddd","led":"yellow","netMonProbeStatus":{ "probeStatus":"Probes 0% Successful", "resolvedProbeTargets":1, "probesSent":562, "responsesReceived":0, "probeTargets":"0 Up / 0 Down / 1 Unknown", "targetArray":[{"targets":{"ip":"192.168.168.168","status":"UNKNOWN"}}]}},{"name":"netMonProbes-1","policy_name":"test","led":"green","netMonProbeStatus":{ "probeStatus":"Probes 100% Successful", "resolvedProbeTargets":1, "probesSent":32857, "responsesReceived":32857, "probeTargets":"1 Up / 0 Down / 0 Unknown", "targetArray":[{"targets":{"ip":"192.168.168.169","status":"UP"}}]}},{"name":"netMonProbes-2","policy_name":"explicit","led":"red","netMonProbeStatus":{ "probeStatus":"Probes 0% Successful", "resolvedProbeTargets":3, "probesSent":1758, "responsesReceived":0, "probeTargets":"0 Up / 2 Down / 1 Unknown", "targetArray":[{"targets":{"ip":"0.0.0.0","status":"DOWN"}},{"targets":{"ip":"0.0.0.0","status":"DOWN"}},{"targets":{"ip":"100.10.0.10","status":"UNKNOWN"}}]}},{"name":"netMonProbes-3","policy_name":"ping","led":"yellow","netMonProbeStatus":{ "probeStatus":"Probes 0% Successful", "resolvedProbeTargets":1, "probesSent":16365, "responsesReceived":0, "probeTargets":"0 Up / 0 Down / 1 Unknown", "targetArray":[{"targets":{"ip":"192.168.168.168","status":"UNKNOWN"}}]}}]},"productModel":"TZ 370","upTime":"8 Days 21:04:49","systime":1612305181,"loggedin":true,"status":"OK","apiLink":"HTTPS://SONICOS-API.SONICWALL.COM/index.html?sonicwallIp=0.0.0.0&sonicwallPort=443&model=TZ&version=7.0.1"}
        try:
            led = output['data']['netMonArray'][0]['led']
        except:
            led = None
            logger.error('Fail to get led info.')
        Assertion.assert_equal(led, 'yellow', f"ERR: The led should be yellow but {led}")
        
    def test_38_39_40_41_03_run_cdrouter(self):
        testvar=''
        if self.testvar:
            testvar = f' -testvar {self.testvar}={self.port} '
        cdrouter.run_case(testvar=testvar, backend=True)

    @repeat_method(3)
    def test_38_39_40_41_04_check_network_monitor_policy_after_traffic(self):
        logger.info('Sleep 30s to wait for the policy become green')
        time.sleep(30)
        output = nm.get_network_monitor_status()
        try:
            led = output['data']['netMonArray'][0]['led']
        except:
            led = None
            logger.error('Fail to get led info.')
        Assertion.assert_equal(led, 'green', f"ERR: The led should be green but {led}")
        
    def test_38_39_40_41_05_disconnect_X1(self):
        Parameter.OS_STACK.set_node_interface_state('UTM','X1', 'disable')
        logger.info('Sleep 30s to wait for the policy become green')
        time.sleep(30)
        output = nm.get_network_monitor_status()
        try:
            led = output['data']['netMonArray'][0]['led']
        except:
            led = None
            logger.error('Fail to get led info.')
        Assertion.assert_equal(led, 'red', f"ERR: The led should be red but {led}")

    def test_38_39_40_41_06_del_network_monitor_policy(self):
        rc = nm.del_network_monitor(name='tc' + str(self.tcid))
        Assertion.assert_equal(rc, True, "ERR: delete nm policy failed")

    def test_38_39_40_41_07_reconnect_X1(self):
        rc = Parameter.OS_STACK.set_node_interface_state('UTM','X1', 'enable')
        Assertion.assert_equal(rc, True, "ERR: reconnect X1 failed")

    def test_38_39_40_41_08_stop_cdrouter(self):
        rc = cdrouter.terminate_case()
        Assertion.assert_equal(rc, True, "ERR: terminate cdrouter failed")


@paramunittest.parametrized(
    {"host":'up','tcid':'55','uuid':'1514786','description':show_testcase_info(Parameter.TESTPLAN, '55', description=True)['title']},
    {"host":'down','tcid':'56','uuid':'1514787','description':show_testcase_info(Parameter.TESTPLAN, '56', description=True)['title']},
)
class Test_55_56_function_test(Test):
    cdrouter = cdrouter_test.CDRTest(Parameter.CDROUTER,path=Parameter.TESTPATH, case=Parameter.CASE, conf=Parameter.CONF, log=Parameter.LOG, ver='cdr2.6')

    def setParameters(self, host, tcid, uuid, description):
        '''parameter host,tcid,uuid must be same with the dict above'''
        self.host=host
        self.tcid = tcid
        self.uuid = uuid
        self.description = description

    def test_55_56_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")  

    def test_55_56_01_add_AO(self):
        ao_opt1= {
            "object_type":"host",
            "name": 'wan_gw',
            "zone": 'WAN',
            "value":  Parameter.DUT_X1_GW
        }
        ao_opt2= {
            "object_type":"host",
            "name": 'remote_host',
            "zone": 'WAN',
            "value":  '3.3.3.3'
        }
        rc = ao.config_addressobject(**ao_opt1) 
        rc &= ao.config_addressobject(**ao_opt2) 
        Assertion.assert_equal(rc, True, "ERR: add ao failed")

    def test_55_56_02_add_nm(self):
        nm_dict={
            "network_monitors": [{
                "policy": {
                    "ipv4": {
                        'name': 'tc' + str(self.tcid),
                        'probe': {'target': {'name':'wan_gw'}, 'type': {'ping': 'non-explicit'}, 'interval': 5},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'comment': ''
                    }
                }
            }]
        }
        rc = nm.add_network_monitor(**nm_dict)
        Assertion.assert_equal(rc, True, "ERR: add nm policy failed")

    def test_55_56_03_run_cdrouter(self):
        cdrouter.run_case(testvar='', backend=True)
        Assertion.assert_equal(True, True, "ERR: add nm policy failed")
        
    def test_55_56_04_add_static_route(self):
        route_opt = {
            "route_policies":[
                {
                    "ipv4":{
                        "name":"test",
                        "interface":"X1",
                        "metric":1,
                        "service":{
                            "any":True
                        },
                        "gateway":{
                            "name":"wan_gw"
                        },
                        "source":{
                            "any":True
                        },
                        "destination":{
                            "name":"remote_host"
                        },
                        "probe":'tc' + str(self.tcid),
                        "disable_when_probes_succeed": False,
                    }
                }
            ]
        }
        rc = route.add_route_policy(**route_opt)
        Assertion.assert_equal(rc, True, "ERR: add static route policy failed")

    @repeat_method(5)
    def test_55_56_05_get_route_policy(self):
        rc = route.get_route_policy_status(name='test')
        if rc != '1':
            time.sleep(5)
        Assertion.assert_equal(rc, '1', "ERR: static route policy should be active")
        
    @repeat_method(5)
    def test_55_56_06_check_traffic(self):
        rc = diag.diag_ping('ping 3.3.3.3')
        Assertion.assert_equal(rc, True, "ERR: ping remotehost from dut failed")

    def test_55_56_07_stop_cdrouter_or_disable_X1(self):
        if self.host == 'up':
            rc = cdrouter.terminate_case()
            Assertion.assert_equal(True, True, "ERR: terminate cdrouter failed")
        else:
            Parameter.OS_STACK.set_node_interface_state('UTM','X1', 'disable')
            logger.info('Sleep 30s to wait for the policy become red')
            time.sleep(30)
            output = nm.get_network_monitor_status()
            try:
                led = output['data']['netMonArray'][0]['led']
            except:
                led = None
                logger.error('Fail to get led info.')
            Assertion.assert_equal(led, 'red', f"ERR: The led should be red but {led}")

    @repeat_method(5)
    def test_55_56_08_get_route_policy(self):
        rc = route.get_route_policy_status(name='test')
        if rc != '0':
            time.sleep(30)
        if self.host == 'down':
            cdrouter.terminate_case()
        Assertion.assert_equal(rc, '0', "ERR: static route policy should be inactive")

    def test_55_56_09_delete_static_route(self):
        rc =route.del_route_policy_by_name('test')  
        Assertion.assert_equal(rc, True, "ERR: delete route policy fail.")

    def test_55_56_10_delete_nm(self):
        rc = nm.del_network_monitor(name='tc' + str(self.tcid))
        Assertion.assert_equal(rc, True, "ERR: delete nm policy failed")
   
    def test_55_56_11_delete_aos(self):
        rc = ao.del_addressobject(**{'ip_type':'ipv4','name':'wan_gw'})
        rc &= ao.del_addressobject(**{'ip_type':'ipv4','name':'remote_host'})
        Assertion.assert_equal(rc, True, "ERR: delete aos failed")

    def test_55_56_12_reconnect_X1(self):
        if self.host == 'down':
            rc = Parameter.OS_STACK.set_node_interface_state('UTM','X1', 'enable')
            Assertion.assert_equal(rc, True, "ERR: reconnect X1 failed")

class Test_62_Check_log(Test):
    description= show_testcase_info(Parameter.TESTPLAN, '62', description=True)['title']
    uuid = "SOSAIOT-TC-58741"
    jira = 'GEN7-21823'

    def test_62_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '62')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_62_01_add_network_monitor_policy(self):
        nm_dict={
            "network_monitors": [{
                "policy": {
                    "ipv4": {
                        "name": 'tc62',
                        'probe': {'target': {'name': 'remotehost'}, 'type':{"tcp":{"port":1234,"explicit":True}}, 'interval': 5,},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'outbound_interface':'X0',
                        'next_hop':{'name':'wanhost'},
                        'comment':'nm for tc22'
                    }
                }
            }]
        }
        rc = nm.add_network_monitor(**nm_dict)
        Assertion.assert_equal(rc, True, "ERR: add nm policy failed")
    
    def test_62_02_check_log(self):
        log_output = log_monitor.show_log()
        logger.info(log_output)
        log_monitor.clear_log()

    def test_62_03_run_cdrouter(self):
        testvar = f' -testvar swl_wanTcpPort=1234 '
        cdrouter.run_case(testvar=testvar, backend=True)

    def test_62_04_check_log(self):
        log_output = log_monitor.show_log()
        logger.info(log_output)
        log_monitor.clear_log()        

    def test_62_07_stop_cdrouter(self):
        rc = cdrouter.terminate_case()
        Assertion.assert_equal(rc, True, "ERR: terminate cdrouter failed")

    @repeat_method(5)
    def test_62_08_check_log(self):
        time.sleep(5)
        log_output = log_monitor.show_log()
        logger.info(log_output)
        log_monitor.clear_log()   

    def test_62_09_edit_network_monitor_policy(self):
        nm_dict={
            "network_monitors": [{
                "policy": {
                    "ipv4": {
                        "name": 'tc62',
                        'probe': {'target': {'name': 'remotehost'}, 'type':{'ping': 'explicit'}, 'interval': 5,},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        'outbound_interface':'X0',
                        'next_hop':{'name':'wanhost'},
                        'comment':'nm for tc22'
                    }
                }
            }]
        }
        rc = nm.edit_network_monitor(**nm_dict)
        Assertion.assert_equal(rc, True, "ERR: edit nm policy failed")

    def test_62_10_check_log(self):
        log_output = log_monitor.show_log()
        logger.info(log_output)
        log_monitor.clear_log() 

    def test_62_11_delete_nm(self):
        rc = nm.del_network_monitor(name='tc62')
        Assertion.assert_equal(rc, True, "ERR: delete nm policy failed")

    def test_62_20_check_log(self):
        log_output = log_monitor.show_log()
        logger.info(log_output)
        log_monitor.clear_log() 