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
import pytz
from tzlocal import get_localzone

URL_ADD_ABSTRACT = 'student_add_abstract'
URL_UPLOAD_SYOPSIS = 'student_upload_synopsis'
URL_UPLOAD_THESIS = 'student_upload_thesis'
URL_ADD_KEYWORDS = 'student_add_keywords'
URL_VIEW_PHD_STATUS = 'student_phd_status'
URL_USER_EDIT_PROFILE = 'user_edit_profile'

from django.test import TestCase

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
    
    def logout(self):
        """
        Performs logout action for the current logged in user. Assumes that there's
        a logout button in the sidebar's footer buttons.
        """
        logout_button = self.driver.find_element_by_id('footer-button-logout')
        logout_button.click()
        self.wait_until_page_loads('Login')

    def _remove_root(self, str):
        """
        Removes the root domain part of a URL.
        http://localhost:8081/student/abstract/ -> /student/abstract/
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

    def _check_if_element_exists(self, css_selector):
        """
        Checks if an element with the specified 'css_selector' exists.
        Returns True / False accordingly.

        Args:
            css_selector: string, css selector string , eg. '#thesis-id .thesis-class input'
        """

        return len(self.driver.find_elements_by_css_selector(css_selector)) > 0
        
    def check_homepage(self):
        """
        Goes and veryifies the contents of the user homepage. Checks if the
        content displayed is valid. Assumes that driver is already on homepage.
        """
        self._check_element_contents(self.driver.find_element_by_class_name("profile_info"), self.full_name)
        self._check_element_contents(self.driver.find_element_by_class_name("user-profile"), self.full_name)
        self._check_element_contents(self.driver.find_element_by_id("user-name"), self.full_name)
        self._check_link(self.driver.find_element_by_id("user-edit-profile"), reverse(URL_USER_EDIT_PROFILE))

    def wait_until_page_loads(self, new_page_title, timeout = 10):
        """
        Makes the Selenium driver to wait unit the new page has completely loaded.
        Uses expected conditions to acheive this. Making the timeout 5sec can mess up things.

        Args:
            new_page_title: string, A substring of the new loading page's title
            timeout: int, seconds for timeout, DEFAULT_VALUE = 10
        """

        element = WebDriverWait(self.driver, timeout).until(EC.title_contains(new_page_title))
        element = WebDriverWait(self.driver, timeout).until(EC.text_to_be_present_in_element_value(
            (By.NAME, "page-load-status"), 'done'))

    def wait_until_element_is_invisible(self, locator, timeout = 10):
        """
        Makes the Selenium driver to wait unit the new page has completely loaded.
        Uses expected conditions to acheive this. Making the timeout 5sec can mess up things.

        Args:
            locator: locator, eg. (By.CSS_SELECTOR, "#tab_content1 blockquote")
            timeout: int, seconds for timeout, DEFAULT_VALUE = 10
        """

        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))

    def go_to_notifications_page(self, check = False):
        """
        Uses the side navbar to navigate to the notifications page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            check: False by default, set to True to check the validity of data displayed on the page
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

        if check:
            self.check_notifications_page()

    def check_notifications_page(self):
        """
        Goes to and veryifies the contents of the user notifications page. Checks if
        the content displayed is valid. Assumes driver is at required page.
        """
        unread_notifications_count = int(self.driver.find_element_by_id('unread-notifications-count').text)
        read_notifications_count = int(self.driver.find_element_by_id('read-notifications-count').text)
        actual_unread = Notification.objects.filter(receiver = self.user).filter(status = 'U')
        actual_read = Notification.objects.filter(receiver = self.user).filter(status = 'R')
        actual_unread_count = len(actual_unread)
        actual_read_count = len(actual_read)

        self.assertEqual(unread_notifications_count, actual_unread_count)
        self.assertEqual(read_notifications_count, actual_read_count)

        date = datetime.now(get_localzone())    # used for date matching
        zone = date.tzinfo.zone                 # used for date matching
        local = pytz.timezone(zone)             # used for date matching
        unread_notifications_displayed = self.driver.find_elements_by_css_selector('#tab_content1 blockquote')
        match_count = 0

        for unread_notification_displayed in unread_notifications_displayed:
            message = unread_notification_displayed.find_element_by_class_name('notification-message').text
            sender = unread_notification_displayed.find_element_by_class_name('notification-sender').text
            sender = User.objects.get(username = sender)
            naive_date = parse(unread_notification_displayed.find_element_by_class_name('notification-date').text)
            local_dt = local.localize(naive_date, is_dst=None)
            utc_dt = local_dt.astimezone (pytz.utc)
            
            if actual_unread.filter(message = message).filter(sender = sender) \
                    .filter(date__year = utc_dt.year, date__month = utc_dt.month, date__day = utc_dt.day,
                    date__hour = utc_dt.hour, date__minute = utc_dt.minute).exists():
                    # checks date accuracy upto minutes
                match_count += 1
        
        self.driver.find_element_by_id('read-notifications-count').click()
        self.wait_until_element_is_invisible((By.CSS_SELECTOR, "#tab_content1 blockquote"))
        self.assertEqual(match_count, actual_unread_count)

        read_notifications_displayed = self.driver.find_elements_by_css_selector('#tab_content2 blockquote')
        match_count = 0
        
        for read_notification_displayed in read_notifications_displayed:
            message = read_notification_displayed.find_element_by_class_name('notification-message').text
            sender = read_notification_displayed.find_element_by_class_name('notification-sender').text
            sender = User.objects.get(username = sender)
            naive_date = parse(read_notification_displayed.find_element_by_class_name('notification-date').text)
            local_dt = local.localize(naive_date, is_dst=None)
            utc_dt = local_dt.astimezone (pytz.utc)
            
            if actual_read.filter(message = message).filter(sender = sender) \
                    .filter(date__year = utc_dt.year, date__month = utc_dt.month, date__day = utc_dt.day,
                    date__hour = utc_dt.hour, date__minute = utc_dt.minute).exists():
                    # checks date accuracy upto minutes
                match_count += 1

        self.assertEqual(match_count, actual_read_count)

    def go_to_edit_profile_page(self, check = False):
        """
        Uses the side navbar to navigate to the Edit profile page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            check: False by default, set to True to check the validity of data displayed on the page
        """
        timeout = 10    # seconds
        new_page_title = 'Edit Profile'
        link = self.driver.find_element_by_id("url-user-edit-profile")

        if not link.is_displayed():
            self.driver.find_element_by_id("child-menu-general").click()
            element = self.driver.find_element_by_class_name('current-page')
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'current-page')))
            
        link.click()

        if check:
            self.wait_until_page_loads(new_page_title)

    def go_to_homepage(self, check = False):
        """
        Uses the side navbar to navigate to the User profile page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            check: False by default, set to True to check the validity of data displayed on the page
        """
        timeout = 10    # seconds
        new_page_title = 'Home'
        link = self.driver.find_element_by_id("url-user-profile")

        if not link.is_displayed():
            self.driver.find_element_by_id("child-menu-general").click()
            element = self.driver.find_element_by_class_name('current-page')
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'current-page')))
            
        link.click()
        self.wait_until_page_loads(new_page_title)

        if check:
            self.check_homepage()

    def check_if_notification_exists(self, message, sender, date, read = False):
        """
        Checks if the receiver has a particular notification or not.
        Assumes driver is logged in as receiver (user object) and is on Notifications page.
        
        Args:
            message: string, the notification text
            sender: string, username of the sender
            date: datetime, date sent for the notification
            read: bool, True if notification is supposed to be read, or False otherwise
        Returns:
            True: if notification exists
            False: if not
        """
        result = False
        print('\nRequired message = ' + message)
        print('\nRequired sender = ' + sender)
        print('\nRequired date = ' + str(date))


        if not read:
            self.driver.find_element_by_id('unread-notifications-count').click()
            self.wait_until_element_is_invisible((By.CSS_SELECTOR, "#tab_content2 blockquote"))
            unread_notifications = self.driver.find_elements_by_css_selector('#tab_content1 blockquote')
            match_count = 0

            for notification in unread_notifications:
                notification_message = notification.find_element_by_class_name('notification-message').text
                notification_sender = notification.find_element_by_class_name('notification-sender').text
                notification_date = parse(notification.find_element_by_class_name('notification-date').text)

                if sender == notification_sender and message == notification_message and \
                    (date - notification_date).total_seconds() < 30:
                    result = True
                    break
        else:
            self.driver.find_element_by_id('read-notifications-count').click()
            self.wait_until_element_is_invisible((By.CSS_SELECTOR, "#tab_content1 blockquote"))
            read_notifications = self.driver.find_elements_by_css_selector('#tab_content2 blockquote')
            match_count = 0

            for notification in read_notifications:
                notification_message = notification.find_element_by_class_name('notification-message').text
                notification_sender = notification.find_element_by_class_name('notification-sender').text
                notification_date = parse(notification.find_element_by_class_name('notification-date').text)

                if sender == notification_sender and message == notification_message and \
                    (date - notification_date).total_seconds() < 30:    # within a 30 sec difference
                    result = True
                    break

        self.assertEqual(result, True)
