from definition.settings import *

def ssh_execute_command(host, username, password, command, port=22):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        
        start_time = time.time()
        while not stdout.channel.exit_status_ready():
            elapsed_time = time.time() - start_time
            if elapsed_time > 30:
                raise Exception(f"Command timed out!")
            time.sleep(1)
        output = stdout.read().decode()
        logger.info(f"output - {output}")
        error = stderr.read().decode()
        if error:
            logger.info(f"Error: {error}")
    except Exception as err:
        logger.info(f"Exception: - {err}")
    finally:
        ssh.close()

    # Check for errors
    if error:
        raise Exception(f"Error executing command: {error}")


class TestConfigWorkStationClient(Test):
    uuid = 'NonTC'
    
    @repeat_method(2)
    def test_01_restart_pcs(self):
        pc2_resp = os_obj.reboot_node('PC2')
        Assertion.assert_equal(pc2_resp, True, f"ERR: Failed to reboot PC2.")
        pc3_resp = os_obj.reboot_node('PC3')
        Assertion.assert_equal(pc3_resp, True, "ERR: Failed to reboot PC3.")
        pc4_resp = os_obj.reboot_node('PC4')
        Assertion.assert_equal(pc4_resp, True, "ERR: Failed to reboot PC4.")
        logger.info("Waiting for PC'S to restart!")
        time.sleep(90)
        start = time.time()
        while time.time() - start < 90:
            if pc1.ping(Parameter.LAN_IP) and pc1.ping(Parameter.SSO_SERV) and pc1.ping(Parameter.DMZ_IP):
                break
            time.sleep(10)
        Assertion.assert_equal(pc1.ping(Parameter.LAN_IP) and pc1.ping(Parameter.SSO_SERV) and pc1.ping(Parameter.DMZ_IP), True, "ERR: Failed to restart PC's.")
    
    @repeat_method(2)
    def test_02_ip_assignment(self):
        # Assertion.assert_equal(pc1.ping(Parameter.LAN_IP) and pc1.ping(Parameter.SSO_SERV) and pc1.ping(Parameter.DMZ_IP), True, "ERR: Failed to ping PC's.")
        output1 = pc1.send_command(f'nslookup {Parameter.DOMAIN}.com 192.168.168.120')
        logger.info(f"{output1}")
        output2 = pc1.send_command(f'nslookup {Parameter.DOMAIN}.com 192.168.168.121')
        logger.info(f"{output2}")
        if Parameter.DOMAIN in str(output1):
            Parameter.SSO_SERV = '192.168.168.120'
            Parameter.LAN_IP = '192.168.168.121'
        elif Parameter.DOMAIN in str(output2):
            Parameter.SSO_SERV = '192.168.168.121'
            Parameter.LAN_IP = '192.168.168.120'
        else:
            Assertion.assert_equal(True, False, "ERR: Failed to do nslookup.")


 
    @repeat_method(2)
    def test_04_config_sso_workstation_LAN_client(self):
        command1 = (
            "powershell -Command \""
            "Copy-Item -Path 'C:\\ProgramData\\ssh\\sshd_config' -Destination 'C:\\ProgramData\\ssh\\sshd_config.bak'; "
            "(Get-Content -Path 'C:\\ProgramData\\ssh\\sshd_config') -replace '#PasswordAuthentication yes', 'PasswordAuthentication yes' | Set-Content -Path 'C:\\ProgramData\\ssh\\sshd_config'; "
            f"Set-DnsClientServerAddress -InterfaceAlias 'Ethernet 2' -ServerAddresses {Parameter.SSO_SERV}; "
            "\""
        )
        logger.info(f"Sending command - {command1}")
        ssh_execute_command(Parameter.LAN_IP, Parameter.WORKSTATION_U, Parameter.WORKSTATION_P, command1)
        
        # Making the client domain joined
        command2 = (
            "powershell -Command \""
            f"$username = '{Parameter.DOMAIN}\\{Parameter.DOMAIN_AU}'; "
            f"$password = '{Parameter.DOMAIN_AP}'; "
            "$securePassword = ConvertTo-SecureString $password -AsPlainText -Force; "
            "$credential = New-Object System.Management.Automation.PSCredential($username, $securePassword); "
            f"Add-Computer -DomainName '{Parameter.DOMAIN}.com' -Credential $credential; "
            "\""
        )
        logger.info(f"Sending command - {command2}")
        ssh_execute_command(Parameter.LAN_IP, Parameter.WORKSTATION_U, Parameter.WORKSTATION_P, command2)
        
        # restart machine
        command3 = "shutdown /r /f /t 0"
        logger.info(f"Sending command - {command3}")
        ssh_execute_command(Parameter.LAN_IP, Parameter.WORKSTATION_U, Parameter.WORKSTATION_P, command3)
        logger.info("Waiting for PC to restart!")
        time.sleep(60)
        start_time = time.time()
        while time.time()-start_time < 60:
            if pc1.ping(Parameter.LAN_IP):
                break
            time.sleep(10)

        # disable fw
        command4 = f"netsh advfirewall set allprofiles state off"
        logger.info(f"Sending command - {command4}")
        ssh_execute_command(Parameter.LAN_IP, Parameter.WORKSTATION_U, Parameter.WORKSTATION_P, command4)
    
  