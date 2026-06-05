from definition.settings import *

class TestConfigMailServer(Test):
    uuid = 'NonTC'

    def test_01_config_mail_server(self):
        #postfix+dovecot,postfix is used for sending email, dovecot(imap+pop) is used for fetching email
        logger.info('Remove old postfix on PC2')
        rc = PC2_login.send_command('yum -y remove postfix')

        # logger.info('Install new postfix and dovecot on PC2')
        # rc = PC2_login.send_command('yum -y install postfix')
        # rc = PC2_login.send_command('yum -y install dovecot')
        # rc = PC2_login.send_command('yum -y install crontabs')
        # rc = PC2_login.send_command('yum -y install cyrus-sasl*')

        postfix_path_rpm = libPath + "/postfix-2.10.1-9.el7.x86_64.rpm"
        dovecot_path_rpm = libPath + "/dovecot-2.2.36-8.el7.i686.rpm"
        cyrus_sasl_path_rpm = libPath + "/cyrus-sasl-2.1.26-23.el7.i686.rpm"
        crontabs_path_rpm = libPath + "/crontabs-1.11-6.20121102git.el7.noarch.rpm"
        PC2_login.send_command('yum -y install {}'.format(postfix_path_rpm))
        PC2_login.send_command('yum -y install {}'.format(dovecot_path_rpm))
        PC2_login.send_command('yum -y install {}'.format(crontabs_path_rpm))
        PC2_login.send_command('yum -y install {}'.format(cyrus_sasl_path_rpm))

        logger.info('Remove old postfix config file')
        rc = PC2_login.send_command('mv /etc/postfix/main.cf /tmp/')
        rc = PC2_login.send_command('mv /etc/postfix/master.cf /tmp/')

        logger.info('Remove old dovecot config file')
        rc = PC2_login.send_command('mv /etc/dovecot/dovecot.conf /tmp/')
        rc = PC2_login.send_command('mv /etc/dovecot/conf.d /tmp/')

        logger.info('Copy config file from mailserver folder to postfix related folder')
        main_path = MailServerfile + '/postfix/main.cf'
        rc = PC2_login.send_command('\cp {} /etc/postfix/' .format(main_path))
        master_path = MailServerfile + '/postfix/master.cf'
        rc = PC2_login.send_command('\cp {} /etc/postfix/' .format(master_path))

        logger.info('Copy config file from mailserver folder to dovecot related folder')
        conf_path = MailServerfile + '/dovecot/conf.d/'
        rc = PC2_login.send_command('\cp -r {} /etc/dovecot/'.format(conf_path))
        dovecot_path = MailServerfile + '/dovecot/dovecot.conf'
        rc = PC2_login.send_command('\cp {} /etc/dovecot/'.format(dovecot_path))

        logger.info('Copy cert file to tls certs folder')
        # Enable SSL, certs must be provided
        key_path = MailServerfile + '/self-signed.key'
        pem_path = MailServerfile + '/self-signed.pem'
        rc = PC2_login.send_command('\cp {} /etc/pki/tls/certs/'.format(key_path))
        rc = PC2_login.send_command('\cp {} /etc/pki/tls/certs/'.format(pem_path))

    # def test_00_02_config_domain_on_pc2(self):
    #     logger.info('Reset hostname for PC2')
    #     rc = PC2_login.send_command('hostname mail.sahil.com')
    #     rc = PC2_login.send_command('hostname')
    #     output = rc.decode('ascii')
    #     logger.info(output)
    #     Assertion.assert_regular(output, 'mail.sahil.com', "ERR: Reset hostname for PC2 failed")

    def test_03_start_service_postfix(self):
        restart_service = [
            "systemctl start postfix",
            "systemctl enable postfix",
            "systemctl status postfix"            
        ]
        output = PC2_login.send_commands(restart_service)
        logger.info("############")
        logger.info(output)
        logger.info("############")
        res = True if ' active (running)' in output else False
        Assertion.assert_equal(res, True, "ERR: setup postfix server on PC2 failed")

    def test_04_start_service_dovecot(self):
        restart_service = [
            "systemctl start dovecot",
            "systemctl enable dovecot",
            "systemctl status dovecot"
        ]
        output = PC2_login.send_commands(restart_service)
        logger.info("############")
        logger.info(output)
        logger.info("############")
        res = True if ' active (running)' in output else False
        Assertion.assert_equal(res, True, "ERR: setup dovecot server on PC2 failed")

    def test_05_start_service_saslauthd(self):
        restart_service = [
            "systemctl start saslauthd",
            "systemctl enable saslauthd",
            "systemctl status saslauthd"
        ]
        output = PC2_login.send_commands(restart_service)
        logger.info("############")
        logger.info(output)
        logger.info("############")
        res = True if ' active (running)' in output else False
        Assertion.assert_equal(res, True, "ERR: setup saslauthd server on PC2 failed")

    def test_06_create_user_passwd(self):
        logger.info('Create new user for mail server')
        rc = PC2_login.send_command('useradd sahil')
        rc = PC2_login.send_command("echo 'password'|passwd --stdin sahil")
        rc = PC2_login.send_command('cat /etc/passwd')
        # output = rc.decode('ascii')
        logger.info(rc)
        Assertion.assert_regular(rc, "sahil:x:1001:1001::/home/sahil:/bin/bash", "ERR: Create new user for mail server failed")

    def test_07_create_mail_box(self):
        logger.info('Create inbox for mail server')
        rc = PC2_login.send_command('mkdir -p /home/sahil/mail/.imap/INBOX')
        rc = PC2_login.send_command('ls -la /home/sahil/mail/.imap/')
        logger.info(rc)
        Assertion.assert_regular(rc, 'INBOX', "ERR: Create inbox for mail server failed")
        
