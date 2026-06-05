#from runner.settings import LOGGING
from runner.settings import logger

#logger = LOGGING.getLogger(__name__)

class AdvancedCli:
    '''AdvancedCli class'''
    def __init__(self, fw):
        self.fw = fw

    def show_firewall(self):
        commands = ['show firewall']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def config_advanced(self, **kwargs):
        commands = ['configure', 'firewall' ]
        self.fw._is_key_exist(commands, kwargs, 'stealth-mode')
        self.fw._is_key_exist(commands, kwargs, 'randomize-id')
        self.fw._is_key_exist(commands, kwargs, 'decrement ttl')
        if 'ftp-transforms-in-service-object' in kwargs.keys() \
                and 'ftp-transforms-in-service-object-type' in kwargs.keys():
            commands.append('ftp-transforms-in-service-object '+
                            kwargs['ftp-transforms-in-service-object-type'] +
                            ' ' +
                            self.fw.process_name(kwargs['ftp-transforms-in-service-object']))
        if 'icmp time-exceeded-packets' in kwargs.keys():
            if 'decrement ttl' in kwargs.keys() and kwargs['decrement ttl'] == True:
                self.fw._is_key_exist(commands, kwargs, 'icmp time-exceeded-packets')
            else:
                logger.error('decrement ttl have to be enable first.')
                return False
        else:
            pass
        self.fw._is_key_exist(commands, kwargs, 'sqlnet')
        self.fw._is_key_exist(commands, kwargs, 'rtsp-transformations')
        self.fw._is_key_exist(commands, kwargs, 'drop source-routed')
        self.fw._is_key_exist(commands, kwargs, 'ip checksum-enforcement')
        self.fw._is_key_exist(commands, kwargs, 'udp checksum-enforcement')
        self.fw._is_key_exist(commands, kwargs, 'control-plane-flood-protection')
        if 'control-plane-flood-protection threshold' in kwargs.keys():
            if 'control-plane-flood-protection' in kwargs.keys() and kwargs['control-plane-flood-protection'] == True:
                self.fw._is_key_exist(commands, kwargs, 'control-plane-flood-protection threshold')
            else:
                logger.error('control-plane-flood-protection have to be enable first.')
                return False
        else:
            pass
        self.fw._is_key_exist(commands, kwargs, 'starting-vlan')
        self.fw._is_key_exist(commands, kwargs, 'jumbo-frame')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def config_advanced_access_rule(self, **kwargs):
        commands = ['configure', 'firewall' ]
        self.fw._is_key_exist(commands, kwargs, 'force-ftp-data')
        self.fw._is_key_exist(commands, kwargs, 'apply-rules-for-intra-lan')
        self.fw._is_key_exist(commands, kwargs, 'issue-rst-for-outgoing-discards')
        self.fw._is_key_exist(commands, kwargs, 'icmp redirect-on-lan')
        self.fw._is_key_exist(commands, kwargs, 'drop source-subnet-broadcast')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def config_advanced_ipv6(self, **kwargs):
        commands = ['configure', 'firewall' ]
        self.fw._is_key_exist(commands, kwargs, 'ipv6 drop all-traffic')
        self.fw._is_key_exist(commands, kwargs, 'ipv6 drop routing-header-0')
        self.fw._is_key_exist(commands, kwargs, 'ipv6 decrement hop-limit')
        self.fw._is_key_exist(commands, kwargs, 'ipv6 drop reserved-address-packets')
        self.fw._is_key_exist(commands, kwargs, 'ipv6 icmp time-exceeded')
        self.fw._is_key_exist(commands, kwargs, 'ipv6 icmp destination-unreachable')
        self.fw._is_key_exist(commands, kwargs, 'ipv6 icmp redirect')
        self.fw._is_key_exist(commands, kwargs, 'ipv6 icmp parameter-problem')
        self.fw._is_key_exist(commands, kwargs, 'ipv6 site-local-unicast')
        self.fw._is_key_exist(commands, kwargs, 'ipv6 extension-header-check')
        self.fw._is_key_exist(commands, kwargs, 'ipv6 extension-header-order-check')
        self.fw._is_key_exist(commands, kwargs, 'ipv6 netbios-for-isatap')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result


