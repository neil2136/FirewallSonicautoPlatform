from definition.settings import *

class TestConfigMailServer(Test):
    uuid = 'NonTC'
    description = "setup mail server"
    goto_teardown = True   

    def test_01_Setup_MAIL_Server_on_PC1(self):
        flag = False        

        # config cert
        localhost.send_command("mkdir /etc/tls -p")
        localhost.send_command("\\cp -f " + config_path + "/ssl_mail_server_certificate.conf /etc/tls/")
        localhost.send_command("openssl req -config /etc/tls/ssl_mail_server_certificate.conf -new -x509 -sha256 \
          -newkey rsa:2048 -nodes -keyout /etc/tls/privkey.pem -days 365 -out /etc/tls/mail_cert.pem")
        localhost.send_command("chmod 600 /etc/tls")

        # config postfix
        localhost.send_command("\\cp -f "+config_path + "/postfix/main.cf /etc/postfix/main.cf")
        localhost.send_command("\\cp -f " + config_path + "/postfix/master.cf /etc/postfix/master.cf")
        localhost.send_command("service postfix restart")

        # config dovecot
        localhost.send_command("\\cp -f " + config_path + "/dovecot/dovecot.conf /etc/dovecot/dovecot.conf")
        localhost.send_command("\\cp -f " + config_path + "/dovecot/10-ssl.conf /etc/dovecot/conf.d/10-ssl.conf")
        localhost.send_command("\\cp -f " + config_path + "/dovecot/10-mail.conf /etc/dovecot/conf.d/10-mail.conf")
        localhost.send_command("\\cp -f " + config_path + "/dovecot/10-master.conf /etc/dovecot/conf.d/10-master.conf")
        localhost.send_command("service dovecot restart")

        #add user
        localhost.send_command("useradd test1")
        localhost.send_command("echo 'password' |passwd --stdin test1")
        localhost.send_command("useradd test2")
        localhost.send_command("echo 'password' |passwd --stdin test2")
      
        postfix_status = os.popen("service postfix status").read()
        dovecot_status = os.popen("service dovecot status").read()
        logger.info(f"postfix status:{postfix_status},dovecot status:{dovecot_status}")

        if 'running' in postfix_status and 'running' in dovecot_status:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Setup mail server on PC1 failed")
