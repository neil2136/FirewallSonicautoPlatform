from definition.settings import *
from bin import check_traffic


class TestVPN_Cert_1507691(Test):
    uuid = "SOSAIOT-TC-54165"
    description= show_testcase_info(TESTPLAN2, '1507691', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507691')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_Add_CA_Cert(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        rc1 = LCACertObj.import_cert_local(cert_path='@' + local_cert1, name='req1', password='123456')
        rc1 &= LCACertObj.import_cert_local(cert_path='@' + local_cert2, name='req2', password='123456')
        rc1 &= LCACertObj.import_cert_local(cert_path='@' + local_cert3, name='req3', password='123456')
        rc1 &= LCACertObj.import_cert_local(cert_path='@' + local_cert4, name='req4', password='123456')
        rc1 &= LCACertObj.import_cert_local(cert_path='@' + local_cert5, name='req5', password='123456')
        cmds = ['show certificates status imported']
        resp = fw_cli.do_cli_commands(cmds, 1)[1]
        if 'req1' in resp and 'req2' in resp and 'req3' in resp and 'req4' in resp:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Add CA cert Failed.')

    @repeat_method(3)
    def test_02_Delete_CA_Cert(self):
        rc1 = LCACertObj.delete_local_cert(filename='req1')
        rc1 &= LCACertObj.delete_local_cert(filename='req2')
        rc1 &= LCACertObj.delete_local_cert(filename='req3')
        rc1 &= LCACertObj.delete_local_cert(filename='req4')
        rc1 &= LCACertObj.delete_local_cert(filename='req5')
        cmds = ['show certificates status imported']
        resp = fw_cli.do_cli_commands(cmds, 1)[1]
        if 'req1' not in resp and 'req2' not in resp and 'req3' not in resp and 'req4' not in resp:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Delete CA cert Failed.')


class TestVPN_Cert_1507693(Test):
    uuid = "SOSAIOT-TC-54167"
    description = show_testcase_info(TESTPLAN2, '1507693', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507693')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_generate_cert_request(self):
        logger.info('-'*10+'generate signing request'+'-'*10)
        if not os.path.isdir('/tmp/logs/'):
            logger.error("no path /tmp/logs not exists, create it now")
            os.system("mkdir /tmp/logs")
        # ref1 = copy.deepcopy(signreq)
        # ref1['certificates']['generate_signing_request'][0]['alias'] = 'req1'
        # ref1['certificates']['generate_signing_request'][0]['key']['size'] = '1024'
        # ref2 = copy.deepcopy(signreq)
        # ref2['certificates']['generate_signing_request'][0]['alias'] = 'req2'
        # ref2['certificates']['generate_signing_request'][0]['key']['size'] = '1536'
        ref3 = copy.deepcopy(signreq)
        ref3['certificates']['generate_signing_request'][0]['alias'] = 'req3'
        ref3['certificates']['generate_signing_request'][0]['key']['size'] = '2048'
        ref4 = copy.deepcopy(signreq)
        ref4['certificates']['generate_signing_request'][0]['alias'] = 'req4'
        ref4['certificates']['generate_signing_request'][0]['key']['size'] = '4096'
        # rc1 = LCACertObj.generate_req(**ref1)
        # rc2 = LCACertObj.generate_req(**ref2)
        rc3 = LCACertObj.generate_req(**ref3)
        rc4 = LCACertObj.generate_req(**ref4)
        cmds = ['show certificates status imported']
        resp = fw_cli.do_cli_commands(cmds, 1)[1]
        if 'req3' in resp and 'req4' in resp:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'add cert request Failed.')

    @repeat_method(3)
    def test_02_Delete_cert_request(self):
        # rc1 = LCACertObj.delete_local_cert(filename='req1')
        # rc1 = LCACertObj.delete_local_cert(filename='req2')
        rc1 = LCACertObj.delete_local_cert(filename='req3')
        rc1 &= LCACertObj.delete_local_cert(filename='req4')
        cmds = ['show certificates status imported']
        resp = fw_cli.do_cli_commands(cmds, 1)[1]
        if 'req3' not in resp and 'req4' not in resp:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'delete cert request Failed.')


