from definition.settings import *

class Test_Guest_Users_01_TC01(Test):
    uuid = "SOSAIOT-TC-75451"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_01_01_add_guest_user(self):
        logger.info(" {} ".center(20, '-').format('add guest user'))
        ref1 = copy.deepcopy(add_guestuser_account)
        ref1['accountname'] = 'guest111'
        ref1['acco_lifetime'] = 2
        rc = guest_user.user_guest_account(**ref1)
        Assertion.assert_equal(rc, True, f"ERR: add guest user failed")

    def test_01_02_check_user_info(self):
        logger.info(" {} ".center(20, '-').format('check the guest user settings info'))
        rc = False
        res = guest_user.show_user_guest_account()  
        user_info = res['user']['guest']['user']
        for user in user_info:
            if user['name'] == 'guest111':
                logger.info(f'-----{user}-----')
                if user['account_lifetime']['days']==2 and user['idle_timeout']['minutes'] == 10:
                    rc = True
                else:
                    logger.info('the setting info is not correct')
            
        logger.info('~~~~'*10)
        logger.info(res)
        Assertion.assert_equal(rc, True, f"ERR: add guest user failed")


class Test_Guest_Users_02_TC02(Test):
    uuid = "SOSAIOT-TC-75461"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_02_01_add_guest_user(self):
        logger.info(" {} ".center(20, '-').format('add guest user'))
        rc = guest_user.user_guest_account(**add_guestuser_account)
        Assertion.assert_equal(rc, True, f"ERR: add guest user failed")

    def test_02_02_delete_guest_user(self):
        logger.info(" {} ".center(20, '-').format('delete guest user'))
        rc = guest_user.del_user_guest_account(accountname='guest123')
        Assertion.assert_equal(rc, True, f"ERR: delete guest user failed")

    def test_02_03_check_guest_user_list(self):
        logger.info(" {} ".center(20, '-').format('check guest user list'))
        res = guest_user.show_user_guest_account()  
        if "'name': 'guest123'" not in str(res):
            rc = True
        else:
            rc = False
            logger.info(res)
        Assertion.assert_equal(rc, True, f"ERR: check guest user list failed")


class Test_Guest_Users_03_TC13(Test):
    uuid = "SOSAIOT-TC-75455"
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']

    def test_03_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_03_01_add_guest_user(self):
        logger.info(" {} ".center(20, '-').format('add multiple guest user'))
        ref1 = copy.deepcopy(add_guestuser_account)
        ref2 = copy.deepcopy(add_guestuser_account)
        ref2['accountname'] = 'guest456'
        rc = guest_user.user_guest_account(**ref1)
        rc &= guest_user.user_guest_account(**ref2)
        Assertion.assert_equal(rc, True, f"ERR: add multiple guest user failed")

    def test_03_02_check_tsr(self):
        logger.info(" {} ".center(20, '-').format(' check all the guest users are listed in TSR file'))
        res = diag_obj.get_tsr_part(func='Users',lab1='Guest Accounts')
        if 'guest123' in res and 'guest456' in res:
            rc = True
        else:
            rc = False
            logger.info(f'check tsr failed,the res is : {res}')
        Assertion.assert_equal(rc, True, f"ERR: check all the guest users are listed in TSR file failed")

    def test_03_03_del_guestuser_and_check_tsr(self):
        logger.info(" {} ".center(20, '-').format(' delete  guest user and check tsr list'))
        rc = guest_user.del_user_guest_account(accountname='guest123')
        res = diag_obj.get_tsr_part(func='Users',lab1='Guest Accounts')
        if 'guest123' not in res and 'guest456' in res:
            rc &= True
        else:
            rc &= False
            logger.info(f'check tsr failed,the res is : {res}')
        Assertion.assert_equal(rc, True, f"ERR: delete  guest user and check tsr list failed")

