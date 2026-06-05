from definition.settings import *


class FWFunctionConfigure:

    def ula_configure(self):
        user_dict = {
            'action': 'add',
            'username': CaseParams.ula_user_name,
            'userpassword': 'S0nic@uto',
            'vpn_client_access': ['LAN Subnets'],
            'member_of': ['Everyone'],
        }
        res, msg = userLocalapi.local_user(msg=True, **user_dict)
        if 'Already exists' in str(msg):
            res = True
        return res


    def logout_users(self):
        rc = userLocalapi.logout_all_users()
        # Assertion.assert_equal(rc, True, "ERR: logout user failed")



