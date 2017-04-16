from app.tests.testing_utilities import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.models import *
from django.core.urlresolvers import reverse
from django.db.models import Q
from app.tests.unit.classes.user import UserTests

STATUS_ID_SUBMIT_ABSTRACT = 5

class GuideTests(UserTests):
    def __init__(self, username, password, driver, methodName = 'runTest'):
        """
        Constructor

        Args:
            username: string
            password: string
            driver: Selenium WebDriver instance
        """

        super().__init__(username, password, driver, methodName)
        self.faculty = self.user.faculty
        self.full_name = self.faculty.first_name + ' ' + self.faculty.last_name

    def _update_instance_variables(self):
        """
        Instance variables which are ORM objects need to be updated (queried again)
        if they were externally modified (say, by the application logic instead of test logic)
        This method updates those instance variables
        """
        
    def check_homepage(self):
        """
        Veryifies the contents of the student homepage. Checks if the content displayed is
        valid. Assumes that 'driver' is at the student homepage.
        """

        super(GuideTests, self).check_homepage()

        self._check_element_contents(self.driver.find_element_by_id("user-email"), self.faculty.email)
    
    def check_edit_profile_page(self):
        """
        Veryifies the contents of the Edit Profile. Checks if the content displayed is
        valid. Assumes that 'driver' is at the Edit Profile page.
        """
        
        first_name = self.driver.find_element_by_id("first-name")
        last_name = self.driver.find_element_by_id("last-name")
        email = self.driver.find_element_by_id("email")

        self.assertEqual(first_name.get_attribute('value'), self.faculty.first_name)
        self.assertEqual(first_name.get_attribute('disabled') is not None, True)
        self.assertEqual(last_name.get_attribute('value'), self.faculty.last_name)
        self.assertEqual(last_name.get_attribute('disabled') is not None, True)
        self.assertEqual(email.get_attribute('value'), self.faculty.email)
        self.assertEqual(email.get_attribute('disabled') is not None, True)

    # start with goto pages
    def go_to_abstract_evalutation_page(self):
        """
        Uses the side navbar to navigate to the Unevaluated PhD Abstracts page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.
        TODO: Also verifes the contents of the page.
        """
        timeout = 10    # seconds
        new_page_title = 'Abstract'
        link = self.driver.find_element_by_id("url-evaluate-abstract")

        if not link.is_displayed():
            self.driver.find_element_by_id("child-menu-evaluation").click()
            element = self.driver.find_element_by_class_name('current-page')
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'current-page')))
            
        link.click()
        self.wait_until_page_loads(new_page_title)

    def go_to_synopsis_evalutation_page(self):
        """
        Uses the side navbar to navigate to the Unevaluated PhD Synopsis page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.
        TODO: Also verifes the contents of the page.
        """
        timeout = 10    # seconds
        new_page_title = 'Synopsis'
        link = self.driver.find_element_by_id("url-evaluate-synopsis")

        if not link.is_displayed():
            self.driver.find_element_by_id("child-menu-evaluation").click()
            element = self.driver.find_element_by_class_name('current-page')
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'current-page')))
            
        link.click()
        self.wait_until_page_loads(new_page_title)

    def go_to_thesis_evalutation_page(self):
        """
        Uses the side navbar to navigate to the Unevaluated PhD Thesis page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.
        TODO: Also verifes the contents of the page.
        """
        timeout = 10    # seconds
        new_page_title = 'Thesis'
        link = self.driver.find_element_by_id("url-evaluate-thesis")

        if not link.is_displayed():
            self.driver.find_element_by_id("child-menu-evaluation").click()
            element = self.driver.find_element_by_class_name('current-page')
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'current-page')))
            
        link.click()
        self.wait_until_page_loads(new_page_title)

    def evaluate_abstract(self, id, approve, feedback = None):
        """
        Evaluates a submitted abstract. Assumes that driver is already
        on the required evaluation page.

        Args:
            id: int, ID of thesis in Thesis model
            approve: bool, True for approval, False for rejection
            feedback: string, optional feedback string
        """

        self.assertEqual(self._check_if_element_exists('#thesis-' + str(id)), True)
        
        thesis = self.driver.find_element_by_id('thesis-' + str(id))
        button_class = 'btn-success' if approve else 'btn-danger'
        timeout = 10
        button = thesis.find_element_by_class_name(button_class)

        if not button.is_displayed():
            title = thesis.find_element_by_class_name('panel-title')
            title.click()
            WebDriverWait(thesis, timeout).until(EC.element_to_be_clickable((By.CLASS_NAME, button_class)))

        feedback_box = thesis.find_element_by_id('thesis-feedback-' + str(id))
        feedback_box.send_keys(feedback)
        button.click()
        self.wait_until_element_is_invisible((By.ID, 'thesis-' + str(id)))