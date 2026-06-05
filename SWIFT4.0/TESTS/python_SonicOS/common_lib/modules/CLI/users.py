import re
import traceback
import sys
import modules.CLI.users
from runner.settings import logger
# from runner.settings import LOGGING
# logger = LOGGING.getLogger(__name__)


class UsersStatusCli:
    '''UsersStatusCli class'''

    def __init__(self, fw):
        self.fw = fw
        
    def show_users_status(self):
        commands = ['show user status']
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result
        
    def show_users_status_active(self):
        commands = ['show user status active']
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result
        
    def show_users_status_inactive(self):
        commands = ['show user status inactive']
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result

    def show_user_status_detailed(self, **kwargs):
        commands = []
        if 'show_type' in kwargs.keys():
            if kwargs['show_type'] == 'name':
                if 'show_username' in kwargs.keys() and kwargs['show_username']:
                    commands.append('show user status name ' + kwargs['show_username'])
                else:
                    logger.error('Please specifie user name that you want to show.')
                    return False
            if kwargs['show_type'] == 'cli':
                commands.append('show user status cli')
            if kwargs['show_type'] == 'at':
                if kwargs['at']:
                    commands.append('show user status at ' + kwargs['at']) 
                else:
                    logger.error('Please specifie the IP you want to show at.')
                    return False
        else:
            commands = ['show user status']

        for command in ['exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result

    def show_unauthenticated_users(self):
        commands = ['show user status unauthenticated']
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result

    def show_inactive_users(self):
        commands = ['show user status inactive']
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result
    
    def status_setting(self, **kwargs):
        commands = ['configure', 'user management' ]
        self.fw._is_key_exist(commands, kwargs, 'include inactive-users')
        self.fw._is_key_exist(commands, kwargs, 'include unauthenticated-users')
        
        for command in ['commit', 'end', 'exit']:
            commands.append(command)            
        result = self.fw.do_cli_commands(commands)
        return result 
    
    def logout_local_users_name(self, usersname):
        commands = ['configure', 'user management']
        try:
            commands.append("kill-user name " + usersname)
        except:
            logger.error('Please specifie user name that need to logout.')
            return False
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result
        
    def logout_local_users_ip(self, usersip):
        commands = ['configure', 'user management']
        try:
            commands.append("kill-user at " + usersip)
        except:
            logger.error('Please specifie user IP that need to logout.')
            return False
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def list_user_methods(self):
        commands = ['show user ?']
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result
        
        
class UsersSettingsCli:    
    '''UsersSettingsCli class'''
    def __init__(self, fw):
        self.fw = fw

    def list_authen_cli(self):
        commands = ['cli ?']
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result

    def show_authen_setting(self, authtype):
        commands = ['show user authentication '+authtype]
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result
        
    def authen_setting(self, **kwargs):
        commands = ['configure', 'user authentication' ]
        for initcmd in kwargs['initcmds']:
            commands.append(initcmd)
        self.fw._is_key_exist(commands, kwargs, 'auth-method')
        # method:ldap | ldap-local | local | radius | radius-local
        self.fw._is_key_exist(commands, kwargs, 'no method')
        self.fw._is_key_exist(commands, kwargs, 'case-sensitive-names')        
        self.fw._is_key_exist(commands, kwargs, 'login-uniqueness')
        self.fw._is_key_exist(commands, kwargs, 'relogin-after-password-change')
        self.fw._is_key_exist(commands, kwargs, 'one-time-password email-format')
        # email-format: html | plain-text
        self.fw._is_key_exist(commands, kwargs, 'one-time-password format')
        # password format: characters | mixed | numbers
        if 'one-time-password length' in kwargs.keys():
            if kwargs['one-time-password length']:
                commands.append('one-time-password length min ' + kwargs['one-time-password length'][0] + ' max ' + kwargs['one-time-password length'][1])
            else:
                logger.error('password length must be specified.')
                return False
        self.fw._is_key_exist(commands, kwargs, 'show-user-status-window')
                
        for command in ['commit', 'end', 'exit']:
            commands.append(command)            
        result = self.fw.do_cli_commands(commands)
        return result
        
    def weblogin_setting(self, **kwargs):
        commands = ['configure', 'user authentication' ]
        self.fw._is_key_exist(commands, kwargs, 'auth-page-timeout')
        self.fw._is_key_exist(commands, kwargs, 'browser-redirect-via')
        # browser-redirect-via: host-name | interface-ip | name-from-certificate|reverse-dns
        self.fw._is_key_exist(commands, kwargs, 'http-redirect-after-login')
        self.fw._is_key_exist(commands, kwargs, 'radius-chap-http-login')
        self.fw._is_key_exist(commands, kwargs, 'redirect-external-page')
        if 'combined-login' in kwargs.keys():
            if kwargs['combined-login']:
                commands.append('combined-login')
                if 'http' in kwargs['combined-login']:
                    commands.append('combined-login http')
                elif 'http' not in kwargs['combined-login']:
                    commands.append('no combined-login http')
                else:
                    pass
            else:
                commands.append('no combined-login')
        self.fw._is_key_exist(commands, kwargs, 'auth-page-as-frame') 
        
        for command in ['commit', 'end', 'exit']:
            commands.append(command)            
        result = self.fw.do_cli_commands(commands)
        return result

    def auth_bypass(self, **kwargs):    
        commands = ['configure', 'user authentication' ]
        if ('action' in kwargs.keys() and kwargs['action']):
            if kwargs['action'] == 'add':
                logger.info('Add auth bypass')
                self.fw._is_key_exist(commands, kwargs, 'rule-auth-bypass-http-url')
            elif kwargs['action'] == 'delete':
                logger.info('Delete auth bypass')
                self.fw._is_key_exist(commands, kwargs, 'no rule-auth-bypass-http-url')
         
        for command in ['commit', 'end', 'exit']:
            commands.append(command)            
        result = self.fw.do_cli_commands(commands)
        return result 
        
    def user_sessions(self, **kwargs):
        commands = ['configure', 'user authentication' ]
        self.fw._is_key_exist(commands, kwargs, 'inactivity-timeout')
        if 'prevent-inactivity-logout service' in kwargs.keys():
            if not kwargs['prevent-inactivity-logout service']:
                commands.append('no prevent-inactivity-logout service')
            elif kwargs['prevent-inactivity-logout service']:
                if ('group' in kwargs['prevent-inactivity-logout service']):
                    commands.append('prevent-inactivity-logout service group ' + kwargs['prevent-inactivity-logout service'][1])
                elif ('name' in kwargs['prevent-inactivity-logout service']):
                    commands.append('prevent-inactivity-logout service name ' + kwargs['prevent-inactivity-logout service'][1])
                elif ('protocol' in kwargs['prevent-inactivity-logout service']):
                    commands.append('prevent-inactivity-logout service protocol ' + kwargs['prevent-inactivity-logout service'][1])
                else:
                    pass
            else:
                pass
        if 'log-user-name' in kwargs.keys():
            if kwargs['inactivity-timeout']:
                if 'bypass-sso' in kwargs['log-user-name']:
                    commands.append('log-user-name bypass-sso ' + kwargs['log-user-name'][1])
                elif 'originating-externally' in kwargs['log-user-name']:
                    commands.append('log-user-name originating-externally ' + kwargs['log-user-name'][1])
                elif 'other-unidentified' in kwargs['log-user-name']:
                    commands.append('log-user-name other-unidentified ' + kwargs['log-user-name'][1])
                elif 'sso-fail' in kwargs['log-user-name']:
                    commands.append('log-user-name sso-fail ' + kwargs['log-user-name'][1])
                else:
                    pass
            else:
                pass
        if 'no log-user-name' in kwargs.keys():
            if kwargs['inactivity-timeout']:
                if 'bypass-sso' in kwargs['log-user-name']:
                    commands.append('no log-user-name bypass-sso')
                elif 'originating-externally' in kwargs['log-user-name']:
                    commands.append('no log-user-name originating-externally')
                elif 'other-unidentified' in kwargs['log-user-name']:
                    commands.append('no log-user-name other-unidentified')
                elif 'sso-fail' in kwargs['log-user-name']:
                    commands.append('no log-user-name sso-fail')
                else:
                    pass  
            else:
                pass
        if 'user-connections-logout inactivity' in kwargs.keys():
            if 'authentication' in kwargs['user-connections-logout inactivity']:
                if 'terminate' in kwargs['user-connections-logout inactivity'][1]:
                    commands.append('user-connections-logout inactivity authentication terminate')
                elif 'keep-alive' in kwargs['user-connections-logout inactivity'][1]:
                    commands.append('user-connections-logout inactivity authentication keep-alive')
                elif 'terminate' in kwargs['user-connections-logout inactivity'][1][0]:
                    if 'after' in kwargs['user-connections-logout inactivity'][1][0]:
                        commands.append('user-connections-logout inactivity authentication terminate after' + ' ' + kwargs['user-connections-logout inactivity'][1][1])
                else:
                        pass
            elif 'other' in kwargs['user-connections-logout inactivity']:
                if 'keep-alive' in kwargs['user-connections-logout inactivity'][1]:
                    commands.append('user-connections-logout inactivity other keep-alive')
                elif 'terminate' in kwargs['user-connections-logout inactivity'][1]:
                    commands.append('user-connections-logout inactivity other terminate')
                elif 'terminate' in kwargs['user-connections-logout inactivity'][1][0]:
                    if 'after' in kwargs['user-connections-logout inactivity'][1][0]:
                        commands.append('user-connections-logout inactivity other terminate after' + ' ' + kwargs['user-connections-logout inactivity'][1][1])
                else:
                    pass
            else:
                pass
        if 'user-connections-logout reported' in kwargs.keys():
            if 'authentication' in kwargs['user-connections-logout reported']:
                if 'terminate' in kwargs['user-connections-logout reported'][1]:
                    commands.append('user-connections-logout reported authentication terminate')
                elif 'keep-alive' in kwargs['user-connections-logout reported'][1]:
                    commands.append('user-connections-logout reported authentication keep-alive')
                elif 'terminate' in kwargs['user-connections-logout reported'][1][0]:
                    if 'after' in kwargs['user-connections-logout reported'][1][0]:
                        commands.append('user-connections-logout reported authentication terminate after' + ' ' + kwargs['user-connections-logout reported'][1][1])
                else:
                        pass
            elif 'other' in kwargs['user-connections-logout reported']:
                if 'keep-alive' in kwargs['user-connections-logout reported'][1]:
                    commands.append('user-connections-logout reported other keep-alive')
                elif 'terminate' in kwargs['user-connections-logout reported'][1]:
                    commands.append('user-connections-logout reported other terminate')
                elif 'terminate' in kwargs['user-connections-logout reported'][1][0]:
                    if 'after' in kwargs['user-connections-logout reported'][1][0]:
                        commands.append('user-connections-logout reported other terminate after' + ' ' + kwargs['user-connections-logout reported'][1][1])
                else:
                    pass
            else:
                pass
        self.fw._is_key_exist(commands, kwargs, 'inactive-user login')
        self.fw._is_key_exist(commands, kwargs, 'inactive-user timeout')
        self.fw._is_key_exist(commands, kwargs, 'age-out')
        self.fw._is_key_exist(commands, kwargs, 'web-login-session-limit')
        if 'show-user-status-window' in kwargs.keys():
            if kwargs['show-user-status-window']:
                commands.append('show-user-status-window')
                commands.append('status-window-heartbeat period' + ' ' + kwargs['show-user-status-window'])
                if 'disconnected-user-detect' in kwargs.keys():
                    if kwargs['disconnected-user-detect']:
                        commands.append('disconnected-user-detect')
                        commands.append('status-window-heartbeat timeout' + ' ' + kwargs['disconnected-user-detect'])
                    else:
                        commands.append('no disconnected-user-detect')
            else:
                commands.append('no show-user-status-window')
            self.fw._is_key_exist(commands, kwargs, 'open-in-same-window')
        
        for command in ['commit', 'end', 'exit']:
            commands.append(command)            
        result = self.fw.do_cli_commands(commands)
        return result                
    
    def user_customization(self, **kwargs):
        commands = ['configure', 'user authentication']
        self.fw._is_key_exist(commands, kwargs, 'policy-banner')
        self.fw._is_key_exist(commands, kwargs, 'policy-banner content')
        if 'acceptable-use-policy' in kwargs.keys():
            commands.append('acceptable-use-policy')
            if 'window-size' in kwargs.keys():
                if kwargs['window-size']:
                    commands.append('window-size ' + kwargs['window-size'][0] + ' ' + kwargs['window-size'][1]) 
                else:
                    logger.error('Windows size must be specified')
                    return False
            self.fw._is_key_exist(commands, kwargs, 'scroll-bars')
            if 'aup-on-zones' in kwargs.keys():
                for s in kwargs['aup-on-zones']:
                    commands.append('aup-on-zones' + ' ' + s)
            if 'no aup-on-zones' in kwargs.keys():
                for s in kwargs['no aup-on-zones']:
                    commands.append('no aup-on-zones' + ' ' + s)
            self.fw._is_key_exist(commands, kwargs, 'content')
            commands.append('commit')
            commands.append('exit')            
        if 'customize-login-page' in kwargs.keys():
            if kwargs['customize-login-page']:
                commands.append('customize-login-page' + ' ' + kwargs['customize-login-page'][0] + ' ' + kwargs['customize-login-page'][1])
            else:
                logger.error('Login page must be specified')
                return False
        self.fw._is_key_exist(commands, kwargs, 'no customize-login-page') 

        for command in ['commit', 'end', 'exit']:
            commands.append(command)            
        result = self.fw.do_cli_commands(commands)
        return result
   
      
class UserRadiusCli:
    '''UserRadiusCli class'''
    def __init__(self, fw):
        self.fw = fw

    def show_radius_setting(self, authtype):
        commands = ['show user radius '+authtype]
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result
        
    def radius_server_settings(self, **kwargs):
        commands = ['configure', 'user radius']
        # RADIUS-Server-Timeout
        self.fw._is_key_exist(commands, kwargs, 'timeout')
        self.fw._is_key_exist(commands, kwargs, 'retries')
        self.fw._is_key_exist(commands, kwargs, 'local-users-only')
        # user-group-mechanism:{ldap | local-only}
        # user-group-mechanism radius-attribute: {filter-id | vendor-specific}
        self.fw._is_key_exist(commands, kwargs, 'user-group-mechanism')
        self.fw._is_key_exist(commands, kwargs, 'user-group-mechanism radius-attribute')
        self.fw._is_key_exist(commands, kwargs, 'default-user-group')
        # default-user-group:SonicWALL Administrators/Content Filtering Bypass
        # /Limited Administrators/SSLVPN Services/SonicWALL Read-Only Admins/
        # Guest Services/Everyone/Guest Administrators/Trusted Users

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def radius_server(self, **kwargs):
        commands = ['configure', 'user radius']
        if ('action' in kwargs.keys() and kwargs['action']):
            if (kwargs['action'] == 'add' or kwargs['action'] == 'edit'):
                if ('server' in kwargs.keys() and kwargs['server']):
                    commands_radius_server = self._edit_radius_server(**kwargs)
                    commands += commands_radius_server
                else:
                    logger.error('Radius server must be specified.')
            else:
                logger.info('Please determine what to do with radius server')

        for command in ['end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def _edit_radius_server(self, **kwargs):
        commands_radius_server = ['server' + ' ' + kwargs['server']]
        self.fw._is_key_exist(commands_radius_server, kwargs, 'enable')
        self.fw._is_key_exist(commands_radius_server, kwargs, 'host')
        self.fw._is_key_exist(commands_radius_server, kwargs, 'port')
        self.fw._is_key_exist(commands_radius_server, kwargs, 'shared-secret')
        self.fw._is_key_exist(commands_radius_server, kwargs, 'user-name-format')
        # user-name-format:down-level-logon/name-dot-domain/user-name/user-principle
        self.fw._is_key_exist(commands_radius_server, kwargs, 'send-through-vpn-tunnel')
        commands_radius_server.append('commit')
        commands_radius_server.append('exit')
        return commands_radius_server

    def del_radius_server(self, radiusserver):
        commands = ['configure', 'user radius']
        commands.append('no server ' + radiusserver)

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_all_radius_servers(self):
        commands = ['configure', 'user radius']
        commands.append('no servers')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def test_radius_server(self, **kwargs):
        commands = ['configure', 'user radius']
        if ('testmethod' in kwargs.keys() and kwargs['testmethod']):
            if kwargs['testmethod'] == 'connectivity':
                if ('radiusserver' in kwargs.keys() and kwargs['radiusserver']):
                    commands.append('test ' + kwargs['radiusserver'])
                else:
                    logger.info('Please specify which radius server to test')
            elif kwargs['testmethod'] == 'authentication':
                if ('radiusserver' in kwargs.keys() and kwargs['radiusserver']):
                    if ('username' in kwargs.keys() and 'password' in kwargs.keys()):
                        commands.append('test ' + kwargs['radiusserver'] + ' user ' +
                                        kwargs['username'] + ' ' + kwargs['password'])
                    else:
                        logger.info("Please specify radius server's username and password")
                else:
                    logger.info('Please specify which radius server to test')
            elif kwargs['testmethod'] == 'chap':
                if ('radiusserver' in kwargs.keys() and kwargs['radiusserver']):
                    if ('username' in kwargs.keys() and 'password' in kwargs.keys()):
                        commands.append('test ' + kwargs['radiusserver'] + ' user ' +
                                        kwargs['username'] + ' ' + kwargs['password'] + ' charp')
                    else:
                        logger.info("Please specify radius server's username and password")
                else:
                    logger.info('Please specify which radius server to test')
            elif kwargs['testmethod'] == 'mschap':
                if ('radiusserver' in kwargs.keys() and kwargs['radiusserver']):
                    if ('username' in kwargs.keys() and 'password' in kwargs.keys()):
                        commands.append('test ' + kwargs['radiusserver'] + ' user ' +
                                        kwargs['username'] + ' ' + kwargs['password'] + ' mscharp')
                    else:
                        logger.info("Please specify radius server's username and password")
                else:
                    logger.info('Please specify which radius server to test')
            elif kwargs['testmethod'] == 'mschapv2':
                if ('radiusserver' in kwargs.keys() and kwargs['radiusserver']):
                    if ('username' in kwargs.keys() and 'password' in kwargs.keys()):
                        commands.append('test ' + kwargs['radiusserver'] + ' user ' +
                                        kwargs['username'] + ' ' + kwargs['password'] + ' mschapv2')
                    else:
                        logger.info("Please specify radius server's username and password")
                else:
                    logger.info('Please specify which radius server to test')
            else:
                logger.info('Please specify which method to use to test radius server')

        for command in ['end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands, timeout=180)
        return result

    def radius_accounting_settings(self, **kwargs):
        commands = ['configure', 'user radius', 'accounting']
        # Send accounting data for
        self.fw._is_key_exist(commands, kwargs, 'data')
        # data:{ all-servers | guest-users | remote-client-users |
        # data:sso-authenticated-users | users-authenticated-by-web-login }
        self.fw._is_key_exist(commands, kwargs, 'no data')
        self.fw._is_key_exist(commands, kwargs, 'include')
        # include:{domain-and-local-users | domain-users | local-users |
        # include:sso-users-identified-via-RADIUS-accounting}
        self.fw._is_key_exist(commands, kwargs, 'no include')
        # user-group-mechanism:{ldap | local-only}
        # user-group-mechanism radius-attribute: {filter-id | vendor-specific}
        self.fw._is_key_exist(commands, kwargs, 'interim-updates')
        self.fw._is_key_exist(commands, kwargs, 'timeout')
        self.fw._is_key_exist(commands, kwargs, 'retries')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result
    
    def radius_accounting_server(self, **kwargs):
        commands = ['configure', 'user radius', 'accounting']
        if ('action' in kwargs.keys() and kwargs['action']):
            if (kwargs['action'] == 'add' or kwargs['action'] == 'edit'):
                if ('server' in kwargs.keys() and kwargs['server']):
                    commands_accounting = self._edit_radius_accounting_server(**kwargs)
                    commands += commands_accounting
                else:
                    logger.error('Radius accounting must be specified.')
            else:
                logger.info('Please determine what to do with radius accounting')

        for command in ['end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def _edit_radius_accounting_server(self, **kwargs):
        commands_radius = ['server' + ' ' + kwargs['server']]
        self.fw._is_key_exist(commands_radius, kwargs, 'enable')
        self.fw._is_key_exist(commands_radius, kwargs, 'host')
        self.fw._is_key_exist(commands_radius, kwargs, 'port')
        self.fw._is_key_exist(commands_radius, kwargs, 'shared-secret')
        self.fw._is_key_exist(commands_radius, kwargs, 'user-name-format')
        commands_radius.append('commit')
        commands_radius.append('exit')
        return commands_radius

    def del_radius_accounting_server(self, accountingserver):
        commands = ['configure', 'user radius', 'accounting']
        commands.append('no server ' + accountingserver)

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_all_radius_accounting_servers(self):
        commands = ['configure', 'user radius', 'accounting']
        commands.append('no servers')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def test_radius_accounting_server(self, **kwargs):
        commands = ['configure', 'user radius', 'accounting']
        if ('testmethod' in kwargs.keys() and kwargs['testmethod']):
            if kwargs['testmethod'] == 'connectivity':
                if ('radiusserver' in kwargs.keys() and kwargs['radiusserver']):
                    commands.append('test ' + kwargs['radiusserver'])
                else:
                    logger.info('Please specify which radius server to test')
            elif kwargs['testmethod'] == 'useraccounting':
                if ('radiusserver' in kwargs.keys() and kwargs['radiusserver']):
                    if ('username' in kwargs.keys() and 'specifiedserver' in kwargs.keys()):
                        commands.append('test ' + kwargs['radiusserver'] + ' user ' +
                                        kwargs['username'] + ' ' + kwargs['specifiedserver'])
                    else:
                        logger.info("Please specify radius server's username and password")
                else:
                    logger.info('Please specify which radius server to test')
            else:
                logger.info('Please specify which method to use to test radius server')

        for command in ['end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands, timeout=180)
        return result
        
class UserLdapCli:  
    '''UserLdapCli class'''    
    def __init__(self, fw):
        self.fw = fw

    def show_ldap_setting(self, ldapdir):
        commands = ['show user ldap '+ldapdir]
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result
        
    def ldap_settings(self, **kwargs):
        commands = ['configure', 'user ldap']
        for initcmd in kwargs['initcmds']:
            commands.append(initcmd)
        self.fw._is_key_exist(commands, kwargs, 'protocol-version')
        self.fw._is_key_exist(commands, kwargs, 'require-valid-certificate')
        self.fw._is_key_exist(commands, kwargs, 'local-users-only')
        self.fw._is_key_exist(commands, kwargs, 'allow-referrals')
        self.fw._is_key_exist(commands, kwargs, 'allow-references')
        # allow-references:{auto-configuration | domain-search | other-search | user-authentication}
        self.fw._is_key_exist(commands, kwargs, 'local-users-only')
        self.fw._is_key_exist(commands, kwargs, 'default-user-group')
        # default-user-group:SonicWALL Administrators/Content Filtering Bypass/Limited Administrators
        # /SSLVPN Services/SonicWALL Read-Only Admins/Guest Services/
        if ('mirror-user-groups' in kwargs.keys() and kwargs['mirror-user-groups']):
            commands.append('mirror-user-groups')
            if kwargs['mirror-user-groups'] == 'have-members':
                commands.append('mirror-user-groups have-members')
            elif kwargs['mirror-user-groups'] == 'all':
                commands.append('mirror-user-groups all')
            elif kwargs['mirror-user-groups'] == 'refresh':
                if ('mirrorrefresh' in kwargs.keys() and kwargs['mirrorrefresh']):
                    if kwargs['mirrorrefresh'] == 'now':
                        commands.append('mirror-user-groups refresh now')
                    else:
                        commands.append('mirror-user-groups refresh period ' + kwargs['mirrorrefresh'])
            else:
                logger.info('Please configure Mirror LDAP user groups locally correctly')
        else:
            commands.append('no mirror-user-groups')
            commands.append('yes')
        self.fw._is_key_exist(commands, kwargs, 'exclude-tree')
        self.fw._is_key_exist(commands, kwargs, 'no exclude-tree')
        if ('relay' in kwargs.keys() and kwargs['relay']):
            commands.append('relay')
            self.fw._is_key_exist(commands, kwargs, 'enable')
            if 'clients-connect' in kwargs.keys():
                for key in kwargs['clients-connect']:
                    commands.append('clients-connect' + ' ' + key)
        # clients-connect:{public-zones | trusted-zones | vpn-zone | wan-zone | wireless-zones}
            if 'no clients-connect' in kwargs.keys():
                for key in kwargs['no clients-connect']:
                    commands.append('no clients-connect' + ' ' + key)
            self.fw._is_key_exist(commands, kwargs, 'shared-secret')
            if 'legacy-user-group' in kwargs.keys() and kwargs['legacy-user-group']:
                if 'vpn' in kwargs['legacy-user-group'][0]:
                    commands.append('legacy-user-group vpn ' + kwargs['legacy-user-group'][1])
                if 'internet' in kwargs['legacy-user-group'][0]:
                    commands.append('legacy-user-group internet ' + kwargs['legacy-user-group'][1])
                if 'l2tp' in kwargs['legacy-user-group'][0]:
                    commands.append('legacy-user-group l2tp ' + kwargs['legacy-user-group'][1])
                if 'vpn-client' in kwargs['legacy-user-group'][0]:
                    commands.append('legacy-user-group vpn-client ' + kwargs['legacy-user-group'][1])
            self.fw._is_key_exist(commands, kwargs, 'no legacy-user-group')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def add_ldap_server(self, **kwargs):
        commands = ['configure', 'user ldap']
        if 'server' in kwargs.keys():
            if kwargs['server']:
                commands_ldap = self._edit_ldap(**kwargs)
                commands += commands_ldap
            elif not kwargs['server']:
                logger.error('Ldap server must be specified.')
            else:
                pass
        self.fw._is_key_exist(commands, kwargs, 'no server')
        self.fw._is_key_exist(commands, kwargs, 'no servers')
        self.fw._is_key_exist(commands, kwargs, 'save dynamic-secondary')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def _edit_ldap(self, **kwargs):
        commands_ldap = ['server' + ' ' + kwargs['server']]
        self.fw._is_key_exist(commands_ldap, kwargs, 'enable')
        self.fw._is_key_exist(commands_ldap, kwargs, 'role')
        self.fw._is_key_exist(commands_ldap, kwargs, 'host')
        self.fw._is_key_exist(commands_ldap, kwargs, 'port')
        self.fw._is_key_exist(commands_ldap, kwargs, 'timeout operation')
        self.fw._is_key_exist(commands_ldap, kwargs, 'timeout server')
        if 'use-tls' in kwargs.keys():
            if kwargs['use-tls']:
                commands_ldap.append('use-tls')
                self.fw._is_key_exist(commands_ldap, kwargs, 'send-start-tls-request')
            elif not kwargs['use-tls']:
                commands_ldap.append('no use-tls')
            else:
                pass
        self.fw._is_key_exist(commands_ldap, kwargs, 'user-name-format')
        if 'bind' in kwargs.keys():
            if 'anonymous' in kwargs['bind']:
                commands_ldap.append('bind' + ' ' + 'anonymous')
                if 'referred-bind-with-account' in kwargs['bind'][1][0]:
                    commands_ldap.append('referred-bind-with-account' + ' ' + kwargs['bind'][1][1])
                else:
                    pass
            elif 'name' in kwargs['bind']:
                commands_ldap.append('bind name ' + kwargs['bind'][1] + ' location ' + kwargs['bind'][3])
                if 'bind-password' in kwargs.keys():
                    commands_ldap.append('bind-password ' + kwargs['bind-password'])
                if 'referred-bind-with-account' in kwargs['bind']:
                    commands_ldap.append('bind-password ' + kwargs['bind'][7])
            elif 'distinguished-name' in kwargs['bind']:
                commands_ldap.append('bind' + ' ' + 'distinguished-name' + kwargs['bind'][1])
                if 'bind-password' in kwargs['bind']:
                    commands_ldap.append('bind-password ' + kwargs['bind'][3])
                if 'referred-bind-with-account' in kwargs['bind']:
                    commands_ldap.append('bind-password ' + kwargs['bind'][5])
            else:
                pass
        if 'schema' in kwargs.keys():
            if 'custom' in kwargs['schema']:
                commands_ldap.append('schema custom')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute additional-group-id')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute framed-ip-address')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute group-membership')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute logon-name')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute qualified-logon-name')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute use-additional-group-id')
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-attribute')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-class')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-group-class')
                if 'user-group-attribute member' in kwargs.keys():
                    if 'user-id' in kwargs['user-group-attribute member']:
                        commands_ldap.append('user-id' + kwargs['user-group-attribute member'][1])
                    elif 'distinguished-name' in kwargs['user-group-attribute member']:
                        commands_ldap.append('distinguished-name' + kwargs['user-group-attribute member'][1])
                    else:
                        pass
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-group-attribute additional-group-match')
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-group-attribute member')
                self.fw._is_key_exist(commands_ldap, kwargs, 'read-from-server display')
                # self.fw._is_key_exist(commands_ldap, kwargs, 'read-from-server auto-configure ')
            if 'inet-org-person' in kwargs['schema']:
                commands_ldap.append('schema inet-org-person')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute additional-group-id')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute framed-ip-address')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute group-membership')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute logon-name')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute qualified-logon-name')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute use-additional-group-id')
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-attribute')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-class')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-group-class')
                if 'user-group-attribute member' in kwargs.keys():
                    if 'user-id' in kwargs['user-group-attribute member']:
                        commands_ldap.append('user-id' + kwargs['user-group-attribute member'][1])
                    elif 'distinguished-name' in kwargs['user-group-attribute member']:
                        commands_ldap.append('distinguished-name' + kwargs['user-group-attribute member'][1])
                    else:
                        pass
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-group-attribute additional-group-match')
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-group-attribute member')
                self.fw._is_key_exist(commands_ldap, kwargs, 'read-from-server display')
                # self.fw._is_key_exist(commands_ldap, kwargs, 'read-from-server auto-configure ')
            if 'microsoft-active-directory' in kwargs['schema']:
                commands_ldap.append('schema microsoft-active-directory')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute additional-group-id')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute framed-ip-address')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute group-membership')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute logon-name')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute qualified-logon-name')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute use-additional-group-id')
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-attribute')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-class')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-group-class')
                if 'user-group-attribute member' in kwargs.keys():
                    if 'user-id' in kwargs['user-group-attribute member']:
                        commands_ldap.append('user-id' + kwargs['user-group-attribute member'][1])
                    elif 'distinguished-name' in kwargs['user-group-attribute member']:
                        commands_ldap.append('distinguished-name' + kwargs['user-group-attribute member'][1])
                    else:
                        pass
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-group-attribute additional-group-match')
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-group-attribute member')
                self.fw._is_key_exist(commands_ldap, kwargs, 'read-from-server display')
                # self.fw._is_key_exist(commands_ldap, kwargs, 'read-from-server auto-configure ')
            if 'network-information-service' in kwargs['schema']:
                commands_ldap.append('schema network-information-service')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute additional-group-id')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute framed-ip-address')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute group-membership')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute logon-name')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute qualified-logon-name')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute use-additional-group-id')
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-attribute')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-class')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-group-class')
                if 'user-group-attribute member' in kwargs.keys():
                    if 'user-id' in kwargs['user-group-attribute member']:
                        commands_ldap.append('user-id' + kwargs['user-group-attribute member'][1])
                    elif 'distinguished-name' in kwargs['user-group-attribute member']:
                        commands_ldap.append('distinguished-name' + kwargs['user-group-attribute member'][1])
                    else:
                        pass
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-group-attribute additional-group-match')
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-group-attribute member')
                self.fw._is_key_exist(commands_ldap, kwargs, 'read-from-server display')
                # self.fw._is_key_exist(commands_ldap, kwargs, 'read-from-server auto-configure ')
            if 'novell-edirectory' in kwargs['schema']:
                commands_ldap.append('schema novell-edirectory')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute additional-group-id')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute framed-ip-address')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute group-membership')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute logon-name')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute qualified-logon-name')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute use-additional-group-id')
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-attribute')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-class')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-group-class')
                if 'user-group-attribute member' in kwargs.keys():
                    if 'user-id' in kwargs['user-group-attribute member']:
                        commands_ldap.append('user-id' + kwargs['user-group-attribute member'][1])
                    elif 'distinguished-name' in kwargs['user-group-attribute member']:
                        commands_ldap.append('distinguished-name' + kwargs['user-group-attribute member'][1])
                    else:
                        pass
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-group-attribute additional-group-match')
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-group-attribute member')
                self.fw._is_key_exist(commands_ldap, kwargs, 'read-from-server display')
                # self.fw._is_key_exist(commands_ldap, kwargs, 'read-from-server auto-configure ')
            if 'samba-smb' in kwargs['schema']:
                commands_ldap.append('schema samba-smb')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute additional-group-id')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute framed-ip-address')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute group-membership')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute logon-name')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute qualified-logon-name')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-attribute use-additional-group-id')
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-attribute')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-class')
                self.fw._is_key_exist(commands_ldap, kwargs, 'user-group-class')
                if 'user-group-attribute member' in kwargs.keys():
                    if 'user-id' in kwargs['user-group-attribute member']:
                        commands_ldap.append('user-id' + kwargs['user-group-attribute member'][1])
                    elif 'distinguished-name' in kwargs['user-group-attribute member']:
                        commands_ldap.append('distinguished-name' + kwargs['user-group-attribute member'][1])
                    else:
                        pass
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-group-attribute additional-group-match')
                self.fw._is_key_exist(commands_ldap, kwargs, 'no user-group-attribute member')
                self.fw._is_key_exist(commands_ldap, kwargs, 'read-from-server display')
                # self.fw._is_key_exist(commands_ldap, kwargs, 'read-from-server auto-configure ')

        if 'directory' in kwargs.keys():
            commands_ldap.append('directory')
            self.fw._is_key_exist(commands_ldap, kwargs, 'primary-domain')
            self.fw._is_key_exist(commands_ldap, kwargs, 'users-tree')
            self.fw._is_key_exist(commands_ldap, kwargs, 'no users-tree')
            self.fw._is_key_exist(commands_ldap, kwargs, 'user-groups-tree')
            self.fw._is_key_exist(commands_ldap, kwargs, 'no user-groups-tree')

        commands_ldap.append('commit')
        commands_ldap.append('exit')
        return commands_ldap

    def test_ldap_server(self, **kwargs):
        commands = ['configure', 'user ldap']
        if 'connectivity-bind' in kwargs['test']:
            commands.append('test ' + kwargs['server'] + 'type ' +
                            'connectivity-bind')
        if 'user-authentication' in kwargs['test']:
            commands.append('test ' + kwargs['server'] + ' type ' +
                            'user-authentication ' +
                            kwargs['user'] +
                            ' ' +
                            kwargs['passwd'])
            if 'chap' in kwargs.keys():
                commands.append('test ' + kwargs['server'] + 'type ' +
                                'user-authentication ' +
                                kwargs['user'] +
                                ' ' +
                                kwargs['passwd'] + ' chap'
                                )
            else:
                pass
        for item in ['commit', 'end', 'exit']:
            commands.append(item)
        result = self.fw.do_cli_commands(commands, tag=1)
        return(result[1])

    def del_ldap_servers(self):
        commands = ['configure', 'user ldap', 'no servers']
        for item in ['commit', 'end', 'exit']:
            commands.append(item)
        return self.fw.do_cli_commands(commands)
        
        
