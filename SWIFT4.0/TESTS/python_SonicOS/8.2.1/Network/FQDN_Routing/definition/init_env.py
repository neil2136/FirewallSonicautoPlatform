from definition.settings import *

class PreConfig_for_FQDN_Testing(Test):
    uuid = 'NonTC'

    def test_00_01_00_Config_X1(self):
        rc = if_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_00_01_01_Sync_License_On_Line(self):
        rc = license_cli.register('online')
        Assertion.assert_equal(rc, True, "ERR: Sync license on line failed")

    def test_00_02_Config_X2(self):
        rc = if_api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_00_03_Config_X3(self):
        rc = if_api.config_interface(**x3_static)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")

    def test_00_04_Enable_DNS_Server_on_Router(self):
        cmd = "cp -f /etc/named.conf /etc/named.rfc1912.zones /var/named/chroot/etc/"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)

        cmd = "cp -rf /usr/share/doc/bind-9.8.2/sample/var/* /var/named/chroot/var/"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)

        cmd = "cp -f " + CONFPATH + "/named.conf /var/named/chroot/etc/"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)

        cmd = "cp -f " + CONFPATH + "/named.rfc1912.zones /var/named/chroot/etc/"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)

        cmd = "cp -f " + CONFPATH + "/sonicwall-fqdn-test.com.zone /var/named/chroot/var/named/"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)

        cmd = "chmod +r -R /var/named/chroot/"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)

        cmd = "service named restart"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)

        cmd = "netstat -an|grep ':53 '"
        output = router.send_command(cmd)
        logger.info("Listen port:")
        logger.info(output)

        cmd = "netstat -an|grep ':53 '|wc -l"
        logger.info("cmd: " + cmd)
        output = router.send_command(cmd)
        logger.info(output)

        rc = False
        if int(output) > 11:
            rc = True
            logger.info("Enable the DNS Server on ROUTER successfully.")
        else:
            logger.info("Enable the DNS Server on ROUTER failed.")

        Assertion.assert_equal(rc, True, "ERR: Enable DNS Server on ROUTER failed")

    def test_00_05_Modify_PC1_DNS_Address(self):
        cmd = "cat /etc/resolv.conf"
        output = os.popen(cmd).readlines()
        logger.info("Old DNS config:")
        logger.info(output)

        if not os.path.exists('/etc/resolv.conf_cp'):
            cmd = "cat /etc/resolv.conf > /etc/resolv.conf_cp"
            logger.info("cmd: " + cmd)
            os.system(cmd)

        cmd = "sed -i '/nameserver/d' /etc/resolv.conf"
        logger.info("cmd: " + cmd)
        os.system(cmd)

        cmd = "echo 'nameserver " + Parameter.ROUTER_E0_X1 + "' >> /etc/resolv.conf"
        logger.info("cmd: " + cmd)
        os.system(cmd)

        cmd = "echo 'nameserver " + Parameter.ROUTER_E1_X2 + "' >> /etc/resolv.conf"
        logger.info("cmd: " + cmd)
        os.system(cmd)

        cmd = "echo 'nameserver " + Parameter.ROUTER_E2_X3 + "' >> /etc/resolv.conf"
        logger.info("cmd: " + cmd)
        os.system(cmd)

        cmd = "cat /etc/resolv.conf"
        output = os.popen(cmd).readlines()
        logger.info("New DNS config:")
        out_str = ','
        if output:
            out_str = out_str.join(output)
        logger.info(out_str)

        rc = False
        if "nameserver " + Parameter.ROUTER_E0_X1 in out_str and \
           "nameserver " + Parameter.ROUTER_E1_X2 in out_str and \
           "nameserver " + Parameter.ROUTER_E2_X3 in out_str:
            rc = True
            logger.info("Modify PC1's DNS Address successfully.")
        else:
            logger.info("Modify PC1's DNS Address failed.")

        Assertion.assert_equal(rc, True, "ERR: Modify PC1's DNS Address failed")

    def test_00_06_Modify_PC1_Route(self):
        cmd = "route -n"
        output = os.popen(cmd).readlines()
        logger.info("Old routing table:")
        logger.info(output)

        cmd = "route add -net " + Parameter.UNREACH_NET + "/16 gw " + Parameter.FIREWALL
        os.system(cmd)
        cmd = "route add -net " + Parameter.PORT_NET + "/16 gw " + Parameter.FIREWALL
        os.system(cmd)

        cmd = "route -n"
        output = os.popen(cmd).readlines()
        logger.info("New routing table:")
        out_str = ','
        if output:
            out_str = out_str.join(output)
        logger.info(out_str)

        rc = False
        search_pattern = re.compile(Parameter.UNREACH_NET + "\s+" + Parameter.FIREWALL)
        match1 = search_pattern.search(out_str)
        search_pattern = re.compile(Parameter.PORT_NET + "\s+" + Parameter.FIREWALL)
        match2 = search_pattern.search(out_str)

        if match1 and match2:
            rc = True
            logger.info("Modify PC1's routing successfully.")
        else:
            logger.info("Modify PC1's routing failed.")

        Assertion.assert_equal(rc, True, "ERR: Modify PC1's routing failed")

    def test_00_07_Add_IPv4_FQDN_Address_Objects(self):
        logger.info('Add IPv4 FQDN address object 1...')
        rc = ao_api.config_addressobject(**ipv4_fqdn_www)
        logger.info('Add IPv4 FQDN address object 2...')
        rc &= ao_api.config_addressobject(**ipv4_fqdn_ftp)
        logger.info('Add IPv4 FQDN address object 3...')
        rc &= ao_api.config_addressobject(**ipv4_fqdn_smb)
        logger.info('Add IPv4 HOST address object...')
        rc &= ao_api.config_addressobject(**ipv4_host)
        logger.info('Add IPv4 NETWORK address object...')
        rc &= ao_api.config_addressobject(**ipv4_network)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add FQDN Address Objects")
