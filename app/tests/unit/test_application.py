from app.tests.testing_utilities import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from app.tests.unit.classes.student import StudentTests
from app.tests.unit.classes.guide import GuideTests
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from datetime import datetime

class ApplicationTests(StaticLiveServerTestCase):
    """
    Tests the whole application work flow starting from
    student login to evaluation of thesis by referees
    """

    fixtures = ['data.json',]

    def setUp(self):
        self.driver = webdriver.Firefox()
        super(ApplicationTests, self).setUp()

    def test_abstract_submission(self, partial = False):
        """
        Tests if the student is able to submit PhD abstract or not.

        Args:
            partial: False by default. Set to True if you want to execute this
                     method partially as a means to progressively build upon this test.

        Returns:
            state: dict object. A dictionary object which has keys and values which
                   have information about the progress in the application workflow.
        """
        driver = self.driver
        student = StudentTests('anshul', 'HelloWorld', driver)
        
        state = {}
        state['student'] = student
        
        student.login()
        student.go_to_submit_phd_abstract()
        state['abstract'] = 'I, ' + student.full_name + ' will be working on ' + student.thesis.title + '.'
        state['abstract'] += """ One of the first applications of digital images was in the newspaper industry,
                                when pictures were first sent by submarine cable between London and
                                New York. Introduction of the Bartlane cable picture transmission system
                                in the early 1920s reduced the time required to transport a picture across
                                the Atlantic from more than a week to less than three hours."""
        
        student.submit_phd_abstract(state['abstract'])

        if not partial:
            student.go_to_homepage()
            student.check_abstract_displayed_on_homepage(abstract)
            student.check_submission_pages(False, False, False, False, False, False, 6)
        
        student.logout()

        return state

    def test_abstract_rejection_first_guide(self, partial = False):
        """
        Tests if the application handles the case when one of the two
        guides (or maybe one guide) rejects the student's abstract.

        Args:
            partial: False by default. Set to True if you want to execute this
                     method partially as a means to progressively build upon this test.

        Returns:
            state: dict object. A dictionary object which has keys and values which
                   have information about the progress in the application workflow.
        """
        state = self.test_abstract_submission(True)
        
        guide = GuideTests('ranjana', 'HelloWorld', self.driver)
        guide.login()
        guide.go_to_abstract_evalutation_page()
        state['abstract-reject-feedback'] = 'Please be more technical in your abstract description.'
        date_rejection = datetime.now()
        guide.evaluate_abstract(id, False, state['abstract-reject-feedback'])
        guide.logout()

        if not partial:
            # check student notification
            student = state['student']
            student.login()
            student.go_to_notifications_page()
            message = guide.full_name + " had rejected the abstract submitted."
            message += " Feedback - " + feedback
            student.check_if_notification_exists(message, guide.username, date_rejection)
            student.logout()

            # RESUME here : check other guides' notification


    def dummy(self):
        guide = GuideTests('sonali', 'HelloWorld', self.driver)
        guide.login()
        guide.go_to_abstract_evalutation_page()
        date = datetime.now()
        guide.evaluate_abstract(id, True, 'Nice!')
        guide.logout()
        
        student = StudentTests('anshul', 'HelloWorld', driver)
        student.login()
        student.go_to_notifications_page()
        message = guide.full_name + " had accepted the abstract submitted."
        sender = guide.username
        student.check_if_notification_exists(message, sender, date)
        student.logout()

    def tearDown(self):
        self.driver.close()
        super(ApplicationTests, self).tearDown()