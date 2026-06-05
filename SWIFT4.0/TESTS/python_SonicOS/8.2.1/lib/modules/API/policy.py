import copy
import json
import sys
from runner.settings import logger

#from modules.API.policy import WebCategoryApi
#from modules.API.policy import SecurityActionProfileApi
from modules.API.policy import SecurityPolicyApi
from modules.API.policy import CFSSettingApi
from modules.API.policy import RoutePolicyApi
from modules.API.policy import PolicySettingsApi
from modules.API.policy import DecryptionPolicyApi
from modules.API.policy import DosPolicyApi
from modules.API.policy import ShadowApi
from modules.API.policy import NatPolicyApi
from modules.API.policy import CFSCustomCategoryApi
from modules.API.policy import AppRulesApi

class PolicySettingsApi(PolicySettingsApi):
    '''PolicySettingsApi class'''

class SecurityPolicyApi(SecurityPolicyApi):
    '''SecurityPolicyApi class'''

class CFSSettingApi(CFSSettingApi):
    '''CFSSettingApi'''


class RoutePolicyApi(RoutePolicyApi):
    '''RoutePolicyApi class'''


class PolicySettingsApi(PolicySettingsApi):
    '''PolicySettingsApi class'''


class DecryptionPolicyApi(DecryptionPolicyApi):
    '''DecryptionPolicyApi class'''


class DosPolicyApi(DosPolicyApi):
    '''DosPolicyApi class'''


class ShadowApi(ShadowApi):
    '''ShadowApi class'''


class NatPolicyApi(NatPolicyApi):
    '''NatPolicyApi class'''
    
class CFSCustomCategoryApi(CFSCustomCategoryApi):
    '''CFSCustomCategoryApi class'''

class AppRulesApi(AppRulesApi):
    '''AppRulesApi class'''