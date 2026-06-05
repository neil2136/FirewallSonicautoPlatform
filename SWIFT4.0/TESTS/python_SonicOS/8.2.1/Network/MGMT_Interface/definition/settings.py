import os
from utm import Firewall
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
from runner.settings import logger
from util.enhancedinfo import show_testcase_info
from trafficGen import ScapyPacketSend
from lib.modules.API.system import PacketmonitorApi
from lib.modules.API.network import ZoneObjectsApi
from lib.modules.CLI.network import InterfaceCli
from lib.modules.API.network import InterfaceIPv4Api

testplan = os.environ["PYTHON_SONICOS_HOME"] + '/Network/'


class Parameter:
    FIREWALL = '192.168.168.168'
    TESTPLAN = testplan + 'MGMT_Interface/testplan/mgmt_interface.json'

    MGMT_HOST = '192.168.1.101'
    X0_HOST = '192.168.168.199'
    X1_HOST = '172.16.1.101'
    MGMT_IP = '192.168.1.254'
    Src_IP = '192.168.168.65'
    Dst_IP = '172.16.1.101'


fw = Firewall(Parameter.FIREWALL,
              user='admin',
              password='password')

packetmonitor = PacketmonitorApi(fw)
zonemember = ZoneObjectsApi(fw)
interface = InterfaceIPv4Api(fw)
interfacecli = InterfaceCli(fw)
packetsend = ScapyPacketSend(iface='eth1', count=1)
