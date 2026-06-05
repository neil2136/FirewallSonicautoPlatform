from runner.settings import logger
import time

class StatusCli:
    '''StatusCli class'''
    def __init__(self, fw):
        self.fw = fw
    # Params
    # base, status, pending-config, with-pending-config
    def show_high_availability(self, mode=''):
        if mode:
            cmd = 'show high-availability ' + mode
            commands = [cmd]
        else:
            commands = ['show high-availability']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def show_high_availability_monitoring(self, **kwargs):
        commands = []
        if 'version' in kwargs.keys() and 'interface' in kwargs.keys():
            cmd = 'show high-availability monitoring '+kwargs['version']+' interface '+kwargs['interface']
            commands.append(cmd)
        elif 'version' in kwargs.keys() and 'interface' not in kwargs.keys():
            logger.error('interface must be specified.')
            return False
        elif 'version' not in kwargs.keys() and 'interface' in kwargs.keys():
            logger.error('ip version must be specified.')
            return False
        else:
            pass
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output


class SettingsCli:
    '''SettingsCli class'''
    def __init__(self, fw):
        self.fw = fw

    def config_settings(self, **kwargs):
        commands = ['configure', 'high-availability' ]
        if kwargs['mode'] in ['None','no mode']:
            commands.append('no mode')
        elif kwargs['mode'] in ['active-standby','active-active-dpi']:
            base_settings = StatusCli(self.fw).show_high_availability('base')
            self.fw._is_key_exist(commands, kwargs, 'mode')
            self.fw._is_key_exist(commands, kwargs, 'primary-serial')
            if 'no mode' in base_settings:
                if 'secondary-serial' not in kwargs.keys() or 'control-interface' not in kwargs.keys():
                    logger.error('Must have Control interface and Secondary serial!')
                    return False
            self.fw._is_key_exist(commands, kwargs, 'secondary-serial')
            self.fw._is_key_exist(commands, kwargs, 'control-interface')
            self.fw._is_key_exist(commands, kwargs, 'virtual-mac')
            self.fw._is_key_exist(commands, kwargs, 'encryption')
            self.fw._is_key_exist(commands, kwargs, 'preempt')

            self.fw._is_key_exist(commands, kwargs, 'stateful-synchronization')
            if kwargs['mode'] == 'active-standby':
                if 'stateful-synchronization' in kwargs.keys():
                    if kwargs['stateful-synchronization'] and 'data-interface' in kwargs.keys():
                        commands.append('data-interface {}'.format(kwargs['data-interface']))
                    else:
                        logger.error('Params Error! Enable stateful need data-interface')
                        return False
            elif kwargs['mode'] == 'active-active-dpi':
                self.fw._is_key_exist(commands, kwargs, 'dpi-interface')
                self.fw._is_key_exist(commands, kwargs, 'data-interface')
        else:
            logger.error('Maybe mode param is not right!')
            return False
        command = ['commit', 'end', 'exit']
        commands.extend(command)
        result = self.fw.do_cli_commands(commands, tag=True)
        return result

    def enable_encrypt_contorl_info(self, **kwargs):
        commands = ['configure', 'high-availability' ]
        self.fw._is_key_exist(commands, kwargs, 'mode')
        ### 'enable-encryption' is not available now. ###
        # self.fw._is_key_exist(commands, kwargs, 'enable-encryption')
        self.fw._is_key_exist(commands, kwargs, 'control-interface')
        self.fw._is_key_exist(commands, kwargs, 'data-interface')
        self.fw._is_key_exist(commands, kwargs, 'dpi-interface')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands, tag=True)
        return result

    # 6700 does not have this mode.
    def config_settings_mode_active_clustering(self, **kwargs):
        commands = ['configure', 'high-availability' ]
        self.fw._is_key_exist(commands, kwargs, 'mode')
        self.fw._is_key_exist(commands, kwargs, 'serial node 1 secondary')
        self.fw._is_key_exist(commands, kwargs, 'rank node 1 virtual-group 1')
        self.fw._is_key_exist(commands, kwargs, 'rank node 1 virtual-group 2')
        self.fw._is_key_exist(commands, kwargs, 'serial node 2 primary')
        self.fw._is_key_exist(commands, kwargs, 'serial node 2 secondary')
        self.fw._is_key_exist(commands, kwargs, 'rank node 2 virtual-group 1')
        self.fw._is_key_exist(commands, kwargs, 'rank node 2 virtual-group 2')
        self.fw._is_key_exist(commands, kwargs, 'control-interface')
        self.fw._is_key_exist(commands, kwargs, 'active-active-cluster-link 1')
        self.fw._is_key_exist(commands, kwargs, 'active-active-cluster-link 2')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands, tag=True)
        return result


