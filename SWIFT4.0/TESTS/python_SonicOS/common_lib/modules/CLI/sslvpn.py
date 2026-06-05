import re
import time
import os
import paramiko
from runner.settings import logger

class SSLVPNServerSettingsCli:
    """SSLVPN Server Settigs Cli class"""
    ###Attributes used###
    '''
    port 14
    certificate 'use-self-signed'
    user - domain LocalDomain
    management web
    no management ssh
    session - timeout 10
    download - url default
    use - radius mschap
    access LAN, WAN,WLAN,DMZ.
    '''

    def __init__(self, fw):
        self.fw = fw

    def config_server_settings(self, **kwargs):
        commands = ['configure', 'ssl-vpn server']
        time.sleep(5)
        self.fw._is_key_exist(commands, kwargs, 'port')
        try:
            if 'certificate' in kwargs.keys():
                if kwargs['certificate'] == 'use-self-signed':
                    self.fw._is_key_exist(commands, kwargs, 'certificate')
                else:
                    commands.append('certificate ' + 'name ' + kwargs['certificate'])
            self.fw._is_key_exist(commands, kwargs, 'user-domain')
            if 'management' in kwargs.keys():
                for value in kwargs['management']:
                    commands.append('management' + ' ' + value)
            if 'no management' in kwargs.keys():
                for value in kwargs['no management']:
                    commands.append('no management ' + value)
            self.fw._is_key_exist(commands, kwargs, 'session-timeout')
            #if 'timeout' in kwargs.keys():
            #    commands.append('session-timeout ' + kwargs['timeout'])
            if 'download-url' in kwargs.keys():
                if kwargs['download-url'] == 'default':
                    self.fw._is_key_exist(commands,kwargs,'download-url')
                else:
                    commands.append('download-url ' + 'custom ' +kwargs['download-url'])
            if 'use_radius' in kwargs.keys():
                commands.append('use-radius ' + kwargs['use_radius'])
            if 'access' in kwargs.keys():
                for value in kwargs['access']:
                    commands.append('access' + ' ' + value)
            if 'no access' in kwargs.keys():
                for value in kwargs['no access']:
                    commands.append('no access' + ' ' + value)
            else:
                raise KeyError
        except KeyError:
            logger.info("Missing key attributes for server settings")
        for command in ['commit', 'end', 'exit']:
           commands.append(command)
        logger.info(commands)
        time.sleep(5)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_serverssl(self):
        commands = ["show ssl-vpn server"]
        output = self.fw.do_cli_commands(commands, tag=1)
        logger.info(output)
        return output
    def show_sslvpn_config(self, *kwargs):
        """
        example:-
        command=" ","servers",

        """
        supported_commands = " ", "server"
        commands = [" "]
        for command in kwargs:
            if command in supported_commands:
                commands.append("show ssl-vpn " + command)
            else:
                logger.info("'" + command + "'" + " is not a supported command ")
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output


class SSLVPNPortalSettingsCli:
    """SSLVPNPortalSettingsCli class"""
    ###Attributes used###
    """  
    auto - launch
    banner - title
    cache - control
    display - link
    home - page - message
    login - message
    logo
    site - title
    """
    def __init__(self, fw):
        self.fw = fw

    def show_portal(self):
        commands = ['show '+'ssl-vpn '+'portal']
        output = self.fw.do_cli_commands(commands, tag=1)
        logger.info(output)
        return output


    def config_portal_settings(self, **kwargs):
        commands = ['configure', 'ssl-vpn portal']
        time.sleep(5)
        self.fw._is_key_exist(commands, kwargs, 'site-title')
        self.fw._is_key_exist(commands, kwargs, 'banner-title')
        if 'home-page-message' in kwargs.keys():
          if kwargs['home-page-message'] == 'default':
             self.fw._is_key_exist(commands, kwargs, 'home-page-message')
          else:
             commands.append('home-page-message ' + 'custom ' + kwargs['home-page-message'])
        if 'login-message' in kwargs.keys():
          if kwargs['login-message'] == 'default':
              self.fw._is_key_exist(commands, kwargs, 'login-message')
          else:
              commands.append('login-message ' + 'custom ' + kwargs['login-message'])
        self.fw._is_key_exist(commands, kwargs, 'auto-launch')
        self.fw._is_key_exist(commands, kwargs, 'cache-control')
        self.fw._is_key_exist(commands, kwargs, 'display-link')
        self.fw._is_key_exist(commands, kwargs, 'virtual-office')
        if 'logo' in kwargs.keys():
           if kwargs['logo'] == 'default':
              self.fw._is_key_exist(commands, kwargs, 'logo')
           else:
              commands.append('logo '+'custom ' + kwargs['logo'])
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        time.sleep(5)
        logger.info(commands)
        result = self.fw.do_cli_commands(commands)
        return result


