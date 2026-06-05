import pexpect
import time
import sys
from runner.settings import Params, logger

class SLCPortTester:
    def __init__(self, ip, device_port, management_port=23, username='admin', password='password', timeout=10, wait_time=300):
        """
        Initialize console server Port Tester
        
        Parameters:
        ip: console server device IP address
        device_port: fw console port to test (2022)
        management_port: Console Management port for recovery (23)
        username: console server Login username
        password: console server Login password
        timeout: console server Telnet timeout (seconds)
        wait_time: console server Wait time after reboot (seconds)
        """
        self.ip = ip
        self.device_port = device_port
        self.management_port = management_port
        self.username = username
        self.password = password
        self.timeout = timeout
        self.wait_time = wait_time
        
        # State variables
        self.initial_status = None
        self.recovery_status = None

    def TestLoginToFWConsole(self):
        """
        Test login to the firewall console port
        
        Returns:
        bool: True if login successful, False otherwise
        """
        try:
            logger.info(f"Testing telnet login to the map port {self.device_port}...")
            # Create Telnet connection using pexpect
            cmd = f'telnet {self.ip} {self.device_port}'
            logger.info(f"Connecting to: {cmd}")
            child = pexpect.spawn(cmd, timeout=self.timeout)
            
            # Handle connection response
            index = child.expect([
                pexpect.EOF,            # Connection closed unexpectedly
                'Escape character is',  # Escape character information
                'login:',               # Login prompt
                'Password:',            # Unexpected password prompt
                'User:'                 # Already logged in
            ], timeout=self.timeout)
            
            if index == 0:  # EOF
                logger.error("Connection closed unexpectedly")
                return False
            elif index == 1:  # Escape character
                logger.info("Escape character detected")
                # Send Enter to continue
                child.sendline()
                time.sleep(3)
                child.expect('login:', timeout=self.timeout)
            elif index == 2:  # login prompt
                logger.info("Login prompt detected")
            elif index == 3:  # Password prompt
                logger.warning("Unexpected password prompt")
                # Try sending username
                child.sendline(self.username)
                child.expect('Password:', timeout=self.timeout)
            elif index == 4:  # User prompt
                logger.info("Already logged in to FW console")
                return True
            
            # Send username
            logger.info(f'Sending CM username: {self.username}')
            child.sendline(self.username)
            
            # Wait for password prompt
            child.expect('Password:', timeout=self.timeout)
            
            # Send password
            logger.info(f'Sending CM password: {self.password}')
            child.sendline(self.password)

            # Send Enter to continue
            child.sendline()
            time.sleep(3)  # Wait a moment for response
            
            # Wait for user prompt or command prompt
            index = child.expect([
                'User:',            # Successful login
                'login:',            # Login failed (incorrect credentials)
                'Password:',         # Password incorrect
                pexpect.TIMEOUT     # Timeout waiting for confirmation
            ], timeout=self.timeout)
            
            if index == 0:  # User prompt
                logger.info("Successfully logged in to FW console")
                return True
            elif index == 1:  # login prompt
                logger.error("Login failed: Incorrect credentials?")
            elif index == 2:  # Password prompt
                logger.error("Login failed: Password incorrect")
            elif index == 3:  # Timeout
                logger.error("Timeout waiting for login confirmation")
            
            return False
            
        except pexpect.EOF:
            logger.error("Connection closed unexpectedly")
            return False
        except pexpect.TIMEOUT:
            logger.error("Timeout during login process")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False
        finally:
            try:
                # Graceful exit: Send Ctrl+] and quit
                child.sendcontrol(']')  # Ctrl+]
                child.expect('telnet>', timeout=2)
                child.sendline('quit')
                child.close()
            except:
                pass

    def reboot_port_via_management(self):
        """
        Reboot the device port using the management port
        
        Returns:
        bool: True if reboot operation succeeded, False otherwise
        """
        max_retries = 3
        retry_interval = 60  # seconds
        
        for attempt in range(1, max_retries + 1):
            logger.info(f"\n===== Attempt {attempt}/{max_retries} =====")
            try:
                logger.info(f"Connecting to management: telnet {self.ip} port {self.management_port}...")
                # Create Telnet connection using pexpect
                child = pexpect.spawn(f'telnet {self.ip} {self.management_port}', timeout=self.timeout)
                
                # Handle initial response
                index = child.expect([
                    pexpect.EOF,        # Connection closed
                    'Escape character is',  # Escape character info
                    'login:',           # Login prompt
                    'Password:',        # Unexpected password prompt
                    '>'                 # Already logged in
                ], timeout=self.timeout)
                
                if index == 0:  # EOF
                    logger.error("Connection closed unexpectedly")
                    continue
                elif index == 1:  # Escape character
                    logger.info("Escape character detected")
                    # Send Enter to continue
                    child.sendline()
                    time.sleep(3)
                    child.expect('login:', timeout=self.timeout)
                elif index == 2:  # login prompt
                    logger.info("Login prompt detected")
                elif index == 3:  # Password prompt
                    logger.warning("Unexpected password prompt")
                    # Try sending username
                    child.sendline(self.username)
                    child.expect('Password:', timeout=self.timeout)
                elif index == 4:  # Command prompt
                    logger.info("Already logged in")
                
                # If login prompt not detected, try to get it
                if index not in [2, 3, 4]:
                    try:
                        child.expect('login:', timeout=5)
                    except pexpect.TIMEOUT:
                        logger.warning("No login prompt detected, sending wakeup")
                        child.sendline()
                        child.expect('login:', timeout=5)
                
                # Send username
                logger.info(f'Sending management username: {self.username}')
                child.sendline(self.username)
                
                # Wait for password prompt
                child.expect('Password:', timeout=self.timeout)
                
                # Send password
                logger.info('Sending management password')
                child.sendline(self.password)
                
                # Wait for command prompt
                child.expect('>', timeout=self.timeout)
                logger.info("Successfully logged in to management port")
                
                # Send reboot command
                logger.info(f"Rebooting device port {self.device_port}...")
                reset_cmd = f'set deviceport port {str(self.device_port)[-2:]} reset'
                logger.info(reset_cmd)
                child.sendline(reset_cmd)
                
                # Handle confirmation prompt
                try:
                    child.expect('\? \[yes\]', timeout=10)
                    logger.info("Confirmation prompt detected")
                    child.sendline('yes')
                except pexpect.TIMEOUT:
                    logger.warning("No confirmation prompt, proceeding")
                
                # Wait for command completion
                child.expect('>', timeout=10)
                logger.info("Port reboot command executed")
                
                # End session
                child.sendline('logout')
                try:
                    child.expect('login:', timeout=5)
                except:
                    pass
                
                child.close()
                logger.info("Management session closed")
                return True
                
            except pexpect.EOF:
                logger.error("Connection closed unexpectedly")
            except pexpect.TIMEOUT:
                logger.error("Timeout during management operation")
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
            finally:
                try:
                    child.close()
                except:
                    pass
                
            # Wait before next attempt if not last
            if attempt < max_retries:
                logger.info(f"⏳ Waiting {retry_interval} seconds before next attempt...")
                time.sleep(retry_interval)
        
        logger.error("All reboot attempts failed")
        return False

    def run_console_port_recovery(self):
        """
        Perform console port recovery
        
        Returns:
        bool: True if recovery succeeded, False otherwise
        """
        logger.info("\n===== Performing console Port Recovery =====")
        logger.info("Device port is inaccessible, attempting recovery...")
        return self.reboot_port_via_management()

    def run_recovery_test(self):
        """
        Execute full port recovery test workflow
        
        Returns:
        bool: True if recovery succeeded, False otherwise
        """   
        # Step 1: Test initial login to device port with retries
        logger.info("\n===== Initial Device Port Login Test =====")
        max_initial_attempts = 3
        initial_retry_interval = 30  # seconds
        
        for initial_attempt in range(1, max_initial_attempts + 1):
            logger.info(f"Initial login attempt {initial_attempt}/{max_initial_attempts}")
            self.initial_status = self.TestLoginToFWConsole()
            
            if self.initial_status:
                logger.info("Device console port is accessible")
                break
            else:
                logger.warning(f"Initial login attempt {initial_attempt} failed")
                if initial_attempt < max_initial_attempts:
                    logger.info(f"⏳ Waiting {initial_retry_interval} seconds before next initial attempt...")
                    time.sleep(initial_retry_interval)
        
        if self.initial_status:
            logger.info("Device console port is already accessible, no recovery needed")
            return True
            
        # Step 2: Perform recovery via management port
        logger.info("\n===== Performing Port Recovery =====")
        logger.info("Device port is inaccessible, attempting recovery...")
        recovery_success = self.reboot_port_via_management()
        
        if not recovery_success:
            logger.error("Recovery operation failed, aborting test")
            return False
            
        # Step 3: Wait for recovery to complete
        logger.info(f"\n===== Waiting {self.wait_time} seconds for recovery =====")
        time.sleep(self.wait_time)
        
        # Step 4: Test recovery status
        logger.info("\n===== Recovery Status Test =====")
        self.recovery_status = self.TestLoginToFWConsole()
        
        # Step 5: Show test summary
        self.show_info_summary()
        
        return self.recovery_status
        
    def show_info_summary(self):
        """
        Show test results summary
        
        Returns:
        bool: Recovery status
        """
        initial_status_text = "Accessible" if self.initial_status else "Inaccessible"
        recovery_status_text = "Accessible" if self.recovery_status else "Inaccessible"
        
        logger.info("\n===== Test Results Summary =====")
        logger.info(f"Initial port status: {initial_status_text}")
        logger.info(f"Recovery port status: {recovery_status_text}")
        
        if self.recovery_status:
            logger.info("✅ Recovery successful: Port is now accessible")
        else:
            logger.error("❌ Recovery failed: Port remains inaccessible")
            
        return self.recovery_status


# if __name__ == "__main__":
#     # Configuration parameters
#     config = {
#         "ip": "10.6.0.46",
#         "device_port": 2022,     # DUT Console port to test (2022)
#         "management_port": 23,   # Console Management port for recovery (23)
#         "username": "admin",     # Console Management username
#         "password": "password",   # Console Management password
#         "timeout": 10,           # Telnet timeout (seconds)
#         "wait_time": 100         # Wait time after reboot (seconds)
#     }
    
#     # Create tester instance
#     tester = SLCPortTester(**config)
    
#     # Execute recovery test
#     success = tester.run_recovery_test()
    
#     # Set exit code based on test result
#     sys.exit(0 if success else 1)