from runner.settings import logger
import re
import os
from runner.unittest.setup import Test, repeat_method
from modules.ui.ui_wrapper import Browser
from runner.utils.assertion import Assertion
import time


class AppFlow(Browser):
	def __init__(self, ip, user, password):
		self.ip = ip
		self.user = user
		self.password = password
		self.base_url = "https://" + self.ip
		self.appflow_url = self.base_url + "/sonicui/7/m/analytics/appflow/reports"
		self.usersession_url = self.base_url + "/sonicui/7/m/mgmt/users/users-settings"

	# login to FW
	def login_ui(self):
		try:
			self.get_browser()
			self.go_to_url(self.base_url)
			logger.info("Logging in")
			# self.wait_for_element_to_be_visible('class', 'sw-login__sslvpn')
			# self.click_element('class', 'sw-login__sslvpn')
			time.sleep(10)
			logger.debug("Configure - Setting username")
			self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
			logger.debug("Configure - Setting password")
			self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
			logger.info("Action - Clicked Login")
			time.sleep(3)
			self.wait_for_element_to_be_visible('class', 'sw-login__trigger')
			self.click_element('class', 'sw-login__trigger')
			time.sleep(10)
			if self.does_page_have_text(self.user):
				logger.info("Logged to Virtual office successfully")
			else:
				logger.info("Login to virtual office failed")
		except Exception as err:
			logger.error("Exception \t: " + str(err))
			print("Virtual Office login failed")

	def go_to_appflow(self):
		self.go_to_url(self.appflow_url)
		time.sleep(60)
		print(self.get_current_browser_url())
		result = self.does_page_have_text("AppFlow Report")
		Assertion.assert_equal(result, True, "Error: AppFlow Report page not loaded.")
		logger.info("AppFlow Report page loaded")

	def go_to_users(self):
		try:
			if self.browser.find_element("xpath",
										 "//h1[contains(text(),'Enhance Security')]/following::button[text()='OK']"):
				logger.info("Found Enhance Security with Login Attempt Lockout pop-up, clicking OK")
				self.click_element("xpath",
								   "//h1[contains(text(),'Enhance Security')]/following::button[text()='OK']")
		except Exception:
			logger.info("No 'Enhance Security with Login Attempt Lockout' pop-up found, proceeding further...")
		try:
			if self.browser.find_element("xpath", "//button[text()='OK']"):
				logger.info("Found Automatic Firmware Updates pop-up, clicking OK")
				self.click_element("xpath", "//button[text()='OK']")
		except Exception:
			logger.info("No 'Automatic Firmware Updates' pop-up found, proceeding further...")
		time.sleep(5)
		try:
			if self.browser.find_element("xpath",
										 "//button[text()='Register Device']/preceding::span[contains(@class,'icon-close-thin')]"):
				logger.info("Found Device not registered status message, closing it")
				self.click_element("xpath",
								   "//button[text()='Register Device']/preceding::span[contains(@class,'icon-close-thin')]")
		except Exception:
			logger.info("No 'Device not registered' status message found, proceeding further...")
		logger.info("Login Test Flag.")
		time.sleep(10)
		self.click_element('xpath',
						   "/html/body/div/div/div/div[2]/div[3]/div[2]/div[1]/div/section/div/div[1]/div[1]/div/div[2]/div[1]/div/ul/li[2]/div/span")
		time.sleep(50)
		result = self.does_page_have_text("admin")
		Assertion.assert_equal(result, True, "Error: AppFlow Report page->Users not loaded.")
		logger.info("AppFlow Report page -> users loaded")

	# @repeat_method(3)
	def verified_user_details(self, user_name="admin"):
		time.sleep(50)
		result = self.does_page_have_text(user_name)
		Assertion.assert_equal(result, True, "Error: " + user_name + " not present")
		logger.info(user_name + "  Found in the appflow report page")

	def go_to_user_session_page(self):
		self.go_to_url(self.usersession_url)
		time.sleep(60)
		"""---- handling popup----"""
		try:
			if self.browser.find_element("xpath",
										 "//h1[contains(text(),'Enhance Security')]/following::button[text()='OK']"):
				logger.info("Found Enhance Security with Login Attempt Lockout pop-up, clicking OK")
				self.click_element("xpath",
								   "//h1[contains(text(),'Enhance Security')]/following::button[text()='OK']")
		except Exception:
			logger.info("No 'Enhance Security with Login Attempt Lockout' pop-up found, proceeding further...")
		try:
			if self.browser.find_element("xpath", "//button[text()='OK']"):
				logger.info("Found Automatic Firmware Updates pop-up, clicking OK")
				self.click_element("xpath", "//button[text()='OK']")
		except Exception:
			logger.info("No 'Automatic Firmware Updates' pop-up found, proceeding further...")
		time.sleep(5)
		try:
			if self.browser.find_element("xpath",
										 "//button[text()='Register Device']/preceding::span[contains(@class,'icon-close-thin')]"):
				logger.info("Found Device not registered status message, closing it")
				self.click_element("xpath",
								   "//button[text()='Register Device']/preceding::span[contains(@class,'icon-close-thin')]")
		except Exception:
			logger.info("No 'Device not registered' status message found, proceeding further...")
		logger.info("Login Test Flag.")
		print("*********************************************")
		print(self.get_page_source)
		print("*********************************************")
		result = self.does_page_have_text("User Authentication Settings")
		Assertion.assert_equal(result, True, "Error: Users->settings page not loaded.")
		logger.info("Users->settings page loaded")
		try:
			self.click_element('xpath',
							   '/html/body/div/div/div/div[2]/div[3]/div[2]/div[1]/div/section/div/div[1]/div[1]/div/div[2]/div[1]/div/ul/li[4]/div/span')
		except:
			logger.info("Unable to click")
		time.sleep(30)
		print("*********************************************")
		print(self.get_page_source)
		print("*********************************************")
		logger.info("User Session Settings page loaded")

	def set_logging(self):
		logger.info("click on radio button")
		self.click_element('xpath',
						   "/html/body/div/div/div/div[2]/div[3]/div[2]/div[1]/div/section/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/label/span[1]")
		time.sleep(5)
		logger.info("check if textbox enabled")
		result = self.is_element_enabled("name","user-external-user-log-name")
		Assertion.assert_equal(result, True, "error: Log user name text box not enable")
		self.set_text_field("name", "user-external-user-log-name", "unknow(external)")

		self.click_element('xpath',
						   "/html/body/div/div/div/div[2]/div[3]/div[2]/div[1]/div/section/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div/div[5]/div/div[2]/label/span[1]")
		time.sleep(5)
		result = self.is_element_enabled("name","user-unknown-user-log-name")
		Assertion.assert_equal(result, True, "error: Log user name text box not enable")
		self.set_text_field("name", "user-unknown-user-log-name", "unknow(internal)")

		self.click_element('xpath',
						   "//button[contains(@class, 'fw-mgmt-ftr-users-settings__buttons-update') and text()='Accept']")
		time.sleep(15)

		# result = self.is_element_set("xpath",
		# 							 "/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div/section/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/label/span[1]")
		# Assertion.assert_equal(result, False, "Error: Setting not saved")
		logger.info("User session setting saved successfully")

	def verify_empty_text_error(self, error=None):
		self.clear_text_field("name", "user-auto-logn-fail-usr-name")
		self.set_text_field("name", "user-auto-logn-fail-usr-name", "")
		self.click_element('name',"user-auto-logn-bypass-usr-name")
		time.sleep(5)
		result = self.does_page_have_text(error)
		Assertion.assert_equal(result, True, "error: Error message didnt appear")
		logger.info("Empty text box raised error message")

	def logout_ui(self):
		try:
			logger.info("Logging out")
			logger.debug("Action - Clicked drop down")
			self.click_element('xpath', '//div/span[contains(@class,"sw-avatar__initials")]')
			logger.debug("Action - Clicked logout")
			self.click_element('xpath', '//span[contains(text(),"Log Out")]')
			logger.debug("Action - Confirmed logout")
			# self.click_element('xpath', '//div/button[contains(text(),"Continue")]')
			self.click_element('xpath', '//button[normalize-space()="Continue"]')
			if self.does_element_exist('xpath', '//div[contains(text(), "You have been logged out.")]'):
				logger.info("Logged out")
			self.close_browser()
			self.quit()
		except Exception as err:
			logger.error("Exception \t: " + str(err))
			self.close_browser()
			self.quit()
			Assertion.fail("Firewall Logout Failed")