class SSLVPNVirtualOfficeCli:
    """SSLVPNVirtualOfficeCli class"""
    ###Attributes used###
    """  
    animation             
    application-path      
    auto-reconnection
    automatic-login       
    colors                
    desktop-background
    display-on-mobile     
    redirect-audio        
    redirect-clipboard
    screen-size           
    start-in-folder       
    window-drag
    """

    def __init__(self, fw):
        self.fw = fw
    
    def show_virtual_office(self):
        commands = ['show '+'ssl-vpn '+'bookmarks']
        output = self.fw.do_cli_commands(commands, tag=1)
        logger.info(output)
        return output

    def config_virtualoffice(self, **kwargs):
        commands = ['configure', 'ssl-vpn virtual-office']
        time.sleep(5)
        commands.append('bookmark ' + kwargs['name'])
        self.fw._is_key_exist(commands, kwargs, 'host')
        # self.fw._is_key_exist(commands, kwargs, 'display-on-mobile')
        try:
            if kwargs['service'] == 'rdp':
                self.fw._is_key_exist(commands, kwargs, 'service')
                self.fw._is_key_exist(commands, kwargs, 'animation')
                self.fw._is_key_exist(commands, kwargs, 'application-path')
                self.fw._is_key_exist(commands, kwargs, 'auto-reconnection')
                self.fw._is_key_exist(commands, kwargs, 'colors')
                self.fw._is_key_exist(commands, kwargs, 'desktop-background')
                self.fw._is_key_exist(commands, kwargs, 'display-on-mobile')
                self.fw._is_key_exist(commands, kwargs, 'start-in-folder')
                self.fw._is_key_exist(commands, kwargs, 'window-drag')
                self.fw._is_key_exist(commands, kwargs, 'redirect-audio')
                self.fw._is_key_exist(commands, kwargs, 'redirect-clipboard')
                self.fw._is_key_exist(commands, kwargs, 'screen-size')
                if kwargs['automatic-login'] == 'ssl-vpn':
                    self.fw._is_key_exist(commands, kwargs, 'automatic-login')
                else:
                    commands.append('automatic-login ' + 'custom name ' + kwargs['custom-name'])
                    commands.append('automatic-login ' + 'custom password ' + kwargs['password'])
                    commands.append('automatic-login ' + 'custom domain ' + kwargs['domain'])
            elif kwargs['service'] == 'ssh':
                self.fw._is_key_exist(commands, kwargs, 'service')
                self.fw._is_key_exist(commands, kwargs, 'automatic-accept-host-key')
                self.fw._is_key_exist(commands, kwargs, 'display-on-mobile')
            elif kwargs['service'] == 'vnc':
                self.fw._is_key_exist(commands, kwargs, 'service')
                self.fw._is_key_exist(commands, kwargs, 'share-desktop')
                self.fw._is_key_exist(commands, kwargs, 'view-only')
                self.fw._is_key_exist(commands, kwargs, 'display-on-mobile')
            elif kwargs['service'] == 'telnet':
                self.fw._is_key_exist(commands, kwargs, 'service')
                self.fw._is_key_exist(commands, kwargs, 'display-on-mobile')
            else:
                raise KeyError
        except KeyError:
            logger.info("Key attributes missing for virtual office")
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        logger.info(commands)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_virtualoffice(self, **kwargs):
        commands = ['configure', 'ssl-vpn virtual-office']
        commands.append('bookmark ' + kwargs['name'])
        self.fw._is_key_exist(commands, kwargs, 'host')
        if kwargs['service'] == 'rdp':
            self.fw._is_key_exist(commands, kwargs, 'service')
            self.fw._is_key_exist(commands, kwargs, 'animation')
            self.fw._is_key_exist(commands, kwargs, 'application-path')
            self.fw._is_key_exist(commands, kwargs, 'auto-reconnection')
            self.fw._is_key_exist(commands, kwargs, 'colors')
            self.fw._is_key_exist(commands, kwargs, 'desktop-background')
            self.fw._is_key_exist(commands, kwargs, 'display-on-mobile')
            self.fw._is_key_exist(commands, kwargs, 'start-in-folder')
            self.fw._is_key_exist(commands, kwargs, 'window-drag')
            self.fw._is_key_exist(commands, kwargs, 'display-on-mobile')
            self.fw._is_key_exist(commands, kwargs, 'redirect-audio')
            self.fw._is_key_exist(commands, kwargs, 'redirect-clipboard')
            self.fw._is_key_exist(commands, kwargs, 'screen-size')
            if kwargs['automatic-login'] == 'ssl-vpn':
                self.fw._is_key_exist(commands, kwargs, 'automatic-login')
            else:
                commands.append('automatic-login ' + 'custom name ' + kwargs['custom-name'])
                commands.append('automatic-login ' + 'custom password ' + kwargs['password'])
                commands.append('automatic-login ' + 'custom domain ' + kwargs['domain'])
        elif kwargs['service'] == 'ssh':
            self.fw._is_key_exist(commands, kwargs, 'service')
            self.fw._is_key_exist(commands, kwargs, 'automatic-accept-host-key')
            self.fw._is_key_exist(commands, kwargs, 'display-on-mobile')
        elif kwargs['service'] == 'vnc':
            self.fw._is_key_exist(commands, kwargs, 'service')
            self.fw._is_key_exist(commands, kwargs, 'share-desktop')
            self.fw._is_key_exist(commands, kwargs, 'view-only')
            self.fw._is_key_exist(commands, kwargs, 'display-on-mobile')
        else:
            self.fw._is_key_exist(commands, kwargs, 'service')
            self.fw._is_key_exist(commands, kwargs, 'display-on-mobile')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        logger.info(commands)
        time.sleep(5)
        result = self.fw.do_cli_commands(commands)
        return result

    #Delete Virtual office bookmark with specific  name
    def del_bookmark(self, *args):
        commands = ['configure', 'ssl-vpn virtual-office']
        if args:
            for value in args:
                commands.append('no bookmark ' + value)
        else:
            logger.info("Entry name should be specified")

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    # Delete All Virtual office bookmark
    def del_all_bookmark(self):
        commands = ['configure', 'ssl-vpn virtual-office']
        commands.append('no bookmarks')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        #logger(commands)
        result = self.fw.do_cli_commands(commands)
        return result