class BwmCli:
    '''BwmCli class'''
    def __init__(self, fw):
        self.fw = fw

    def show_bandwidth_management(self):
        commands = ['show bandwidth-management']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def config_bwm_priority(self, **kwargs):
        commands = ['configure', 'bandwidth-management', 'type global' ]
        for key in kwargs:
            for key1 in kwargs[key]:
                commands.append('priority ' + key1 + ' ' + key + ' ' + kwargs[key][key1])
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def config_bwm_type(self, **kwargs):
        commands = ['configure', 'bandwidth-management' ]
        self.fw._is_key_exist(commands, kwargs, 'type')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result


class FloodprotectionCli:
    '''FloodprotectionCli class'''
    def __init__(self, fw):
        self.fw = fw

    def show_floodprotection(self, **kwargs):
        commands = []
        self.fw._is_key_exist(commands, kwargs, 'show')
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result

    def config_tcp(self, **kwargs):
        commands = ['configure', 'tcp' ]
        self.fw._is_key_exist(commands, kwargs, 'enforce-strict-compliance')
        if 'handshake-enforcement' in kwargs.keys():
            if 'enforce-strict-compliance' in kwargs.keys() and kwargs['enforce-strict-compliance'] == True:
                self.fw._is_key_exist(commands, kwargs, 'handshake-enforcement')
            else:
                logger.error('enforce-strict-compliance have to be enable first.')
                return False
        else:
            pass
        self.fw._is_key_exist(commands, kwargs, 'checksum-enforcement')
        self.fw._is_key_exist(commands, kwargs, 'drop syn-with-data')
        self.fw._is_key_exist(commands, kwargs, 'handshake-time')
        self.fw._is_key_exist(commands, kwargs, 'default-connection-timeout')
        self.fw._is_key_exist(commands, kwargs, 'maximum-segment-lifetime')
        self.fw._is_key_exist(commands, kwargs, 'syn-flood-protection-mode')
        self.fw._is_key_exist(commands, kwargs, 'syn-attack-threshold')
        if 'support-tcp-sack' in kwargs.keys() or \
                'limit-mss' in kwargs.keys() or \
                'always-log-syn-packets' in kwargs.keys():
            if 'syn-flood-protection-mode' in kwargs.keys() and kwargs['syn-flood-protection-mode'] != 'watch-and-report':
                self.fw._is_key_exist(commands, kwargs, 'support-tcp-sack')
                self.fw._is_key_exist(commands, kwargs, 'limit-mss')
                self.fw._is_key_exist(commands, kwargs, 'always-log-syn-packets')
            else:
                logger.error('can not config in current flood protection mode.')
                return False
        else:
            pass
        self.fw._is_key_exist(commands, kwargs, 'syn-flood-blacklisting')
        if 'blacklist-threshold' in kwargs.keys() or \
                'never-blacklist-wan' in kwargs.keys() or \
                'always-allow-management' in kwargs.keys():
            if 'syn-flood-blacklisting' in kwargs.keys() and kwargs['syn-flood-blacklisting'] == True:
                self.fw._is_key_exist(commands, kwargs, 'blacklist-threshold')
                self.fw._is_key_exist(commands, kwargs, 'never-blacklist-wan')
                self.fw._is_key_exist(commands, kwargs, 'always-allow-management')
            else:
                logger.error('syn-flood-blacklisting have to be enable first.')
                return False
        else:
            pass
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def config_tcp_ddos(self, **kwargs):
        commands = ['configure', 'tcp' ]
        self.fw._is_key_exist(commands, kwargs, 'ddos on-wan-interfaces')
        if 'ddos always-allow-management' in kwargs.keys() or \
                'ddos threshold' in kwargs.keys() or \
                'ddos fliter-bypass-rate' in kwargs.keys() or \
                'ddos allow-list-timeout' in kwargs.keys() or \
                'ddos always-allow-negotiation' in kwargs.keys():
            if 'ddos on-wan-interfaces' in kwargs.keys() and kwargs['ddos on-wan-interfaces'] == True:
                self.fw._is_key_exist(commands, kwargs, 'ddos always-allow-management')
                self.fw._is_key_exist(commands, kwargs, 'ddos threshold')
                self.fw._is_key_exist(commands, kwargs, 'ddos fliter-bypass-rate')
                self.fw._is_key_exist(commands, kwargs, 'ddos allow-list-timeout')
                self.fw._is_key_exist(commands, kwargs, 'ddos always-allow-negotiation')
            else:
                logger.error('ddos always-allow-management have to be enable first.')
                return False
        else:
            pass
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def clear_tcp_stats(self):
        commands = ['configure', 'tcp', 'clear tcp statistics', 'commit', 'end', 'exit']
        return self.fw.do_cli_commands(commands)

    def config_udp(self, **kwargs):
        commands = ['configure', 'udp' ]
        self.fw._is_key_exist(commands, kwargs, 'default-connection-timeout')
        command_fa = self._config_flood_attack(**kwargs)
        commands.extend(command_fa)
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def config_icmp(self, **kwargs):
        commands = ['configure', 'icmp' ]
        command_fa = self._config_flood_attack(**kwargs)
        commands.extend(command_fa)
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def _config_flood_attack(self, **kwargs):
        commands_fa = []
        self.fw._is_key_exist(commands_fa, kwargs, 'flood protection')
        if 'flood attack-threshold' in kwargs.keys() or \
                'flood block-timeout' in kwargs.keys() or \
                'flood protected-dest-list' in kwargs.keys():
            if 'flood protection' in kwargs.keys() and kwargs['flood protection'] == True:
                self.fw._is_key_exist(commands_fa, kwargs, 'flood attack-threshold')
                self.fw._is_key_exist(commands_fa, kwargs, 'flood block-timeout')
                self.fw._is_key_exist(commands_fa, kwargs, 'flood protected-dest-list')
            else:
                logger.error('flood protection have to be enable first.')
                return False
        else:
            pass
        return commands_fa


