# import re
from runner.settings import logger

class VpnBaseSettingsCli:
    '''VpnBaseSettingsCli'''
    default_options = { 
        'edit_authmode': False, 
        'edit_network': False,    
        'edit_proposal': False,
        'edit_advanced': False
        }

    def __init__(self, fw):
        self.fw = fw

    def add_vpnpolicy(self, **kwargs):
        commands = ['configure']
        if ('type' in kwargs.keys() and 'name' in kwargs.keys()):                        #add a vpn
            commands.append('vpn policy ' + kwargs['type'] + ' ' + kwargs['name'])
#            if (kwargs['type'] == 'site-to-site'):
#                commands_network = self._get_local_remote_network(**kwargs)              #add local network
#                commands = commands + commands_network
#            Vera update: network dhcp needs first choose proposal exchange mode "main" or "aggressive"
        else:
            logger.error('vpn_type and vpn_name must be specified.')
            return False
        ### 
        if ('pri_gate' in kwargs.keys()):                                                 #con gw
            commands.append('gateway primary ' + kwargs['pri_gate'])
            if ('sec_gate' in kwargs.keys() and kwargs['type'] == 'site-to-site'):
                commands.append('gateway secondary ' + kwargs['sec_gate'])
        else:
            logger.error('pri_gate must be specified.')
            return False
        ### config vpn auth mode
        commands_network = self._get_vpn_auth(**kwargs)
        commands = commands +  commands_network
        ### config vpn proposal
        commands_proposal= self._edit_vpnpolicy_proposal(**kwargs)                #edit_vpnpolicy_proposal
        commands = commands +  commands_proposal
        #add local network
        if (kwargs['type'] == 'site-to-site'):
            commands_network = self._get_local_remote_network(**kwargs)              #add local network
            commands = commands + commands_network

        ### config vpn advanced
        commands_advanced= self._edit_vpnpolicy_advanced(**kwargs)                #edit_vpnpolicy_advanced
        commands = commands +  commands_advanced
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def add_ipv6_vpnpolicy(self, **kwargs):
        commands = ['configure']
        if ('name' in kwargs.keys()):                    
            commands.append('vpn policy ipv6 site-to-site ' + kwargs['name'])
        else:
            logger.error('vpn_name must be specified.')
            return False
        if ('pri_gate' in kwargs.keys()):                                                 #con gw
            commands.append('gateway primary ' + kwargs['pri_gate'])
            if ('sec_gate' in kwargs.keys()):
                commands.append('gateway secondary ' + kwargs['sec_gate'])
        else:
            logger.error('pri_gate must be specified.')
            return False
        ### config ipv6 vpn auth mode    
        commands_auth = self._get_vpn_auth(**kwargs)
        commands = commands +  commands_auth
        ### config ipv6 local & remote network
        commands_network = self._get_local_remote_network(**kwargs)                #add local network
        commands = commands + commands_network
        ### config ipv6 proposal
        commands_proposal= self._edit_vpnpolicy_proposal(**kwargs)                #edit_vpnpolicy_proposal
        commands = commands +  commands_proposal
        ### config ipv6 advacned
        if (kwargs['mode'] == 'certificate') or (kwargs['mode'] == 'shared-secret'):
            self.fw._is_key_exist(commands, kwargs, 'keep-alive')
            self.fw._is_key_exist(commands, kwargs, 'anti-replay')
            # self.fw._is_key_exist(commands, kwargs, 'suiteB')
            self.fw._is_key_exist(commands, kwargs, 'allow-sonicpointn-layer3')
            self.fw._is_key_exist(commands, kwargs, 'management https')
            self.fw._is_key_exist(commands, kwargs, 'management ssh')
            self.fw._is_key_exist(commands, kwargs, 'management snmp')
            self.fw._is_key_exist(commands, kwargs, 'bound-to')
            self.fw._is_key_exist(commands, kwargs, 'local-ip')
            self.fw._is_key_exist(commands, kwargs, 'suppress-trigger-packet')
            self.fw._is_key_exist(commands, kwargs, 'accept-hash')
            self.fw._is_key_exist(commands, kwargs, 'send-hash')
        elif (kwargs['mode'] == 'manual-key'):
            self.fw._is_key_exist(commands, kwargs, 'allow-sonicpointn-layer3')
            self.fw._is_key_exist(commands, kwargs, 'management https')
            self.fw._is_key_exist(commands, kwargs, 'management ssh')
            self.fw._is_key_exist(commands, kwargs, 'management snmp')
            self.fw._is_key_exist(commands, kwargs, 'bound-to')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_vpnpolicy(self, **kwargs):
        self.options = dict(VpnBaseSettingsCli.default_options)
        self.options.update(kwargs)      
        kwargs = self.options 

        commands = ['configure']
        if ('type' in kwargs.keys() and 'name' in kwargs.keys()):                         #add a vpn
            if (kwargs['type'] == 'site-to-site'):
                commands.append('vpn policy site-to-site ' + kwargs['name'])
                ### edit a new sec gateway
                if ('sec_gate' in kwargs.keys()):
                    commands.append('gateway secondary ' + kwargs['sec_gate'])
                #### edit local&remote network of s2svpn
                if (kwargs['edit_network']):
                    commands_network = self._get_local_remote_network(**kwargs)                #add local network
                    commands = commands + commands_network
            elif (kwargs['type'] == 'tunnel-interface'):
                commands.append('vpn policy tunnel-interface ' + kwargs['name'])
            else:
                logger.error('vpn_type value error.')
                return False
        else:
            logger.error('vpn_type and vpn_name must be specified.')
            return False
        ### edit a new vpn name
        if ('new_name' in kwargs.keys()):                                                 #con gw
            commands.append('name ' + kwargs['new_name'])
        ### edit a new pri gateway
        if ('pri_gate' in kwargs.keys()):                                                 #con gw
            commands.append('gateway primary ' + kwargs['pri_gate'])
        ### edit vpn auth mode
        if (kwargs['edit_authmode']):
            commands_auth = self._get_vpn_auth(**kwargs)
            commands = commands +  commands_auth
        ### config vpn proposal
        commands_proposal = self._edit_vpnpolicy_proposal(**kwargs)                #edit_vpnpolicy_proposal
        commands = commands +  commands_proposal
        ### config vpn advanced
        commands_advanced = self._edit_vpnpolicy_advanced(**kwargs)                #edit_vpnpolicy_advanced
        commands = commands +  commands_advanced
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_ipv6_vpnpolicy(self, **kwargs):
        commands = ['configure']
        if ('name' in kwargs.keys()):                    
            commands.append('vpn policy ipv6 site-to-site ' + kwargs['name'])
        else:
            logger.error('vpn_name must be specified.')
            return False
        ### edit a new vpn name
        if ('new_name' in kwargs.keys()):                                                 #con gw
            commands.append('name ' + kwargs['new_name'])
        ### edit a new pri gw
        if ('pri_gate' in kwargs.keys()):                                                 #con gw
            commands.append('gateway primary ' + kwargs['pri_gate'])
        ### edit a new sec gw
        if ('sec_gate' in kwargs.keys()):
                commands.append('gateway secondary ' + kwargs['sec_gate'])

        ### edit ipv6 vpn auth mode    
        commands_auth = self._get_vpn_auth(**kwargs)
        commands = commands +  commands_auth
        ### edit ipv6 local & remote network
        commands_network = self._get_local_remote_network(**kwargs)                #add local network
        commands = commands + commands_network
        ### edit ipv6 proposal
        commands_proposal= self._edit_vpnpolicy_proposal(**kwargs)                #edit_vpnpolicy_proposal
        commands = commands +  commands_proposal
        ### edit ipv6 advacned
        self.fw._is_key_exist(commands, kwargs, 'keep-alive')
        self.fw._is_key_exist(commands, kwargs, 'anti-replay')
        # self.fw._is_key_exist(commands, kwargs, 'suiteB')
        self.fw._is_key_exist(commands, kwargs, 'allow-sonicpointn-layer3')
        self.fw._is_key_exist(commands, kwargs, 'management https')
        self.fw._is_key_exist(commands, kwargs, 'management ssh')
        self.fw._is_key_exist(commands, kwargs, 'management snmp')
        self.fw._is_key_exist(commands, kwargs, 'bound-to')
        self.fw._is_key_exist(commands, kwargs, 'local-ip')
        self.fw._is_key_exist(commands, kwargs, 'suppress-trigger-packet')
        self.fw._is_key_exist(commands, kwargs, 'accept-hash')
        self.fw._is_key_exist(commands, kwargs, 'send-hash')
        self.fw._is_key_exist(commands, kwargs, 'allow-sonicpointn-layer3')
        self.fw._is_key_exist(commands, kwargs, 'management https')
        self.fw._is_key_exist(commands, kwargs, 'management ssh')
        self.fw._is_key_exist(commands, kwargs, 'management snmp')
        self.fw._is_key_exist(commands, kwargs, 'bound-to')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_group_vpnpolicy(self, msg=False, **kwargs):
        # kwargs = {
        #             'policy group-vpn': 'WAN GroupVPN',  # WAN GroupVPN     WLAN GroupVPN
        #             'auth-method': 'shared-secret',  # shared-secret    certificate
        #             'shared secret': '72488677C31AB9FD',
        #             'proposal ike dh-group': '14',
        #             'proposal ike encryption': 'aes-256',
        #             'proposal ike authentication': 'sha-256',
        #             'proposal ipsec encryption': 'aes-256',
        #             'proposal ipsec authentication': 'sha-256',
        #             'management ssh': False,
        #             'management snmp': False,
        #             'management https': False,
        #         }
        if 'policy group-vpn' not in kwargs.keys():
            logger.error('the key group-vpn can not empty !')
            return False, None
        commands = ['configure', 'vpn']
        self.fw._is_key_exist(commands, kwargs, 'policy group-vpn')

        # edit general
        methodres = self.fw._is_key_exist(commands, kwargs, 'auth-method')
        if methodres and kwargs['auth-method'] == 'shared-secret':
            commands.append(f'shared-secret {kwargs["shared secret"]}')
            commands.append('exit')

        # edit proposals
        self.fw._is_key_exist(commands, kwargs, 'proposal ike encryption')
        self.fw._is_key_exist(commands, kwargs, 'proposal ike dh-group')
        self.fw._is_key_exist(commands, kwargs, 'proposal ike authentication')
        self.fw._is_key_exist(commands, kwargs, 'proposal ike lifetime')
        self.fw._is_key_exist(commands, kwargs, 'proposal ipsec encryption')
        self.fw._is_key_exist(commands, kwargs, 'proposal ipsec protocol')
        self.fw._is_key_exist(commands, kwargs, 'proposal ipsec perfect-forward-secrecy')
        self.fw._is_key_exist(commands, kwargs, 'proposal ipsec authentication')
        self.fw._is_key_exist(commands, kwargs, 'proposal ipsec lifetime')

        # edit advanced
        self.fw._is_key_exist(commands, kwargs, 'anti-replay')  # bool
        self.fw._is_key_exist(commands, kwargs, 'multicast')  # bool
        self.fw._is_key_exist(commands, kwargs, 'accept-multiple-proposals')  # bool
        self.fw._is_key_exist(commands, kwargs, 'default-lan-gateway')
        self.fw._is_key_exist(commands, kwargs, 'management ssh')  # bool
        self.fw._is_key_exist(commands, kwargs, 'management snmp')  # bool
        self.fw._is_key_exist(commands, kwargs, 'management https')  # bool
        # edit client-authentication
        self.fw._is_key_exist(commands, kwargs, 'client-authentication require-xauth')
        self.fw._is_key_exist(commands, kwargs, 'client-authentication allow-unauthenticated')

        # edit client
        self.fw._is_key_exist(commands, kwargs, 'client cache-xauth')
        self.fw._is_key_exist(commands, kwargs, 'client virtual-adaptor')
        self.fw._is_key_exist(commands, kwargs, 'client allow-connections-to')
        self.fw._is_key_exist(commands, kwargs, 'client default-route')  # bool
        self.fw._is_key_exist(commands, kwargs, 'client access-list')  # bool
        self.fw._is_key_exist(commands, kwargs, 'client simple-provisioning')  # bool

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands, msg)
        return result

    def enable_global_vpn(self):
        commands = ['con', 'vpn', 'enable', 'commit', 'end']
        output = self.fw.do_cli_commands(commands)
        return output

    def enable_vpnpolicy(self, **kwargs):
        commands = ['con']
        if ('type' in kwargs.keys() and 'name' in kwargs.keys()):
            commands.append('vpn policy ' + kwargs['type'] + ' ' + kwargs['name'])
            commands.append('enable')
            for command in ['commit', 'end']:
                commands.append(command)
            output = self.fw.do_cli_commands(commands)
            return output
        else:
            logger.error('vpn_type and vpn_name must be specified.')
            return False

    def disable_global_vpn(self):
        commands = ['con', 'vpn', 'no enable', 'commit', 'end']
        output = self.fw.do_cli_commands(commands)
        return output

    def disable_vpnpolicy(self, **kwargs):
        commands = ['con']
        if ('type' in kwargs.keys() and 'name' in kwargs.keys()):
            commands.append('vpn policy ' + kwargs['type'] + ' ' + kwargs['name'])
            commands.append('no enable')
            for command in ['commit', 'end']:
                commands.append(command)
            output = self.fw.do_cli_commands(commands)
            return output
        else:
            logger.error('vpn_type and vpn_name must be specified.')
            return False

    def show_vpnpolicy(self, **kwargs):
        if ('type' in kwargs.keys() and 'name' in kwargs.keys()):
            commands = ['show vpn policy ipv4 ' + kwargs['type'] + ' ' + kwargs['name']]
            output = self.fw.do_cli_commands(commands, tag=1)[1]
            return output
        else:
            logger.error('vpn_type and vpn_name must be specified.')
            return False

    def show_allvpnpolicy(self):
        commands = ['show vpn policies']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def show_vpn_tunnel(self, vpnname, vpntype):  # vpntype: ike/ipsec/summary
        commands = ['show vpn tunnel ' + vpnname + ' ' + vpntype]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def delete_vpnpolicy(self, **kwargs):
        commands = ['con']
        if ('type' in kwargs.keys() and 'name' in kwargs.keys()):
            commands.append('no vpn policy ' + kwargs['type'] + ' ' + kwargs['name'])
            for command in ['commit', 'end']:
                commands.append(command)
            output = self.fw.do_cli_commands(commands)
            return output
        else:
            logger.error('vpn_type and vpn_name must be specified.')
            return False

    def delete_allvpnpolicy(self):
        commands = ['con', 'no vpn policies', 'commit', 'end']
        output = self.fw.do_cli_commands(commands)
        return output

    def _get_local_remote_network(self, **kwargs):
        commands_network = []
        if ('local_net_type' in kwargs.keys() and \
           ('local_network' in kwargs.keys() or kwargs['local_net_type'] == 'dhcp' or kwargs['local_net_type'] == 'any')):
            if kwargs['local_net_type'] == 'name':
                commands_network.append('network local ' + kwargs['local_net_type'] + ' ' + kwargs['local_network'])
            elif kwargs['local_net_type'] == 'any':
                commands_network.append('network local ' + kwargs['local_net_type'])
            elif kwargs['local_net_type'] == 'group':
                commands_network.append('network local ' + kwargs['local_net_type'] + ' ' + kwargs['local_network'])
            elif kwargs['local_net_type'] == 'host':
                commands_network.append('network local ' + kwargs['local_net_type'] + ' ' + kwargs['local_network'])
            elif kwargs['local_net_type'] == 'network':
                commands_network.append('network local ' + kwargs['local_net_type'] + ' ' + kwargs['local_network'])
            elif kwargs['local_net_type'] == 'range':
                commands_network.append('network local ' + kwargs['local_net_type'] + ' ' + kwargs['local_network'])
            elif kwargs['local_net_type'] == 'dhcp':
                commands_network.append('network local ' + kwargs['local_net_type'])
            else:
                logger.error('local_net_type error.')
                commands_network.append('network local ')
        else:
            logger.error('local_net_type & local_network must be specified.')
            return False
        if ('remote_net_type' in kwargs.keys() and \
           ('remote_network' in kwargs.keys() or kwargs['remote_net_type'] == 'dhcp' or kwargs['remote_net_type'] == 'any')):
            if kwargs['remote_net_type'] == 'name':
                commands_network.append('network remote destination-network ' + kwargs['remote_net_type'] + ' ' + kwargs['remote_network'])
            elif kwargs['remote_net_type'] == 'any':
                commands_network.append('network remote ' + kwargs['remote_net_type'])
            elif kwargs['remote_net_type'] == 'group':
                commands_network.append('network remote ' + kwargs['remote_net_type'] + ' ' + kwargs['remote_network'])
            elif kwargs['remote_net_type'] == 'host':
                commands_network.append('network remote ' + kwargs['remote_net_type'] + ' ' + kwargs['remote_network'])
            elif kwargs['remote_net_type'] == 'network':
                commands_network.append('network remote ' + kwargs['remote_net_type'] + ' ' + kwargs['remote_network'])
            elif kwargs['remote_net_type'] == 'range':
                commands_network.append('network remote ' + kwargs['remote_net_type'] + ' ' + kwargs['remote_network'])
            elif kwargs['remote_net_type'] == 'dhcp':
                commands_network.append('network remote ' + kwargs['remote_net_type'])
            else:
                logger.error('remote_net_type error.')
                commands_network.append('network remote ')
        else:
            logger.error('remote_net_type & remote_network must be specified.')
        return commands_network

    def _get_vpn_auth(self, **kwargs):
        commands_auth = []
        if ('mode' in  kwargs.keys()):
            if kwargs['mode'] == 'certificate':
                if ('local_cert' in kwargs.keys() and 'local_ike_type' in kwargs.keys() \
                        and 'peer_ike_type' in kwargs.keys() and 'peer_ike_id' in kwargs.keys()):
                    commands_auth = ['auth-method ' + kwargs['mode']]        
                    commands_auth.append('certificate ' + kwargs['local_cert'])
                    commands_auth.append('ike-id local ' + kwargs['local_ike_type'])
                    commands_auth.append('ike-id peer ' + kwargs['peer_ike_type'] + ' ' + kwargs['peer_ike_id'])
                    commands_auth.append('exit')
                else:
                    logger.error('local_cert & local_ike_type & peer_ike_type & peer_ike_id must be specified.')
                    return False
            elif kwargs['mode'] == 'shared-secret':
                commands_auth = ['auth-method ' + kwargs['mode']]
                if ('local_ike_id' in kwargs.keys() and 'peer_ike_id' in kwargs.keys() \
                and 'secret' in kwargs.keys()):
                    commands_auth.append('shared-secret ' + kwargs['secret'])
                    commands_auth.append('ike-id local ' + kwargs['local_ike_id'])
                    commands_auth.append('ike-id peer ' + kwargs['peer_ike_id'])
                    commands_auth.append('exit')
                else:
                    logger.error('local_ike_id & peer_ike_id & secret must be specified.')
                    return False

            elif (kwargs['mode'] == 'manual-key'):
                commands_auth.append('auth-method ' + kwargs['mode'])
            else:
                logger.error('vpn auth mode type error.')
                return False
        else:
            logger.error('vpn auth mode must be specified.')
            return False            
        return commands_auth

    def _edit_vpnpolicy_proposal(self, **kwargs):
        commands_proposal = []
        if (kwargs['mode'] == 'certificate' or kwargs['mode'] == 'shared-secret'):
            self.fw._is_key_exist(commands_proposal, kwargs, 'proposal ike exchange')                   #con proposal
            self.fw._is_key_exist(commands_proposal, kwargs, 'proposal ike dh-group')
            self.fw._is_key_exist(commands_proposal, kwargs, 'proposal ike encryption')
            self.fw._is_key_exist(commands_proposal, kwargs, 'proposal ike authentication')
            self.fw._is_key_exist(commands_proposal, kwargs, 'proposal ike lifetime')
            self.fw._is_key_exist(commands_proposal, kwargs, 'proposal ipsec protocol')
            self.fw._is_key_exist(commands_proposal, kwargs, 'proposal ipsec encryption')
            self.fw._is_key_exist(commands_proposal, kwargs, 'proposal ipsec authentication')
            self.fw._is_key_exist(commands_proposal, kwargs, 'proposal ipsec lifetime')
            if ('proposal ipsec perfect-forward-secrecy' in kwargs.keys() and 'proposal ike dh-group' in kwargs.keys()):
                if kwargs['proposal ipsec perfect-forward-secrecy']:
                    commands_proposal.append('proposal ipsec perfect-forward-secrecy dh-group ' + kwargs['proposal ike dh-group'])
                elif not kwargs['proposal ipsec perfect-forward-secrecy']:
                    commands_proposal.append('no proposal ipsec perfect-forward-secrecy')
                else:
                    logger.error('proposal ike dh-group must be specified and ipsec perfect-forward-secrecy specified as bool.')
        elif (kwargs['mode'] == 'manual-key'):
            self.fw._is_key_exist(commands_proposal, kwargs, 'proposal ipsec protocol')                   #con proposal
            self.fw._is_key_exist(commands_proposal, kwargs, 'proposal ipsec authentication')                   #con proposal
            self.fw._is_key_exist(commands_proposal, kwargs, 'proposal ipsec authentication-key')
            self.fw._is_key_exist(commands_proposal, kwargs, 'proposal ipsec encryption-key')                   #con proposal
            self.fw._is_key_exist(commands_proposal, kwargs, 'proposal ipsec in-spi')
            self.fw._is_key_exist(commands_proposal, kwargs, 'proposal ipsec out-spi')
            
            if (kwargs['proposal ipsec protocol'] == 'esp'):
                self.fw._is_key_exist(commands_proposal, kwargs, 'proposal ipsec encryption')
            else:
                pass
        return commands_proposal

    def _edit_vpnpolicy_advanced(self, **kwargs):
        commands_advanced = []
        if (kwargs['mode'] == 'certificate' or kwargs['mode'] == 'shared-secret'):
            self.fw._is_key_exist(commands_advanced, kwargs, 'keep-alive')                              #con keepalive
            self.fw._is_key_exist(commands_advanced, kwargs, 'anti-replay')
            self.fw._is_key_exist(commands_advanced, kwargs, 'netbios')
            self.fw._is_key_exist(commands_advanced, kwargs, 'multicast')
            self.fw._is_key_exist(commands_advanced, kwargs, 'wxa-group')
            # self.fw._is_key_exist(commands_advanced, kwargs, 'suite B')
            self.fw._is_key_exist(commands_advanced, kwargs, 'allow-sonicpointn-layer3')
            self.fw._is_key_exist(commands_advanced, kwargs, 'management https')
            self.fw._is_key_exist(commands_advanced, kwargs, 'management ssh')
            self.fw._is_key_exist(commands_advanced, kwargs, 'management snmp')
            self.fw._is_key_exist(commands_advanced, kwargs, 'user-login http')
            self.fw._is_key_exist(commands_advanced, kwargs, 'user-login https')
            self.fw._is_key_exist(commands_advanced, kwargs, 'bound-to')
            if ('proposal ike exchange' in kwargs.keys()):
                if (kwargs['type'] == 'site-to-site'):
                    self.fw._is_key_exist(commands_advanced, kwargs, 'suppress-auto-add-rule')
                    self.fw._is_key_exist(commands_advanced, kwargs, 'default_lan_gw')
                    commands_applynat = self._edit_vpn_applynat(**kwargs)
                    commands_advanced = commands_advanced + commands_applynat
                    ##### setting ocsp
                    if ('ocsp-checking' in kwargs.keys()):
                        self.fw._is_key_exist(commands_advanced, kwargs, 'ocsp-checking')
                        if (kwargs['ocsp-checking']):
                            self.fw._is_key_exist(commands_advanced, kwargs, 'responder-url')
                            commands_advanced.append('exit')
                    if (kwargs['proposal ike exchange'] == 'ikev2'):
                        self.fw._is_key_exist(commands_advanced, kwargs, 'suppress-trigger-packet')
                        self.fw._is_key_exist(commands_advanced, kwargs, 'accept-hash')
                        self.fw._is_key_exist(commands_advanced, kwargs, 'send-hash')
                    elif (kwargs['proposal ike exchange'] == 'main' or kwargs['proposal ike exchange'] == 'aggressive'):
                        self.fw._is_key_exist(commands_advanced, kwargs, 'XAUTH')
                elif (kwargs['type'] == 'tunnel-interface'):
                    self.fw._is_key_exist(commands_advanced, kwargs, 'advanced-routing')
                    if (kwargs['proposal ike exchange'] == 'ikev2'):
                        self.fw._is_key_exist(commands_advanced, kwargs, 'suppress-trigger-packet')
                        self.fw._is_key_exist(commands_advanced, kwargs, 'accept-hash')
                        self.fw._is_key_exist(commands_advanced, kwargs, 'send-hash')
                    elif (kwargs['proposal ike exchange'] == 'main' or kwargs['proposal ike exchange'] == 'aggressive'):
                        self.fw._is_key_exist(commands_advanced, kwargs, 'transport-mode')
                else:
                    pass
            else:
                pass
        elif (kwargs['mode'] == 'manual-key'):
            self.fw._is_key_exist(commands_advanced, kwargs, 'netbios')
            self.fw._is_key_exist(commands_advanced, kwargs, 'wxa-group')
            self.fw._is_key_exist(commands_advanced, kwargs, 'allow-sonicpointn-layer3')
            self.fw._is_key_exist(commands_advanced, kwargs, 'management https')
            self.fw._is_key_exist(commands_advanced, kwargs, 'management ssh')
            self.fw._is_key_exist(commands_advanced, kwargs, 'management snmp')
            self.fw._is_key_exist(commands_advanced, kwargs, 'user-login http')
            self.fw._is_key_exist(commands_advanced, kwargs, 'user-login https')
            self.fw._is_key_exist(commands_advanced, kwargs, 'bound-to')
            if (kwargs['type'] == 'site-to-site'):
                self.fw._is_key_exist(commands_advanced, kwargs, 'suppress-auto-add-rule')
                self.fw._is_key_exist(commands_advanced, kwargs, 'default-lan-gateway')
                commands_applynat = self._edit_vpn_applynat(**kwargs)
                commands_advanced = commands_advanced + commands_applynat
        else:
            logger.error('vpn mode error.')
            return False
        return commands_advanced

    def _edit_vpn_applynat(self, **kwargs):
        commands_applynat = []
        if ('nat_local_type' in kwargs.keys() and 'nat_local_network' in kwargs.keys()):
            if kwargs['nat_local_type'] == 'name':
                commands_applynat.append('apply-nat translated-local ' + kwargs['nat_local_type'] + ' ' + kwargs['nat_local_network'])
            elif kwargs['nat_local_type'] == 'group':
                commands_applynat.append('apply-nat translated-local ' + kwargs['nat_local_type'] + ' ' + kwargs['nat_local_network'])
            elif kwargs['nat_local_type'] == 'host':
                commands_applynat.append('apply-nat translated-local ' + kwargs['nat_local_type'] + ' ' + kwargs['nat_local_network'])
            elif kwargs['nat_local_type'] == 'network':
                commands_applynat.append('apply-nat translated-local ' + kwargs['nat_local_type'] + ' ' + kwargs['nat_local_network'])
            elif kwargs['nat_local_type'] == 'range':
                commands_applynat.append('apply-nat translated-local ' + kwargs['nat_local_type'] + ' ' + kwargs['nat_local_network'])
            elif kwargs['nat_local_type'] == 'original':
                commands_applynat.append('apply-nat translated-local ' + kwargs['nat_local_type'])
            else:
                logger.error('nat_local_type error.')
                return False
        else:
            pass

        if ('nat_remote_type' in kwargs.keys() and 'nat_remote_network' in kwargs.keys()):
            if kwargs['nat_remote_type'] == 'name':
                commands_applynat.append('apply-nat translated-remote ' + kwargs['nat_remote_type'] + ' ' + kwargs['nat_remote_network'])
            elif kwargs['nat_remote_type'] == 'group':
                commands_applynat.append('apply-nat translated-remote ' + kwargs['nat_remote_type'] + ' ' + kwargs['nat_remote_network'])
            elif kwargs['nat_remote_type'] == 'host':
                commands_applynat.append('apply-nat translated-remote ' + kwargs['nat_remote_type'] + ' ' + kwargs['nat_remote_network'])
            elif kwargs['nat_remote_type'] == 'network':
                commands_applynat.append('apply-nat translated-remote ' + kwargs['nat_remote_type'] + ' ' + kwargs['nat_remote_network'])
            elif kwargs['nat_remote_type'] == 'range':
                commands_applynat.append('apply-nat translated-remote ' + kwargs['nat_remote_type'] + ' ' + kwargs['nat_remote_network'])
            elif kwargs['nat_remote_type'] == 'original':
                commands_applynat.append('apply-nat translated-remote ' + kwargs['nat_remote_type'])
            else:
                logger.error('nat_remote_type error.')
                return False
        else:
            pass
        return commands_applynat