class SSLVPNClientSettingsCli:
    """SSLVPNClientsettingsCliclass"""

    ##Basic settings attributes
    '''
    'ipv4',
    'ipv6',
    '''
    #Client Routes attributes
    '''
    'name'
    'ipv6_name'
    'group',
    'ipv6_group'
    'tunnel-all'
    '''
    #Client settings attributes
    '''
    'auto-update'
    'cache': 'credentials' or 'user-name-only',
    'create-connection-profile'
    'exit-after-disconnect'
    'fingerprint-authentication'
    'netbios-over-sslvpn'
    'touch-id-authentication'
    'uninstall-after-exit'
    'inherit'
    'primary'
    'secondary'
    'search-list'
    'wins-primary'
    'wins-secondary'
    'no search-list'
    '''

    def __init__(self, fw):
        self.fw = fw

    def show_clientdefaultdeviceprofile(self):
        commands = ['show '+'ssl-vpn '+'device-profile '+'Default\ Device\ Profile']
        output = self.fw.do_cli_commands(commands, tag=1)
        logger.info(output)
        return output

    def show_sslvpn_session(self):
        commands = ['show ssl-vpn sessions']
        output = self.fw.do_cli_commands(commands, tag=1)
        logger.info(output)
        return output

    def config_basic_settings(self, **kwargs):
            commands = ['configure', 'ssl-vpn profile']
            commands.append('device-profile ' + 'Default\ Device\ Profile')
            self.fw._is_key_exist(commands, kwargs, 'description')
            if 'name_ipv4' in kwargs.keys():
                commands.append('network-address ipv4 ' + 'name ' +  kwargs['name_ipv4'] + ' zone ' + 'SSLVPN')
            if 'host_ipv4' in kwargs.keys():
                commands.append('network-address ipv4 ' + 'host ' +  kwargs['host_ipv4'] + ' zone ' + 'SSLVPN')
            if 'network_ipv4' in kwargs.keys():
                commands.append('network-address ipv4 ' + 'network ' +  kwargs['network_ipv4'] + ' zone ' + 'SSLVPN')
            if 'range_ipv4' in kwargs.keys():
                commands.append('network-address ipv4 ' + 'range ' +  kwargs['range_ipv4']+ ' zone ' + 'SSLVPN') 
            if 'name_ipv6' in kwargs.keys():
                commands.append('network-address ipv6 ' + 'name ' + kwargs['name_ipv6']+ ' zone ' + 'SSLVPN')
            if 'host_ipv6' in kwargs.keys():
                commands.append('network-address ipv6 ' + 'host ' + kwargs['host_ipv6']+ ' zone ' + 'SSLVPN')
            if 'network_ipv6' in kwargs.keys():
                commands.append('network-address ipv6 ' + 'network ' + kwargs['network_ipv6']+ ' zone ' + 'SSLVPN')
            if 'range_ipv6' in kwargs.keys():
                commands.append('network-address ipv6 ' + 'range ' + kwargs['range_ipv6']+ ' zone ' + 'SSLVPN')            
            for command in ['commit', 'end', 'exit']:
                commands.append(command)
            time.sleep(5)
            logger.info(commands)
            result = self.fw.do_cli_commands(commands)
            return result

    def config_client_routes(self, **kwargs):
        commands = ['configure', 'ssl-vpn profile']
        commands.append('device-profile ' + 'Default\ Device\ Profile ')
        commands.append('routes')
        self.fw._is_key_exist(commands, kwargs, 'tunnel-all')
        if 'name' in kwargs.keys():
            for value in kwargs['name']:
                commands.append('route ' + 'name ' + value)
        if 'group' in kwargs.keys():
            for value in kwargs['group']:
                commands.append('route ' + 'group ' + value)
        if 'ipv6_name' in kwargs.keys():
            for value in kwargs['ipv6_name']:
                commands.append('route ' + 'ipv6 name ' + value)
        if 'ipv6_group' in kwargs.keys():
            for value in kwargs['ipv6_group']:
                commands.append('route ' + 'ipv6 group ' + value)
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        logger.info(commands)
        result = self.fw.do_cli_commands(commands)
        return result

    def config_client_settings(self, **kwargs):
        commands = ['configure', 'ssl-vpn profile ']
        commands.append('device-profile ' + 'Default\ Device\ Profile ')
        commands.append('client')
        try:
            self.fw._is_key_exist(commands, kwargs, 'auto-update')
            self.fw._is_key_exist(commands, kwargs, 'cache')
            self.fw._is_key_exist(commands, kwargs, 'create-connection-profile')
            self.fw._is_key_exist(commands, kwargs, 'exit-after-disconnect')
            self.fw._is_key_exist(commands, kwargs, 'fingerlogger-authentication')
            self.fw._is_key_exist(commands, kwargs, 'touch-id-authentication')
            self.fw._is_key_exist(commands, kwargs, 'uninstall-after-exit')
            self.fw._is_key_exist(commands, kwargs, 'netbios-over-sslvpn')

            if 'inherit' in kwargs.keys():
                commands.append('dns ' + 'inherit')
            else:
                commands.append('no dns ' + 'inherit')
            if 'primary' in kwargs.keys():
                commands.append('dns ' + 'primary ' + kwargs['primary'])
            else:
                commands.append('no dns ' + 'primary')
            if 'secondary' in kwargs.keys():
                commands.append('dns ' + 'secondary ' + kwargs['secondary'])
            else:
                commands.append('no dns ' + 'secondary')
            if 'wins-primary' in kwargs.keys():
                commands.append('wins ' + 'primary ' + kwargs['wins-primary'])
            else:
                commands.append('no wins ' + 'primary')
            if 'wins-secondary' in kwargs.keys():
                commands.append('wins ' + 'secondary '+ kwargs['wins-secondary'])
            else:
                commands.append('no wins ' + 'secondary' )
            if 'search-list' in kwargs.keys():
                for value in kwargs['search-list']:
                    commands.append('dns ' + 'search-list' + ' ' + value)
            if 'no search-list' in kwargs.keys():
                for value in kwargs['no search-list']:
                    commands.append('no dns ' + 'search-list' + ' ' + value)
            else:
                raise KeyError
        except KeyError:
            logger.info("Missing Key attributes for configure client settings")
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        logger.info(commands)
        result = self.fw.do_cli_commands(commands)
        return result


    def del_all_search_list(self):
        commands = ['configure', 'ssl-vpn profile ']
        commands.append('device-profile ' + 'Default\ Device\ Profile ')
        commands.append('client')
        commands.append('no dns search-lists')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        logger.info(commands)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_client_routes(self,**kwargs):
        commands = ['configure', 'ssl-vpn profile']
        commands.append('device-profile ' + 'Default\ Device\ Profile ')
        commands.append('routes')
        if 'name_del' in kwargs.keys():
            for value in kwargs['name_del']:
                commands.append('no '+'route ' + 'name ' + value)
        if 'group_del' in kwargs.keys():
            for value in kwargs['group_del']:
                commands.append('no '+'route ' + 'group ' + value)
        if 'ipv6_name_del' in kwargs.keys():
            for value in kwargs['ipv6_name_del']:
                commands.append('no '+'route ' + 'ipv6 name ' + value)
        if 'ipv6_group_del' in kwargs.keys():
            for value in kwargs['ipv6_group_del']:
                commands.append('no ' +'route ' + 'ipv6 group ' + value)
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        logger.info(commands)
        time.sleep(5)
        result = self.fw.do_cli_commands(commands)
        return result
  

