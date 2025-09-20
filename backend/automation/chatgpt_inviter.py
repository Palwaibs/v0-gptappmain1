import os
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, WebDriverException,
    ElementClickInterceptedException, StaleElementReferenceException
)
from webdriver_manager.chrome import ChromeDriverManager

class ChatGPTTeamInviter:
    def __init__(self, headless=True, timeout=30):
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.logger = logging.getLogger(__name__)
        self.screenshots_dir = os.path.join(os.path.dirname(__file__), '..', 'screenshots')
        
        # Create screenshots directory if it doesn't exist
        os.makedirs(self.screenshots_dir, exist_ok=True)
    
    def _setup_driver(self):
        """Initialize Chrome WebDriver with optimal settings"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
            
            # Anti-detection measures
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Performance optimizations
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')
            chrome_options.add_argument('--disable-javascript')  # Remove if ChatGPT requires JS
            
            # User agent to appear more human-like
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Window size
            chrome_options.add_argument('--window-size=1920,1080')
            
            # Setup Chrome service
            service = Service(ChromeDriverManager().install())
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Set timeouts
            self.driver.implicitly_wait(10)
            self.driver.set_page_load_timeout(self.timeout)
            
            self.logger.info("Chrome WebDriver initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {str(e)}")
            return False
    
    def _take_screenshot(self, filename_prefix="error"):
        """Take screenshot for debugging purposes"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename_prefix}_{timestamp}.png"
            filepath = os.path.join(self.screenshots_dir, filename)
            
            self.driver.save_screenshot(filepath)
            self.logger.info(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            return None
    
    def _wait_and_find_element(self, by, value, timeout=None):
        """Wait for element and return it"""
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {by}={value}")
            return None
    
    def _wait_and_click_element(self, by, value, timeout=None):
        """Wait for element to be clickable and click it"""
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            
            # Scroll to element
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            
            # Try regular click first
            try:
                element.click()
                return True
            except ElementClickInterceptedException:
                # If regular click fails, try JavaScript click
                self.driver.execute_script("arguments[0].click();", element)
                return True
                
        except (TimeoutException, ElementClickInterceptedException) as e:
            self.logger.error(f"Failed to click element {by}={value}: {str(e)}")
            return False
    
    def login(self, email, password, login_url="https://chatgpt.com/auth/login"):
        """Login to ChatGPT account"""
        try:
            self.logger.info(f"Attempting to login with email: {email}")
            
            # Navigate to login page
            self.driver.get(login_url)
            time.sleep(3)
            
            # Wait for and fill email field
            email_field = self._wait_and_find_element(By.CSS_SELECTOR, 'input[type="email"], input[name="email"], #email')
            if not email_field:
                # Try alternative selectors
                email_field = self._wait_and_find_element(By.XPATH, '//input[@placeholder="Email address"]')
            
            if not email_field:
                raise Exception("Email input field not found")
            
            email_field.clear()
            email_field.send_keys(email)
            time.sleep(1)
            
            # Click continue button
            continue_btn = self._wait_and_find_element(By.XPATH, '//button[contains(text(), "Continue") or contains(text(), "Next")]')
            if continue_btn:
                continue_btn.click()
                time.sleep(3)
            
            # Wait for and fill password field
            password_field = self._wait_and_find_element(By.CSS_SELECTOR, 'input[type="password"], input[name="password"], #password')
            if not password_field:
                raise Exception("Password input field not found")
            
            password_field.clear()
            password_field.send_keys(password)
            time.sleep(1)
            
            # Click login/continue button
            login_btn = self._wait_and_find_element(By.XPATH, '//button[contains(text(), "Continue") or contains(text(), "Log in") or contains(text(), "Sign in")]')
            if not login_btn:
                raise Exception("Login button not found")
            
            login_btn.click()
            time.sleep(5)
            
            # Check if login was successful
            # Look for elements that indicate successful login
            success_indicators = [
                '//div[contains(@class, "sidebar")]',
                '//button[contains(text(), "New chat")]',
                '//div[contains(text(), "ChatGPT")]'
            ]
            
            login_success = False
            for indicator in success_indicators:
                if self._wait_and_find_element(By.XPATH, indicator, timeout=10):
                    login_success = True
                    break
            
            if login_success:
                self.logger.info("Login successful")
                return True
            else:
                # Check for error messages
                error_element = self._wait_and_find_element(By.XPATH, '//div[contains(@class, "error") or contains(text(), "error") or contains(text(), "invalid")]', timeout=5)
                if error_element:
                    error_msg = error_element.text
                    self.logger.error(f"Login failed with error: {error_msg}")
                    raise Exception(f"Login failed: {error_msg}")
                else:
                    raise Exception("Login failed: Unknown error")
                    
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            self._take_screenshot("login_failed")
            return False
    
    def navigate_to_team_management(self, team_url):
        """Navigate to team management page"""
        try:
            # Use admin URL instead of team URL based on screenshot
            admin_url = "https://chatgpt.com/admin?tab=members"
            self.logger.info(f"Navigating to admin members page: {admin_url}")
            
            self.driver.get(admin_url)
            time.sleep(5)
            
            # Wait for admin members page to load
            team_indicators = [
                '//h1[contains(text(), "Members")]',
                '//button[contains(text(), "Invite member")]',
                '//div[contains(@class, "members")]',
                '//button[@class="btn relative btn-primary" and contains(text(), "Invite member")]'
            ]
            
            for indicator in team_indicators:
                if self._wait_and_find_element(By.XPATH, indicator, timeout=15):
                    self.logger.info("Successfully navigated to admin members page")
                    return True
            
            raise Exception("Admin members page not loaded properly")
            
        except Exception as e:
            self.logger.error(f"Failed to navigate to admin members: {str(e)}")
            self._take_screenshot("admin_navigation_failed")
            return False
    
    def invite_member(self, member_email):
        """Send invitation to team member"""
        try:
            self.logger.info(f"Attempting to invite member: {member_email}")
            
            # Look for "Invite member" button (based on screenshot)
            invite_selectors = [
                '//button[contains(text(), "Invite member")]',
                '//button[@class="btn relative btn-primary" and contains(text(), "Invite member")]',
                '//button[contains(@class, "btn-primary") and contains(text(), "Invite")]'
            ]
            
            invite_button = None
            for selector in invite_selectors:
                invite_button = self._wait_and_find_element(By.XPATH, selector, timeout=10)
                if invite_button:
                    break
            
            if not invite_button:
                raise Exception("Invite button not found")
            
            # Click invite button
            invite_button.click()
            time.sleep(3)
            
            # Wait for invite modal to appear
            modal_selectors = [
                '//div[contains(text(), "Invite members to the") and contains(text(), "workspace")]',
                '//h2[contains(text(), "Invite members")]',
                '//div[@role="dialog"]'
            ]
            
            modal_found = False
            for selector in modal_selectors:
                if self._wait_and_find_element(By.XPATH, selector, timeout=10):
                    modal_found = True
                    break
            
            if not modal_found:
                raise Exception("Failed to click invite button")
            
            time.sleep(3)
            
            # Wait for invite modal/form to appear
            # Based on screenshot, look for email input in the modal
            email_input_selectors = [
                '//input[@placeholder="Enter email address"]',
                '//div[contains(@class, "emails")]//input',
                '//input[@type="email"]'
            ]
            
            email_input = None
            for selector in email_input_selectors:
                email_input = self._wait_and_find_element(By.XPATH, selector, timeout=10)
                if email_input:
                    break
            
            if not email_input:
                raise Exception("Email input field not found in invite form")
            
            # Fill email field
            email_input.clear()
            email_input.send_keys(member_email)
            time.sleep(1)
            
            # Select Member role from dropdown (based on screenshot)
            role_selectors = [
                '//select[@name="role"]',
                '//div[contains(@class, "role")]//select',
                '//button[contains(text(), "Member") and contains(@class, "dropdown")]'
            ]
            
            # Find role dropdown and select Member
            for selector in role_selectors:
                role_element = self._wait_and_find_element(By.XPATH, selector, timeout=5)
                if role_element:
                    try:
                        # If it's a select dropdown (most likely based on screenshot)
                        if role_element.tag_name == 'select':
                            from selenium.webdriver.support.ui import Select
                            select = Select(role_element)
                            # Select Member role (default option)
                            try:
                                select.select_by_visible_text('Member')
                                self.logger.info("Selected Member role from dropdown")
                            except:
                                try:
                                    select.select_by_value('member')
                                    self.logger.info("Selected member role by value")
                                except:
                                    # Member is usually the default, so continue
                                    self.logger.info("Using default Member role")
                    except Exception as e:
                        self.logger.warning(f"Could not set role to Member: {str(e)}")
                    break
            
            # Look for send invite button
            # Based on screenshot, look for "Next" button
            send_selectors = [
                '//button[contains(text(), "Next")]',
                '//button[contains(text(), "Send")]',
                '//button[contains(text(), "Invite") and not(contains(text(), "Invite member"))]',
                '//button[@type="submit"]'
            ]
            
            send_button = None
            for selector in send_selectors:
                send_button = self._wait_and_find_element(By.XPATH, selector, timeout=10)
                if send_button and send_button.is_enabled():
                    break
            
            if not send_button:
                raise Exception("Send invite button not found or not enabled")
            
            # Click send button
            send_button.click()
            time.sleep(5)
            
            # Wait for confirmation
            success_indicators = [
                '//div[contains(text(), "invited")]',
                '//div[contains(text(), "sent")]',
                '//div[contains(text(), "success")]',
                '//div[contains(text(), "Invitation sent")]',
                '//div[contains(text(), "Member added")]'
            ]
            
            for indicator in success_indicators:
                if self._wait_and_find_element(By.XPATH, indicator, timeout=10):
                    self.logger.info(f"Successfully invited member: {member_email}")
                    return True
            
            # If no success message, check if the email appears in pending invitations
            if self.verify_invitation_status(member_email):
                self.logger.info(f"Invitation verified for: {member_email}")
                return True
            
            raise Exception("No confirmation of successful invitation")
            
        except Exception as e:
            self.logger.error(f"Failed to invite member {member_email}: {str(e)}")
            self._take_screenshot("invite_failed")
            return False
    
    def verify_invitation_status(self, member_email):
        """Verify if invitation was sent successfully"""
        try:
            self.logger.info(f"Verifying invitation status for: {member_email}")
            
            # Look for the email in pending invitations or member list
            email_elements = self.driver.find_elements(By.XPATH, f'//*[contains(text(), "{member_email}")]')
            
            if email_elements:
                self.logger.info(f"Found {member_email} in team management page")
                return True
            
            # Try refreshing the page and checking again
            self.driver.refresh()
            time.sleep(5)
            
            email_elements = self.driver.find_elements(By.XPATH, f'//*[contains(text(), "{member_email}")]')
            
            return len(email_elements) > 0
            
        except Exception as e:
            self.logger.error(f"Failed to verify invitation status: {str(e)}")
            return False
    
    def process_invitation(self, member_email, admin_id=None, admin_email=None, admin_password=None, team_url=None):
        """Complete invitation process"""
        try:
            self.logger.info(f"Starting invitation process for {member_email}")
            
            # Get admin credentials if not provided
            if not admin_email or not admin_password:
                admin_info = get_next_admin()
                if not admin_info:
                    raise Exception("No active admin accounts available")
                
                admin_id = admin_info['id']
                admin_email = admin_info['email']
                admin_password = admin_info['password']
            
            # Use default team URL if not provided
            if not team_url:
                team_url = "https://chatgpt.com/admin?tab=members"
            
            # Initialize driver
            if not self._setup_driver():
                if admin_id:
                    mark_admin_failure(admin_id)
                raise Exception("Failed to setup WebDriver")
            
            # Login
            if not self.login(admin_email, admin_password):
                if admin_id:
                    mark_admin_failure(admin_id)
                raise Exception("Login failed")
            
            # Navigate to team management
            if not self.navigate_to_team_management(team_url):
                if admin_id:
                    mark_admin_failure(admin_id)
                raise Exception("Failed to navigate to team management")
            
            # Send invitation
            if not self.invite_member(member_email):
                if admin_id:
                    mark_admin_failure(admin_id)
                raise Exception("Failed to send invitation")
            
            # Verify invitation
            if not self.verify_invitation_status(member_email):
                self.logger.warning(f"Could not verify invitation status for {member_email}")
            
            # Mark admin as successful
            if admin_id:
                mark_admin_success(admin_id)
            
            self.logger.info(f"Invitation process completed successfully for {member_email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Invitation process failed: {str(e)}")
            if admin_id:
                mark_admin_failure(admin_id)
            self._take_screenshot("process_failed")
            return False
        finally:
            self.close()
    
    def close(self):
        """Close the browser and clean up"""
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("WebDriver closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing WebDriver: {str(e)}")

# Factory function for easy instantiation
def create_inviter(headless=True, timeout=30):
    """Create and return a ChatGPTTeamInviter instance"""
    return ChatGPTTeamInviter(headless=headless, timeout=timeout)
