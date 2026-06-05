from settings import *


@paramunittest.parametrized(
    {"wan_mode":"dhcp","sec_wan":'dhcp',"ospf_auth":"MSGAUTH1","ospf_orig_route": 'never',"ospf_bw_ref":'100',"metric":'110',"verify_method":'route',"expect_result":'RRFOUND-NODR',"need_restart":'no',"lb_state":False,"probe_state":'off',"rt_orig_route":"never","tc_id":'126','uuid':'SOSAIOT-TC-55744'},
    {"wan_mode":"dhcp","sec_wan":'dhcp',"ospf_auth":"MSGAUTH10","ospf_orig_route": 'never',"ospf_bw_ref":'100',"metric":'110',"verify_method":'route',"expect_result":'RRFOUND-NODR',"need_restart":'no',"lb_state":False,"probe_state":'off',"rt_orig_route":"never","tc_id":'127','uuid':'SOSAIOT-TC-55745'},
    {"wan_mode":"dhcp","sec_wan":'dhcp',"ospf_auth":"MSGAUTH10","ospf_orig_route": 'never',"ospf_bw_ref":'100',"metric":'110',"verify_method":'packet',"expect_result":'RRFOUND-NODR',"need_restart":'no',"lb_state":False,"probe_state":'off',"rt_orig_route":"never","tc_id":'128','uuid':'SOSAIOT-TC-55755'},
    {"wan_mode":"dhcp","sec_wan":'dhcp',"ospf_auth":"NOAUTH","ospf_orig_route": 'always',"ospf_bw_ref":'100',"metric":'110',"verify_method":'route',"expect_result":'RRFOUND-DRFOUND',"need_restart":'yes',"lb_state":False,"probe_state":'off',"rt_orig_route":"never","tc_id":'130','uuid':'SOSAIOT-TC-55746'},
    {"wan_mode":"dhcp","sec_wan":'dhcp',"ospf_auth":"NOAUTH","ospf_orig_route": 'wan-up',"ospf_bw_ref":'100',"metric":'110',"verify_method":'route',"expect_result":'RRFOUND-NODR',"need_restart":'no',"lb_state":False,"probe_state":'off',"rt_orig_route":"never","tc_id":'131','uuid':'SOSAIOT-TC-55756'},
    {"wan_mode":"static","sec_wan":'dhcp',"ospf_auth":"NOAUTH","ospf_orig_route": 'wan-up',"ospf_bw_ref":'100',"metric":'110',"verify_method":'route',"expect_result":'RRFOUND-DRFOUND',"need_restart":'no',"lb_state":False,"probe_state":'off',"rt_orig_route":"never","tc_id":'132','uuid':'SOSAIOT-TC-55747'},
    {"wan_mode":"dhcp","sec_wan":'dhcp',"ospf_auth":"NOAUTH","ospf_orig_route": 'wan-up',"ospf_bw_ref":'100',"metric":'110',"verify_method":'route',"expect_result":'RRFOUND-NODR',"need_restart":'no',"lb_state":True,"probe_state":'off',"rt_orig_route":"never","tc_id":'133','uuid':'SOSAIOT-TC-55748'},
    {"wan_mode":"static","sec_wan":'dhcp',"ospf_auth":"NOAUTH","ospf_orig_route": 'wan-up',"ospf_bw_ref":'100',"metric":'110',"verify_method":'route',"expect_result":'RRFOUND-DRFOUND',"need_restart":'no',"lb_state":True,"probe_state":'off',"rt_orig_route":"never","tc_id":'134','uuid':'SOSAIOT-TC-55749'},
    {"wan_mode":"dhcp","sec_wan":'dhcp',"ospf_auth":"NOAUTH","ospf_orig_route": 'wan-up',"ospf_bw_ref":'100',"metric":'110',"verify_method":'route',"expect_result":'RRFOUND-NODR',"need_restart":'no',"lb_state":True,"probe_state":'on_good',"rt_orig_route":"never","tc_id":'135','uuid':'SOSAIOT-TC-55757'},
    {"wan_mode":"static","sec_wan":'dhcp',"ospf_auth":"NOAUTH","ospf_orig_route": 'wan-up',"ospf_bw_ref":'100',"metric":'110',"verify_method":'route',"expect_result":'RRFOUND-NODR',"need_restart":'no',"lb_state":True,"probe_state":'on_bad',"rt_orig_route":"never","tc_id":'136','uuid':'SOSAIOT-TC-55750'},
    {"wan_mode":"static","sec_wan":'dhcp',"ospf_auth":"NOAUTH","ospf_orig_route": 'wan-up',"ospf_bw_ref":'100',"metric":'110',"verify_method":'route',"expect_result":'RRFOUND-DRFOUND',"need_restart":'no',"lb_state":True,"probe_state":'on_good',"rt_orig_route":"never","tc_id":'137','uuid':'SOSAIOT-TC-55758'},
    {"wan_mode":"dhcp","sec_wan":'dhcp',"ospf_auth":"NOAUTH","ospf_orig_route": 'always',"ospf_bw_ref":'100',"metric":'110',"verify_method":'rtable',"expect_result":'RRFOUND-NODR',"need_restart":'no',"lb_state":False,"probe_state":'off',"rt_orig_route":"always","tc_id":'138','uuid':'SOSAIOT-TC-55751'},
    {"wan_mode":"dhcp","sec_wan":'dhcp',"ospf_auth":"NOAUTH","ospf_orig_route": 'never',"ospf_bw_ref":'100',"metric":'10',"verify_method":'rtable',"expect_result":'RRFOUND-NODR',"need_restart":'no',"lb_state":False,"probe_state":'off',"rt_orig_route":"always","tc_id":'139','uuid':'SOSAIOT-TC-55752'},
    {"wan_mode":"dhcp","sec_wan":'dhcp',"ospf_auth":"NOAUTH","ospf_orig_route": 'never',"ospf_bw_ref":'100',"metric":'110',"verify_method":'cost',"expect_result":'RRFOUND-NODR',"need_restart":'no',"lb_state":False,"probe_state":'off',"rt_orig_route":"never","tc_id":'140','uuid':'SOSAIOT-TC-55753'},
    {"wan_mode":"dhcp","sec_wan":'dhcp',"ospf_auth":"NOAUTH","ospf_orig_route": 'never',"ospf_bw_ref":'40000',"metric":'110',"verify_method":'cost',"expect_result":'RRFOUND-NODR',"need_restart":'no',"lb_state":False,"probe_state":'off',"rt_orig_route":"never","tc_id":'141','uuid':'SOSAIOT-TC-55754'},
)


