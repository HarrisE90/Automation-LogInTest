import json
import pytest
import logging
from selenium import webdriver
from Resources.Pages.login_page import LoginPage


@pytest.fixture(scope="class")
def setup(request):
    # Set up the Chrome webdriver
    driver = webdriver.Chrome()
    # Maximize the browser window
    driver.maximize_window()
    # Instantiate the LoginPage object
    login_page = LoginPage(driver)

    with open('Data/test_data.json') as file:
        # Load the test data from the JSON file
        test_data = json.load(file)

    # Set up logging
    log_file = "../Output/test_log.log"
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')
    logging.info('This is an informational log message')
    logging.error('An error occurred')

    # Pass the necessary objects to the test class
    request.cls.driver = driver
    request.cls.login_page = login_page
    request.cls.test_data = test_data

    yield

    # Quit the browser after the test
    driver.quit()


@pytest.mark.usefixtures("setup")
class TestLogin:

    def test_successful_login(self):
        # Get the test data for successful login
        credentials = self.test_data['valid_credentials'][0]
        username = credentials['username']
        password = credentials['password']

        # Navigate to the login page
        self.login_page.navigate_to_login_page()

        # Login
        self.login_page.login(username, password)

        # Verify successful login
        assert self.login_page.is_logged_in()

    def test_failed_login_invalid_username(self):
        # Get the test data for failed login with invalid username
        credentials = self.test_data['invalid_credentials'][0]
        username = credentials['username']
        password = self.test_data['valid_credentials'][0]['password']

        # Navigate to the login page
        self.login_page.navigate_to_login_page()

        # Login
        self.login_page.login(username, password)

        # Verify login failure
        assert self.login_page.check_login_failure()

    def test_failed_login_invalid_password(self):
        # Get the test data for failed login with invalid password
        credentials = self.test_data['valid_credentials'][0]
        username = credentials['username']
        password = self.test_data['invalid_credentials'][0]['password']

        # Navigate to the login page
        self.login_page.navigate_to_login_page()

        # Login
        self.login_page.login(username, password)

        # Verify login failure
        assert self.login_page.check_login_failure()

    def test_failed_login_locked_user(self):
        # Get the test data for failed login with locked user
        credentials = self.test_data['locked_credentials'][0]
        username = credentials['username']
        password = credentials['password']

        # Navigate to the login page
        self.login_page.navigate_to_login_page()

        # Login
        self.login_page.login(username, password)

        # Verify login failure due to locked user
        assert self.login_page.is_user_locked_out()

    def test_successful_login_different_browser(self):
        # Get the test data for successful login
        credentials = self.test_data['valid_credentials'][0]
        username = credentials['username']
        password = credentials['password']

        # Set up the Edge webdriver
        edge_driver = webdriver.Edge()
        # Maximize the browser window
        edge_driver.maximize_window()

        # Instantiate the LoginPage object for Edge browser
        edge_login_page = LoginPage(edge_driver)

        # Pass the Edge login page object to the test class
        self.login_page = edge_login_page

        # Navigate to the login page
        self.login_page.navigate_to_login_page()

        # Login
        self.login_page.login(username, password)

        # Verify successful login
        assert self.login_page.is_logged_in()

        # Quit the Edge browser
        edge_driver.quit()

if __name__ == '__main__':
    pytest.main(['-v', '-s', '--html=Output/Login_Test_Report.html', '--self-contained-html'])
