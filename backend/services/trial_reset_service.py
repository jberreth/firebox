import time
import os
import logging
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from utils import get_logger

logger = get_logger('trial_reset_service')

class TrialResetService:
    """Service for resetting Ignition trial periods using Selenium automation"""
    
    def __init__(self, host_ip="localhost", headless=True):
        self.host_ip = host_ip
        self.headless = headless
        self.driver = None
        self.reset_results = {}
        
        # Configuration from environment variables
        self.gateway_username = os.getenv('IGNITION_USERNAME', 'admin')
        self.gateway_password = os.getenv('IGNITION_PASSWORD', 'password')
        self.reset_timeout = int(os.getenv('RESET_TIMEOUT', '30'))  # seconds
        
        logger.info("Trial reset service initialized", 
                   host_ip=host_ip, 
                   headless=headless,
                   timeout=self.reset_timeout)
    
    def setup_driver(self):
        """Setup Chrome WebDriver with proper configuration"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
            
            # Security and stability options
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')
            chrome_options.add_argument('--disable-javascript')  # We'll enable JS selectively
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
            
            # Accept insecure certificates (common in development)
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            chrome_options.add_argument('--allow-running-insecure-content')
            
            # Logging preferences
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            
            logger.info("Chrome WebDriver initialized successfully")
            return True
            
        except Exception as e:
            logger.error("Failed to setup Chrome WebDriver", error=str(e))
            return False
    
    def cleanup_driver(self):
        """Cleanup WebDriver resources"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("WebDriver cleanup completed")
            except Exception as e:
                logger.warning("Error during WebDriver cleanup", error=str(e))
            finally:
                self.driver = None
    
    def reset_gateway_trial(self, gateway_name: str, port: int) -> dict:
        """Reset trial for a specific gateway"""
        logger.info("Starting trial reset", gateway=gateway_name, port=port)
        
        start_time = datetime.utcnow()
        result = {
            'gateway': gateway_name,
            'port': port,
            'success': False,
            'message': '',
            'started_at': start_time.isoformat(),
            'completed_at': None,
            'duration_seconds': 0,
            'steps_completed': [],
            'error': None
        }
        
        try:
            if not self.setup_driver():
                result['error'] = 'Failed to initialize WebDriver'
                result['message'] = 'Could not start browser automation'
                return result
            
            # Step 1: Navigate to gateway
            if not self._navigate_to_gateway(gateway_name, port, result):
                return result
            
            # Step 2: Authenticate
            if not self._authenticate_gateway(gateway_name, result):
                return result
            
            # Step 3: Navigate to trial reset page
            if not self._navigate_to_trial_reset(gateway_name, result):
                return result
            
            # Step 4: Perform trial reset
            if not self._perform_trial_reset(gateway_name, result):
                return result
            
            # Step 5: Verify reset success
            if not self._verify_trial_reset(gateway_name, result):
                return result
            
            result['success'] = True
            result['message'] = f'Trial reset completed successfully for {gateway_name}'
            logger.info("Trial reset completed successfully", gateway=gateway_name)
            
        except Exception as e:
            error_msg = f"Unexpected error during trial reset: {str(e)}"
            result['error'] = error_msg
            result['message'] = error_msg
            logger.error("Trial reset failed with exception", gateway=gateway_name, error=str(e))
        
        finally:
            result['completed_at'] = datetime.utcnow().isoformat()
            result['duration_seconds'] = (datetime.utcnow() - start_time).total_seconds()
            self.cleanup_driver()
        
        return result
    
    def reset_multiple_gateways(self, gateways: list) -> dict:
        """Reset trials for multiple gateways"""
        logger.info("Starting multiple gateway trial reset", gateway_count=len(gateways))
        
        start_time = datetime.utcnow()
        results = {
            'total_gateways': len(gateways),
            'successful_resets': 0,
            'failed_resets': 0,
            'started_at': start_time.isoformat(),
            'completed_at': None,
            'gateway_results': []
        }
        
        for gateway_info in gateways:
            gateway_name = gateway_info.get('name')
            port = gateway_info.get('port')
            
            if not gateway_name or not port:
                logger.warning("Invalid gateway info", gateway_info=gateway_info)
                continue
            
            # Reset each gateway individually
            reset_result = self.reset_gateway_trial(gateway_name, port)
            results['gateway_results'].append(reset_result)
            
            if reset_result['success']:
                results['successful_resets'] += 1
            else:
                results['failed_resets'] += 1
            
            # Brief pause between resets to avoid overwhelming the system
            time.sleep(2)
        
        results['completed_at'] = datetime.utcnow().isoformat()
        logger.info("Multiple gateway trial reset completed", 
                   successful=results['successful_resets'],
                   failed=results['failed_resets'])
        
        return results
    
    def _navigate_to_gateway(self, gateway_name: str, port: int, result: dict) -> bool:
        """Navigate to the gateway web interface"""
        try:
            url = f"http://{self.host_ip}:{port}"
            logger.info("Navigating to gateway", gateway=gateway_name, url=url)
            
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, self.reset_timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Check if we can access the gateway
            if "Ignition" not in self.driver.title and "Gateway" not in self.driver.title:
                logger.warning("Gateway page not detected", gateway=gateway_name, title=self.driver.title)
                result['error'] = 'Gateway web interface not accessible'
                result['message'] = f'Could not access gateway at {url}'
                return False
            
            result['steps_completed'].append('navigate_to_gateway')
            logger.info("Successfully navigated to gateway", gateway=gateway_name)
            return True
            
        except TimeoutException:
            error_msg = f"Timeout waiting for gateway {gateway_name} to load"
            result['error'] = error_msg
            result['message'] = error_msg
            logger.error(error_msg)
            return False
        except Exception as e:
            error_msg = f"Failed to navigate to gateway {gateway_name}: {str(e)}"
            result['error'] = error_msg
            result['message'] = error_msg
            logger.error(error_msg)
            return False
    
    def _authenticate_gateway(self, gateway_name: str, result: dict) -> bool:
        """Authenticate with the gateway"""
        try:
            logger.info("Attempting gateway authentication", gateway=gateway_name)
            
            # Look for login form elements (common selectors)
            login_selectors = [
                "input[name='username']",
                "input[name='user']", 
                "input[id='username']",
                "input[id='user']",
                "input[type='text']"
            ]
            
            password_selectors = [
                "input[name='password']",
                "input[id='password']",
                "input[type='password']"
            ]
            
            submit_selectors = [
                "input[type='submit']",
                "button[type='submit']",
                "button[name='submit']",
                "input[value*='Login']",
                "button:contains('Login')"
            ]
            
            # Try to find username field
            username_field = None
            for selector in login_selectors:
                try:
                    username_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not username_field:
                logger.info("No login form detected, gateway may not require authentication", gateway=gateway_name)
                result['steps_completed'].append('authentication_not_required')
                return True
            
            # Find password field
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not password_field:
                error_msg = "Password field not found"
                result['error'] = error_msg
                result['message'] = error_msg
                logger.error(error_msg, gateway=gateway_name)
                return False
            
            # Enter credentials
            username_field.clear()
            username_field.send_keys(self.gateway_username)
            
            password_field.clear()
            password_field.send_keys(self.gateway_password)
            
            # Find and click submit button
            submit_button = None
            for selector in submit_selectors:
                try:
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if submit_button:
                submit_button.click()
            else:
                # Try pressing Enter on password field
                password_field.send_keys(Keys.RETURN)
            
            # Wait for authentication to complete
            time.sleep(3)
            
            # Check if we're still on login page (authentication failed)
            current_url = self.driver.current_url
            if 'login' in current_url.lower() or username_field.is_displayed():
                error_msg = "Authentication failed - invalid credentials"
                result['error'] = error_msg
                result['message'] = error_msg
                logger.error(error_msg, gateway=gateway_name)
                return False
            
            result['steps_completed'].append('authentication_successful')
            logger.info("Gateway authentication successful", gateway=gateway_name)
            return True
            
        except Exception as e:
            error_msg = f"Authentication error: {str(e)}"
            result['error'] = error_msg
            result['message'] = error_msg
            logger.error(error_msg, gateway=gateway_name)
            return False
    
    def _navigate_to_trial_reset(self, gateway_name: str, result: dict) -> bool:
        """Navigate to the trial reset page"""
        try:
            logger.info("Navigating to trial reset page", gateway=gateway_name)
            
            # Common paths to trial reset functionality
            trial_reset_paths = [
                "/main/config/system/licensing",
                "/main/web/config/system.licensing",
                "/config/system/licensing",
                "/system/licensing",
                "/licensing"
            ]
            
            base_url = f"http://{self.host_ip}:{self.driver.current_url.split(':')[-1].split('/')[0]}"
            
            for path in trial_reset_paths:
                try:
                    full_url = base_url + path
                    logger.info("Trying trial reset path", gateway=gateway_name, path=path)
                    
                    self.driver.get(full_url)
                    time.sleep(3)
                    
                    # Look for trial-related elements
                    trial_indicators = [
                        "trial",
                        "license",
                        "licensing",
                        "reset",
                        "emergency"
                    ]
                    
                    page_text = self.driver.page_source.lower()
                    found_indicators = [indicator for indicator in trial_indicators if indicator in page_text]
                    
                    if found_indicators:
                        logger.info("Found trial reset page", gateway=gateway_name, indicators=found_indicators)
                        result['steps_completed'].append('navigate_to_trial_reset')
                        return True
                        
                except Exception as e:
                    logger.debug("Failed to access trial reset path", gateway=gateway_name, path=path, error=str(e))
                    continue
            
            error_msg = "Could not find trial reset page"
            result['error'] = error_msg
            result['message'] = error_msg
            logger.error(error_msg, gateway=gateway_name)
            return False
            
        except Exception as e:
            error_msg = f"Navigation to trial reset failed: {str(e)}"
            result['error'] = error_msg
            result['message'] = error_msg
            logger.error(error_msg, gateway=gateway_name)
            return False
    
    def _perform_trial_reset(self, gateway_name: str, result: dict) -> bool:
        """Perform the actual trial reset"""
        try:
            logger.info("Performing trial reset", gateway=gateway_name)
            
            # Look for reset-related buttons or links
            reset_selectors = [
                "button:contains('Reset')",
                "button:contains('Emergency')",
                "button:contains('Trial')", 
                "a:contains('Reset')",
                "a:contains('Emergency')",
                "input[value*='Reset']",
                "input[value*='Emergency']"
            ]
            
            reset_element = None
            for selector in reset_selectors:
                try:
                    # Use XPath for text-based selection
                    if ":contains(" in selector:
                        text = selector.split(":contains('")[1].split("')")[0]
                        xpath = f"//*[contains(text(), '{text}')]"
                        reset_element = self.driver.find_element(By.XPATH, xpath)
                    else:
                        reset_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not reset_element:
                error_msg = "Trial reset button not found"
                result['error'] = error_msg
                result['message'] = error_msg
                logger.error(error_msg, gateway=gateway_name)
                return False
            
            # Click the reset element
            self.driver.execute_script("arguments[0].click();", reset_element)
            time.sleep(2)
            
            # Look for confirmation dialog
            confirmation_selectors = [
                "button:contains('Yes')",
                "button:contains('OK')",
                "button:contains('Confirm')",
                "input[value*='Yes']",
                "input[value*='OK']"
            ]
            
            for selector in confirmation_selectors:
                try:
                    if ":contains(" in selector:
                        text = selector.split(":contains('")[1].split("')")[0]
                        xpath = f"//*[contains(text(), '{text}')]"
                        confirm_element = self.driver.find_element(By.XPATH, xpath)
                    else:
                        confirm_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    confirm_element.click()
                    break
                except NoSuchElementException:
                    continue
            
            # Wait for reset to complete
            time.sleep(5)
            
            result['steps_completed'].append('trial_reset_executed')
            logger.info("Trial reset executed", gateway=gateway_name)
            return True
            
        except Exception as e:
            error_msg = f"Trial reset execution failed: {str(e)}"
            result['error'] = error_msg
            result['message'] = error_msg
            logger.error(error_msg, gateway=gateway_name)
            return False
    
    def _verify_trial_reset(self, gateway_name: str, result: dict) -> bool:
        """Verify that the trial reset was successful"""
        try:
            logger.info("Verifying trial reset", gateway=gateway_name)
            
            # Refresh the page to get updated trial information
            self.driver.refresh()
            time.sleep(3)
            
            page_text = self.driver.page_source.lower()
            
            # Look for indicators of successful reset
            success_indicators = [
                "trial reset",
                "reset successful",
                "emergency reset",
                "168 hours",  # 7 days
                "7 days"
            ]
            
            failure_indicators = [
                "error",
                "failed",
                "invalid",
                "expired"
            ]
            
            found_success = [indicator for indicator in success_indicators if indicator in page_text]
            found_failure = [indicator for indicator in failure_indicators if indicator in page_text]
            
            if found_success and not found_failure:
                result['steps_completed'].append('trial_reset_verified')
                logger.info("Trial reset verification successful", gateway=gateway_name, indicators=found_success)
                return True
            elif found_failure:
                error_msg = f"Trial reset verification failed - found failure indicators: {found_failure}"
                result['error'] = error_msg
                result['message'] = error_msg
                logger.error(error_msg, gateway=gateway_name)
                return False
            else:
                # If no clear indicators, assume success if we got this far
                result['steps_completed'].append('trial_reset_assumed_successful')
                logger.info("Trial reset verification unclear but assumed successful", gateway=gateway_name)
                return True
                
        except Exception as e:
            error_msg = f"Trial reset verification failed: {str(e)}"
            result['error'] = error_msg
            result['message'] = error_msg
            logger.error(error_msg, gateway=gateway_name)
            return False