class Test_OSPF_Test(Test):
    def setParameters(self, wan_mode,sec_wan,ospf_auth, ospf_orig_route,ospf_bw_ref,metric, verify_method,expect_result,need_restart,lb_state,probe_state,rt_orig_route,tc_id,uuid):
        '''parameter wan_mode,sec_wan,expect_result,ospf_auth, ospf_orig_route,ospf_bw_ref,metric, verify_method,expect_result,need_restart,lb_state,proce_state,rt_orig_route,tc_id,uuid must be same with the dict above'''
        self.wan_mode = wan_mode
        self.sec_wan = sec_wan
        self.ospf_auth = ospf_auth
        self.ospf_orig_route = ospf_orig_route
        self.ospf_bw_ref =ospf_bw_ref
        self.metric =metric
        self.verify_method = verify_method
        self.expect_result =expect_result
        self.need_restart = need_restart
        self.lb_state=lb_state
        self.probe_state=probe_state
        self.rt_orig_route=rt_orig_route
        self.tc_id = tc_id
        self.uuid =uuid
        self.description= show_testcase_info(Parameter.TESTPLAN, self.tc_id, description=True)['title']

    def test_00_show_testcase_info(self):
        print(self.tc_id)
        show_testcase_info(Parameter.TESTPLAN, self.tc_id)
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_config_interface(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.DUT_X1_IP,
            'gateway': Parameter.DUT_X1_GATEWAY,
        }
        x1_dhcp= {
             'if': 'X1',
            'zone': 'WAN', 
            'mode': 'dhcp',
        }
        if self.wan_mode == 'static':
            rc = interface_obj.config_interface(**x1_static)
        else:
            rc = interface_obj.config_interface(**x1_dhcp)
        x2_dmz={
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'static',
            'ip': Parameter.DUT_X2_IP,
        }

        rc &= interface_obj.config_interface(**x2_dmz)
        Assertion.assert_equal(rc, True, "ERR: set X1,X2 ip fail.") 

    def test_02_config_lb(self):
        rc =True
        if self.lb_state :
            x3_static = {
                'if': 'X3',
                'zone': 'WAN', 
                'mode': 'static',
                'ip': Parameter.DUT_X3_IP,
                'gateway': Parameter.DUT_X3_GATEWAY,
            }      
            x3_dhcp= {
                'if': 'X3',
                'zone': 'WAN', 
                'mode': 'dhcp',
            }
            if self.sec_wan == 'static':
                rc = interface_obj.config_interface(**x3_static)
            else:
                rc = interface_obj.config_interface(**x3_dhcp)
        lb_opt = {
            'enable'    : self.lb_state,
            'probes'    : probe_map[self.probe_state],
        }
        rc &= lb_obj.config_failover_settings(**lb_opt)
        if probe_map[self.probe_state]:
            probe_opt= {
                "failover_lb": {
                    "group": [
                        {
                            "name": " Default LB Group",
                            "type": "basic",
                            "probing": {
                                "health_check": 5,
                                "missed_intervals": 6,
                                "successful_intervals": 3,
                                "global_responder": False
                            },
                            "interface": [
                                {
                                    "name": "X1",
                                    "rank": 1,
                                    "probe_type": "logical",
                                    "probe_condition": "either",
                                    "main_target":{
                                        "protocol":{"ping":True},
                                        "host":"0.0.0.0"
                                    },
                                    "alternate_target":{
                                        "protocol":{"ping":True},
                                        "host":"204.212.170.23"
                                    },
                                    "default_target":{"value":'204.212.170.23'}
                                }
                            ]
                        }
                    ]
                }
            }
            if 'good' in self.probe_state:
                probe_opt["failover_lb"]["group"][0]["interface"][0]["main_target"]["host"] =Parameter.PC1_ETH2_IP
                rc &= lb_obj.config_failover_settings(**probe_opt)
                logger.info(f'Ping {Parameter.PC1_ETH2_IP} before config ospf.')
                diag_obj.ping(Parameter.PC1_ETH2_IP)
            else:
                probe_opt["failover_lb"]["group"][0]["interface"][0]["main_target"]["host"] = '1.2.3.4'
                rc &= lb_obj.config_failover_settings(**probe_opt)
        Assertion.assert_equal(rc, True, "ERR: set lb fail.") 

    def test_02_config_ospf_on_dut(self):
        ospf_setting= {
            'default_route': self.ospf_orig_route,
            'route_metric':self.metric,
            'metric_type':param_map[self.ospf_orig_route][2]
        }  
        rc =route_obj.ospf2_config(**ospf_setting)
        logger.info("Enable and configure OSPF on DUT X2.")
        auth_cmd = ospf_auth_cmd[self.ospf_auth]
        auth_allow =''
        if self.ospf_auth != 'NOAUTH':
            auth_allow = 'ip ospf authentication message-digest'        
        logger.info(f"OSPF auth mode, {self.ospf_auth}: {auth_cmd}")
        commands=["configure",
                  "routing", 
                  "ospf",
                  "conf t", 
                  "router ospf",
                  "router-id 10.0.0.1",
                  f"auto-cost reference-bandwidth {self.ospf_bw_ref}",
                  f"network {Parameter.ROUTER_X1_IP}/24 area 0", 
                  "exit",
                  "interface X2",
                  "no ip ospf disable all", 
                  f"{auth_allow}",
                  f"{auth_cmd}", 
                  "end", "exit", "end", "end",]
        rc &=fw_cli.do_cli_commands(commands)
        Assertion.assert_equal(rc, True, "ERR: conf ospf fail.") 

    def test_03_restart_dut(self):
        rc =True
        if self.need_restart == 'on':
            rc=setting_obj.boot_fw(2)
        Assertion.assert_equal(rc, True, "ERR: restart fail.") 

    def test_04_config_ospf_on_remote(self):
        ospf_setting= {
            'default_route': self.rt_orig_route,
            'metric':param_map[self.rt_orig_route][1],
            'metric_type':param_map[self.rt_orig_route][2]
        }  
        rc =rem_route_obj.ospf2_config(**ospf_setting)
        logger.info("Enable and configure OSPF on DUT X2.")
        auth_cmd = ospf_auth_cmd[self.ospf_auth]
        auth_allow =''
        if self.ospf_auth != 'NOAUTH':
            auth_allow = 'ip ospf authentication message-digest'          
        logger.info(f"OSPF auth mode, {self.ospf_auth}: {auth_cmd}")
        commands=["configure",
                  "routing", 
                  "ospf",
                  "conf t", 
                  "router ospf",
                  "router-id 9.1.1.1",
                  f"no network {Parameter.ROUTER_X2_IP}/24 area 0",
                  f"network {Parameter.ROUTER_X2_IP}/24 area 10",
                  f"network {Parameter.DUT_X2_IP}/24 area 0",
                  'exit',
                  "interface X1", 
                  "no ip ospf disable all", 
                  f"{auth_cmd}",
                  "exit",
                  "interface X2", 
                  "no ip ospf disable all", 
                  f"{auth_allow}",
                  f"{auth_cmd}", 
                  "end", "exit", "end", "end",]
        rc &=fw_cli_rt.do_cli_commands(commands)
        Assertion.assert_equal(rc, True, "ERR: conf ospf fail.") 

    @repeat_method(5)
    def test_05_verify_ospf(self):
        if self.verify_method == 'traffic':
            rc=diag_obj.ping(Parameter.PC1_ETH4_IP)
        elif self.verify_method == 'route':
            route_result=''
            commands=["configure",
                      "routing", 
                      "ospf",    
                      "show ip ospf database",
                      'exit',
                      'end',
                      'exit',
            ]                
            rc,result =fw_cli_rt.do_cli_commands(commands,tag=1)
            logger.info(result)
            if re.search('3.3.3.0\s+9.1.1.1\s+\d+(\s+0x[a-f\d]+){2}\s+3.3.3.0\/24',result,re.I|re.S):
                logger.info("Remote route Found.")
                route_result += "RRFOUND"
            else:
                logger.info("Remote route not Found.")
                route_result += "NORR"
            if re.search('0.0.0.0\s+10.0.0.1\s+\d+(\s+0x[a-f\d]+){2}\s+E2\s+0.0.0.0\/0',result,re.I|re.S):
                logger.info("Default  route Found.")
                route_result += "-DRFOUND"
            else:
                logger.info("Default  route not Found.")
                route_result += "-NODR"
            if self.expect_result == route_result:
                total_result = f'Route verification PASSED: {route_result}, expected: {self.expect_result}'
            else:
                total_result = f'Route verification FAILED: {route_result}, expected: {self.expect_result}'
        elif self.verify_method == 'rtable':
            table_result=''
            logger.info(f"Expected gateway: {Parameter.ROUTER_X1_IP}, " + "destination: 0.0.0.0")
            time.sleep(30)
            route_policies= r_policy_obj.route_policies_reporting(r_type='dynamic')
            logger.info(route_policies)
            table_result = "RTABLE-FAILED"
            for route in route_policies:
                if route['destination'] == '0.0.0.0/0' and route['gateway'] == Parameter.ROUTER_X1_IP:
                    print(route['metric'])
                    if int(route['metric']) == int(self.metric):
                        table_result = "RTABLE-PASSED"
            if 'PASSED' in table_result:
                total_result = "Route table verification PASSED:" + table_result
            else:
                total_result = "Route table verification FAILED:" + table_result
        elif self.verify_method == 'cost':
            band_width = ''
            fw_network=status_obj.show_status()
            match1 =  re.search('X2.*(\d+)\s+Mbps',fw_network,re.I)
            match2 =  re.search('X2.*(\d+)\s+Gbps',fw_network,re.I)
            if match1:
                band_width = int(match1.group(1))
            elif match2:
                band_width = int(match2.group(1)) *1000
            logger.info(f"X2 BW: {str(band_width)} Mbps")
            logger.info(f'MY cost: {self.ospf_bw_ref}')
            commands=["configure",
                    "routing", 
                    "ospf",
                    "show ip ospf interface X2", 
                    "exit", "end", "end",]
            output =fw_cli.do_cli_commands(commands, 1)[1]
            match3 =  re.search('Cost:\s+(\d+)',output,re.I)
            if match3:
                cost= match3.group(1)
                num1 = int(self.ospf_bw_ref)/band_width
                if int(num1) < num1:
                    num2 = num1+1
                else:
                    num2 =num1
                if int(cost)== int(num2):
                    total_result = "Interface cost verification PASSED"
                else:
                    total_result = "Interface cost verification FAILED"
        elif self.verify_method == 'packet':
            pkt_setting= {   
                'display_filter': {
                    'interfaces':'X2',
                    'ether_types': 'IP',
                    'source_ips':Parameter.DUT_X2_IP,
                    'ip_types': 'OSPF',
                }
            }
            packet_obj.conf_packmon(**pkt_setting)
            packet_obj.start_capture()
            logger.info('sleep 60s...')
            time.sleep(60)
            rc=packet_obj.export_captured_packets_libpcap(filepath ='/tmp/ospf.pcap')
            packet_obj.stop_capture()
            packet_obj.clear_packets()
            rc =pc1.send_command(f"tcpdump -v -r /tmp/ospf.pcap|grep 'Crypto Sequence Number'|cut -d',' -f3|cut -d':' -f2")
            seq=list(map(lambda x:int(x,16),rc.strip('\n').split('\n')))
            if check_increasing(seq):
                total_result = 'Packet verification PASSED'
            else:
                total_result = 'Packet verification FAILED'
            logger.info(f'packet as follow:{rc}')
        logger.info(f'Total result:{total_result}')
        Assertion.assert_regular(total_result, 'PASSED', "ERR:Verify ospf fail.") 

    def test_06_unconfig_ospf_on_remote(self):
        logger.info(f"reset OSPF auth mode.")
        auth_allow=''
        if self.ospf_auth != 'NOAUTH':
            auth_allow = 'no ip ospf authentication message-digest'  
        commands=["configure",
                  "routing", 
                  "ospf",
                  "conf t", 
                  "router ospf",
                  "router-id 9.1.1.1",
                  f"no network {Parameter.ROUTER_X2_IP}/24 area 10",
                  f"no network {Parameter.ROUTER_X2_IP}/24 area 0",
                  'exit',
                  "interface X1", 
                  "ip ospf disable all", 
                  f"{auth_allow}",
                  "exit",
                  "interface X2", 
                  "ip ospf disable all", 
                  "end", "exit", "end", "end",]
        rc =fw_cli_rt.do_cli_commands(commands)
        Assertion.assert_equal(rc, True, "ERR: unconf ospf fail.")     

    def test_07_unconfig_ospf_on_dut(self):
        logger.info(f"reset OSPF auth mode")
        auth_allow=''
        if self.ospf_auth != 'NOAUTH':
            auth_allow = 'no ip ospf authentication message-digest'  
        commands=["configure",
                  "routing", 
                  "ospf",
                  "conf t", 
                  "router ospf",
                  "router-id 10.0.0.1",
                  f"no network {Parameter.DUT_X2_IP}/24 area 0", 
                  "exit",
                  "interface X2",
                  f"{auth_allow}",
                  "ip ospf disable all", 
                  "end", "exit", "end", "end",]
        rc =fw_cli.do_cli_commands(commands)
        Assertion.assert_equal(rc, True, "ERR: unconf ospf fail.")            
      
       