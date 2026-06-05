from utm import is_Firewall_up
#from runner.settings import LOGGING
#logger = LOGGING.getLogger(__name__)
from runner.settings import logger

class DiagCli:
    ''' DiagCli Class
        Configure diag.html page using CLI
    '''
    def __init__(self, fw):
        self.fw = fw

    def diag_clear(self, func: str):
        ''' abr-entries | active-utm | cp-stats | hw-stats |  pp-stats can be passed in '''
        commands = ['diag clear ' + func]
        return self.fw.do_cli_commands(commands, 1)[0]

    def cli_pagertest(self):
        ''' Do not know the effect '''
        pass

    def show_abrentries(self, ip: str):
        ''' ip can be IPv4 or IPv6 '''
        commands = ['diag show abrentries ' + ip]
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_activeutm(self):
        commands = ['diag show active-utm']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_alerts(self, top=0):
        commands = ['diag show alerts']
        if top>0:
            commands = ['diag show alerts top ' + str(top)]
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_bufmemzone(self):
        commands = ['diag show buf-memzone']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_build_info(self):
        commands = ['diag show build-info']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_cores(self, core=0):
        commands = ['diag show cores']
        if core>0:
            commands = ['diag show core ' + str(core)]
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_cpstat(self):
        commands = ['diag show cp-stats']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_cpu(self):
        commands = ['diag show cpu']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_ifdebug(self, port):
        cmd = 'diag show debug interface '
        port = str(port)
        if port.isdigit():
            cmd = cmd + 'X' + port
        else:
            cmd = cmd + port
        return self.fw.do_cli_commands([cmd], 1)[1]

    def show_dropstats(self):
        commands = ['diag show drop-stats']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_fpa(self):
        commands = ['diag show fpa']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_hwstat(self):
        commands = ['diag show hw-stats']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_ipnet(self, mode: str):
        ''' mode can be: interfaces | ndp | route | sockets | statistic | tcp-statistic '''
        commands = ['diag show ipnet ' + mode]
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_log(self, top=0):
        cmd = 'diag show log'
        if top>0:
            cmd = cmd + ' top ' + str(top)
        return self.fw.do_cli_commands([cmd], 1)[1]

    def show_mempool(self):
        commands = ['diag show mem-pools']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_mem(self):
        commands = ['diag show memory']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_memzone(self, mode='', period=0, repeat_mode='', console=0):
        cmd = 'diag show memzone'
        if mode in ['summary', 'verbose']:
            cmd = cmd + ' ' + mode
        if period>0:
            cmd = cmd + ' period ' + str(period)
        if repeat_mode and period:
            repeat_mode = str(repeat_mode)
            if str(repeat_mode).isdigit():
                cmd = cmd + ' repeats ' + repeat_mode
            elif repeat_mode == 'repeat-forever':
                cmd = cmd + ' repeat-forever'
        if console and period:
            cmd = cmd + ' on-console'
        return self.fw.do_cli_commands([cmd], 1)[1]

    def show_multicore(self):
        commands = ['diag show multicore']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_netstat(self):
        commands = ['diag show netstat']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_coredump(self):
        commands = ['show sysfile diag']
        return self.fw.do_cli_commands(commands, 1)
        
    def show_ppstat(self):
        commands = ['diag show pp-stats']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_process(self, process=0):
        cmd = 'diag show process'
        if process>0:
            cmd = cmd + ' ' + str(process)
        else:
            cmd = cmd + 'es'
        return self.fw.do_cli_commands([cmd], 1)[1]

    def show_swport(self, func: str, iface=''):
        cmd = 'diag show switch port ' + func
        if iface:
            if iface.isdigit():
                cmd = cmd + ' interface X' + iface
            else:
                cmd = cmd + ' interface ' + iface
        return self.fw.do_cli_commands([cmd], 1)[1]

    def show_timecount(self):
        commands = ['diag show timer-counters']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_tracelog(self, period=''):
        commands = ['diag show tracelog ' + period]
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_wdstat(self):
        commands = ['diag show wd-stats']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_websvr(self):
        commands = ['diag show web-server']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_wmi(self, func='status'):
        ''' status | configs '''
        commands = ['diag show wmi ' + func]
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_advance(self, func='' , para=''):
        cmd = 'diag show advanced ' + func
        if para:
            cmd = cmd + ' ' + para
        return self.fw.do_cli_commands([cmd], 1)[1]

    def diag_lookup(self, mode: str, simple_para='', params={}):
        cmd = 'diag ' + mode
        if simple_para:
            cmd = cmd + ' ' + str(simple_para)
        if params:
            for key in params.keys():
                cmd = cmd + ' ' + key + ' ' + str(params[key])
        return self.fw.do_cli_commands([cmd], 1)[1]

    def unconf_diag_advance(self, para: str, option=''):
        commands = ['configure']
        cmd = 'diag no advanced ' + para + ' ' + str(option)
        commands.append(cmd)
        commands.append('end')
        return self.fw.do_cli_commands(commands, 1)[0]

    def conf_diag_adv(self, func: str, simple_para='', sub_para={}):
        commands = ['configure']
        cmd = 'diag advanced ' + func
        if simple_para:
            if func=='log-reschedule' and simple_para.isdigit():
                cmd = cmd + ' interval ' + str(simple_para)
            else:
                cmd = cmd + ' ' + str(simple_para)
        commands.append(cmd)
        end = ''
        if sub_para:
            end = 'end'
            for key in sub_para.keys():
                cmd = key
                if type(sub_para[key]).__name__ == 'dict':
                    for sub_key in sub_para[key].keys():
                        cmd = cmd + ' ' + sub_key + ' ' + sub_para[key][sub_key]
                elif type(sub_para[key]).__name__ == 'str' or type(sub_para[key]).__name__ == 'int':
                    cmd = cmd + ' ' + str(sub_para[key])
                elif type(sub_para[key]).__name__ == 'bool' and not sub_para[key]:
                    cmd = 'no ' + cmd
                commands.append(cmd)            
        commands.append('commit')
        commands.append('end')
        if end:
            commands.append('end')
        return self.fw.do_cli_commands(commands, 1)[0]
        
    def diag_conf_dns_tunnel(self, **kwargs):
        commands = ['configure', 'diag advanced dns-security']
        for key in kwargs:
            commands.append(key+' '+str(kwargs[key]))
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def config_encryption_tls_version(self,version):
        ##########tls-v10 tls-v11  tls-v12  tls-v13 ###########
        if not version:
            logger.info('pls enter tls version')
            return False
        else:
            commands = ['configure', 'diag advanced encryption',version]
            for command in ['commit', 'end', 'exit']:
                commands.append(command)
                result = self.fw.do_cli_commands(commands)
        return result
    
    def config_dpissl_tls_version(self,version):
        if not version:
            logger.info('pls enter tls version')
            return False
        else:
            commands = ['configure', 'diag advanced dpi-ssl','ssl-version ' + version]
            for command in ['commit', 'end', 'exit']:
                commands.append(command)
                result = self.fw.do_cli_commands(commands)
        return result

    def config_force_through_interface(self):
        commands = ['configure', 'administration']
        self.fw.do_cli_commands(commands)
        self.fw.do_cli_command('administration')
        result = self.fw.do_cli_command('force-through interface X\t')
        return result

    def config_ssh_host_key_check(self, mode='disable'):
        commands = ['configure', 'diag advanced firewall']
        if mode == 'disable':
            commands.append('no scp-host-key-check')
        elif mode == 'enable':
            commands.append('scp-host-key-check')
        else:
            logger.info('Wrong mode, please input disable or enable')
            return False
        for command in ['commit', 'end', 'exit']:
            commands.append(command)

        try:
            result = self.fw.do_cli_commands(commands)
        except Exception as e:
            print("===================== Exception Information =====================")
            print("==== The command scp-host-key-check may not exist on this build.")
            print("==== Please check the output, if 'No matching command found' shown, please ignore this failure.")
            print(str(e))
            print("===================== Exception Information End =================")
            return False
        return result

