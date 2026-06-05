import re

from utm import is_ipv4
from runner.settings import logger

from modules.CLI.network import WebproxyCli
from modules.CLI.network import InterfaceCli
from modules.CLI.network import FailoverLBCli
from modules.CLI.network import NatpolicyCli
from modules.CLI.network import DhcpServerCli
from modules.CLI.network import DNSCli
from modules.CLI.network import ARPCli
from modules.CLI.network import IpHelperCli
from modules.CLI.network import DDNSCli
from modules.CLI.network import NeighborDiscoveryCli
from modules.CLI.network import ZonesCli
from modules.CLI.network import RouteCli
from modules.CLI.network import PortShieldGroupCli
from modules.CLI.network import NeighborDiscoveryCli
from modules.CLI.network import MacIPAntiSproofCli
from modules.CLI.network import VlanTranslationCli
from modules.CLI.network import NetworkMonitorCli
from modules.CLI.network import ServiceCli
from modules.CLI.network import AddressObjectCli
from modules.CLI.network import ApplicationObjectCli
from modules.CLI.network import DNSfilteringCli
from modules.CLI.network import DNSPolicyCli


def _get_version(kwargs):
    ver = ''
    if 'version' in kwargs.keys() and 'v6' in kwargs['version'].lower():
        ver = 'ipv6'
    return ver 


class WebproxyCli(WebproxyCli):
    '''WebproxyCli class'''
    
    
class DNSfilteringCli(DNSfilteringCli):
    '''DNSfilteringCli class'''


class DNSPolicyCli(DNSPolicyCli):
    '''DNSPolicyCli class'''


class InterfaceCli(InterfaceCli):
    '''InterfaceCli class''' 


class FailoverLBCli(FailoverLBCli):
    '''FailoverLBCli Class'''


class NatpolicyCli(NatpolicyCli):
    '''NatpolicyCli class'''

 
class DhcpServerCli(DhcpServerCli):
    '''DhcpServerCli class'''


class DNSCli(DNSCli):
    '''DNSCli class'''


class ARPCli(ARPCli):

    '''ARPCli class'''

class IpHelperCli(IpHelperCli):
    '''IpHelper class'''


class DDNSCli(DDNSCli):
    '''DDNSCli class'''


class NeighborDiscoveryCli(NeighborDiscoveryCli):
    '''NeighborDiscoveryCli class'''


class ZonesCli(ZonesCli):
    '''ZonesCli class'''


class RouteCli(RouteCli):
    '''RouteCli class'''


 
class PortShieldGroupCli(PortShieldGroupCli):
    '''PortShieldGroupCli class'''


    
class MacIPAntiSproofCli(MacIPAntiSproofCli):
    '''RouteCli class'''



class VlanTranslationCli(VlanTranslationCli):
    '''VlanTranslationCli'''


class NetworkMonitorCli(NetworkMonitorCli):
    '''NetworkMonitorCli class'''


class ServiceCli(ServiceCli):
    '''ServiceCli class'''


class AddressObjectCli(AddressObjectCli):
    '''AddressObjectCli class'''

class ApplicationObjectCli(ApplicationObjectCli):
    '''ApplicationObjectCli'''
