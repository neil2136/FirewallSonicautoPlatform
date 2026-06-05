from definition.settings import *


class TestConfigTB1(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True
    
    @repeat_method(5)
    def test_00_00_Config_Interface_and_register_fw(self):
        logger.info(" {} ".center(20, '-').format('Config  ip address '))
        rc = Linterface.config_interface(**Lx1_r)
        time.sleep(10)
        rc &= license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: Config ip address failed")


    def test_00_01_Config_DNS_Server(self):
        logger.info('-'*10+'Config  DNS  Server '+'-'*10)
        dns_server.send_commands(rm_conf)
        logger.info("install bind9 ...")
        out1 = dns_server.send_commands(install_bind9_cmds)
        logger.info("configure bind9 ...")
        out2 = dns_server.send_commands(config_bind9_cmds)
        logger.info("start up bind9 ...")
        out3 = dns_server.send_commands(dns_route_cmds)
        if ("bind-9.11.4-26.P2.el7_9.14.x86_64" in str(out1) or 'bind-9.8.2-0.30.rc1.el6_6.3.i686' in str(out1)) \
            and "named.localhost" in str(out2):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Config  DNS  Server  Failed.')
        
    def test_00_02_Config_PC3(self):
        logger.info('-'*10+'Config PC3 '+'-'*10)
        out1 = PC3.send_commands(config_pc3_cmds)
        out2 = PC3.send_commands(pc3_route_cmds)
        if '/usr/local/bin/netwox' in out1 and f"{PC1_Network}/24 via {DUT_X2} dev {PC3_IF}" in out2:
            rc = True
        else:
            rc = False
            logger.error(out2)
        Assertion.assert_equal(rc, True, 'Config PC3  Failed.')

    def test_00_03_Config_PC1(self):
        logger.info('-'*10+'Config PC1 '+'-'*10)
        out1 = PC1.send_commands(pc1_route_cmds)
        if f"{PC2_Network}/24 via {DUT_X0}" in out1 and f"{PC3_Network}/24 via {DUT_X0}" in out1:
            rc = True
        else:
            rc = False
            logger.error(out1)
        Assertion.assert_equal(rc, True, 'Config PC1  Failed.')

    def test_00_04_Disable_LB(self):
        logger.info(" {} ".center(20, '-').format('Disable Load Balance...'))
        rc = faillb_obj.config_failover_settings(**lb_opt)
        Assertion.assert_equal(rc, True, "ERR: Disable Load Balance... failed")

    def test_00_05_Config_Interface(self):
        logger.info(" {} ".center(20, '-').format('Config  ip address '))
        rc = Linterface.config_interface(**Lx1)
        Assertion.assert_equal(rc, True, "ERR: Config ip address failed")

    def test_00_06_Add_AddObj(self):
        logger.info('-'*10+'Add  AddObj for DUT '+'-'*10)
        rc = LAddrOBJ.config_addressobject(**fqdn_ao)
        rc &= LAddrOBJ.config_addressobject(**fqdn_ao_com)
        rc &= LAddrOBJ.config_addressobject(**fqdn_ao_net)
        for i in range(ord("a"),ord("z")+1):
            i = chr(i)
            ao = {
                    'name': f'{i}{i}{i}',
                    'zone': 'WAN',
                    'object_type': 'fqdn',
                    'value': f'{i}{i}{i}.com',
                    'dns_ttl':0
                }
            rc &= LAddrOBJ.config_addressobject(**ao)
            ao_group1['address_groups'][0]['ipv4']['address_object']['fqdn'].append({"name":f'{i}{i}{i}'})
            ao_group2['address_groups'][0]['ipv4']['address_object']['fqdn'].append({"name":f'{i}{i}{i}'})
        ao_group1['address_groups'][0]['ipv4']['address_object']['fqdn'].append({"name":'test'})
        rc &= LAddrGroupOBJ.add_addressgroup(**ao_group1)
        rc &= LAddrGroupOBJ.add_addressgroup(**ao_group2)
        Assertion.assert_equal(rc, True, 'Add local and remote AddObj for DUT  Failed.')

    





   