class sslvpn_netex:
	def __init__(self,hostname,username,password):
		self.hostname=hostname
		self.username=username
		self.password=password
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.ssh.connect(hostname=self.hostname, port=22, username=self.username, password=self.password)
		self.netex_win_exe="NXSetupU-x64-10.2.339.exe"
		self.localFilePath = os.environ["PYTHON_COMMON_HOME"]+"/tools/sslvpn_nx_win/"+self.netex_win_exe
		self.remoteFilePath = "Downloads/"



	def send_cmd(self,cmd):
		logger.info(cmd + "in send_cmd func")
		stdin, stdout, stderr=self.ssh.exec_command(cmd)
		result=stdout.read()
		logger.info(result)
		if result:
			result=result
		else:
			result = stderr.read()
		result = str(result, encoding="utf-8")
		logger.info("send_cmd results : "+result)
		return  result


	def scp_exe_file(self):
		logger.info("scp file from local file path to remote file path")
		sftp_client = self.ssh.open_sftp()

		try:
			sftp_client.put(self.localFilePath, self.remoteFilePath+self.netex_win_exe)
		except FileNotFoundError as err:
			logger.info(f"File {localFilePath} was not found on the local system")
			raise err
		sftp_client.close()

	def install_nxwind(self):
		logger.info("installing exe file in windows os")
		self.scp_exe_file()
		install_cmd="cd "+self.remoteFilePath+" & "+self.netex_win_exe+" /S & echo installed\n"
		result=self.send_cmd(cmd=install_cmd)
		time.sleep(30)
		logger.info("results while installing exe file in windows os "+result)
		if 'installed' in result:
			return "installed"
		else:
			return "installation failed"

	def uninstall_nxwind(self):
		logger.info("uninstalling exe file in windows os")
		self.scp_exe_file()
		uninstall_cmd="cd " + self.remoteFilePath + " & " + self.netex_win_exe + " /S & echo uninstalled\n"
		result=self.send_cmd(cmd=uninstall_cmd)
		time.sleep(30)
		logger.info("results while uninstalling exe file in windows os " + result)
		if 'uninstalled' in result:
			return "uninstalled"
		else:
			return "uninstallation failed"

	def nxcli_path_cmd(self,cmd):
		logger.info("moving to windows terminal path to NXCLI to execute NX cli commands")
		nxcli_path= r"cd C:\Program Files (x86)\SonicWall\SSL-VPN\NetExtender & "
		nxcli_cmd = nxcli_path +cmd
		return nxcli_cmd

	def nx_connect(self,cmd):
		nx_connect=cmd
		nx_connect_cmd=self.nxcli_path_cmd(nx_connect)
		nx_connect_result=self.send_cmd(nx_connect_cmd)
		logger.info("inside nx connect func")
		logger.info(nx_connect_result)
		return nx_connect_result
	def nx_disconnect(self,cmd):
		nx_disconnect=cmd
		nx_disconnect_cmd=self.nxcli_path_cmd(nx_disconnect)
		nx_disconnect_result=self.send_cmd(nx_disconnect_cmd)
		logger.info("inside nx disconnect func")
		logger.info(nx_disconnect_result)
		return nx_disconnect_result
	def nx_status(self):
		nx_status="NECLI showstatus"
		nx_status_cmd=self.nxcli_path_cmd(nx_status)
		nx_status_result=self.send_cmd(nx_status_cmd)
		logger.info("inside nx nx_status_result func")
		logger.info(nx_status_result)
		return nx_status_result





















