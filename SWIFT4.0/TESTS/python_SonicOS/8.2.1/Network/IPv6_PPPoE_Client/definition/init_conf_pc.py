from definition.settings import *


class TestConfig_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True
    location = "pc2"
    pcobj = PC2_login

    @repeat_method(5)
    def test_01_setup_pppoev6_dibbler_sysctl_radvd_server(self):
        logger.info(f"set up pppoev6 server on {self.location}")
        conf_path = os.environ[
                        'PYTHON_SONICOS_HOME'] + f'/Network/IPv6_PPPoE_Client/definition/config/{self.location}'
        pppoe_cmd_list = [
            'timeout 5 systemctl stop pppoe-server',
            f'timeout 5 \cp {conf_path}/pppoe-server-options  /etc/ppp/',
            f'timeout 5 \cp {conf_path}/chap-secrets  /etc/ppp/',
            f'timeout 5 \cp {conf_path}/pppoe-server-env  /etc/ppp/',
            'timeout 5 systemctl restart pppoe-server',
            'timeout 5 systemctl status pppoe-server',]
        pppoe_res = self.pcobj.send_commands(pppoe_cmd_list)
        pppoe_flag = True if 'active (running)' in str(pppoe_res) else False

        logger.info(f"set up dibbler sysctl radvd server on {self.location}")
        dibbler_sysctl_radvd_cmd_list =[    
            'dibbler-server stop',
            f'timeout 5 \cp {conf_path}/server.conf /etc/dibbler/',

            f'timeout 5 \cp {conf_path}/sysctl.conf /etc/',  
             'timeout 5 sysctl -p',

            f'timeout 5 \cp {conf_path}/radvd.conf /etc/',
            'timeout 5 systemctl restart radvd',
            'timeout 5 systemctl status radvd',
           ]
        radvd_res = self.pcobj.send_commands(dibbler_sysctl_radvd_cmd_list)
        radvd_flag = True if 'active (running)' in str(radvd_res) else False
        Assertion.assert_equal(radvd_flag & pppoe_flag, True, 'ERR: start server on pc failed.')

    def test_02_setup_setup_pppoev6_dibbler_sysctl_radvd_server_on_pc3(self):
        self.location = "pc3"
        self.pcobj = PC3_login
        self.test_01_setup_pppoev6_dibbler_sysctl_radvd_server()

    def test_03_setup_pppoev6_dibbler_sysctl_radvd_server_on_pc4(self):
        self.location = "pc4"
        self.pcobj = PC4_login
        self.test_01_setup_pppoev6_dibbler_sysctl_radvd_server()
   