import copy
import json
import re
from pprint import pprint
import requests
from collections import OrderedDict
from runner.settings import logger
from modules.API.firewall import ConfigModeApi
from modules.API.firewall import EmailObjectApi
from modules.API.firewall import ActionObjectApi
from modules.API.firewall import BandwidthObjectApi
from modules.API.firewall import AppRuleApi
from modules.API.firewall import AppControlApi
from modules.API.firewall import MatchobjectApi
from modules.API.firewall import CfoObjectApi
from modules.API.firewall import CfoGroupApi
from modules.API.firewall import CfoActionApi
from modules.API.firewall import CfoProfilesApi
from modules.API.firewall import AccessRuleApi
from modules.API.firewall import DNSRuleApi
from modules.API.firewall import AccessRuleIPv6Api
from modules.API.firewall import FipsApi
from modules.API.firewall import CaptureATPApi


class FipsApi(FipsApi):
    '''FipsApi class'''

class DNSRuleApi(DNSRuleApi):
    '''DNSRuleApi class'''

class ConfigModeApi(ConfigModeApi):
    '''ConfigModeApi class'''

class CaptureATPApi(CaptureATPApi):
    '''CaptureATPApi class'''

class EmailObjectApi(EmailObjectApi):
    '''Email Object Api class'''

        
class ActionObjectApi(ActionObjectApi):
    '''Action Object Api class'''

        
class BandwidthObjectApi(BandwidthObjectApi):
    '''Bandwidth Object Api class'''

        
class AppRuleApi(AppRuleApi):
    '''App Rule Object Api class'''

        
class AppControlApi(AppControlApi):
    '''App control Object Api class'''

        
class MatchobjectApi(MatchobjectApi):
    '''Matchobject class'''

        
class CfoObjectApi(CfoObjectApi):
    '''CfoObjectApi class'''

        
class CfoGroupApi(CfoGroupApi):
    '''CfoGroupApi class'''

        
class CfoActionApi(CfoActionApi):
    '''CfoActionApi class'''

        
class CfoProfilesApi(CfoProfilesApi):
    '''CfoProfilesApi class'''

        
class AccessRuleApi(AccessRuleApi):
    '''AccessRuleApi class'''


class AccessRuleIPv6Api(AccessRuleIPv6Api):
    '''AccessRuleIPv6Api class'''
    