class UserPartitioncli:
    '''UserPartitioncli class'''

    def __init__(self, fw):
        self.fw = fw

    def add_authen_partition(self, **kwargs):
        commands = ['configure', 'user partitioning']
        if 'enable' in kwargs.keys():
            if kwargs['enable']:
                commands.append('enable')
                if 'partition' in kwargs.keys():
                    if kwargs['partition']:
                        commands.append('partition ' + kwargs['partition'])
                        commands_pati = self._auth_partition(**kwargs)
                        commands += commands_pati
                    else:
                        logger.error('authen_partition information must be specified')
            elif not kwargs['enable']:
                commands.append('no enable')
            else:
                logger.error('Enable must be open for user partition edit')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_authen_partition(self, **kwargs):
        commands = ['configure', 'user partitioning']
        if 'enable' in kwargs.keys():
            if kwargs['enable']:
                commands.append('enable')
                if 'partition' in kwargs.keys():
                    if kwargs['partition']:
                        commands.append('partition ' + kwargs['partition'])
                        commands_pati = self._auth_partition(**kwargs)
                        commands += commands_pati
                    else:
                        logger.error('authen_partition information must be specified')
            elif not kwargs['enable']:
                commands.append('no enable')
            else:
                logger.error('Enable must be open for user partition edit')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def delete_authen_partition(self, **kwargs):
        commands = ['configure', 'user partitioning']
        if 'enable' in kwargs.keys():
            if kwargs['enable']:
                commands.append('enable')
                self.fw._is_key_exist(commands, kwargs, 'no partition')
                self.fw._is_key_exist(commands, kwargs, 'no partitions')
            elif not kwargs['enable']:
                commands.append('no enable')
            else:
                pass

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def _auth_partition(self, **kwargs):
        commands_pati = []
        self.fw._is_key_exist(commands_pati, kwargs, 'name')
        self.fw._is_key_exist(commands_pati, kwargs, 'parent-partition')
        self.fw._is_key_exist(commands_pati, kwargs, 'domain')
        self.fw._is_key_exist(commands_pati, kwargs, 'no domain')
        self.fw._is_key_exist(commands_pati, kwargs, 'domains')
        self.fw._is_key_exist(commands_pati, kwargs, 'comment')

        return commands_pati

    def add_partition_policy(self, **kwargs):
        commands = ['configure', 'user partitioning']
        if 'enable' in kwargs.keys():
            if kwargs['enable']:
                commands.append('enable')
                if ('policy' in kwargs.keys() and kwargs['policy']):
                        commands_policy = self._part_policy(**kwargs)
                        commands += commands_policy
                else:
                    logger.error('Policy information must be specified')
            elif not kwargs['enable']:
                commands.append('no enable')
            else:
                logger.error('Enable must be open for user partition edit')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_partition_policy(self, **kwargs):
        commands = ['configure', 'user partitioning']
        if 'enable' in kwargs.keys():
            if kwargs['enable']:
                commands.append('enable')
                if ('policy' in kwargs.keys() and kwargs['policy']):
                        commands_policy = self._part_policy(**kwargs)
                        commands += commands_policy
                else:
                    logger.error('Policy information must be specified')
            elif not kwargs['enable']:
                commands.append('no enable')
            else:
                logger.error('Enable must be open for user partition edit')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def delete_part_policy(self, **kwargs):
        commands_policy = ['configure', 'user partitioning']
        self.fw._is_key_exist(commands, kwargs, 'no policies')
        if 'for-console-user' in kwargs.keys():
            _del_policy.append('no policy for-console-user interface console')
        if 'for-remote-user' in kwargs.keys():
            _del_policy.append('no policy for-console-user interface any')
        # if 'interface' in kwargs.keys():

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result



    def _part_policy(self, **kwargs):
        commands_policy = ['configure', 'user partitioning']
        if 'for-console-user' in kwargs.keys():
            commands_policy.append('policy for-console-user interface console')
            self.fw._is_key_exist(commands_policy, kwargs, 'comment')
            self.fw._is_key_exist(commands_policy, kwargs, 'partition')  ##partition is a must parameter
        if 'for-remote-user' in kwargs.keys():
            commands_policy.append('policy for-console-user interface any')
            self.fw._is_key_exist(commands_policy, kwargs, 'comment')
            self.fw._is_key_exist(commands_policy, kwargs, 'partition')  ##partition is a must parameter
        if 'interface_init' in kwargs.keys():   ##interface means local
            commands_policy.append('policy interface ' + kwargs['interface_init'])  ##only X0 and X2
            self.fw._is_key_exist(commands_policy, kwargs, 'comment')
            self.fw._is_key_exist(commands_policy, kwargs, 'interface')
            self.fw._is_key_exist(commands_policy, kwargs, 'zone')
            self.fw._is_key_exist(commands_policy, kwargs, 'partition')  ##partition is a must parameter
            if 'address-object' in kwargs.keys():
                if kwargs['address-object']:
                    commands_policy.append('address-object ' + kwargs['address-object'][0] + ' ' + kwargs['address-object'][1])
                elif not kwargs['address-object']:
                    commands_policy.append('address-object any')
                else:
                    pass
        commands_policy.append('commit')
        commands_policy.append('exit')
        return commands_policy


