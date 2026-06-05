from runner.settings import logger


class Settings:
    '''Rules and Policies Settings, including policy mode APP_FW, CFS, GEO-IP, Botnet, DPI-SSL, DPI-SSH, Signature'''

    def __init__(self, fw):
        self.fw = fw

    def enable_dpissl_client(self, mode='enable'):
        if mode == 'disable':
            mode = 'no enable'
        commands = ['configure', 'dpi-ssl client', mode, 'commit', 'end', 'end']
        out = self.fw.do_cli_commands(commands)
        return out
   
    def dpissl_client_general_settings(self, service, negate_value=''):
        commands = ['configure', 'dpi-ssl client', negate_value + service, 'commit', 'end', 'end']
        out = self.fw.do_cli_commands(commands)
        return out
   
    def dpissl_client_cert(self, cert_name):
        cmd = f'resigning-authority certificate "{cert_name}"'
        commands = ['configure', 'dpi-ssl client', cmd, 'commit', 'end', 'end']
        out = self.fw.do_cli_commands(commands)
        return out
   
    def dpissl_client_object_inclusion_exclusion(self, cmd):
        commands = ['configure', 'dpi-ssl client', cmd, 'commit', 'end', 'end']
        out = self.fw.do_cli_commands(commands)
        return out
   
    def dpissl_client_common_name(self, common_name, action):
        cmd = f'common-name {common_name} action {action}'
        commands = ['configure', 'dpi-ssl client', cmd, 'commit', 'end', 'end']
        out = self.fw.do_cli_commands(commands)
        return out
   
    def dpissl_client_del_common_name(self, name):
        cmd = f'no common-name {name}'
        commands = ['configure', 'dpi-ssl client', cmd, 'commit', 'end', 'end']
        out = self.fw.do_cli_commands(commands)
        return out
   
    def dpissl_client_cfs_category_inclusion_exclusion(self, mode='include', negate_value=''):
        if mode in ('include', 'exclude'):
            append_cmd = mode
        else:
            append_cmd = 'category ' + mode
        cmd = negate_value + 'cfs-categories ' + append_cmd
        commands = ['configure', 'dpi-ssl client', cmd, 'commit', 'end', 'end']
        out = self.fw.do_cli_commands(commands)
        return out
   
    def enable_dpissl_server(self, mode='enable'):
        if mode == 'disable':
            mode = 'no enable'
        commands = ['configure', 'dpi-ssl server', mode, 'commit', 'end', 'end']
        out = self.fw.do_cli_commands(commands)
        return out
   
    def dpissl_server_inclusion_exclusion(self, cmd):
        commands = ['configure', 'dpi-ssl server', cmd, 'commit', 'end', 'end']
        out = self.fw.do_cli_commands(commands)
        return out
   
    def dpissl_server_add_cert(self, address_obj, cert_name, cleartext=False):
        cmd = f'ssl-server {address_obj} certificate "{cert_name}"'
        if cleartext:
            cmd = cmd + ' cleartext'
        commands = ['configure', 'dpi-ssl server', cmd, 'commit', 'end', 'end']
        out = self.fw.do_cli_commands(commands)
        return out
   
    def dpissl_server_del_cert(self, name):
        cmd = f'no ssl-server name {name}'
        commands = ['configure', 'dpi-ssl server', cmd, 'commit', 'end', 'end']
        out = self.fw.do_cli_commands(commands)
        return out
   
    def enable_dpissh(self, mode='enable'):
        if mode == 'disable':
            mode = 'no enable'
        commands = ['configure', 'dpi-ssh', mode, 'commit', 'end', 'end']
        out = self.fw.do_cli_commands(commands)
        return out
   
    def dpissh_inclusion_exclusion(self, cmd):
        commands = ['configure', 'dpi-ssh', cmd, 'commit', 'end', 'end']
        out = self.fw.do_cli_commands(commands)
        return out


class SecurityPolicyCli:
    '''SecurityPolicyCli class'''

    def __init__(self, fw):
        self.fw = fw

    def del_all_policies(self, mode='ipv4', msg=False):
        cmd = 'no security-policies ' + str(mode)
        commands = ['configure', cmd, 'commit', 'end']
        out = self.fw.do_cli_commands(commands, 1)
        return ( out[0] if not msg else out )