class TestVPN_Cert_1507694(Test):
    uuid = "SOSAIOT-TC-54168"
    description = show_testcase_info(TESTPLAN2, '1507694', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507694')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_generate_cert_request(self):
        logger.info('-'*10+'generate signing request'+'-'*10)
        if not os.path.isdir('/tmp/logs/'):
            logger.error("no path /tmp/logs not exists, create it now")
            os.system("mkdir /tmp/logs")
        ref1 = copy.deepcopy(signreq)
        ref1['certificates']['generate_signing_request'][0]['alias'] = 'req1'
        ref1['certificates']['generate_signing_request'][0]['alternate_name'] = {"ipv4_address": "1.1.1.1"}
        ref2 = copy.deepcopy(signreq)
        ref2['certificates']['generate_signing_request'][0]['alias'] = 'req2'
        rc1 = LCACertObj.generate_req(**ref1)
        rc2 = LCACertObj.generate_req(**ref2)
        cmds = ['show certificates status imported']
        resp = fw_cli.do_cli_commands(cmds, 1)[1]
        if 'req1' in resp and 'req2' in resp:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'add cert request Failed.')

    @repeat_method(3)
    def test_02_Delete_cert_request(self):
        rc1 = LCACertObj.delete_local_cert(filename='req1')
        rc1 &= LCACertObj.delete_local_cert(filename='req2')
        cmds = ['show certificates status imported']
        resp = fw_cli.do_cli_commands(cmds, 1)[1]
        if 'req1' not in resp and 'req2' not in resp:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'delete cert request Failed.')


