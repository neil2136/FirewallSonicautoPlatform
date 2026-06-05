from definition.settings import *


class TestAddTunnel(Test):
    uuid = "NonTC"

    def test_01_01_add_vpn_tunnel(self):
        logger.info(" {} ".center(20, '*').format('Add Local VPN Tunnel'))
        rc1 = Lvpn_obj.add_vpn_policy(**Lvpn)
        logger.info(" {} ".center(20, '*').format('Add rmt VPN Tunnel'))
        rc2 = Rvpn_obj.add_vpnpolicy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Tunnel Failed.')

    def test_01_02_add_tunnel_interface(self):
        logger.info(" {} ".center(20, '*').format('Add Local Tunnel Interface'))
        rc1 = LIntObj.add_interface(**LInt_tunnel)
        logger.info(" {} ".center(20, '*').format('Add rmt Tunnel Interface'))
        rc2 = RIntObj.add_interface(**RInt_tunnel)
        Assertion.assert_equal(rc1&rc2, True, "ERR: Add Tunnel Interface Failed")

    def test_01_03_add_any2any_acl_in_RMT(self):
        cmds = ['configure',
                'access-rule from any to any action allow',
                'name any-any',
                'from any',
                'to any',
                'source address any',
                'service any',
                'commit',
                'exit',
                'exit',
            ]
        rc = rmt.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, "ERR: add any2any acl in RMT via cli failed")


class TestDelTunnel(Test):
    uuid = "NonTC"

    def test_02_01_remove_tunnel_interface(self):
        logger.info(" {} ".center(20, '-').format('Delete Local Tunnel Interface'))
        rc1 = LIntObj.del_interface(**LInt_tunnel)
        logger.info(" {} ".center(20, '-').format('Delete rmt Tunnel Interface'))
        rc2 = RIntObj.del_interface(**RInt_tunnel)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Tunnel Failed.')

    def test_02_02_remove_vpn_tunnel(self):
        logger.info(" {} ".center(20, '-').format('Delete Local VPN Tunnel'))
        rc = Lvpn_obj.del_tunnelvpn_policy(**Lvpn)
        logger.info(" {} ".center(20, '-').format('Delete rmt VPN Tunnel'))
        rc = Rvpn_obj.delete_vpnpolicy(**Rvpn)
        Assertion.assert_equal(rc,True,'Remove VPN Tunnel Failed.')

    def test_02_03_del_any2any_acl_in_RMT(self):
        cmds = ['configure',
                'no access-rule name any-any',
                'commit',
                'exit',
            ]
        rc = rmt.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, "ERR: del any2any acl in RMT via cli failed")