class VpnAdvancedSettingsCli:
    '''VpnAdvancedSettingsCli class'''

    def __init__(self, fw):
        self.fw = fw

    def vpn_advanced_setting(self, **kwargs):
        commands = ['configure', 'vpn']
        self.fw._is_key_exist(commands, kwargs, 'nat-traversal')
        self.fw._is_key_exist(commands, kwargs, 'cleanup-tunnels')
        self.fw._is_key_exist(commands, kwargs, 'traps-on-change')
        ##### setting DPD
        if ('ike-dpd' in kwargs.keys()):
            if (kwargs['ike-dpd']):
                self.fw._is_key_exist(commands, kwargs, 'ike-dpd')
                self.fw._is_key_exist(commands, kwargs, 'interval')
                self.fw._is_key_exist(commands, kwargs, 'trigger')
                self.fw._is_key_exist(commands, kwargs, 'idle-dpd')
                self.fw._is_key_exist(commands, kwargs, 'idle-dpd interval')
                commands.append('exit')
            elif (not kwargs['ike-dpd']):
                commands.append('ike-dpd')
                self.fw._is_key_exist(commands, kwargs, 'idle-dpd')
                commands.append('exit')
                self.fw._is_key_exist(commands, kwargs, 'ike-dpd')
        ##### setting frag-packets
        if ('frag-packets' in kwargs.keys()):
            self.fw._is_key_exist(commands, kwargs, 'frag-packets')
            if (kwargs['frag-packets']):
                self.fw._is_key_exist(commands, kwargs, 'ignore-df-bit')
                commands.append('exit')
        ##### setting dns-server
        if ('dns server' in kwargs.keys()):
            if (kwargs['dns server'] == 'inherit'):
                self.fw._is_key_exist(commands, kwargs, 'dns server')
            elif (kwargs['dns server'] == 'static'):
                self.fw._is_key_exist(commands, kwargs, 'dns server static primary')
                self.fw._is_key_exist(commands, kwargs, 'dns server static secondary')
                self.fw._is_key_exist(commands, kwargs, 'dns server static tertiary')
            else:
                logger.error('dns server type error')
                return False
        ##### setting win-server
        self.fw._is_key_exist(commands, kwargs, 'win primary')
        self.fw._is_key_exist(commands, kwargs, 'win secondary')
        ##### setting IKEv2
        commands.append('ikev2')
        self.fw._is_key_exist(commands, kwargs, 'send-cookie')
        self.fw._is_key_exist(commands, kwargs, 'send-invalid-spi')
        self.fw._is_key_exist(commands, kwargs, 'proposal dh-group')
        self.fw._is_key_exist(commands, kwargs, 'proposal encryption')
        self.fw._is_key_exist(commands, kwargs, 'proposal authentication')
        self.fw._is_key_exist(commands, kwargs, 'proposal prf')
        commands.append('exit')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result


