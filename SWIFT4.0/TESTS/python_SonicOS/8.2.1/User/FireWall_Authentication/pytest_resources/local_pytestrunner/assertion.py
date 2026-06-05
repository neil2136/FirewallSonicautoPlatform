# This file contains all assertion libraries.
# This file contains all assertion libraries.
import traceback
import unittest

from pytest_resources.local_pytestrunner.log import *
logger = logging.getLogger('all_logs')


class Assertion(unittest.TestCase):
    @classmethod
    def assert_equal(cls, actual_output, expected_output, msg="Not Equal"):
        logger.debug("assert_equal method")
        logger.info("actual output is:")
        logger.info(actual_output)
        logger.debug("actual output is: " + str(actual_output))

        logger.info("expected output is:")
        logger.info(expected_output)
        logger.debug("expected_output is: " + str(expected_output))
        try:
            assert actual_output == expected_output, msg
        except AssertionError as e:
            logger.error(traceback.format_exc(), "error")
            logger.debug("Exception while assert_equal output : " + str(e))
            raise e

    @classmethod
    def assert_not_equal(cls, actual_output, expected_output, msg="Equal"):
        logger.debug("assert_not_equal method")
        logger.info("actual output is:")
        logger.info(actual_output)
        logger.debug("actual output is: " + str(actual_output))

        logger.info("expected output is:")
        logger.info(expected_output)
        logger.debug("expected_output is: " + str(expected_output))
        try:
            assert actual_output != expected_output, msg
        except AssertionError as e:
            logger.debug("Exception while assert_not_equal output : " + str(e))
            logger.error(traceback.format_exc(), "error")
            raise e

