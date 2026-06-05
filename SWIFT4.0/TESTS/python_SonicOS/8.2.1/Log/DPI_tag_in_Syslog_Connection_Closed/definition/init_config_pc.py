from definition.settings import *
from definition.utils import *


class TestConfig_PC1(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_routes_on_pc1(self):
        pc1_login.send_command(
            f"route add -net 12.12.1.0/24 gateway {Parameter.FIREWALL}")
        out = pc1_login.send_command('ip -4 r')
        Assertion.assert_regular(
            out, f'12.12.1.0/24 via {Parameter.FIREWALL} dev eth2', 'ERR: add route failed on pc1')

    def test_02_setup_syslog_server_on_pc1(self):
        cmd_list = [f'\cp {syslog_conf_path}/rsyslog.conf /etc/',
                    f'\cp {syslog_conf_path}/rsyslog /etc/sysconfig',
                    'systemctl restart rsyslog']
        pc1_login.send_commands(cmd_list)
        output = pc1_login.send_command('systemctl status rsyslog')
        Assertion.assert_regular(
            output, 'active \(running\)', 'ERR: start syslog server on PC1 failed')

    def test_03_cp_udp_file(self):
        pc1_login.send_command(f'\cp {udp_path}/udpclient.py /tmp/')


class TestConfig_PC2(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_install_https_server(self):
        cmd_list = [
            'unalias cp',
            f'cp -rf {http_path} /etc/nginx/confs',
            'cp /etc/nginx/confs/conf/nginx.conf /etc/nginx/nginx.conf',
            'service httpd stop',
            '/usr/sbin/nginx -s stop',
            '/usr/sbin/nginx'
        ]
        for cmd in cmd_list:
            out = pc2_login.send_command(cmd)
            logger.info(out)
        logger.info("check httpserver installed")
        resp = pc2_login.send_command(f'curl {Parameter.httpserver_ip}')
        if 'Welcome to Nginx' in str(resp):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: install https server failed")

    def test_02_cp_udp_file(self):
        pc2_login.send_command(f'\cp {udp_path}/udpserver.py /tmp/')


class TestConfig_PC3(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_install_https_server(self):
        cmd_list = [
            'unalias cp',
            f'cp -rf {http_path} /etc/nginx/confs',
            'cp /etc/nginx/confs/conf/nginx.conf /etc/nginx/nginx.conf',
            'service httpd stop',
            '/usr/sbin/nginx -s stop',
            '/usr/sbin/nginx'
        ]
        for cmd in cmd_list:
            out = pc3_login.send_command(cmd)
            logger.info(out)
        logger.info("check httpserver installed")
        resp = pc3_login.send_command(f'curl {Parameter.dmz_httpserver}')
        if 'Welcome to Nginx' in str(resp):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: install https server failed")
