import copy
import json
import sys
from runner.settings import logger

from modules.API.securityservices import GAV, SecurityServicesSummary, ClientEnforcementAPI, CFS_Enforcement
from modules.API.securityservices import ContentFilterApi
from modules.API.securityservices import CFSCustomCategoryApi
from modules.API.securityservices import ContentFilterPolicyApi
from modules.API.securityservices import IPSApi
from modules.API.securityservices import GAVCloudApi
from modules.API.securityservices import AntiSpywareApi
from modules.API.securityservices import GeoIP
from modules.API.securityservices import Botnet
from modules.API.securityservices import AppControl


class SecurityServicesSummary(SecurityServicesSummary):
    '''SecurityServicesSummary class '''

class ClientEnforcementAPI(ClientEnforcementAPI):
    '''ClientEnforcementAPI class '''

class CFS_Enforcement(CFS_Enforcement):
    '''CFS_Enforcement class '''

class GAV(GAV):
    '''GAV class '''

class ContentFilterApi(ContentFilterApi):
    '''ContentFilterApi class '''
    
class ContentFilterPolicyApi(ContentFilterPolicyApi):
    '''ContentFilterPolicyApi class '''

class CFSCustomCategoryApi(CFSCustomCategoryApi):
    '''CFSCustomCategoryApi class '''
    
class IPSApi(IPSApi):
    '''IPSApi class '''

class GAVCloudApi(GAVCloudApi):
    '''GAVCloudApii class '''

class AntiSpywareApi(AntiSpywareApi):
    '''AntiSpywareApi class'''

class GeoIP(GeoIP):
    '''GeoIP class'''

class Botnet(Botnet):
    '''Botnet class'''

class AppControl(AppControl):
    '''AppControl class '''
