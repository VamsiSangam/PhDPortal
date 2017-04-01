from app.tests.testing_utilities import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from app.tests.unit.classes.student import StudentTests

class ApplicationTests(TestCase):
    """
    Tests the whole application work flow starting from
    student login to evaluation of thesis by referees
    """

    fixtures = ['data.json',]

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test(self):
        driver = self.driver
        student = StudentTests('anshul', 'HelloWorld', driver)

        student.login()
        student.check_homepage()
        student.go_to_notifications_page()

        #student.check_notifications_page()
        
    def tearDown(self):
        self.driver.quit()