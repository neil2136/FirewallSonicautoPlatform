import unittest
import traceback
import re
from runner.settings import logger,Descriptions


class Assertion(unittest.TestCase):
    def __init__(self, test_case_id,test_method_id):
        Assertion.test_case_id = test_case_id
        Assertion.test_method_id = test_method_id

    @classmethod
    def assert_equal(cls, actual_output, expected_output, msg):
        logger.info("actual output is:")
        logger.info(actual_output)
        logger.info("expected output is:")
        logger.info(expected_output)
        try:
            assert actual_output == expected_output, msg
        except AssertionError as e:
            error_msg=traceback.format_exc()
            logger.error(error_msg)
            Descriptions.teststage[-1][Assertion.test_case_id][Assertion.test_method_id]= '\n' + error_msg
            raise e

    @classmethod
    def assert_not_equal(cls, actual_output, expected_output, msg):
        logger.info("actual output is:")
        logger.info(actual_output)
        logger.info("expected output is:")
        logger.info(expected_output)
        try:
            assert actual_output != expected_output, msg
        except AssertionError as e:
            error_msg=traceback.format_exc()
            logger.error(error_msg)
            Descriptions.teststage[-1][Assertion.test_case_id][Assertion.test_method_id]= '\n' + error_msg
            raise e

    @classmethod
    def assert_regular(cls, actual_output, expected_output, msg):
        logger.info("actual output is:")
        logger.info(actual_output)
        logger.info("expected output is:")
        logger.info(expected_output)
        try:
            assert re.search(r''+ expected_output +'', actual_output, re.I|re.S), msg
        except AssertionError as e:
            error_msg=traceback.format_exc()
            logger.error(error_msg)
            Descriptions.teststage[-1][Assertion.test_case_id][Assertion.test_method_id]= '\n' + error_msg
            raise e

    @classmethod
    def assert_not_regular(cls, actual_output, expected_output, msg):
        logger.info("actual output is:")
        logger.info(actual_output)
        logger.info("expected output is:")
        logger.info(expected_output)
        try:
            assert not re.search(r''+ expected_output +'', actual_output, re.I), msg
        except AssertionError as e:
            error_msg=traceback.format_exc()
            logger.error(error_msg)
            Descriptions.teststage[-1][Assertion.test_case_id][Assertion.test_method_id]= '\n' + error_msg
            raise e

    @classmethod
    def assert_equal_multiple_value(cls, actual_output, expected_output, msg):
        logger.info("actual output is : " + str(actual_output))
        logger.info("expected output is any from : ")
        logger.info(expected_output)
        try:
            assert any(expected_input == actual_output for expected_input in expected_output), msg
        except AssertionError as e:
            error_msg=traceback.format_exc()
            logger.error(error_msg)
            Descriptions.teststage[-1][Assertion.test_case_id][Assertion.test_method_id]= '\n' + error_msg
            raise e

    @classmethod
    def assert_raises(cls, methodToRun, expected_exception, msg):
        try:
            with Assertion.assertRaises(cls, expected_exception=expected_exception) as cm:
                methodToRun()
        except Exception as e:
            error_msg=traceback.format_exc()
            logger.error("actual exception is:")
            logger.error(e)
            logger.error("expected exception is:")
            logger.error(expected_exception)
            logger.error(msg)
            logger.error(error_msg)
            Descriptions.teststage[-1][Assertion.test_case_id][Assertion.test_method_id]= '\n' + error_msg
            raise e

        logger.info("actual exception is:")
        logger.info(cm.exception)
        logger.info("expected exception is:")
        logger.info(expected_exception)

    @classmethod
    def fail(cls, msg):
        logger.error(str(msg))
        raise AssertionError(msg)