class TestVPN_Cert_1507700(Test):
    uuid = "SOSAIOT-TC-54174"
    description= show_testcase_info(TESTPLAN2, '1507700', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507700')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_CA_Cert(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        rc = LCACertObj.import_ca_cert(file=ca_cert)
        Assertion.assert_equal(rc, True, 'Add CA cert Failed.')
        
    def test_02_Delete_CA_Cert(self):
        rc = LCACertObj.delete_ca_cert(ca_hash="p2A%2F1TcKHZ44xMpyXCH2Rw%3D%3D")
        Assertion.assert_equal(rc, True, 'Delete CA cert Failed.')


class TestVPN_Cert_1507704(Test):
    uuid = "SOSAIOT-TC-54178"
    description = show_testcase_info(TESTPLAN2, '1507704', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507704')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref1['ike_exchange'] = 'main'
        ref2 = copy.deepcopy(Rvpn)
        ref2['ike_exchange'] = 'main'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_test_log(self):
        log_list = ['IKE\s+negotiation\s+complete']        
        rc = check_traffic.check_test_log_list(log_list)
        Assertion.assert_equal(rc, True, "ERR: check test log failed")

    def test_04_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_1507705(Test):
    uuid = "SOSAIOT-TC-54179"
    description = show_testcase_info(TESTPLAN2, '1507705', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507705')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref1['ike_exchange'] = 'aggressive'
        ref2 = copy.deepcopy(Rvpn)
        ref2['ike_exchange'] = 'aggressive'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_test_log(self):
        log_list = ['IKE\s+negotiation\s+complete']        
        rc = check_traffic.check_test_log_list(log_list)
        Assertion.assert_equal(rc, True, "ERR: check test log failed")

    def test_04_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_1507708(Test):
    uuid = "SOSAIOT-TC-54182"
    description = show_testcase_info(TESTPLAN2, '1507708', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507708')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref1['ike_exchange'] = 'main'
        ref2 = copy.deepcopy(Rvpn)
        ref2['ike_exchange'] = 'main'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_test_log(self):
        log_list = ['IKE\s+negotiation\s+complete']        
        rc = check_traffic.check_test_log_list(log_list)
        Assertion.assert_equal(rc, True, "ERR: check test log failed")

    def test_04_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_1507709(Test):
    uuid = "SOSAIOT-TC-54183"
    description = show_testcase_info(TESTPLAN2, '1507709', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507709')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref1['ike_exchange'] = 'main'
        ref1['local_cert'] = 'revokecert'
        ref1['peer_ike_id'] = ocsp_dn_id
        ref2 = copy.deepcopy(Rvpn)
        ref2['ike_exchange'] = 'main'
        ref2['local_cert'] = 'revokecert'
        ref2['peer_ike_id'] = ocsp_dn_id
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_test_log(self):
        log_list = ['IKE\s+negotiation\s+complete']        
        rc = check_traffic.check_test_log_list(log_list)
        Assertion.assert_equal(rc, True, "ERR: check test log failed")

    def test_04_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_1507710(Test):
    uuid = "SOSAIOT-TC-54184"
    description = show_testcase_info(TESTPLAN2, '1507710', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507710')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref1['ike_exchange'] = 'aggressive'
        ref1['local_cert'] = 'revokecert'
        ref1['peer_ike_id'] = ocsp_dn_id
        ref2 = copy.deepcopy(Rvpn)
        ref2['ike_exchange'] = 'aggressive'
        ref2['local_cert'] = 'revokecert'
        ref2['peer_ike_id'] = ocsp_dn_id
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_test_log(self):
        log_list = ['IKE\s+negotiation\s+complete']        
        rc = check_traffic.check_test_log_list(log_list)
        Assertion.assert_equal(rc, True, "ERR: check test log failed")

    def test_04_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_1507712(Test):
    uuid = "SOSAIOT-TC-54186"
    description = show_testcase_info(TESTPLAN2, '1507712', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507712')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_route_from_PC2_to_NAT(self):
        cmd = "route add -net {} netmask {} gw {}".format(Parameter.LOCTRANSNET, Parameter.NETMASK, Parameter.REMOTEX0)
        PC2_login.send_command(cmd)
        rt_info = PC2_login.send_command("route -n")
        if re.search('9\.9\.9\.0.*172\.16\.1\.101', rt_info):
            rc = True
        else:
            rc = False
            logger.info(rt_info)
        Assertion.assert_equal(rc, True, 'Add NAT route Failed.')
        
    def test_02_add_vpn_policy(self):
        LogObj.clear_log
        ref1 = copy.deepcopy(Lvpn)
        ref1['ike_exchange'] = 'aggressive'
        ref1['local_cert'] = 'revokecert'
        ref1['peer_ike_id'] = ocsp_dn_id
        ref1['apply_nat'] = True
        ref1['nat_local_type'] = 'name'
        ref1['nat_local_name'] = local_Tran_l['name']
        ref1['nat_remote_type'] = 'original'
        ref2 = copy.deepcopy(Rvpn)
        ref2['ike_exchange'] = 'aggressive'
        ref2['local_cert'] = 'revokecert'
        ref2['peer_ike_id'] = ocsp_dn_id     
        ref2['remote_net_name'] = remote_Tran_r['name']
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_03_initiate_continuous_pings_from_remote_to_NAT(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = PC2_login.send_command("ping 9.9.9.3 -c 1")
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_04_check_vpn_ping(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_05_test_log(self):
        log_list = ['IKE\s+negotiation\s+complete']        
        rc = check_traffic.check_test_log_list(log_list)
        Assertion.assert_equal(rc, True, "ERR: check test log failed")

    def test_06_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')

    def test_07_add_vpn_policy(self):
        LogObj.clear_log
        ref1 = copy.deepcopy(Lvpn)
        ref1['ike_exchange'] = 'main'
        ref1['local_cert'] = 'revokecert'
        ref1['peer_ike_id'] = ocsp_dn_id
        ref1['apply_nat'] = True
        ref1['nat_local_type'] = 'name'
        ref1['nat_local_name'] = local_Tran_l['name']
        ref1['nat_remote_type'] = 'original'
        ref2 = copy.deepcopy(Rvpn)
        ref2['ike_exchange'] = 'main'
        ref2['local_cert'] = 'revokecert'
        ref2['peer_ike_id'] = ocsp_dn_id     
        ref2['remote_net_name'] = remote_Tran_r['name']
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_08_initiate_continuous_pings_from_remote_to_NAT(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = PC2_login.send_command("ping 9.9.9.3 -c 1")
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_09_check_vpn_ping(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_10_test_log(self):
        log_list = ['IKE\s+negotiation\s+complete']        
        rc = check_traffic.check_test_log_list(log_list)
        Assertion.assert_equal(rc, True, "ERR: check test log failed")

    def test_11_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_1507713(Test):
    uuid = "SOSAIOT-TC-54187"
    description = show_testcase_info(TESTPLAN2, '1507713', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507713')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_route_from_PC1_to_NAT(self):
        cmd = "route add -net {} netmask {} gw {}".format(Parameter.REMTRANSNET, Parameter.NETMASK, Parameter.DUT)
        resp = os.popen(cmd).read()
        logger.info(resp)
        rt_info = os.popen("route -n").read()
        if re.search('8\.8\.8\.0.*192\.168\.168\.168', rt_info):
            rc = True
        else:
            rc = False
            logger.info(rt_info)
        Assertion.assert_equal(rc, True, 'Add NAT route Failed.')
        
    def test_02_add_vpn_policy(self):
        LogObj.clear_log
        ref1 = copy.deepcopy(Lvpn)
        ref1['ike_exchange'] = 'aggressive'
        ref1['local_cert'] = 'revokecert'
        ref1['peer_ike_id'] = ocsp_dn_id
        ref1['remote_net_name'] = remote_Tran_l['name']
        ref2 = copy.deepcopy(Rvpn)
        ref2['ike_exchange'] = 'aggressive'
        ref2['local_cert'] = 'revokecert'
        ref2['peer_ike_id'] = ocsp_dn_id     
        ref2['apply_nat'] = True
        ref2['nat_local_type'] = 'name'
        ref2['nat_local_name'] = local_Tran_r['name']
        ref2['nat_remote_type'] = 'original'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_03_initiate_continuous_pings_from_local_to_NAT(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping 8.8.8.3 -c 1").read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_04_check_vpn_ping(self):
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_05_test_log(self):
        log_list = ['IKE\s+negotiation\s+complete']        
        rc = check_traffic.check_test_log_list(log_list)
        Assertion.assert_equal(rc, True, "ERR: check test log failed")

    def test_06_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')

    def test_07_add_vpn_policy(self):
        LogObj.clear_log
        ref1 = copy.deepcopy(Lvpn)
        ref1['ike_exchange'] = 'main'
        ref1['local_cert'] = 'revokecert'
        ref1['peer_ike_id'] = ocsp_dn_id
        ref1['remote_net_name'] = remote_Tran_l['name']
        ref2 = copy.deepcopy(Rvpn)
        ref2['ike_exchange'] = 'main'
        ref2['local_cert'] = 'revokecert'
        ref2['peer_ike_id'] = ocsp_dn_id     
        ref2['apply_nat'] = True
        ref2['nat_local_type'] = 'name'
        ref2['nat_local_name'] = local_Tran_r['name']
        ref2['nat_remote_type'] = 'original'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_08_initiate_continuous_pings_from_local_to_NAT(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping 8.8.8.3 -c 1").read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_09_check_vpn_ping(self):
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_10_test_log(self):
        log_list = ['IKE\s+negotiation\s+complete']        
        rc = check_traffic.check_test_log_list(log_list)
        Assertion.assert_equal(rc, True, "ERR: check test log failed")

    def test_11_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_1507720(Test):
    uuid = "SOSAIOT-TC-54194"
    description= show_testcase_info(TESTPLAN2, '1507720', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507720')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_Local_Cert(self):
        rc = LCACertObj.import_cert_local(cert_path='@' + local_cert, name='my_cert', password='123456')
        Assertion.assert_equal(rc, True, 'Add loacl cert Failed.')

    def test_02_export_local_Cert(self):
        resp = LCACertObj.export_cert_local(name='my_cert',password='123456')
        logger.info(resp)
        Assertion.assert_regular(str(resp), 'HTTP\/1\.0 200 OK', 'Add CA cert Failed.')


class TestVPN_Cert_1507723(Test):
    uuid = "SOSAIOT-TC-54197"
    description= show_testcase_info(TESTPLAN2, '1507723', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507723')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Delete_CA_Cert(self):
        rc = LCACertObj.delete_local_cert(filename='my_cert')
        Assertion.assert_equal(rc, True, 'Delete loacl cert Failed.')

    def test_02_Add_Local_Cert(self):
        rc = LCACertObj.import_cert_local(cert_path='@' + local_cert, name='my_cert', password='123456')
        Assertion.assert_equal(rc, True, 'Add loacl cert Failed.')

    def test_03_Delete_local_Cert(self):
        rc = LCACertObj.delete_local_cert(filename='my_cert')
        Assertion.assert_equal(rc, True, 'Delete loacl cert Failed.')


class TestVPN_Cert_1507719(Test):
    uuid = "SOSAIOT-TC-54193"
    description= show_testcase_info(TESTPLAN2, '1507719', description=True)['title']
    jira = 'QAA-11887'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507719')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_Exipred_CA_Cert(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        expiredca = ts_path + '/cert/expiredca.pem'
        resp = LCACertObj.import_ca_cert(file=expiredca, msg=True)
        logger.info(resp)
        if not re.search('\"success\":false.*CA Certificate has expired',resp,re.M|re.I):
            rc = False
        else:
            rc = True
        Assertion.assert_equal(rc, True, 'test cannot add expired CA cert Failed.')


class TestVPN_Cert_1507724(Test):
    uuid = "SOSAIOT-TC-54198"
    description= show_testcase_info(TESTPLAN2, '1507724', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507724')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_time(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "00:00:00",
                "date": "2030:01:01",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = LTimeObj.set_time(**time_json)
        Assertion.assert_equal(rc, True, 'set DUT time Failed.')

    def test_02_Add_Local_Cert(self):
        rc = LCACertObj.import_cert_local(cert_path='@' + local_cert, name='my_cert', password='123456')
        Assertion.assert_equal(rc, True, 'Add loacl cert Failed.')

    def test_03_Delete_local_Cert(self):
        rc = LCACertObj.delete_local_cert(filename='my_cert')
        Assertion.assert_equal(rc, True, 'Delete loacl cert Failed.')

    def test_04_restore_time(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        date_tmp = os.popen('date +%Y:%m:%d').read()
        print(date_tmp)
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "00:00:00",
                "date": date_tmp,
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = LTimeObj.set_time(**time_json)
        logger.info(rc)
        Assertion.assert_equal(rc, True, 'restore DUT time Failed.')


class TestVPN_Cert_1507711(Test):
    uuid = "SOSAIOT-TC-54185"
    description= show_testcase_info(TESTPLAN2, '1507711', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507711')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_CA_Cert(self):
        rc = LCACertObj.import_ca_cert(file=ca_cert)
        Assertion.assert_equal(rc, True, 'add CA cert Failed.')

    def test_02_Add_Local_Cert(self):
        rc = LCACertObj.import_cert_local(cert_path='@' + local_cert, name='my_cert', password='123456')
        Assertion.assert_equal(rc, True, 'Add loacl cert Failed.')

    def test_03_Delete_local_Cert(self):
        rc = LCACertObj.delete_local_cert(filename='my_cert')
        Assertion.assert_equal(rc, True, 'Delete loacl cert Failed.')

    def test_04_Delete_CA_Cert(self):
        rc = LCACertObj.delete_ca_cert(ca_hash="p2A%2F1TcKHZ44xMpyXCH2Rw%3D%3D")
        Assertion.assert_equal(rc, True, 'Delete CA cert Failed.')


class TestVPN_Cert_1507692(Test):
    uuid = "SOSAIOT-TC-54166"
    description= show_testcase_info(TESTPLAN2, '1507692', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN2, '1507692')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_time(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "00:00:00",
                "date": "2024:01:01",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = LTimeObj.set_time(**time_json)
        Assertion.assert_equal(rc, True, 'set DUT time Failed.')

    def test_02_clear_CA_Cert(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        rc = LCACertObj.delete_ca_cert(ca_hash="p2A%2F1TcKHZ44xMpyXCH2Rw%3D%3D")
        rc &= LCACertObj.delete_ca_cert(ca_hash="VWS7EkUs5ueUBrXsrA1CAg==")
        rc &= LCACertObj.delete_ca_cert(ca_hash="VaEBnKW5x8nJxfkbHOs9Yg==")
        Assertion.assert_equal(True, True, 'clear CA cert Failed.')
    
    def test_03_Add_max_CA_Cert(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        rc = LCACertObj.import_ca_cert(file=ca_cert)
        rc &= LCACertObj.import_ca_cert(file=ocsp_root)
        rc &= LCACertObj.import_ca_cert(file=ocsp_revk_root)
        cmds = ['show certificates status imported']
        (resp, output) = fw_cli.do_cli_commands(cmds, 1)
        Assertion.assert_equal(rc, True, 'add CA cert Failed.')

    def test_04_Delete_CA_Cert(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        rc = LCACertObj.delete_ca_cert(ca_hash="p2A%2F1TcKHZ44xMpyXCH2Rw%3D%3D")
        rc &= LCACertObj.delete_ca_cert(ca_hash="VWS7EkUs5ueUBrXsrA1CAg==")
        rc &= LCACertObj.delete_ca_cert(ca_hash="VaEBnKW5x8nJxfkbHOs9Yg==")
        Assertion.assert_equal(rc, True, 'delete CA cert Failed.')

    def test_05_restore_time(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        date_tmp = os.popen('date +%Y:%m:%d').read()
        print(date_tmp)
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "00:00:00",
                "date": date_tmp,
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = LTimeObj.set_time(**time_json)
        logger.info(rc)
        Assertion.assert_equal(rc, True, 'restore DUT time Failed.')
