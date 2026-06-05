from definition.settings import *


class TestConfigTB1(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True
    
#--------Test local destination is DMZ and remote destination is LAN---------
    def test_00_01_Add_zone(self):
        logger.info(" {} ".center(20, '-').format('Add zone for cst'))
        rc = Lzone_obj.add_zone_object(**zone_ref)
        Assertion.assert_equal(rc, True, "ERR: Add zone for cst failed")
    
    def test_00_02_Config_Interface(self):
        logger.info(" {} ".center(20, '-').format('Config  ip address '))
        rc = Linterface.config_interface(**Lx1)
        rc &= Linterface.config_interface(**Lx2)
        rc &= Linterface.config_interface(**Lx3)
        Assertion.assert_equal(rc, True, "ERR: Config ip address failed")
        
    def test_00_03_Add_AddObj(self):
        logger.info('-'*10+'Add  AddObj for DUT '+'-'*10)
        rc = LAddrOBJ.config_addressobject(**http_public_ao)
        rc &= LAddrOBJ.config_addressobject(**http_private1_ao)
        rc &= LAddrOBJ.config_addressobject(**http_private2_ao)
        rc &= LAddrOBJ.config_addressobject(**http_private3_ao)
        Assertion.assert_equal(rc, True, 'Add local and remote AddObj for DUT  Failed.')
        
    def test_00_04_Config_DNS_Server(self):
        logger.info('-'*10+'Config  DNS  Server '+'-'*10)
        logger.info("install bind9 ...")
        out1 = dns_server.send_commands(install_bind9_cmds)
        logger.info("configure bind9 ...")
        out2 = dns_server.send_commands(config_bind9_cmds)
        logger.info("start up bind9 ...")
        out3 = dns_server.send_commands(start_bind9_cmds)
        if "/usr/bin/install" in str(out1) and "named.localhost" in str(out2):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Config  DNS  Server  Failed.')
        
    def test_00_05_Config_HTTP_Server(self):
        logger.info('-'*10+'Config  HTTP  Server '+'-'*10)
        out = http_server.send_commands(config_http_cmds)
        logger.info(out)
        if "Active: active (running)" in str(out):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Config  HTTP  Server  Failed.')

    def test_00_06_Restart_DNS_Server(self):
        logger.info('-'*10+'Restart DNS  Server '+'-'*10)
        out = dns_server.send_commands(['systemctl restart dnsmasq','systemctl status dnsmasq'])
        logger.info(out)
        if "Active: active (running)" in str(out) :
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Restart DNS  Server  Failed.')

    





   
