from definition.settings import *

CONFS_PATH = os.environ["PYTHON_SONICOS_HOME"] + \
             '/Log/App_Control_Filename_Logging/definition/confs/'
print(CONFS_PATH)


class TestInitConfigPC(Test):
    uuid = 'NonTC'
    description = "initial setup server"
    goto_teardown = True

    def test_01_add_create_txt_attachment(self):
        PC1_login.send_command('echo "HELLO WORLD FILE ATTACHMENT" > /tmp/test.txt')

    def test_02_setup_syslog_server_on_PC2(self):
        ret = PC2_login.system(f"\\cp -f {CONFS_PATH}/rsyslog.conf /etc/rsyslog.conf")
        ret += PC2_login.system(f"\\cp -f {CONFS_PATH}/rsyslog /etc/sysconfig/rsyslog")
        ret += PC2_login.system("service rsyslog restart")
        logger.info("############")
        logger.info(ret)
        logger.info("############")
        # Assertion.assert_equal(ret, 0, "ERR: Setup syslog server failed")
        output = PC2_login.send_command("lsof -i:514")
        time.sleep(3)
        logger.info("############")
        logger.info(output)
        logger.info("############")
        Assertion.assert_regular(
            output, 'LISTEN', "Verify syslog server port failed")

    def test_03_setup_snmp_server_on_PC2(self):
        PC2_login.send_command(
            f"\\cp -f {CONFS_PATH}/snmptrapd.conf /etc/snmp/snmptrapd.conf")
        PC2_login.send_command('snmptrapd -c /etc/snmp/snmptrapd.conf')
        output = PC2_login.send_command("lsof -i:162")
        time.sleep(3)
        Assertion.assert_regular(
            output, 'snmptrap', "Verify snmp server port failed")

    def test_04_setup_ftp_server_on_PC2(self):
        ftp_server_config = [
            "mkdir /var/www/html/virus",
            "echo 'FTP CHECK!' > /var/www/html/virus/test.txt",
            "sed -i 's/^root/#root/' /etc/vsftpd/ftpusers",
            "sed -i 's/^root/#root/' /etc/vsftpd/user_list",
            "echo 1 > /proc/sys/net/ipv4/ip_forward",
            'service vsftpd restart',
            'service vsftpd status',
        ]
        output = PC2_login.send_commands(ftp_server_config)
        logger.info("############")
        logger.info(output)
        logger.info("############")
        res = True if 'running' in output else False
        Assertion.assert_equal(res, True, "ERR: setup ftp server on PC2 failed")

    def test_05_setup_http_server_on_PC2(self):
        http_server_config = [
            'echo "HELLO WORLD" > /var/www/html/test.html',
            '\cp {}/httpd.conf /etc/httpd/conf/httpd.conf'.format(http_confs_path),
            'systemctl restart httpd',
            'systemctl status httpd'
        ]
        output = PC2_login.send_commands(http_server_config)
        logger.info("############")
        logger.info(output)
        logger.info("############")
        res = True if ' active (running)' in output else False
        Assertion.assert_equal(res, True, "ERR: setup http server on PC2 failed")

    def test_06_config_SMB_server_PC2(self):
        SMB_path = CONFS_PATH + 'smb/smb.conf'
        smb_config = [
            "mkdir /root/shared_sbharaj",
            "yum -y install samba samba-client samba-common",
            "mv /etc/samba/smb.conf /tmp",
            "\cp -f {}  /etc/samba/smb.conf".format(SMB_path),
            "echo 'CONTENT FROM SHARED DIRECTORY OVER SMB PROTOCOL' > /root/shared_sbharaj/test.txt"

        ]
        output = PC2_login.send_commands(smb_config)
        logger.info("############")
        logger.info(output)
        logger.info("############")
        # res = True if ' active (running)' in output else False
        # Assertion.assert_equal(res, True, "ERR: setup samba server on PC2 failed")

    def test_07_create_user_passwd(self):
        logger.info('Create new user for mail server')
        rc = PC2_login.send_command('useradd sambauser')
        rc = PC2_login.send_command("echo Sonicauto | passwd --stdin sambauser")
        rc = PC2_login.send_command("printf 'Sonicauto\nSonicauto' | smbpasswd -a -s sambauser")
        rc = PC2_login.send_command("smbpasswd -e sambauser")
        rc = PC2_login.send_command('cat /etc/passwd')
        logger.info(rc)
        Assertion.assert_regular(rc, "sambauser:x:1002:1002::/home/sambauser:/bin/bash", "ERR: Create new user for SMB protocol failed")

    def test_08_restart_SMB_server_PC2(self):
        smb_config = [
            "smbd start",
            "systemctl restart smb.service",
            "systemctl start smb.service",
            "systemctl enable smb.service",
            "systemctl status smb.service"

        ]
        output = PC2_login.send_commands(smb_config)
        logger.info("############")
        logger.info(output)
        logger.info("############")
        res = True if ' active (running)' in output else False
        Assertion.assert_equal(res, True, "ERR: setup samba server on PC2 failed")

    def test_09_PCs_ipv6_configure(self):
        res = {}
        logger.info(" {} ".center(50, '-').format('PC1 ipv6 Route Configure'))
        cmds = [f'ip -6 route add 2001::/64 via {Parameter.X0_IPV6}',
                'sleep 3',
                'ip -6 r']
        output = PC1_login.send_commands(cmds)
        res['pc1'] = True if f'2001::/64 via' in output else False

        logger.info(" {} ".center(50, '-').format('PC2 ipv6 Route Configure'))
        cmds = [f'ip -6 route add 2000::/64 via {Parameter.X1_IPV6}',
                'sleep 3',
                'ip -6 r']
        output = PC2_login.send_commands(cmds)
        res['pc2'] = True if f'2000::/64 via' in output else False

        logger.info(f'configure pc ipv6 result: {res}')
        Assertion.assert_equal(all(res.values()), True, "ERR: Config PCs ipv6 settings failed")

