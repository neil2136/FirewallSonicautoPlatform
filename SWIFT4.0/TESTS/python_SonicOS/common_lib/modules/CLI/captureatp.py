from runner.settings import logger

class CaptureATPCli:
    ''' CaptureATPCli
        Show Capture ATP
        Show Capture ATP status
        Configure Capture ATP
    '''
    def __init__(self, fw):
        self.fw = fw

    def show_capatp(self):
        commands = ['show capture-atp']
        return self.fw.do_cli_commands(commands, 1)[1]

    def show_capatp_stat(self):
        commands = ['show capture-atp status']
        return self.fw.do_cli_commands(commands, 1)[1]

    def enable_capatp(self, enable=True):
        commands = ['configure', 'capture-atp']
        commands.append(self.fw.simple_check_box('enable', enable))
        commands.extend(['commit', 'end', 'end'])
        (rc, output) = self.fw.do_cli_commands(commands, 1)
        if not rc:
            logger.info(output)
        return rc

    def conf_capatp(self, **kwargs):
        commands = ['configure', 'capture-atp']
        if 'file-size' in kwargs.keys():
            cmd = self.fw.simple_value('file-size', kwargs['file-size'])
            if kwargs['file-size'] == 'restrict':
                if 'file-size-restrict' in kwargs.keys():
                    cmd = cmd + ' ' + str(kwargs['file-size-restrict'])
                else:
                    logger.error('You need to specify a restrict value.')
                    cmd = ''
            commands.append(cmd)
        if 'file-type-yes' in kwargs.keys():
            for item in kwargs['file-type-yes']:
                commands.append('file-type ' + str(item))
        if 'file-type-no' in kwargs.keys():
            for item in kwargs['file-type-no']:
                commands.append('no file-type ' + str(item))
        #### exclude
        if 'ex-md5-yes' in kwargs.keys():
            for item in kwargs['ex-md5-yes']:
                commands.append('exclude md5-entry ' + str(item))
        if 'ex-md5-no' in kwargs.keys():
            for item in kwargs['ex-md5-no']:
                if item.lower() == 'all':
                    commands.append('no exclude md5-entries')
                    break
                commands.append('no exclude md5-entry ' + str(item))
        if 'ex-addr-action' in kwargs.keys():
            cmd = self.fw.simple_check_box('exclude address for-capture-atp', kwargs['ex-addr-action'])
            if kwargs['ex-addr-action']:
                if 'ex-addr-type' not in kwargs.keys() and 'ex-addr-value' not in kwargs.keys():
                    logger.error('You must specify excluded address type and value.')
                    cmd = ''
                else:
                    cmd = cmd + ' ' + kwargs['ex-addr-type']
                    if kwargs['ex-addr-type'] in ['host', 'fqdn', 'group', 'mac', 'name']:
                        cmd = cmd + ' ' + self.fw.process_name(kwargs['ex-addr-value'])
                    elif kwargs['ex-addr-type'] in ['network', 'range'] and \
                         'ex-addr-ip1' in kwargs.keys() and 'ex-addr-ip2' in kwargs.keys():
                        cmd = cmd + ' ' + str(kwargs['ex-addr-ip1']) + ' ' + str(kwargs['ex-addr-ip2'])
                    elif kwargs['ex-addr-type'] == 'ipv6' and 'ex-addr-ipv6' in kwargs.keys():
                        cmd = cmd + ' ' + kwargs['ex-addr-ipv6']
                        if kwargs['ex-addr-ipv6'] == 'host' and 'ex-addr-ipv6-value' in kwargs.keys():
                            cmd = cmd + ' ' + str(kwargs['ex-addr-ipv6-value'])
                        elif kwargs['ex-addr-ipv6'] in ['range', 'network'] and \
                             'ex-addr-ipv6-ip1' in kwargs.keys() and 'ex-addr-ipv6-ip2' in kwargs.keys():
                            cmd = cmd + ' ' + str(kwargs['ex-addr-ipv6-ip1']) + ' ' + str(kwargs['ex-addr-ipv6-ip2'])
            if cmd != '':
                commands.append(cmd)
        commands.extend(['commit', 'end', 'end'])
        (rc, output) = self.fw.do_cli_commands(commands, 1)
        if not rc:
            logger.info(output)
        return rc

    def conf_custom_behav(self, **kwargs):
        commands = ['configure', 'capture-atp']
        if 'await-verdict' in kwargs.keys():
            if kwargs['await-verdict']:
                commands.append('await-verdict allow')
            else:
                commands.append('await-verdict block')
                if 'ex-file-yes' in kwargs.keys():
                    for item in kwargs['ex-file-yes']:
                        commands.append('exclude file-type ' + str(item))
                if 'ex-file-no' in kwargs.keys():
                    for item in kwargs['ex-file-no']:
                        commands.append('no exclude file-type ' + str(item))
                if 'ex-addr-action' in kwargs.keys():
                    cmd = self.fw.simple_check_box('exclude address for-block-until-verdict',
                                                   kwargs['ex-addr-action'])
                    if kwargs['ex-addr-action']:
                        if 'ex-addr-type' not in kwargs.keys() or 'ex-addr-value' not in kwargs.keys():
                            logger.error('You must specify excluded address type and value.')
                            cmd = ''
                        else:
                            cmd = cmd + ' ' + kwargs['ex-addr-type']
                            if kwargs['ex-addr-type'] in ['host', 'fqdn', 'group', 'mac', 'name']:
                                cmd = cmd + ' ' + self.fw.process_name(kwargs['ex-addr-value'])
                            elif kwargs['ex-addr-type'] in ['network', 'range'] and \
                                 'ex-addr-ip1' in kwargs.keys() and 'ex-addr-ip2' in kwargs.keys():
                                cmd = cmd + ' ' + str(kwargs['ex-addr-ip1']) + ' ' + str(kwargs['ex-addr-ip2'])
                            elif kwargs['ex-addr-type'] == 'ipv6' and 'ex-addr-ipv6' in kwargs.keys():
                                cmd = cmd + ' ' + kwargs['ex-addr-ipv6']
                                if kwargs['ex-addr-ipv6'] == 'host' and 'ex-addr-ipv6-value' in kwargs.keys():
                                    cmd = cmd + ' ' + str(kwargs['ex-addr-ipv6-value'])
                                elif kwargs['ex-addr-ipv6'] in ['range', 'network'] and \
                                     'ex-addr-ipv6-ip1' in kwargs.keys() and 'ex-addr-ipv6-ip2' in kwargs.keys():
                                    cmd = cmd + ' ' + str(kwargs['ex-addr-ipv6-ip1']) + ' ' + \
                                          str(kwargs['ex-addr-ipv6-ip2'])
                    if cmd != '':
                        commands.append(cmd)
        commands.extend(['commit', 'end', 'end'])
        (rc, output) = self.fw.do_cli_commands(commands, 1)
        if not rc:
            logger.info(output)
        return rc