class AdvancedCli:
    '''AdvancedCli class'''
    def __init__(self, fw):
        self.fw = fw

    def config_advanced(self, **kwargs):
        commands = ['configure', 'high-availability' ]
        self.fw._is_key_exist(commands, kwargs, 'heartbeat-interval')
        self.fw._is_key_exist(commands, kwargs, 'failover-trigger-level')
        self.fw._is_key_exist(commands, kwargs, 'probe interval')
        self.fw._is_key_exist(commands, kwargs, 'probe count')
        self.fw._is_key_exist(commands, kwargs, 'election-delay-time')
        self.fw._is_key_exist(commands, kwargs, 'failover-when-aggregate-down')
        self.fw._is_key_exist(commands, kwargs, 'sdwan-hold-down-time')
        self.fw._is_key_exist(commands, kwargs, 'include-certificates-keys')
        command = ['commit', 'end', 'exit']
        commands.extend(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def synchronize_settings(self):#
        commands = ['configure', 'high-availability', 'synchronize settings' ]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        logger.info('---> Please waiting for 300s <---')
        time.sleep(300)
        for i in range(10):
            out = StatusCli(self.fw).show_high_availability(mode='status')
            if 'STANDBY' in out:
                logger.info('--->>> Peer boots up!')
                return output
            logger.info(" {} ".center(20, '-').format('Sleep 30s for firewall up'))
            time.sleep(30)
        return False


    def synchronize_firmware(self):#
        commands = ['configure', 'high-availability', 'synchronize firmware' ]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def force_failover(self):#
        commands = ['configure', 'high-availability', 'force-failover' ]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output


class MonitoringCli:
    '''MonitoringCli class'''
    def __init__(self, fw):
        self.fw = fw

    def config_monitoring_interface(self, **kwargs):
        commands = ['configure', 'high-availability' ]
        if 'version' in kwargs.keys() and 'interface' in kwargs.keys():
            cmd ='monitoring interface ' + kwargs['version'] + ' ' + kwargs['interface']
            commands.append(cmd)
        elif 'version' in kwargs.keys() and 'interface' not in kwargs.keys():
            logger.error('interface must be specified.')
            return False
        elif 'version' not in kwargs.keys() and 'interface' in kwargs.keys():
            logger.error('ip version must be specified.')
            return False
        else:
            pass
        self.fw._is_key_exist(commands, kwargs, 'link-monitoring')

        base_monitor = StatusCli(self.fw).show_high_availability_monitoring(**kwargs)
        pri = False if 'no primary'   in base_monitor else True
        sec = False if 'no secondary' in base_monitor else True

        if 'primary' in kwargs.keys():
            commands.append('primary {}'.format(kwargs['primary']))
            pri = True
        if 'secondary' in kwargs.keys():
            commands.append('secondary {}'.format(kwargs['secondary']))
            sec = True
        flag = pri and sec

        if 'allow-management' in kwargs.keys():
            if kwargs['allow-management']:
                if not flag:
                    logger.error('Both Pri and Sec IPs are needed')
                    return False
                else:
                    commands.append('allow-management')
            else:
                commands.append('no allow-management')

        if 'logical-probe-enable' in kwargs.keys():
            if kwargs['logical-probe-enable']:
                commands.append('logical-probe enable')
                if 'logical-probe-ip' in kwargs.keys():
                    if flag:
                        ip = kwargs['logical-probe-ip']
                        commands.append('logical-probe ip {}'.format(ip))
                    else:
                        logger.error('Both Pri and Sec IPs are needed')
                        return False
                else:
                    logger.error('Logical probe ip need to config!')
                    return False
            else:
                commands.append('no logical-probe enable')
        else:
            ret = False if 'no logical-probe enable' in base_monitor else True
            if ret and 'logical-probe-ip' in kwargs.keys():
                ip = kwargs['logical-probe-ip']
                commands.append('logical-probe ip {}'.format(ip))

        if 'override-virtual-mac-enable' in kwargs.keys():
            if kwargs['override-virtual-mac-enable']:
                commands.append('override-virtual-mac enable')
                if 'override-virtual-mac' in kwargs.keys():
                    mac = kwargs['override-virtual-mac']
                    commands.append('override-virtual-mac mac {}'.format(mac))
                # override-virtual-mac have default value
            else:
                commands.append('no override-virtual-mac enable')

        command = ['commit', 'end', 'exit']
        commands.extend(command)
        result = self.fw.do_cli_commands(commands)
        return result