class UserSSOcli:
    '''UserSSOcli class'''

    def __init__(self, fw):
        self.fw = fw

    def list_sso_cli(self):
        commands = ['configure', 'user sso', 'cli ?', 'end', 'exit']
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result

    def show_sso_setting(self, authtype):
        if authtype == 'sso':
            commands = ['show user sso']
        else:
            commands = ['show user sso '+authtype]
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result
        
    def sso_agent(self, **kwargs):
        commands = ['configure', 'user sso']
        if 'agent' in kwargs.keys():
            commands.append('agent ' + kwargs['agent'])
            self.fw._is_key_exist(commands, kwargs, 'enable')
            self.fw._is_key_exist(commands, kwargs, 'host')
            self.fw._is_key_exist(commands, kwargs, 'port')
            self.fw._is_key_exist(commands, kwargs, 'retries')
            self.fw._is_key_exist(commands, kwargs, 'max-requests')
            self.fw._is_key_exist(commands, kwargs, 'timeout')
            self.fw._is_key_exist(commands, kwargs, 'shared-key')
            commands.append('commit')
            commands.append('exit')
        self.fw._is_key_exist(commands, kwargs, 'method terminal-services-agent')
        self.fw._is_key_exist(commands, kwargs, 'next-agent-on-no-name')
        if 'no block-traffic' in kwargs.keys():
            if kwargs['no block-traffic']:
                commands.append('no block-traffic')
                self.fw._is_key_exist(commands, kwargs, 'including-for-access-rules')
            elif not kwargs['no block-traffic']:
                commands.append('block-traffic')
            else:
                pass
        self.fw._is_key_exist(commands, kwargs, 'windows-service-user-name')
        self.fw._is_key_exist(commands, kwargs, 'no windows-service-user-name')
        
        for command in ['end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def users(self, **kwargs):
        commands = ['configure', 'user sso']
        self.fw._is_key_exist(commands, kwargs, 'local-users-only')
        self.fw._is_key_exist(commands, kwargs, 'non-domain-limited-access')
        self.fw._is_key_exist(commands, kwargs, 'user-group-mechanism')
        self.fw._is_key_exist(commands, kwargs, 'poll rate')
        self.fw._is_key_exist(commands, kwargs, 'poll same-agent')
        self.fw._is_key_exist(commands, kwargs, 'hold-time after-failure')
        self.fw._is_key_exist(commands, kwargs, 'hold-time after-no-user')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def enforcement(self, **kwargs):
        commands = ['configure', 'user sso']
        if 'enforce-on-zone' in kwargs.keys():
            for s in kwargs['enforce-on-zone']:
                commands.append('enforce-on-zone' + ' ' + s)
        if 'no enforce-on-zone' in kwargs.keys():
            for s in kwargs['no enforce-on-zone']:
                commands.append('no enforce-on-zone' + ' ' + s)
        # configure security-service-bypass service
        if 'built-in' in kwargs.keys():
            commands.append('security-service-bypass service built-in ' + kwargs['built-in'])
            if 'type' in kwargs.keys():
                commands.append('type ' + kwargs['type'])
            elif 'type' not in kwargs.keys():
                logger.error('type must be specified')
            else:
                pass
            commands.append('commit')
            commands.append('exit')
        if 'service_group' in kwargs.keys():
            commands.append('security-service-bypass service group ' + kwargs['service_group'])
            if 'type' in kwargs.keys():
                commands.append('type ' + kwargs['type'])
            elif 'type' not in kwargs.keys():
                logger.error('type must be specified')
            else:
                pass
            commands.append('commit')
            commands.append('exit')
        if 'service_name' in kwargs.keys():
            commands.append('security-service-bypass service name ' + kwargs['service_name'])
            if 'type' in kwargs.keys():
                commands.append('type ' + kwargs['type'])
            elif 'type' not in kwargs.keys():
                logger.error('type must be specified')
            else:
                pass
            commands.append('commit')
            commands.append('exit')
        if 'protocol' in kwargs.keys():
            if kwargs['protocol']:
                commands.append('security-service-bypass service protocol ' + kwargs['protocol'][0] + ' ' +
                                kwargs['protocol'][1] + ' ' + kwargs['protocol'][2])
                if 'type' in kwargs.keys():
                    commands.append('type ' + kwargs['type'])
                elif 'type' not in kwargs.keys():
                    logger.error('type must be specified')
                else:
                    pass
            commands.append('commit')
            commands.append('exit')
        if 'no security-service-bypass service' in kwargs.keys():
            if kwargs['no security-service-bypass service']:
                commands.append('no security-service-bypass service ' + kwargs['no security-service-bypass service'][0]
                                + ' ' + kwargs['no security-service-bypass service'][1])
            else:
                logger.error('The sso bypass that need be deleted must be specified')
        # configure security-service-bypass address
        # if 'ipv6' in kwargs.keys():
        if 'host' in kwargs.keys():
            commands.append('security-service-bypass address host ' + kwargs['host'])
            if 'type' in kwargs.keys():
                commands.append('type ' + kwargs['type'])
            elif 'type' not in kwargs.keys():
                logger.error('type must be specified')
            else:
                pass
            commands.append('commit')
            commands.append('exit')
        if 'network' in kwargs.keys():
            commands.append('security-service-bypass address network '
                            + kwargs['network'][0] + ' ' + kwargs['network'][1])
            if 'type' in kwargs.keys():
                commands.append('type ' + kwargs['type'])
            elif 'type' not in kwargs.keys():
                logger.error('type must be specified')
            else:
                pass
            commands.append('commit')
            commands.append('exit')
        if 'range' in kwargs.keys():
            commands.append('security-service-bypass address range '
                            + kwargs['range'][0] + ' ' + kwargs['range'][1])
            if 'type' in kwargs.keys():
                commands.append('type ' + kwargs['type'])
            elif 'type' not in kwargs.keys():
                logger.error('type must be specified')
            else:
                pass
            commands.append('commit')
            commands.append('exit')
        if 'address_group' in kwargs.keys():
            commands.append('security-service-bypass address group ' + kwargs['address_group'])
            if 'type' in kwargs.keys():
                commands.append('type ' + kwargs['type'])
            elif 'type' not in kwargs.keys():
                logger.error('type must be specified')
            else:
                pass
            commands.append('commit')
            commands.append('exit')
        if 'address_name' in kwargs.keys():
            commands.append('security-service-bypass address name ' + kwargs['address_name'])
            if 'type' in kwargs.keys():
                commands.append('type ' + kwargs['type'])
            elif 'type' not in kwargs.keys():
                logger.error('type must be specified')
            else:
                pass
            commands.append('commit')
            commands.append('exit')
        self.fw._is_key_exist(commands, kwargs, 'no security-service-bypass address') 
        self.fw._is_key_exist(commands, kwargs, 'dummy-user')
        self.fw._is_key_exist(commands, kwargs, 'dummy-user name')
        self.fw._is_key_exist(commands, kwargs, 'dummy-user timeout')
        self.fw._is_key_exist(commands, kwargs, 'no dummy-user')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def terminalservices(self, **kwargs):
        commands = ['configure', 'user sso']
        self.fw._is_key_exist(commands, kwargs, 'tsa-services-bypass')
        self.fw._is_key_exist(commands, kwargs, 'method terminal-services-agent')
        if 'terminal-services-agent' in kwargs.keys():
            commands.append('terminal-services-agent' + ' ' + kwargs['terminal-services-agent'])
            self.fw._is_key_exist(commands, kwargs, 'host')
            self.fw._is_key_exist(commands, kwargs, 'port')
            self.fw._is_key_exist(commands, kwargs, 'enable')
            self.fw._is_key_exist(commands, kwargs, 'shared-key')
            commands.append('commit')
            commands.append('exit')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def radiusaccounting(self, **kwargs):
        commands = ['configure', 'user sso']
        self.fw._is_key_exist(commands, kwargs, 'no radius-accounting-client')
        self.fw._is_key_exist(commands, kwargs, 'no radius-accounting-clients')
        if 'radius-accounting-client' in kwargs.keys():
            commands.append('radius-accounting-client' + ' ' + kwargs['radius-accounting-client'])
            self.fw._is_key_exist(commands, kwargs, 'host')
            self.fw._is_key_exist(commands, kwargs, 'log-user-out')
            self.fw._is_key_exist(commands, kwargs, 'user-name-format')
            self.fw._is_key_exist(commands, kwargs, 'shared-secret')
            self.fw._is_key_exist(commands, kwargs, 'proxy-forward timeout')
            self.fw._is_key_exist(commands, kwargs, 'proxy-forward retries')
            self.fw._is_key_exist(commands, kwargs, 'no server')
            if 'server' in kwargs.keys():
                commands.append('server ' + kwargs['server'][0] + ' ' + kwargs['server'][1] + ' '
                                + 'port ' + kwargs['server'][2] + ' ' + 'shared-secret ' + kwargs['server'][3])
            else:
                logger.error('Server information must be specified')
            commands.append('commit')
            commands.append('exit')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def test(self, **kwargs):
        commands = ['configure', 'user sso']
        if 'method' in kwargs.keys():
            commands.append('method terminal-services-agent')
            commands.append('commit')
            if 'agent' in kwargs.keys():
                if 'user-ip'in kwargs['agent']:
                    commands.append('test agent ' + kwargs['agent'][0] + ' ' + 'user-ip ' + kwargs['agent'][2])
                elif 'user-ip'not in kwargs['agent']:
                    commands.append('test agent ' + kwargs['agent'])
                else:
                    logger.error('Agent information must be specified')
            if 'user-ip' in kwargs.keys():
                if kwargs['user-ip']:
                    commands.append('test user-ip ' + kwargs['user-ip'])
                else:
                    logger.error('User Ip that need to be test must be specified')
            if 'terminal-services-agent' in kwargs.keys():
                if kwargs['terminal-services-agent']:
                    commands.append('test terminal-services-agent ' + kwargs['terminal-services-agent'])
                else:
                    logger.error('terminal-services-agent that need to be test must be specified')

        for command in ['end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands, timeout=180)
        return result
        
    def del_sso_agents(self):
        commands = ['configure', 'user sso', 'no agents']
        for item in ['commit', 'end', 'exit']:
            commands.append(item)
        return self.fw.do_cli_commands(commands)
        

class Userlocalcli:
    """Userlocalcli class"""

    def __init__(self, fw):
        self.fw = fw

    def show_local_setting(self, authtype):
        commands = ['show user local '+authtype]
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result
        
    def local_settings(self, **kwargs):
        commands = ['configure', 'user local']
        self.fw._is_key_exist(commands, kwargs, 'apply-password-constraints')
        self.fw._is_key_exist(commands, kwargs, 'prune-on-expiry')
        self.fw._is_key_exist(commands, kwargs, 'refresh-ldap-server')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result
    
    def add_local_user(self, **kwargs):
        commands = ['configure', 'user local']
        if 'user' in kwargs.keys():
            if ('domain' in kwargs.keys() and kwargs['user'] and kwargs['domain']):
                commands.append('user ' + kwargs['user'] + ' ' + 'domain ' + kwargs['domain'])
                commands_add_user = self._local_user(**kwargs)
                commands += commands_add_user
            elif ('domain' not in kwargs.keys() and kwargs['user']):
                commands.append('user ' + kwargs['user'])
                commands_add_user = self._local_user(**kwargs)
                commands += commands_add_user  
            else:
                logger.error('User information that need be added must be specified')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_local_user(self, **kwargs):
        commands = ['configure', 'user local']
        if 'user' in kwargs.keys():
            if ('domain' in kwargs.keys() and kwargs['user'] and kwargs['domain']):
                commands.append('user ' + kwargs['user'] + ' ' + 'domain ' + kwargs['domain'])
                self.fw._is_key_exist(commands, kwargs, 'no bookmark')
                self.fw._is_key_exist(commands, kwargs, 'no bookmarks')
                if 'name' in kwargs.keys():
                    if kwargs['name']:
                        commands.append('name ' + kwargs['name'])
                    else:
                        logger.error('name information must be specified')
                    commands.append('commit')
                if 'changedomain' in kwargs.keys():
                    if kwargs['changedomain']:
                        commands.append('domain ' + kwargs['changedomain'])
                    else:
                        logger.error('domain information must be specified')
                    commands.append('commit')
                commands_edit_user = self._local_user(**kwargs)
                commands += commands_edit_user
            elif ('domain' not in kwargs.keys() and kwargs['user']):
                commands.append('user ' + kwargs['user'])
                self.fw._is_key_exist(commands, kwargs, 'no bookmark')
                self.fw._is_key_exist(commands, kwargs, 'no bookmarks')
                if 'name' in kwargs.keys():
                    if kwargs['name']:
                        commands.append('name ' + kwargs['name'])
                    else:
                        logger.error('name information must be specified')
                    commands.append('commit')
                if 'changedomain' in kwargs.keys():
                    if kwargs['changedomain']:
                        commands.append('domain ' + kwargs['changedomain'])
                    else:
                        logger.error('domain information must be specified')
                    commands.append('commit')
                commands_edit_user = self._local_user(**kwargs)
                commands += commands_edit_user  
            else :
                logger.error('User information that need be edited must be specified')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def delete_local_user(self, **kwargs):
        commands = ['configure', 'user local']
        if 'no user' in kwargs.keys():
            if ('domain' in kwargs.keys() and kwargs['domain'] and kwargs['no user']):
                commands.append('no user ' + kwargs['no user'] + ' ' + 'domain ' + kwargs['domain'])
            elif ('domain' not in kwargs.keys() and kwargs['no user']):
                commands.append('no user ' + kwargs['no user'])
            else:
                logger.error('The user information that need be deleted must be specified')
        self.fw._is_key_exist(commands, kwargs, 'no users')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result
        
    def del_local_users(self):
        commands = ['configure', 'user local', 'no users']
        for item in ['commit', 'end', 'exit']:
            commands.append(item)
        return self.fw.do_cli_commands(commands)

    def _local_user(self, **kwargs):
        commands_local_user = []
        self.fw._is_key_exist(commands_local_user, kwargs, 'password')
        self.fw._is_key_exist(commands_local_user, kwargs, 'expiration')
        self.fw._is_key_exist(commands_local_user, kwargs, 'force-password-change')
        self.fw._is_key_exist(commands_local_user, kwargs, 'one-time-password')
        self.fw._is_key_exist(commands_local_user, kwargs, 'email-address')
        self.fw._is_key_exist(commands_local_user, kwargs, 'comment')
        self.fw._is_key_exist(commands_local_user, kwargs, 'member-of')
        self.fw._is_key_exist(commands_local_user, kwargs, 'no member-of')
        self.fw._is_key_exist(commands_local_user, kwargs, 'uuid')
        self.fw._is_key_exist(commands_local_user, kwargs, 'prune-on-expiry')
        self.fw._is_key_exist(commands_local_user, kwargs, 'unbind-totp-key')
        self.fw._is_key_exist(commands_local_user, kwargs, 'quota-cycle')
        if 'receive' in kwargs.keys():
            if kwargs['receive']:
                commands_local_user.append('limit receive ' + kwargs['receive'])
            elif not kwargs['receive']:
                commands_local_user.append('no limit receive')
            else:
                logger.error('Limit receive must be specified')
        if 'transmit' in kwargs.keys():
            if kwargs['transmit']:
                commands_local_user.append('limit transmit ' + kwargs['transmit'])
            elif not kwargs['transmit']:
                commands_local_user.append('no limit transmit')
            else:
                logger.error('Limit transmit must be specified')
        if ('account-lifetime' in kwargs.keys() and kwargs['account-lifetime']):
            commands_local_user.append('account-lifetime ' + kwargs['account-lifetime'][0] + ' ' + kwargs['account-lifetime'][1])
        if ('session-lifetime' in kwargs.keys() and kwargs['session-lifetime']):
            commands_local_user.append('session-lifetime ' + kwargs['session-lifetime'][0] + ' ' + kwargs['session-lifetime'][1])
        if 'vpn-client-access' in kwargs.keys():
            if kwargs['vpn-client-access']:
                commands_local_user.append('vpn-client-access name ' + kwargs['vpn-client-access'])
            elif not kwargs['vpn-client-access']:
                commands_local_user.append('no vpn-client-access name ' + kwargs['vpn-client-access'])
            else:
                pass
        if 'bookmark' in kwargs.keys():
            if kwargs['bookmark']:
                commands_user_bm = self._user_book_mark(**kwargs)
                commands_local_user += commands_user_bm
            else:
                logger.error('bookmark information is needed')
        commands_local_user.append('commit')
        commands_local_user.append('exit')

        return commands_local_user

    def _user_book_mark(self, **kwargs):
        commands_user_bm = ['bookmark ' + kwargs['bookmark']]
        if 'bmuserhost' in kwargs.keys():
            commands_user_bm.append('host ' + kwargs['bmuserhost'])
        if 'bmusername' in kwargs.keys():
            commands_user_bm.append('name ' + kwargs['bmusername'])
        if 'bmuserservice' in kwargs.keys():
            if 'rdp' in kwargs['bmuserservice']:
                commands_user_bm_rdp_service = self._edit_user_rdp_service(**kwargs)
                commands_user_bm += commands_user_bm_rdp_service
            if 'sshv2' in kwargs['bmuserservice']:
                commands_user_bm.append('service sshv2')
                if 'host-key' in kwargs.keys():
                    if kwargs['host-key']:
                        commands_user_bm.append('automatic-accept-host-key')
                    else:
                        commands_user_bm.append('no automatic-accept-host-key')
                if 'display-on-mobilessh' in kwargs.keys():
                    if kwargs['display-on-mobilessh']:
                        commands_user_bm.append('display-on-mobile')
                    else:
                        commands_user_bm.append('no display-on-mobile')
                commands_user_bm.append('commit')
                commands_user_bm.append('exit')
            if 'telnet' in kwargs['bmuserservice']:
                commands_user_bm.append('service telnet')
                if 'display-on-mobiletel' in kwargs.keys():
                    if kwargs['display-on-mobiletel']:
                        commands_user_bm.append('display-on-mobile')
                    else:
                        commands_user_bm.append('no display-on-mobile')
                commands_user_bm.append('commit')
                commands_user_bm.append('exit')
            if 'vnc' in kwargs['bmuserservice']:
                commands_user_bm.append('service vnc')
                if 'display-on-mobilevnc' in kwargs.keys():
                    if kwargs['display-on-mobilevnc']:
                        commands_user_bm.append('display-on-mobile')
                    else:
                        commands_user_bm.append('no display-on-mobile')
                if 'share-desktopvnc' in kwargs.keys():
                    if kwargs['share-desktopvnc']:
                        commands_user_bm.append('share-desktop')
                    else:
                        commands_user_bm.append('no share-desktop')
                if 'view-onlyvnc' in kwargs.keys():
                    if kwargs['view-onlyvnc']:
                        commands_user_bm.append('view-only')
                    else:
                        commands_user_bm.append('no view-only')
                commands_user_bm.append('commit')
                commands_user_bm.append('exit')
        commands_user_bm.append('commit')
        commands_user_bm.append('exit')

        return commands_user_bm

    def _edit_user_rdp_service(self, **kwargs):
        commands_user_bm_rdp_service = ['service rdp']
        self.fw._is_key_exist(commands_user_bm_rdp_service, kwargs, 'colors')
        self.fw._is_key_exist(commands_user_bm_rdp_service, kwargs, 'screen-size')
        self.fw._is_key_exist(commands_user_bm_rdp_service, kwargs, 'application-path')
        self.fw._is_key_exist(commands_user_bm_rdp_service, kwargs, 'start-in-folder')
        self.fw._is_key_exist(commands_user_bm_rdp_service, kwargs, 'redirect-clipboard')
        self.fw._is_key_exist(commands_user_bm_rdp_service, kwargs, 'redirect-audio')
        self.fw._is_key_exist(commands_user_bm_rdp_service, kwargs, 'auto-reconnection')
        self.fw._is_key_exist(commands_user_bm_rdp_service, kwargs, 'desktop-background')
        self.fw._is_key_exist(commands_user_bm_rdp_service, kwargs, 'window-drag')
        self.fw._is_key_exist(commands_user_bm_rdp_service, kwargs, 'animation')
        self.fw._is_key_exist(commands_user_bm_rdp_service, kwargs, 'automatic-login ssl-vpn')
        if ('custom' in kwargs.keys() and kwargs['custom']):
            if 'domain' in kwargs['custom']:
                commands_user_bm_rdp_service.append('automatic-login custom name '
                 + kwargs['custom'][1] + ' ' + 'password ' +
                kwargs['custom'][3] + ' ' + 'domain ' + kwargs['custom'][5])
            elif 'domain' not in kwargs['custom']:
                commands_user_bm_rdp_service.append('automatic-login custom name '
                 + kwargs['custom'][1] + ' ' + 'password ' + kwargs['custom'][3])
            else:
                logger.error('custom information must be specified')
        self.fw._is_key_exist(commands_user_bm_rdp_service, kwargs, 'no automatic-login')
        self.fw._is_key_exist(commands_user_bm_rdp_service, kwargs, 'no automatic-login custom')

        commands_user_bm_rdp_service.append('commit')
        commands_user_bm_rdp_service.append('exit')
        return commands_user_bm_rdp_service

    def add_local_group(self, **kwargs):
        commands = ['configure', 'user local']
        if 'group' in kwargs.keys():
            if ('domain' in kwargs.keys() and kwargs['domain'] and kwargs['group']):
                commands.append('group ' + kwargs['group'] + ' ' + 'domain ' + kwargs['domain'])
                commands_local_group = self._local_group(**kwargs)
                commands += commands_local_group
            elif ('domain' not in kwargs.keys() and kwargs['group']):
                commands.append('group ' + kwargs['group'])
                commands_local_group = self._local_group(**kwargs)
                commands += commands_local_group
            else:
                logger.error('Group information that need be added must be specified')
                
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result
    
    def edit_local_group(self, **kwargs):
        commands = ['configure', 'user local']
        if 'group' in kwargs.keys():
            if ('domain' in kwargs.keys() and kwargs['domain'] and kwargs['group']):
                commands.append('group ' + kwargs['group'] + ' ' + 'domain ' + kwargs['domain'])
                self.fw._is_key_exist(commands, kwargs, 'no bookmark')
                self.fw._is_key_exist(commands, kwargs, 'no bookmarks')
                if 'name' in kwargs.keys():
                    if kwargs['name']:
                        commands.append('name ' + kwargs['name'])
                    else:
                        logger.error('name information must be specified')
                    commands.append('commit')
                if 'changedomain' in kwargs.keys():
                    if kwargs['changedomain']:
                        commands.append('domain ' + kwargs['changedomain'])
                    else:
                        logger.error('domain information must be specified')
                    commands.append('commit')
                commands_edit_group = self._local_group(**kwargs)
                commands +=  commands_edit_group
            elif ('domain' not in kwargs.keys() and kwargs['group']):
                commands.append('group ' + kwargs['group'])
                self.fw._is_key_exist(commands, kwargs, 'no bookmark')
                self.fw._is_key_exist(commands, kwargs, 'no bookmarks')
                if 'name' in kwargs.keys():
                    if kwargs['name']:
                        commands.append('name ' + kwargs['name'])
                    else:
                        logger.error('name information must be specified')
                    commands.append('commit')
                if 'changedomain' in kwargs.keys():
                    if kwargs['changedomain']:
                        commands.append('domain ' + kwargs['changedomain'])
                    else:
                        logger.error('domain information must be specified')
                    commands.append('commit')
                commands_edit_group = self._local_group(**kwargs)
                commands +=  commands_edit_group
            else:
                logger.error('Group information that need be edited must be specified')
                
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result
        
    def delete_local_group(self, **kwargs):
        commands = ['configure', 'user local']
        if 'no group' in kwargs.keys():
            if ('domain' in kwargs.keys() and kwargs['domain'] and kwargs['no group']):
                commands.append('no group ' + kwargs['no group'] + ' ' + 'domain ' + kwargs['domain'])
            elif ('domain' not in kwargs.keys() and kwargs['no group']):
                commands.append('no group ' + kwargs['no group'])
            else:
                logger.error('The group information that need be deleted must be specified')
        self.fw._is_key_exist(commands, kwargs, 'no groups')
        
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result
    
    def _local_group(self, **kwargs):
        commands_local_group = []
        self.fw._is_key_exist(commands_local_group, kwargs, 'comment')
        self.fw._is_key_exist(commands_local_group, kwargs, 'one-time-password')
        self.fw._is_key_exist(commands_local_group, kwargs, 'uuid')
        self.fw._is_key_exist(commands_local_group, kwargs, 'member')
        self.fw._is_key_exist(commands_local_group, kwargs, 'no member')
        if 'vpn-client-access' in kwargs.keys():
            if kwargs['vpn-client-access']:
                commands_local_group.append('vpn-client-access name ' + kwargs['vpn-client-access'])
            elif not kwargs['vpn-client-access']:
                commands_local_group.append('no vpn-client-access name ' + kwargs['vpn-client-access'])
            else:
                pass
        if 'ldap-location' in kwargs.keys():
            if kwargs['ldap-location']:
                commands_local_group.append('ldap-location ' + kwargs['ldap-location'][0])
                if 'at' in kwargs['ldap-location']:
                    commands_local_group.append('memberships-by-ldap-location at')
                elif 'under' in kwargs['ldap-location']:
                    commands_local_group.append('memberships-by-ldap-location under-or-at')
                else:
                    commands_local_group.append('no memberships-by-ldap-location')
            else:
                commands_local_group.append('no ldap-location')       
        if 'bookmark' in kwargs.keys():
            if kwargs['bookmark']:
                commands_group_bm = self._group_book_mark(**kwargs) 
                commands_local_group += commands_group_bm 
            else:
                logger.error('bookmark information is needed')
        commands_local_group.append('commit')
        commands_local_group.append('exit') 

        return commands_local_group

    def _group_book_mark(self, **kwargs):
        commands_group_bm = ['bookmark ' + kwargs['bookmark']]
        if 'bmgrouphost' in kwargs.keys():
            commands_group_bm.append('host ' + kwargs['bmgrouphost'])
        if 'bmgroupname' in kwargs.keys():
            commands_group_bm.append('name ' + kwargs['bmgroupname'])
        if 'bmgroupservice' in kwargs.keys():
            if 'rdp' in kwargs['bmgroupservice']:
                commands_group_bm_rdp_service = self._edit_group_rdp_service(**kwargs)
                commands_group_bm += commands_group_bm_rdp_service
            if 'sshv2' in kwargs['bmgroupservice']:
                commands_group_bm.append('service sshv2')
                if 'host-key' in kwargs.keys():
                    if kwargs['host-key']:
                        commands_group_bm.append('automatic-accept-host-key')
                    else:
                        commands_group_bm.append('no automatic-accept-host-key')
                if 'display-on-mobilessh' in kwargs.keys():
                    if kwargs['display-on-mobilessh']:
                        commands_group_bm.append('display-on-mobile')
                    else:
                        commands_group_bm.append('no display-on-mobile')
                commands_group_bm.append('commit')
                commands_group_bm.append('exit')
            if 'telnet' in kwargs['bmgroupservice']:
                commands_group_bm.append('service telnet')
                if 'display-on-mobiletel' in kwargs.keys():
                    if kwargs['display-on-mobiletel']:
                        commands_group_bm.append('display-on-mobile')
                    else:
                        commands_group_bm.append('no display-on-mobile')
                commands_group_bm.append('commit')
                commands_group_bm.append('exit')
            if 'vnc' in kwargs['bmgroupservice']:
                commands_group_bm.append('service vnc')
                if 'display-on-mobilevnc' in kwargs.keys():
                    if kwargs['display-on-mobilevnc']:
                        commands_group_bm.append('display-on-mobile')
                    else:
                        commands_group_bm.append('no display-on-mobile')
                if 'share-desktopvnc' in kwargs.keys():
                    if kwargs['share-desktopvnc']:
                        commands_group_bm.append('share-desktop')
                    else:
                        commands_group_bm.append('no share-desktop')
                if 'view-onlyvnc' in kwargs.keys():
                    if kwargs['view-onlyvnc']:
                        commands_group_bm.append('view-only')
                    else:
                        commands_group_bm.append('no view-only')
                commands_group_bm.append('commit')
                commands_group_bm.append('exit')
        commands_group_bm.append('commit')
        commands_group_bm.append('exit')
        return commands_group_bm

    def _edit_group_rdp_service(self, **kwargs):
        commands_group_bm_rdp_service = ['service rdp']
        self.fw._is_key_exist(commands_group_bm_rdp_service, kwargs, 'colors')
        self.fw._is_key_exist(commands_group_bm_rdp_service, kwargs, 'screen-size')
        self.fw._is_key_exist(commands_group_bm_rdp_service, kwargs, 'application-path')
        self.fw._is_key_exist(commands_group_bm_rdp_service, kwargs, 'start-in-folder')
        self.fw._is_key_exist(commands_group_bm_rdp_service, kwargs, 'redirect-clipboard')
        self.fw._is_key_exist(commands_group_bm_rdp_service, kwargs, 'redirect-audio')
        self.fw._is_key_exist(commands_group_bm_rdp_service, kwargs, 'auto-reconnection')
        self.fw._is_key_exist(commands_group_bm_rdp_service, kwargs, 'desktop-background')
        self.fw._is_key_exist(commands_group_bm_rdp_service, kwargs, 'window-drag')
        self.fw._is_key_exist(commands_group_bm_rdp_service, kwargs, 'animation')
        self.fw._is_key_exist(commands_group_bm_rdp_service, kwargs, 'automatic-login ssl-vpn')
        if ('custom' in kwargs.keys() and kwargs['custom']):
            if 'domain' in kwargs['custom']:
                commands_group_bm_rdp_service.append('automatic-login custom name '
                                                    + kwargs['custom'][1] + ' ' + 'password ' +
                                                    kwargs['custom'][3] + ' ' + 'domain ' + kwargs['custom'][5])
            elif 'domain' not in kwargs['custom']:
                commands_group_bm_rdp_service.append('automatic-login custom name '
                                                    + kwargs['custom'][1] + ' ' + 'password ' + kwargs['custom'][3])
            else:
                logger.error('custom information must be specified')
        self.fw._is_key_exist(commands_group_bm_rdp_service, kwargs, 'no automatic-login')
        self.fw._is_key_exist(commands_group_bm_rdp_service, kwargs, 'no automatic-login custom')

        commands_group_bm_rdp_service.append('commit')
        commands_group_bm_rdp_service.append('exit')
        return commands_group_bm_rdp_service


class GuestServicecli:
    '''GuestServicecli class'''

    def __init__(self, fw):
        self.fw = fw

    def show_profile(self, name=None):
        commands = []
        if name:
            command = 'show user guest profile ' + name
        else:
            command = 'show user guest profiles'
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def add_guest_profile(self, **kwargs):
        commands = ['configure', 'user guest']
        self.fw._is_key_exist(commands, kwargs, 'show-guest-status-window')
        if 'profile' in kwargs.keys():
            if kwargs['profile']:
                commands.append('profile ' + kwargs['profile'])
                add_guest_profile = self._guest_profile(**kwargs)
                commands += add_guest_profile
            else:
                return False

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_guest_profile(self, **kwargs):
        commands = ['configure', 'user guest']
        self.fw._is_key_exist(commands, kwargs, 'show-guest-status-window')
        if 'profile' in kwargs.keys():
            if kwargs['profile']:
                commands.append('profile ' + kwargs['profile'])
                edit_guest_profile = self._guest_profile(**kwargs)
                commands += edit_guest_profile
            else:
                return False

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def delete_guest_profile(self, **kwargs):
        commands = ['configure', 'user guest']
        self.fw._is_key_exist(commands, kwargs, 'no profile')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def _guest_profile(self, **kwargs):
        guest_profile = []
        self.fw._is_key_exist(guest_profile, kwargs, 'activate-on-login')
        self.fw._is_key_exist(guest_profile, kwargs, 'comment')
        self.fw._is_key_exist(guest_profile, kwargs, 'limit receive')
        self.fw._is_key_exist(guest_profile, kwargs, 'limit transmit')
        self.fw._is_key_exist(guest_profile, kwargs, 'enable')
        self.fw._is_key_exist(guest_profile, kwargs, 'name')
        self.fw._is_key_exist(guest_profile, kwargs, 'generate')
        self.fw._is_key_exist(guest_profile, kwargs, 'no generate')
        self.fw._is_key_exist(guest_profile, kwargs, 'login-uniqueness')
        self.fw._is_key_exist(guest_profile, kwargs, 'name-prefix')
        self.fw._is_key_exist(guest_profile, kwargs, 'prune-on-expiry')
        self.fw._is_key_exist(guest_profile, kwargs, 'quota-cycle')
        if 'session-lifetime' in kwargs.keys():
            if kwargs['session-lifetime']:
                guest_profile.append('session-lifetime ' + kwargs['session-lifetime'][0] + ' ' + kwargs['session-lifetime'][1])
            else:
                logger.error('Profile session life must be specified')
        if 'account-lifetime' in kwargs.keys():
            if kwargs['account-lifetime']:
                guest_profile.append('account-lifetime ' + kwargs['account-lifetime'][0] + ' ' + kwargs['account-lifetime'][1])
            else:
                logger.error('Profile account life must be specified')
        if 'idle-timeout' in kwargs.keys():
            if kwargs['idle-timeout']:
                guest_profile.append('idle-timeout ' + kwargs['idle-timeout'][0] + ' ' + kwargs['idle-timeout'][1])
            else:
                logger.error('Profile idle-timeout must be specified')

        return guest_profile


class GuestAccountcli:
    '''GuestAccountcli class'''

    def __init__(self, fw):
        self.fw = fw

    def show_user_account(self, name=None):
        commands = []
        if name:
            command = 'show user guest user ' + name
        else:
            command = 'show user guest users'
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def generate_guest_account(self, **kwargs):
        commands = ['configure', 'user guest']
        if 'generate' in kwargs.keys():
            if 'profile' in kwargs.keys() and 'number' in kwargs.keys():
                commands.append('generate ' + kwargs['number'] + ' profile' + kwargs['profile'] + 'hide-password')
            else:
                logger.error('To provide information to generate some guest acconuts automatically')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def add_guest_account(self, **kwargs):
        commands = ['configure', 'user guest']
        if 'user' in kwargs.keys():
            if (kwargs['user'] and 'password' in kwargs.keys() and 'hide-password' in kwargs.keys()):
                commands.append('user ' + kwargs['user'] + ' ' + 'password ' + kwargs['password'] + ' hide-password')
                add_guest_account = self._guest_account(**kwargs)
                commands += add_guest_account
            elif (kwargs['user'] and 'password' in kwargs.keys()):
                commands.append('user ' + kwargs['user'] + ' ' + 'password ' + kwargs['password'])
                add_guest_account = self._guest_account(**kwargs)
                commands += add_guest_account
            elif kwargs['user']:
                commands.append('user ' + kwargs['user'])
                add_guest_account = self._guest_account(**kwargs)
                commands += add_guest_account
            else:
                return False

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_guest_account(self, **kwargs):
        commands = ['configure', 'user guest']
        if 'user' in kwargs.keys():
            if (kwargs['user'] and 'password' in kwargs.keys() and 'hide-password' in kwargs.keys()):
                commands.append('user ' + kwargs['user'] + ' ' + 'password ' + kwargs['password'] + ' hide-password')
                add_guest_account = self._guest_account(**kwargs)
                commands += add_guest_account
            elif (kwargs['user'] and 'password' in kwargs.keys()):
                commands.append('user ' + kwargs['user'] + ' ' + 'password ' + kwargs['password'])
                add_guest_account = self._guest_account(**kwargs)
                commands += add_guest_account
            elif kwargs['user']:
                commands.append('user ' + kwargs['user'])
                add_guest_account = self._guest_account(**kwargs)
                commands += add_guest_account
            else:
                return False

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def delete_guest_account(self, **kwargs):
        commands = ['configure', 'user guest']
        self.fw._is_key_exist(commands, kwargs, 'no user')
        self.fw._is_key_exist(commands, kwargs, 'no users')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def _guest_account(self, **kwargs):
        guest_account = []
        self.fw._is_key_exist(guest_account, kwargs, 'activate-on-login')
        self.fw._is_key_exist(guest_account, kwargs, 'comment')
        self.fw._is_key_exist(guest_account, kwargs, 'name')
        self.fw._is_key_exist(guest_account, kwargs, 'limit receive')
        self.fw._is_key_exist(guest_account, kwargs, 'limit transmit')
        self.fw._is_key_exist(guest_account, kwargs, 'enable')
        self.fw._is_key_exist(guest_account, kwargs, 'password')
        self.fw._is_key_exist(guest_account, kwargs, 'uuid')
        self.fw._is_key_exist(guest_account, kwargs, 'generate')
        self.fw._is_key_exist(guest_account, kwargs, 'no generate')
        self.fw._is_key_exist(guest_account, kwargs, 'login-uniqueness')
        self.fw._is_key_exist(guest_account, kwargs, 'prune-on-expiry')
        self.fw._is_key_exist(guest_account, kwargs, 'quota-cycle')
        if 'session-lifetime' in kwargs.keys():
            if kwargs['session-lifetime']:
                guest_account.append(
                    'session-lifetime ' + kwargs['session-lifetime'][0] + ' ' + kwargs['session-lifetime'][1])
            else:
                logger.error('Account session life must be specified')
        if 'account-lifetime' in kwargs.keys():
            if kwargs['account-lifetime']:
                guest_account.append(
                    'account-lifetime ' + kwargs['account-lifetime'][0] + ' ' + kwargs['account-lifetime'][1])
            else:
                logger.error('Account account life must be specified')
        if 'idle-timeout' in kwargs.keys():
            if kwargs['idle-timeout']:
                guest_account.append('idle-timeout ' + kwargs['idle-timeout'][0] + ' ' + kwargs['idle-timeout'][1])
            else:
                logger.error('Account idle-timeout must be specified')
        if 'profile' in kwargs.keys():
            if ('hide-password' in kwargs.keys() and kwargs['profile']):
                guest_account.append('profile ' + kwargs['profile'] + ' hide-password')
            elif kwargs['profile']:
                guest_account.append('profile ' + kwargs['profile'])
            else:
                logger.error('Profile of account must be specified')

        return guest_account


class UserAuthCli:
    """UserAuthCli class"""
    def __init__(self, fw):
        self.fw = fw

    def auth_cli3(self, **kwargs):
        commands = ['configure', 'user authentication']
        if 'initcmds'in kwargs.keys():
            for initcmd in kwargs['initcmds']:
                commands.append(initcmd)
        if 'acceptable-use-policy' in kwargs.keys():
            commands.append('acceptable-use-policy')
            if 'window-size' in kwargs.keys():
                if kwargs['window-size']  and len(kwargs['window-size']) == 2:
                    commands.append('window-size ' + kwargs['window-size'][0] + ' ' + kwargs['window-size'][1])
                else:
                    logger.error('Windows size must be specified  as two params.')
                    return False
            self.fw._is_key_exist(commands, kwargs, 'scroll-bars')
            if 'aup-on-zones' in kwargs.keys():
                if isinstance(kwargs['aup-on-zones'],list):
                    for s in kwargs['aup-on-zones']:
                        commands.append('aup-on-zones' + ' ' + s)
                else:
                    commands.append('aup-on-zones' + ' ' + kwargs['aup-on-zones'])
            if 'no aup-on-zones' in kwargs.keys():
                if isinstance(kwargs['no aup-on-zones'], list):
                    for s in kwargs['no aup-on-zones']:
                        commands.append('no aup-on-zones' + ' ' + s)
                else:
                    commands.append('no aup-on-zones' + ' ' + kwargs['no aup-on-zones'])
            self.fw._is_key_exist(commands, kwargs, 'content')
            commands.append('commit')
            commands.append('exit')
        self.fw._is_key_exist(commands, kwargs, 'auth-page-timeout')
        self.fw._is_key_exist(commands, kwargs, 'case-sensitive-names')
        self.fw._is_key_exist(commands, kwargs, 'disconnected-user-detect')
        self.fw._is_key_exist(commands, kwargs, 'http-redirect-after-login')
        self.fw._is_key_exist(commands, kwargs, 'inactivity-timeout')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def ldap_cli3(self, **kwargs):
        commands = ['configure', 'user ldap']
        if 'initcmds'in kwargs.keys():
            for initcmd in kwargs['initcmds']:
                commands.append(initcmd)
        if 'server' in kwargs.keys():
            commands.append('server '+kwargs['server'])
            if 'primary-domain' in kwargs.keys():
                for command in ['directory', 'primary-domain '+kwargs['primary-domain'], 'exit']:
                    commands.append(command)
            if 'operation-timeout' in kwargs.keys():
                commands.append('timeout operation '+kwargs['operation-timeout'])
            if 'schema' in kwargs.keys():
                commands.append('schema '+kwargs['schema'])
                commands.append('exit')
            for command in ['commit', 'exit']:
                commands.append(command)
        if 'relay' in kwargs.keys():
            for command in ['relay', 'enable', 'exit']:
                commands.append(command)
        self.fw._is_key_exist(commands, kwargs, 'default-user-group')
        self.fw._is_key_exist(commands, kwargs, 'local-tls-certificate')
        self.fw._is_key_exist(commands, kwargs, 'local-users-only')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def local_cli3(self, **kwargs):
        commands = ['configure', 'user local']
        if 'initcmds'in kwargs.keys():
            for initcmd in kwargs['initcmds']:
                commands.append(initcmd)
        if 'groupmember' in kwargs.keys():
            for command in ['group Limited\ Administrators', 'member '+kwargs['groupmember'], 'exit']:
                commands.append(command)

        self.fw._is_key_exist(commands, kwargs, 'apply-password-constraints')
        self.fw._is_key_exist(commands, kwargs, 'prune-on-expiry')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def radius_cli3(self, **kwargs):
        commands = ['configure', 'user radius']
        if 'initcmds'in kwargs.keys():
            for initcmd in kwargs['initcmds']:
                commands.append(initcmd)
        if 'serverhost' in kwargs.keys():
            for command in ['server '+ kwargs['serverhost'], 'shared-secret password', 'enable', 'port 2222', 'exit']:
                commands.append(command)
        if 'user-group-mechanism' in kwargs.keys():
            for command in ['user-group-mechanism radius-attribute '+ kwargs['user-group-mechanism']]:
                commands.append(command)
        self.fw._is_key_exist(commands, kwargs, 'default-user-group')
        self.fw._is_key_exist(commands, kwargs, 'local-users-only')
        self.fw._is_key_exist(commands, kwargs, 'retries')
        self.fw._is_key_exist(commands, kwargs, 'timeout')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def sso_cli3(self, **kwargs):
        commands = ['configure', 'user sso']
        if 'initcmds'in kwargs.keys():
            for initcmd in kwargs['initcmds']:
                commands.append(initcmd)

        if 'agent' in kwargs.keys():
            for command in ['agent '+ kwargs['agent'], 'shared-key 123456', 'enable', 'port 2222', 'commit', 'exit']:
                commands.append(command)

        if 'security-services-bypass-ip' in kwargs.keys():
            if security_services_dict['security-services-bypass-ip'] == 'no':
                commands.append('no security-service-bypass address name X1\ IP')
            else:
                for command in ['security-service-bypass address name X1\ IP', 'type '+ kwargs['security-services-bypass-ip']]:
                    commands.append(command)
        if 'security-services-bypass-dns' in kwargs.keys():
            for command in ['security-service-bypass service name DNS', 'type '+ kwargs['security-services-bypass-dns'], 'commit', 'exit']:
                commands.append(command)
        if 'terminal-services-agent' in kwargs.keys():
            for command in ['terminal-services-agent '+ kwargs['terminal-services-agent'], 'enable', 'port 8888', 'shared-key 123456', 'commit', 'exit']:
                commands.append(command)
        if 'hold-time' in kwargs.keys():
            commands.append('hold-time '+ kwargs['hold-time'])

        self.fw._is_key_exist(commands, kwargs, 'enforce-on-zone')
        self.fw._is_key_exist(commands, kwargs, 'local-users-only')
        self.fw._is_key_exist(commands, kwargs, 'non-domain-limited-access')
        self.fw._is_key_exist(commands, kwargs, 'poll rate')
        self.fw._is_key_exist(commands, kwargs, 'method sso-agent')
        self.fw._is_key_exist(commands, kwargs, 'tsa-services-bypass')
        self.fw._is_key_exist(commands, kwargs, 'user-group-mechanism')
        self.fw._is_key_exist(commands, kwargs, 'windows-service-user-name')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result


class SAMLCli:

    def __init__(self, fw):
        self.fw = fw

    def show_saml_identity_providers(self):
        cmds = ['show user saml identity-providers']
        return self.fw.do_cli_commands(cmds, tag=1)[1]

    def show_saml_identity_provider_by_name(self, name):
        cmds = [f'show user saml identity-provider {name}']
        return self.fw.do_cli_commands(cmds, tag=1)[1]

    def show_saml_service_providers(self):
        cmds = ['show user saml service-providers']
        return self.fw.do_cli_commands(cmds, tag=1)[1]

    def show_saml_service_provider_by_name(self, name):
        cmds = [f'show user saml service-provider {name}']
        return self.fw.do_cli_commands(cmds, tag=1)[1]

    def show_saml_profiles(self):
        cmds = ['show user saml profiles']
        return self.fw.do_cli_commands(cmds, tag=1)[1]

    def show_saml_profile_by_name(self, name):
        cmds = [f'show user saml profile {name}']
        return self.fw.do_cli_commands(cmds, tag=1)[1]

    def add_saml_identity_provider(self, tag=0, **kwargs):
        '''
        :param kwargs:
        params = {
            'idp_name': 'idp3',
            'auth_url': 'test.com',
            'group-name-attribute':'idp3',
            'logout-url': 'test.com',
            'server-id': 'idp3',
            'trusted-certificate': '',
            'user-name-attribute': ''
        }
        '''
        for key in ['idp_name', 'auth_url', 'group-name-attribute', 'logout-url', 'server-id', 'trusted-certificate']:
            if key not in kwargs:
                logger.error(f'param <{key}> must be specify!!')
                return False
        cmds = ['configure', 'user saml']
        self.fw._is_key_exist(cmds, kwargs, 'idp_name', 'identity-provider')
        self.fw._is_key_exist(cmds, kwargs, 'auth_url', 'authentication-url')
        self.fw._is_key_exist(cmds, kwargs, 'group-name-attribute')
        self.fw._is_key_exist(cmds, kwargs, 'logout-url')
        self.fw._is_key_exist(cmds, kwargs, 'server-id')
        self.fw._is_key_exist(cmds, kwargs, 'trusted-certificate')
        self.fw._is_key_exist(cmds, kwargs, 'user-name-attribute')
        cmds.extend(['commit', 'end', 'exit'])
        return self.fw.do_cli_commands(cmds, tag)

    def add_saml_service_provider(self, tag=0, **kwargs):
        '''
        :param kwargs:
        params = {
            'service_name': 'sev4',
            'address-object': 'X0\ IP',
            'domain-name':'test',
            'service': 'https',
            'type': 'ip'
        }
        '''
        for key in ['sp_name', 'service', 'type']:
            if key not in kwargs:
                logger.error(f'param <{key}> must be specify!!')
                return False
        if kwargs['type'] == 'ip':
            if 'address-object' not in kwargs:
                logger.error('param <address-object> must be specify!!')
                return False
        if kwargs['type'] == 'domain':
            if 'domain-name' not in kwargs:
                logger.error('param <domain-name> must be specify!!')
                return False
        cmds = ['configure', 'user saml']
        self.fw._is_key_exist(cmds, kwargs, 'sp_name', 'service-provider')
        self.fw._is_key_exist(cmds, kwargs, 'type')
        self.fw._is_key_exist(cmds, kwargs, 'address-object')
        self.fw._is_key_exist(cmds, kwargs, 'domain-name')
        self.fw._is_key_exist(cmds, kwargs, 'service')
        cmds.extend(['commit', 'end', 'exit'])
        return self.fw.do_cli_commands(cmds, tag)

    def add_saml_profile(self, tag=0, **kwargs):
        '''
        :param kwargs:
        profile = {
            'name': 'profile_tc48',
            'idp': 'idp_tc36',
            'sp': 'sp_tc35_edit',
            'management': True,
        }
        '''
        cmds = ['configure', 'user saml']
        for key in ['name', 'idp', 'sp']:
            if key not in kwargs.keys():
                logger.error(f'param <{key} must be specify!!>')
                return False
        self.fw._is_key_exist(cmds, kwargs, 'name', 'profile')
        self.fw._is_key_exist(cmds, kwargs, 'idp', 'identity-provider')
        self.fw._is_key_exist(cmds, kwargs, 'sp', 'service-provider')
        if 'use-certificate-sign-sp-request' in kwargs.keys():
            if kwargs['use-certificate-sign-sp-request']:
                if 'certificate' not in kwargs:
                    logger.error(f'param <"certificate"> must be specify!!')
                    return False
                cmds.append('use-certificate-sign-sp-request')
                cmds.append('certificate ' + kwargs['certificate'])
            else:
                cmds.append('no use-certificate-sign-sp-request')
        if 'single-sign-off' in kwargs:
            if kwargs['single-sign-off']:
                cmds.append('single-sign-off')
            else:
                cmds.append('no single-sign-off')
        if 'management' in kwargs:
            if kwargs['management']:
                cmds.append('management')
            else:
                cmds.append('no management')
        cmds.extend(['commit', 'end', 'exit'])
        return self.fw.do_cli_commands(cmds, tag)

    def edit_saml_identity_provider_by_name(self, idp_name, tag=0, **kwargs):
        '''
        :param kwargs:
        idp = {
            'name': 'idp_tc20_edit'
        }
        '''
        cmds = ['configure', 'user saml', f'identity-provider {idp_name}']
        for key in kwargs.keys():
            cmds.append(key + ' ' + kwargs[key])
        cmds.extend(['commit', 'end', 'exit'])
        return self.fw.do_cli_commands(cmds, tag)

    def edit_saml_service_provider_by_name(self, sp_name, tag=0, **kwargs):
        '''
        :param kwargs:
        sp = {
            'name': 'sp_tc31_edit',
        }
        '''
        cmds = ['configure', 'user saml', f'service-provider {sp_name}']
        for key in kwargs:
            cmds.append(key + ' ' + kwargs[key])
        cmds.extend(['commit', 'end', 'exit'])
        return self.fw.do_cli_commands(cmds, tag)

    def edit_saml_profile_by_name(self, pro_name, tag=0, **kwargs):
        '''
        :param kwargs:
        profile = {'name': 'profile_tc48_edit'}
        '''
        cmds = ['configure', 'user saml', f'profile {pro_name}']
        for key in kwargs:
            if key in (['name', 'identity-provider', 'service-provider']):
                cmds.append(key + ' ' + kwargs[key])
            if key in (['management', 'single-sign-off']):
                if kwargs[key]:
                    cmds.append(key)
                else:
                    cmds.append('no ' + key)
            if 'use-certificate-sign-sp-request' in kwargs:
                if kwargs['use-certificate-sign-sp-request']:
                    cmds.append('use-certificate-sign-sp-request')
                    if 'certificate' not in kwargs:
                        logger.error(f'param <"certificate"> must be specify!!')
                        return False
                    cmds.append('certificate ' + kwargs['certificate'])

        cmds.extend(['commit', 'end', 'exit'])
        return self.fw.do_cli_commands(cmds, tag)

    def delete_saml_profile_by_name(self, name, tag=0):
        cmds = ['configure', 'user saml', f'no profile {name}', 'commit', 'end', 'exit']
        return self.fw.do_cli_commands(cmds, tag)

    def delete_saml_service_provider_by_name(self, name, tag=0):
        cmds = ['configure', 'user saml', f'no service-provider {name}', 'commit', 'end', 'exit']
        return self.fw.do_cli_commands(cmds, tag)

    def delete_saml_identity_provider_by_name(self, name, tag=0):
        cmds = ['configure', 'user saml', f'no identity-provider {name}', 'commit', 'end', 'exit']
        return self.fw.do_cli_commands(cmds, tag)

    def delete_all_idp_profiles(self, tag=0):
        cmds = ['configure', 'user saml', 'no identity-providers', 'commit', 'end', 'exit']
        return self.fw.do_cli_commands(cmds, tag)

    def delete_all_sp(self, tag=0):
        cmds = ['configure', 'user saml', 'no service-providers', 'commit', 'end', 'exit']
        return self.fw.do_cli_commands(cmds, tag)

    def delete_all_saml_profiles(self, tag=0):
        cmds = ['configure', 'user saml', 'no profiles', 'commit', 'end', 'exit']
        return self.fw.do_cli_commands(cmds, tag)
