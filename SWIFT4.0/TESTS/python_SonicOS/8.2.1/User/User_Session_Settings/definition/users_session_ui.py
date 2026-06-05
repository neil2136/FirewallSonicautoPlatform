from runner.settings import logger
import re
import os
from modules.ui.ui_wrapper import Browser
from runner.utils.assertion import Assertion
import time
from definition.settings import *

class UserSessionUI(Browser,Test):
	def __init__(self):
		self.usersession_url = "https://" + Parameter.FIREWALL + "/sonicui/7/m/mgmt/users/users-settings"

	def login(self):
		app_flow.login_ui()

	def go_to_user_session_page(self):
		self.go_to_url(self.usersession_url)
		time.sleep(10)
		result = self.does_page_have_text("User Authentication Settings")
		Assertion.assert_equal(result,True,"Error: Users->settings page not loaded.")
		logger.info("Users->settings page loaded")
		self.click_element('xpath',
						   "/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div/section/div/div[1]/div[1]/div/div[2]/div[1]/div/ul/li[4]/div/span")
		time.sleep(15)
		result = self.does_page_have_text("User Session Settings")
		Assertion.assert_equal(result, True, "Error: User Session Settings page not loaded.")
		logger.info("User Session Settings page loaded")

	def set_logging(self):
		self.click_element('xpath',
						   "/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div/section/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/label/span[1]")
		time.sleep(5)
		result = self.is_element_enabled("xpath","/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div/section/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/div/input")
		Assertion.assert_equal(result,True,"error: Log user name text box not enable")
		self.set_text_field("name","user-external-user-log-name","unknow(external)")

		self.click_element('xpath',
						   "/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div/section/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div/div[4]/div[1]/div[2]/label/span[1]")
		time.sleep(5)
		result = self.is_element_enabled("xpath","/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div/section/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div/div[4]/div[1]/div[2]/div/div/input")
		Assertion.assert_equal(result, True, "error: Log user name text box not enable")
		self.set_text_field("name","user-unknown-user-log-name", "unknow(internal)")

		self.click_element('xpath',
						   "/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div/section/div/div[2]/div/div/div[2]/span/div/div/button")
		time.sleep(15)

		result = self.does_page_have_text("unknow(internal)")
		Assertion.assert_equal(result, True, "Error: Setting not saved")
		logger.info("User session setting saved successfully")

