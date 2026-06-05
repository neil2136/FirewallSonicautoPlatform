import sys
import os
sys.path.append(os.environ["PYTHON_COMMON_HOME"] + '/modules')
from API.switchcontroller import Switch
from API.switchcontroller import Port
from API.switchcontroller import Voice_vlan
from API.switchcontroller import Arp
from API.switchcontroller import Users
from API.switchcontroller import QOS
from API.switchcontroller import Static_routes
from API.switchcontroller import Radius_server


class Switch(Switch):
    '''Switch'''

        
class Port(Port):
    '''Port'''

        
class Voice_vlan(Voice_vlan):
    '''Voice_vlan'''

        
class Arp(Arp):
    '''Arp'''

        
class QOS(QOS):
    '''QOS'''

        
class Users(Users):
    '''Arp'''

        
class Static_routes(Static_routes):
    '''Static_routes'''

        
class Radius_server(Radius_server):
    '''Radius_server'''

        
        