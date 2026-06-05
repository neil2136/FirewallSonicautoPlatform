import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/Multi_factor_auth_otp_mail/')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw',
        'definition.setup_mail_server',
        'testcases.MFA_otp_mail.sslvpn_config',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_1',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_2',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_3',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_4',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_5',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_6',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_7',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_8',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_9',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_10',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_11',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_12',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_13',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_14',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_15',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_16',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_17',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_18',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_19',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_20',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_21',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_22',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_23',
        'testcases.MFA_otp_mail.MFA_OTP_MAIL_24',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()