from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_locator = (By.ID, "user-name")  # Locator for username field
        self.password_locator = (By.ID, "password")  # Locator for password field
        self.login_button_locator = (By.ID, "login-button")  # Locator for login button
        self.error_message = (By.XPATH, "//h3[@data-test='error']")  # Locator for error message
        self.url = "https://www.saucedemo.com/"  # URL of the login page

    def navigate_to_login_page(self):
        # Navigates to the login page
        self.driver.get(self.url)

    def enter_username(self, username):
        # Enters the username in the username field
        self.driver.find_element(*self.username_locator).send_keys(username)

    def enter_password(self, password):
        # Enters the password in the password field
        self.driver.find_element(*self.password_locator).send_keys(password)

    def click_login_button(self):
        # Clicks on the login button
        self.driver.find_element(*self.login_button_locator).click()

    def login(self, username, password):
        # Performs the login action by entering the username, password, and clicking the login button
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def is_logged_in(self):
        # Checks if the user is successfully logged in
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH,
                                                                                   "//span[@class='title' "
                                                                                   "and text()='Products']")))
            return True
        except TimeoutException:
            return False

    def check_login_failure(self):
        # Checks if a login failure occurred by verifying the error message
        error_element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.error_message)
        )
        error_message = error_element.text
        return "Epic sadface: Username and password do not match any user in this service" in error_message

    def is_user_locked_out(self):
        # Checks if the user is locked out by verifying the error message
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//h3[@data-test='error']")))
            error_element = self.driver.find_element(*self.error_message)
            error_message = error_element.text
            return "Epic sadface: Sorry, this user has been locked out." in error_message
        except TimeoutException:
            return False
