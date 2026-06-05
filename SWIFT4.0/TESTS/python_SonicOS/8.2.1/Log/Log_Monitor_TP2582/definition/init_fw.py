__author__ = 'chu'
from definition.settings import *

class TestConfigSyslogTB(Test):
    uuid = 'NonTC'
    description = "initial syslog testbed"
    goto_teardown = True

    def test_00_00_global(self):
        logger.info(f" {Params.testbed} ".center(20, '-'))
        cmd1 = f'cp -f {TestPath}/confs/rsyslog {file_path1}'
        cmd2 = f'cp -f {TestPath}/confs/rsyslog.conf {file_path2}'
        logger.info(cmd1)
        logger.info(cmd2)
        os.system(cmd1)
        os.system(cmd2)

        rc = os.path.exists(file_path1)
        rc &= os.path.exists(file_path2)
        Assertion.assert_equal(rc, True, 'Copy file failed')

    def test_00_01_config_network(self):
        logger.info(" Config network ".center(40, '-'))
        rc = False
        cmd = " service smb restart;service nmb restart "
        ret  = PC2.send_command(cmd)
        logger.info(ret)
        if 'Starting SMB services: [  OK  ]' in ret and 'Starting NMB services: [  OK  ]' in ret:
            logger.info('service smb and service nmb restart successfully.')
            rc = True
        Assertion.assert_equal(rc, True, 'config Network failed')

    def test_00_02_add_vpn_address_object(self):
        logger.info(" Add VPN Address Object ".center(40, '-'))
        rc = 0
        rc1 = LAddrOBJ.config_addressobject(msg=True, **vpn_local_obj)
        if rc1[0]:
            rc += 1
            logger.info(f"Add {vpn_local_obj['name']} address objects success.")
        elif 'Already exists' in rc1[1]['status']['info'][0]['message']:
            rc += 1
            logger.info('Local Address Object already exists')
        else:
            logger.info(f"Add {vpn_local_obj['name']} Failed")

        rc2 = RAddrOBJ.config_addressobject(msg=True, **vpn_remote_obj)
        if rc2[0]:
            rc += 1
            logger.info(f"Add {vpn_remote_obj['name']} address objects success.")
        elif 'Already exists' in rc2[1]['status']['info'][0]['message']:
            rc += 1
            logger.info('Remote Address Object already exists')
        else:
            logger.info(f"Add {vpn_remote_obj['name']} Failed")

        Assertion.assert_equal(rc,2,'Add address objects Failed.')

    def test_00_03_add_remote_vpn_access_rule(self):
        logger.info(" Add VPN Access Rule on Remote ".center(40, '-'))
        cmd1= ['config',
            'access-rule ipv4 from LAN to VPN action allow source port any service any destination address any',
            'enable', 'commit', 'exit', 'exit' ]
        rc = rmt.do_cli_commands(cmd1)
        cmd2 = ['config',
                'access-rule ipv4 from VPN to LAN action allow source port any service any destination address any',
                'enable', 'commit', 'exit', 'exit']
        rc &= rmt.do_cli_commands(cmd2)
        cmd3 = ['config',
                'access-rule ipv4 from VPN to VPN action allow source port any service any destination address any',
                'enable', 'commit', 'exit', 'exit']
        rc &= rmt.do_cli_commands(cmd3)
        Assertion.assert_equal(rc,True, 'Add VPN Access Rule on Remote Failed.')

    def test_00_04_add_syslog_address_objects(self):
        logger.info(' Add Syslog address objects '.center(40,'-'))
        rc = True
        ret = RAddrOBJ.config_addressobject(msg=True, **log_addr_obj)
        if ret[0]:
            logger.info(f"Add {log_addr_obj['name']} address objects success.")
        elif 'Already exists' in ret[1]['status']['info'][0]['message']:
            logger.info('Local Address Object already exists')
        else:
            rc = False
            logger.info(f'Add {log_addr_obj["name"]} Failed')
        Assertion.assert_equal(rc, True, 'Add Syslog address objects Failed.')