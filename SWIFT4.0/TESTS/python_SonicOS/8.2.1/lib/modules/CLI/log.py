from modules.CLI.log import ExportlogCli
from modules.CLI.log import ClearlogCli
from modules.CLI.log import EmaillogCli
from modules.CLI.log import LogdisplayCli
from modules.CLI.log import SyslogSettingsCli
from modules.CLI.log import AuditLogsCli
from modules.CLI.log import LogAutomationCli

class SyslogSettingsCli(SyslogSettingsCli):
    '''Syslog Settings'''


class ExportlogCli(ExportlogCli):
    '''export log '''
  

class ClearlogCli(ClearlogCli):
    '''clear log '''
    '''example: clear log'''


class EmaillogCli(EmaillogCli):
    '''email log '''
    '''example: email log'''


class LogdisplayCli(LogdisplayCli):
    '''Configure time range and max unm for showing log view in CLI'''
    '''example: log display max-number 100 '''
    '''         log display time-range last 5 minutes'''



class AuditLogsCli(AuditLogsCli):
    '''Auditing Logs '''



class LogAutomationCli(LogAutomationCli):
    '''Log automation'''
    '''example: 
    1.log automation
    2. email-address audit test@sonicwall.com/ email-format-audit csv
    '''
