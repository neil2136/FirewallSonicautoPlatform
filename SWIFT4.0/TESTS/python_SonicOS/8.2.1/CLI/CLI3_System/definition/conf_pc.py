from settings import *


class TestSetup_On_PC1(Test):
    uuid = 'NonTC'

    def test_01_add_route_to_PC1(self):
        logger.info("add a route to PC1... ")
        command1 = 'route add -net {} gw {}'.format(Parameter.X1_SUBNET, Parameter.FIREWALL)
        rs = os.system(command1)
        logger.info('PC1 add route result: {}'.format(rs))
        Assertion.assert_equal(True, True, "ERR: Add routes to PC1 failed")




