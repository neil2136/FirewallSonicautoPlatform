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

    finally:
        ssh.close()

    # Check for errors
    if error:
        raise Exception(f"Error executing command: {error.strip()}")


class TestConfigWorkStationClient(Test):
    uuid = 'NonTC'

    @repeat_method(2)
    def test_01_config_sso_workstation_client(self):
        command1 = (
            "powershell -Command \""
            "Copy-Item -Path 'C:\\ProgramData\\ssh\\sshd_config' -Destination 'C:\\ProgramData\\ssh\\sshd_config.bak'; "
            "(Get-Content -Path 'C:\\ProgramData\\ssh\\sshd_config') -replace '#PasswordAuthentication yes', 'PasswordAuthentication yes' | Set-Content -Path 'C:\\ProgramData\\ssh\\sshd_config'; "
            f"Set-DnsClientServerAddress -InterfaceAlias 'Ethernet 2' -ServerAddresses {Parameter.SSO_SERV}; "
            "\""
        )
        logger.info(f"Sending command - {command1}")
        ssh_execute_command(Parameter.WORKSTATION_IP, Parameter.WORKSTATION_U, Parameter.WORKSTATION_P, command1)
        
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
        ssh_execute_command(Parameter.WORKSTATION_IP, Parameter.WORKSTATION_U, Parameter.WORKSTATION_P, command2)
        
        # restart machine
        command3 = "shutdown /r /f /t 0"
        logger.info(f"Sending command - {command3}")
        ssh_execute_command(Parameter.WORKSTATION_IP, Parameter.WORKSTATION_U, Parameter.WORKSTATION_P, command3)
        logger.info("Waiting for PC to restart!")
        time.sleep(60)
        start_time = time.time()
        while time.time()-start_time < 60:
            if pc1.ping(Parameter.WORKSTATION_IP):
                break
            time.sleep(10)

        # disable fw and ad route
        command4 = f"netsh advfirewall set allprofiles state off"
        logger.info(f"Sending command - {command4}")
        ssh_execute_command(Parameter.WORKSTATION_IP, Parameter.WORKSTATION_U, Parameter.WORKSTATION_P, command4)
       
    def test_02_config_routes(self):
        command1 = f"route add 13.0.0.0 MASK 255.255.255.0 {Parameter.FIREWALL}"
        logger.info(f"Sending command - {command1}")
        ssh_execute_command(Parameter.WORKSTATION_IP, Parameter.WORKSTATION_U, Parameter.WORKSTATION_P, command1)