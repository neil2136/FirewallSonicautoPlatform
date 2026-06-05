import sys
import os
sys.path.append(os.environ["PYTHON_COMMON_HOME"]+ '/modules')


from CLI.Sw_Switch import SWOCLI
from CLI.Sw_Switch import StaticRoute
from CLI.Sw_Switch import STP
from CLI.Sw_Switch import Network
from CLI.Sw_Switch import Upgrade
from CLI.Sw_Switch import Macaddress
from CLI.Sw_Switch import Users
from CLI.Sw_Switch import Qos
from CLI.Sw_Switch import RadiusServer
from CLI.Sw_Switch import VoiceVlan


class SWOCLI(SWOCLI):
    '''Sw_Switch class'''

        
        
class StaticRoute(StaticRoute):
    '''StaticRoute class'''

        
class STP(STP):
    '''STP class'''

        
class Network(Network):
    '''Network class'''

        
class Upgrade(Upgrade):
    '''Upgrade class'''

        
class Macaddress(Macaddress):
    '''Macaddress class'''

        
class Users(Users):
    '''Users class'''

        
class Qos(Qos):
    '''Qos class'''

        
class RadiusServer(RadiusServer):
    '''RadiusServer class'''

        
class VoiceVlan(VoiceVlan):
    '''VoiceVlan class'''

        
        