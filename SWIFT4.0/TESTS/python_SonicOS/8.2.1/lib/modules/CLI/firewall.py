from modules.CLI.firewall import AccessRuleCli
from modules.CLI.firewall import ContentFilterObjectCli
from modules.CLI.firewall import ContentFilterPoliciesCli
from modules.CLI.firewall import BandwidthObjectCli
from modules.CLI.firewall import ActionObjectCli
from modules.CLI.firewall import MatchObjectCli
from modules.CLI.firewall import EmailObjectCli
from modules.CLI.firewall import AppControlCli
from modules.CLI.firewall import AppRuleCli


class AccessRuleCli(AccessRuleCli):
    '''AccessRuleCli class'''

        
class ContentFilterObjectCli(ContentFilterObjectCli):
    '''ContentFilterObjectCli class'''

        
class ContentFilterPoliciesCli(ContentFilterPoliciesCli):
    '''ContentFilterPoliciesCli class'''

    def show_cfs_policy_object(self, name=None):
        commands = []
        if name:
            command = 'show content-filter cfs policy name "' + name + '"'
        else:
            command = 'show content-filter cfs policies'
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output   
        
        
class ActionObjectCli(ActionObjectCli):
    '''ActionObjectCli class'''

        
class MatchObjectCli(MatchObjectCli):
    '''MatchObjectCli class'''

        
class EmailObjectCli(EmailObjectCli):
    '''EmailObjectCli class'''

        
class BandwidthObjectCli(BandwidthObjectCli):
    '''BandwidthObjectCli class'''   

        
class AppControlCli(AppControlCli):
    '''AppControlCli class'''

        
class AppRuleCli(AppRuleCli):
    '''AppRuleCli class'''

        