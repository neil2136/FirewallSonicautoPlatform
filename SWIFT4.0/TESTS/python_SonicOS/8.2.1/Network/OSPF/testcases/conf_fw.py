from settings import *



class TestConfigENV(Test):
    uuid = 'NonTC'
    description = 'Configure TB'

    def test_00_01_restore_remote(self):
        logger.info(" {} ".center(20, '-').format('Restore Remote'))
        path = Parameter.cfg_path + 'restore_gw_rmt_tel.py'
        cmd = f'python3 {path} -os=1 --testbed={Params.testbed} -device=RemoteGEN5 -if=X1 -zone=WAN -ip={Parameter.ROUTER_X1_IP}  -restore=1'
        logger.info(cmd)
        out = os.popen(cmd).read()
        logger.info(out)
        logger.info('time sleep 10 sec.')
        time.sleep(10)
        rc= pc1.ping(Parameter.ROUTER_X1_IP)
        Assertion.assert_equal(rc, True, "ERR: restore remote failed.")

    def test_00_02_configure_remote_interface(self):
        logger.info(" {} ".center(20, '-').format('Configure remote Interface'))
        dut2_x2 = {
            'if'    : 'X2',
            'zone'  : 'DMZ',
            'mode'  : 'static',
            'ip'    : Parameter.ROUTER_X2_IP,
            'mask'  : '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh'  : True,
            'mgmt_ping' : True,
        }
        rc = rem_interface_obj.config_interface(**dut2_x2)
        Assertion.assert_equal(rc, True, "ERR: config remote x2 failed")
    
