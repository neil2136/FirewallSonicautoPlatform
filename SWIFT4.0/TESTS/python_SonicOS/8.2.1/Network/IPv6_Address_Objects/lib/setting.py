import os
import sys

testplan = os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_Address_Objects/testplan/IPv6_AddrObj.json'

class Parameter():
    FIREWALL = '192.168.168.168'
    Mask = '255.255.255.0'
    TESTPLAN = testplan
    lan_ipv6 = '2000:1111::100'
    wan_ipv6 = '2001:222::100'
    x0_ipv6 = '2000:1111::150'
    x1_ipv6 = '2001:222::182'
