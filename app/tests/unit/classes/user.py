from app.tests.testing_utilities import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.models import *
from django.core.urlresolvers import reverse
from django.db.models import Q
from dateutil.parser import parse
from datetime import datetime

URL_ADD_ABSTRACT = 'student_add_abstract'
URL_UPLOAD_SYOPSIS = 'student_upload_synopsis'
URL_UPLOAD_THESIS = 'student_upload_thesis'
URL_ADD_KEYWORDS = 'student_add_keywords'
URL_VIEW_PHD_STATUS = 'student_phd_status'
URL_USER_EDIT_PROFILE = 'user_edit_profile'

class UserTests(TestCase):
    def __init__(self, username, password, driver, methodName = 'runTest'):
        """
        Constructor

        Args:
            username: string
            password: string
        """

        super().__init__(methodName)
        self.username = username
        self.password = password
        self.driver = driver
        self.user = User.objects.get(username = username)

    def login(self):
        """
        Logins from the login page using the credentials stored in this
        object. Checks if user is redirected to homepage.

        Args:
            driver: webdriver.Firefox() or webdriver.Chrome(), depending on tests
        """

        self.driver.get(LOGIN_URL)
        self.wait_until_page_loads('Login')
        self.assertIn("Login", self.driver.title)
        elem = self.driver.find_element_by_name("username")
        elem.send_keys(self.username)
        elem = self.driver.find_element_by_name("password")
        elem.send_keys(self.password)
        elem.send_keys(Keys.RETURN)
        # TODO: change the ine below to a proper wait unit page fully loads condition
        self.wait_until_page_loads('Home')
        self.assertIn("Home", self.driver.title)
    
    def _remove_root(self, str):
        """
        Removes the root domain part of a URL.
        http://localhost:8000/student/abstract/ -> /student/abstract/
        """

        str = str[str.index('/', 7):]
        return  str

    def _check_element_contents(self, element, content):
        """
        Checks if a tag is visible and checks if it's
        contents have 'content' parameter as a substring

        Args:
            element: WebElement object, anchor tag element selected from the DOM
            content: string, string to check if it is present inside the element
        """

        self.assertTrue(element.is_displayed(), True)
        self.assertTrue(content in element.text, True)

    def _check_link(self, element, href):
        """
        Checks if an 'a' tag is visible and checks if it's href
        attribute is same as that of the parameter 'href'

        Args:
            element: WebElement object, anchor tag element selected from the DOM
            href: string, link without domain, eg. /student/abstract/
        """

        self.assertTrue(element.is_displayed(), True)
        self.assertEqual(self._remove_root(element.get_attribute('href')), href)
        
    def check_homepage(self):
        """
        Veryifies the contents of the user homepage. Checks if the content displayed is
        valid. Assumes that 'driver' is at the user homepage.

        Args:
            driver: webdriver.Firefox() or webdriver.Chrome(), depending on tests
        """

        self._check_element_contents(self.driver.find_element_by_class_name("profile_info"), self.full_name)
        self._check_element_contents(self.driver.find_element_by_class_name("user-profile"), self.full_name)
        self._check_element_contents(self.driver.find_element_by_id("user-name"), self.full_name)
        self._check_element_contents(self.driver.find_element_by_id("user-email"), self.student.email)
        self._check_link(self.driver.find_element_by_id("user-edit-profile"), reverse(URL_USER_EDIT_PROFILE))

    def wait_until_page_loads(self, new_page_title, timeout = 5):
        """
        Makes the Selenium driver to wait unit the new page has completely loaded.
        Uses expected conditions to acheive this.

        Args:
            new_page_title: string, A substring of the new loading page's title
            timeout: int, seconds for timeout, DEFAULT_VALUE = 5
        """

        element = WebDriverWait(self.driver, timeout).until(EC.title_contains(new_page_title))
        element = WebDriverWait(self.driver, timeout).until(EC.text_to_be_present_in_element_value(
            (By.NAME, "page-load-status"), 'done'))

    def go_to_notifications_page(self):
        """
        Uses the side navbar to navigate to the notifications page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            driver: webdriver.Firefox() or webdriver.Chrome(), depending on tests
        """
        timeout = 10    # seconds
        new_page_title = 'Notifications'
        link = self.driver.find_element_by_id("url-user-notifications")

        if not link.is_displayed():
            self.driver.find_element_by_id("child-menu-general").click()
            element = self.driver.find_element_by_class_name('current-page')
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'current-page')))
            
        link.click()
        self.wait_until_page_loads(new_page_title)

    def check_notifications_page(self):
        """
        Veryifies the contents of the user homepage. Checks if the content displayed is
        valid. Assumes that 'driver' is at the Notifications page.

        Args:
            driver: webdriver.Firefox() or webdriver.Chrome(), depending on tests
        """
        unread_notifications_count = int(self.driver.find_element_by_id('unread-notifications-count').text)
        read_notifications_count = int(self.driver.find_element_by_id('read-notifications-count').text)
        actual_unread = Notification.objects.filter(receiver = self.user).filter(status = 'U')
        actual_read = Notification.objects.filter(receiver = self.user).filter(status = 'R')
        actual_unread_count = len(actual_unread)
        actual_read_count = len(actual_read)

        self.assertEqual(unread_notifications_count, actual_unread_count)
        self.assertEqual(read_notifications_count, actual_read_count)

        unread_notifications_displayed = self.driver.find_elements_by_css_selector('#tab_content1 blockquote')
        match_count = 0

        for unread_notification_displayed in unread_notifications_displayed:
            message = unread_notification_displayed.find_element_by_class_name('notification-message').text
            sender = unread_notification_displayed.find_element_by_class_name('notification-sender').text
            sender = User.objects.get(username = sender)
            date = parse(unread_notification_displayed.find_element_by_class_name('notification-date').text)

            if actual_unread.filter(message = message).filter(sender = sender) \
                    .filter(date__year = date.year, date__month = date.month, date__day = date.day,
                    date__hour = date.hour, date__minute = date.minute, date__second = date.second).exists():
                match_count += 1

        self.assertEqual(match_count, actual_unread_count)

        read_notifications_displayed = self.driver.find_elements_by_css_selector('#tab_content2 blockquote')
        match_count = 0

        for read_notification_displayed in read_notifications_displayed:
            message = read_notification_displayed.find_element_by_class_name('notification-message').text
            print(message)
            sender = read_notification_displayed.find_element_by_class_name('notification-sender').text
            print(sender)
            sender = User.objects.get(username = sender)
            date = parse(read_notification_displayed.find_element_by_class_name('notification-date').text)

            if actual_read.filter(message = message).filter(sender = sender) \
                    .filter(date__year = date.year, date__month = date.month, date__day = date.day,
                    date__hour = date.hour, date__minute = date.minute, date__second = date.second).exists():
                match_count += 1

        self.assertEqual(match_count, actual_read_count)


    def go_to_edit_profile_page(self):
        """
        Uses the side navbar to navigate to the Edit profile page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            driver: webdriver.Firefox() or webdriver.Chrome(), depending on tests
        """
        timeout = 10    # seconds
        new_page_title = 'Edit Profile'
        link = self.driver.find_element_by_id("url-user-edit-profile")

        if not link.is_displayed():
            self.driver.find_element_by_id("child-menu-general").click()
            element = self.driver.find_element_by_class_name('current-page')
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'current-page')))
            
        link.click()
        self.wait_until_page_loads(new_page_title)