class MulticastCli:
    '''MulticastCli class'''
    def __init__(self, fw):
        self.fw = fw

    def show_multicast(self):
        commands = ['show multicast']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def enable_multicast(self, **kwargs):
        commands = ['configure' ]
        self.fw._is_key_exist(commands, kwargs, 'multicast')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def config_multicast_snooping(self, **kwargs):
        commands = ['configure', 'multicast' ]
        self.fw._is_key_exist(commands, kwargs, 'require-igmp-membership')
        if 'require-igmp-membership timeout' in kwargs.keys():
            if 'require-igmp-membership' in kwargs.keys() and kwargs['require-igmp-membership'] == True:
                self.fw._is_key_exist(commands, kwargs, 'require-igmp-membership timeout')
            else:
                logger.error('require-igmp-membership have to be enable first.')
                return False
        else:
            pass
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def config_multicast_policies(self, **kwargs):
        commands = ['configure', 'multicast' ]
        if 'reception' in kwargs.keys():
            commands.append('reception ' + kwargs['reception'])
        elif not kwargs['reception']:
            logger.error('please specify the multicast address.')
            return False
        else:
            pass
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result


class QosmappingCli:
    '''QosmappingCli class'''
    def __init__(self, fw):
        self.fw = fw

    def show_qos_mapping(self):
        commands = ['show qos-mapping']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def reset_qos_setting(self):
        commands = ['configure', 'qos-mapping reset' ]
        # not need cmd 'end'
        for command in ['commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def config_qos_setting(self, **kwargs):
        commands = ['configure' ]
        if 'qos-index' in kwargs.keys() and \
            'to-dscp-value' in kwargs.keys() and \
            'from-dscp-value' in kwargs.keys():
            commands.append('qos-mapping cos ' + kwargs['qos-index'] + ' ' + 'to-dscp ' + kwargs['to-dscp-value'] + ' ' + 'from-dscp ' + kwargs['from-dscp-value'])
        elif 'qos-index' not in kwargs.keys() or 'to-dscp-value' not in kwargs.keys() or 'from-dscp-value' not in kwargs.keys():
            logger.error('need more service information.')
            return False
        else:
            pass
        # not need cmd 'end'
        for command in ['commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def clear_state_entry(self, **kwargs):
        commands = ['configure', 'multicast' ]
        if 'address' in kwargs.keys() and 'interface' in kwargs.keys():
            commands.append('clear multicast state-entry address ' + kwargs['address'] + ' interface ' + kwargs['interface'])
        else:
            logger.error('please specify the right address and interface.')
            return False
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result


class SslcontrolCli:
    '''SslcontrolCli class'''
    def __init__(self, fw):
        self.fw = fw

    def show_ssl_control(self):
        commands = ['show ssl-control']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def set_ssl_control(self, **kwargs):
        commands = ['configure', 'ssl-control' ]
        self.fw._is_key_exist(commands, kwargs, 'enable')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def set_ssl_control_action(self, **kwargs):
        commands = ['configure', 'ssl-control' ]
        self.fw._is_key_exist(commands, kwargs, 'action-type', key_new='action')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def config_ssl_control(self, **kwargs):
        commands = ['configure', 'ssl-control' ]
        self.fw._is_key_exist(commands, kwargs, 'blacklist')
        self.fw._is_key_exist(commands, kwargs, 'whitelist')
        self.fw._is_key_exist(commands, kwargs, 'detect weak-ciphers')
        self.fw._is_key_exist(commands, kwargs, 'detect expired')
        self.fw._is_key_exist(commands, kwargs, 'detect weak-digest-cert')
        self.fw._is_key_exist(commands, kwargs, 'detect self-signed')
        self.fw._is_key_exist(commands, kwargs, 'detect untrusted-ca')
        self.fw._is_key_exist(commands, kwargs, 'detect ssl-v2')
        self.fw._is_key_exist(commands, kwargs, 'detect ssl-v3')
        self.fw._is_key_exist(commands, kwargs, 'detect tls-v1')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def config_ssl_customlists(self, **kwargs):
        commands = ['configure', 'ssl-control' ]
        if 'action' in kwargs.keys():
            if kwargs['action'] == 'add':
                command = 'blacklist-certificate'
            else:
                command = 'no blacklist-certificate'
            if 'black_name' in kwargs.keys():
                for i in range(len(kwargs['black_name'])):
                    commands.append(command + ' ' + kwargs['black_name'][i])
            if 'white_name' in kwargs.keys():
                for i in range(len(kwargs['white_name'])):
                    commands.append(command + ' ' + kwargs['white_name'][i])
        else:
            logger.error('action must be specified.')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result


class CiphercontrolCli:
    '''CiphercontrolCli class'''
    def __init__(self, fw):
        self.fw = fw

    def config_ssh_control(self,  msg=False, **kwargs):
        # kwargs = {
        #     'encryption chacha20-poly1305': True,
        #     'encryption aes256-gcm': True,
        #     }
        if kwargs is None:
            logger.error('the cipher value can not empty !')
            return False, None
        commands = ['configure', ' cipher-control ssh']
        res1 = self.fw._is_key_exist(commands, kwargs, 'encryption chacha20-poly1305')  # bool
        res1 &= self.fw._is_key_exist(commands, kwargs, 'encryption aes256-gcm')  # bool
        res1 &= self.fw._is_key_exist(commands, kwargs, 'encryption aes256-ctr')  # bool
        res1 &= self.fw._is_key_exist(commands, kwargs, 'encryption aes192-ctr')  # bool
        res1 &= self.fw._is_key_exist(commands, kwargs, 'encryption aes128-gcm')  # bool
        res1 &= self.fw._is_key_exist(commands, kwargs, 'encryption aes128-ctr')  # bool
        if res1:
            commands.append('commit')

        res2 = self.fw._is_key_exist(commands, kwargs, 'key-exchange ecdh-sha2-nistp521')  # bool
        res2 &= self.fw._is_key_exist(commands, kwargs, 'key-exchange ecdh-sha2-nistp384')  # bool
        res2 &= self.fw._is_key_exist(commands, kwargs, 'key-exchange ecdh-sha2-nistp256')  # bool
        res2 &= self.fw._is_key_exist(commands, kwargs, 'key-exchange diffie-hellman-group14-sha1')  # bool
        res2 &= self.fw._is_key_exist(commands, kwargs, 'key-exchange diffie-hellman-group1-sha1')  # bool
        res2 &= self.fw._is_key_exist(commands, kwargs, 'key-exchange diffie-hellman-group-exchange-sha256')  # bool
        res2 &= self.fw._is_key_exist(commands, kwargs, 'key-exchange diffie-hellman-group-exchange-sha1')  # bool
        if res2:
            commands.append('commit')

        res3 = self.fw._is_key_exist(commands, kwargs, 'mac hmac-sha2-512')  # bool
        res3 &= self.fw._is_key_exist(commands, kwargs, 'mac hmac-sha2-256')  # bool
        res3 &= self.fw._is_key_exist(commands, kwargs, 'mac hmac-sha1')  # bool
        if res3:
            commands.append('commit')

        res4 = self.fw._is_key_exist(commands, kwargs, 'public-key ssh-rsa')  # bool
        res4 &= self.fw._is_key_exist(commands, kwargs, 'public-key rsa-sha2-512')  # bool
        res4 &= self.fw._is_key_exist(commands, kwargs, 'public-key rsa-sha2-256')  # bool
        if res4:
            commands.append('commit')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands, msg)
        return result        

    def config_tls_control(self, cipher='TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384', block=False):
        commands = ['configure', 'cipher-control tls', 'cipher ' + cipher, block]
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result
        