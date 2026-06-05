from definition.settings import *


@paramunittest.parametrized(
    {'port': '1', 'mode': 'MAIN', 'side': 'INI', 'uuid': '1530000', 'tcid': '2'},
    {'port': '1', 'mode': 'MAIN', 'side': 'RES', 'uuid': '1754039', 'tcid': '3'},
    {'port': '1', 'mode': 'AGGRESSIVE', 'side': 'INI', 'uuid': '1754040', 'tcid': '4'},
    {'port': '1', 'mode': 'AGGRESSIVE', 'side': 'RES', 'uuid': '1530001', 'tcid': '5'},
    {'port': '1', 'mode': 'MANUAL', 'side': 'INI', 'uuid': '1754042', 'tcid': '6'},
    {'port': '1', 'mode': 'MANUAL', 'side': 'RES', 'uuid': '1754043', 'tcid': '7'},
    {'port': '1', 'mode': 'THIRD', 'side': 'INI', 'uuid': '1754044', 'tcid': '8'},
    {'port': '1', 'mode': 'THIRD', 'side': 'RES', 'uuid': '1754045', 'tcid': '9'},
    {'port': '2', 'mode': 'MAIN', 'side': 'INI', 'uuid': '', 'tcid': '10'},
    {'port': '2', 'mode': 'MAIN', 'side': 'RES', 'uuid': '', 'tcid': '10'},
    {'port': '2', 'mode': 'AGGRESSIVE', 'side': 'INI', 'uuid': '', 'tcid': '10'},
    {'port': '2', 'mode': 'AGGRESSIVE', 'side': 'RES', 'uuid': '', 'tcid': '10'},
    {'port': '2', 'mode': 'MANUAL', 'side': 'INI', 'uuid': '', 'tcid': '10'},
    {'port': '2', 'mode': 'MANUAL', 'side': 'RES', 'uuid': '', 'tcid': '10'},
    {'port': '2', 'mode': 'THIRD', 'side': 'INI', 'uuid': '', 'tcid': '10'},
    {'port': '2', 'mode': 'THIRD', 'side': 'RES', 'uuid': '1529998', 'tcid': '10'},
)
class TestVPN_bound_to_01(Test):

    def setParameters(self, port, mode, side, uuid, tcid):
        self.port = port
        self.mode = mode
        self.side = side
        self.uuid = uuid
        self.tcid = tcid
        self.description = 'test'
        self.description = show_testcase_info(TESTPLAN, self.tcid, description=True)['title']
        self.Lvpn, self.Rvpn = get_vpn_policy_optionals(self.port,self.mode)

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_01_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    @repeat_method(3)
    def test_01_02_add_vpn_policy(self):
        
        ref1 = copy.deepcopy(self.Lvpn)
        ref2 = copy.deepcopy(self.Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        logger.info("Local VPN Policy {} ".format(ref1))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        logger.info("Remote VPN Policy {} ".format(ref2))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.') 

    def test_01_03_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = False
        
        for i in range(10):
            if self.side == 'INI':
                cmd = "ping {} -c 1 -w 1".format(PC2_IP)
                logger.info("send the command {}".format(cmd))
                out = os.system(cmd)
            elif self.side == 'RES':
                cmd = "ping {} -c 1".format(PC1_IP)
                logger.info("send the command {}".format(cmd))
                out = PC2.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_01_04_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        if self.mode == 'MANUAL':
            logger.info("Manual key mode doesn't have logs.")
            return ()
        time.sleep(2)
        
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKE\s+negotiation\s+complete', log, re.I | re.M):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_01_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**self.Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**self.Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class Test_Tear_down(Test):
    uuid = 'NonTC'
    description = "clear env config settings"
    
    def test_00_01_remove_CA_Cert(self):
        logger.info('-'*10+'Remove CA cert'+'-'*10)
        rc = LCACertObj.delete_ca_cert(ca_hash="nfB5Erd0dz1GD5B6eXXkdQ==")
        rc &= RCACertObj.delete_ca_cert(ca_hash="nfB5Erd0dz1GD5B6eXXkdQ==")
        Assertion.assert_equal(rc, True, 'Remove CA cert Failed.')

    def test_00_02_Remove_Local_Cert(self):
        logger.info('-'*10+'Remove local cert'+'-'*10)
        rc = LCACertObj.delete_local_cert(filename='my_cert')
        rc &= RCACertObj.delete_local_cert(filename='my_cert')
        Assertion.assert_equal(rc, True, 'Remove local cert Failed.')

    def test_00_03_delete_AddObj(self):
        logger.info('-'*10+'delete AO'+'-'*10)
        rc = LAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=local_l['name'],ip_type='ipv4')
        rc &= LAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=local_r['name'],ip_type='ipv4')
        rc &= RAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=remote_l['name'],ip_type='ipv4')
        rc &= RAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=remote_r['name'],ip_type='ipv4')
        Assertion.assert_equal(rc, True, 'Delet AO for DUT and RDUT Failed.')