class DhcpOverVpnCli:
    '''DhcpOverVpnCli class''' ###only for dhcp-tunel-type vpn

    def __init__(self, fw):
        self.fw = fw

    ### for setting dhcp-client
    def central_gw_setting(self, **kwargs):
        commands = ['configure', 'vpn', 'dhcp-over-vpn central']
        ### setting send-requests
        self.fw._is_key_exist(commands, kwargs, 'send-requests')
        if ('dhcp-server' in kwargs.keys()):
            commands.append('send-requests')
            commands.append('dhcp-server ' + kwargs['dhcp-server'])
        ### setting internal dhcp server
        self.fw._is_key_exist(commands, kwargs, 'internal-dhcp')        
        if ('global-vpn' in kwargs.keys() or 'remote' in kwargs.keys()):
            if ('internal-dhcp' in kwargs.keys()):
                if (kwargs['internal-dhcp']):
                    self.fw._is_key_exist(commands, kwargs, 'global-vpn')
                    self.fw._is_key_exist(commands, kwargs, 'remote')
                else:
                    logger.error('internal-dhcp should be enable first')
            else:
                logger.error('internal-dhcp should be enable first')
        self.fw._is_key_exist(commands, kwargs, 'relay-ip')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    ### for setting dhcp-remote
    def remote_gw_setting(self, **kwargs):
        commands = ['configure', 'vpn', 'dhcp-over-vpn remote']
        self.fw._is_key_exist(commands, kwargs, 'vpn tunnel')
        self.fw._is_key_exist(commands, kwargs, 'bound-to')
        self.fw._is_key_exist(commands, kwargs, 'accept-bridged-wlan-request')
        self.fw._is_key_exist(commands, kwargs, 'relay-ip')
        self.fw._is_key_exist(commands, kwargs, 'management-ip')
        self.fw._is_key_exist(commands, kwargs, 'block-spoof')
        self.fw._is_key_exist(commands, kwargs, 'temp-lease')
        self.fw._is_key_exist(commands, kwargs, 'lease-time')
        if 'static-device' in kwargs.keys():
            if not kwargs['static-device']:
                commands.append('no static-devices')
            else:
                commands.append('static-device ' + str(kwargs['static-device']))
        if 'del-static-device' in kwargs.keys():
            commands.append('no static-device ' + str(kwargs['del-static-device']))
        if 'excluded-device' in kwargs.keys():
            if not kwargs['excluded-device']:
                commands.append('no excluded-devices')
            else:
                commands.append('excluded-device ' + str(kwargs['excluded-device']))
        if 'del-excluded-device' in kwargs.keys():
            commands.append('no excluded-device ' + str(kwargs['del-excluded-device']))
        for command in ['commit', 'end', 'exit']:
            commands.append(command)  
        result = self.fw.do_cli_commands(commands)
        return result

    def show_dhcp_over_vpn_leases(self):
        commands = ['show vpn dhcp-over-vpn leases']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output


class VpnL2TPServerCli:
    '''VpnL2TPServerCli class'''

    def __init__(self, fw):
        self.fw = fw

    def vpn_l2tpserver_setting(self, **kwargs):
        commands = ['configure', 'vpn']
        if ('l2tp-server' in kwargs.keys()):
            self.fw._is_key_exist(commands, kwargs, 'l2tp-server')
            if (kwargs['l2tp-server']):
                self.fw._is_key_exist(commands, kwargs, 'keep-alive')
                self.fw._is_key_exist(commands, kwargs, 'dns primary')
                self.fw._is_key_exist(commands, kwargs, 'dns secondary')
                self.fw._is_key_exist(commands, kwargs, 'wins primary')
                self.fw._is_key_exist(commands, kwargs, 'wins secondary')
                self.fw._is_key_exist(commands, kwargs, 'ip-pool')
                self.fw._is_key_exist(commands, kwargs, 'user-group')
                commands.append('exit')
    
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_vpn_l2tp_server(self):
        commands = ['show vpn l2tp-server']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output
