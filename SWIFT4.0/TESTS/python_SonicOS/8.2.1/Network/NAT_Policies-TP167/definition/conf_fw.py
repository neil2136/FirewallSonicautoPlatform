from definition.initial_parameter import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"

    def test_00_00_config_x1_interface(self):
        logger.info("config x1 interface... ")
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS_1,
            'dns2': Parameter.X1_DNS_2,
            'mgmt_https': False,
            'mgmt_ssh': False,
            'mgmt_ping': False,
        }
        rc = interface_ipv4.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_00_01_add_address_object(self):
        lanpc1 = {
            "object_type": "host",
            "name": "lanpc",
            "zone": "LAN",
            "value": PC1_ETH0_IP  #192.168.168.200
        }
        rc = ao_obj.config_addressobject(**lanpc1)
        Assertion.assert_equal(rc, True, "ERR:add ao failed")

    def test_00_02_Setup_for_Lanpc(self):
        #ftp user:ftpuser pwd:password dir:/tmp/
        localhost.send_command('cp ' + os.environ["PYTHON_SONICOS_HOME"] + '/Network/NAT_Policies-TP167/testfiles/test_file.txt /tmp/')
        localhost.send_command('nohup python3 ' + lib_path + '/ftp_server.py' + ' -server ' + PC1_ETH0_IP + ' -user ftpuser -pwd password  -dir /tmp/ >/dev/null 2>&1 &'  )

        localhost.send_command('route add -net 10.0.0.0/8 gw ' + pc1_defaultgw)
        localhost.send_command('route delete default')
        localhost.send_command('route add default gw 192.168.168.168')
        out = localhost.send_command("route")
        if re.search(r'default\s+?VTB\d*-UTM', out, re.M):
            logger.info('add default route for pc1 successfully')

