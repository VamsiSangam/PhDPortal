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

URL_ADD_ABSTRACT = 'student_add_abstract'
URL_UPLOAD_SYOPSIS = 'student_upload_synopsis'
URL_UPLOAD_THESIS = 'student_upload_thesis'
URL_ADD_KEYWORDS = 'student_add_keywords'
URL_VIEW_PHD_STATUS = 'student_phd_status'

class StudentTests(UserTests):
    def __init__(self, username, password, driver, methodName = 'runTest'):
        """
        Constructor

        Args:
            username: string
            password: string
            driver: Selenium WebDriver instance
        """

        super().__init__(username, password, driver, methodName)
        self.student = self.user.student
        self.full_name = self.student.first_name + ' ' + self.student.last_name
        self.thesis = Thesis.objects.get(student = self.student)
        self.thesis_guides = ThesisGuide.objects.filter(thesis = self.thesis)
        
    def check_homepage(self):
        """
        Veryifies the contents of the student homepage. Checks if the content displayed is
        valid. Assumes that 'driver' is at the student homepage.

        Args:
            driver: webdriver.Firefox() or webdriver.Chrome(), depending on tests
        """

        super(StudentTests, self).check_homepage()
        
        if self.thesis.title is not None:
            self._check_element_contents(self.driver.find_element_by_id("thesis-title"), self.thesis.title)

        if self.thesis.abstract is not None:
            self._check_element_contents(self.driver.find_element_by_id("thesis-abstract"), self.thesis.abstract)
    
        # for checking guides displayed
        html_list = self.driver.find_element_by_id('student-guides')
        items = html_list.find_elements_by_tag_name('li')
        matches = 0

        for item in items:
            guide_name = item.find_element_by_class_name('thesis-guide-name').text
            guide_type = item.find_element_by_class_name('thesis-guide-type').text
            guide_profile_link = item.find_element_by_class_name('thesis-guide-profile-link').get_attribute('href')
            guide_profile_link = self._remove_root(guide_profile_link)

            for thesis_guide in ThesisGuide.objects.filter(thesis = self.thesis):
                type = 'Guide' if thesis_guide.type == 'G' else 'Co-guide'
                guide = thesis_guide.guide
                full_name = guide.first_name + ' ' + guide.last_name
                profile_link = '/user/profile/' + guide.user.username + '/'

                if guide_name == full_name and guide_type == type and guide_profile_link == profile_link:
                    matches += 1

        actual_guide_count = ThesisGuide.objects.filter(thesis = self.thesis).count()
        
        self.assertEqual(len(items), actual_guide_count)    # number of displayed guides = actual_guide_count
        self.assertEqual(matches, actual_guide_count)       # guides properly matched = actual_guide_count
        self._check_link(self.driver.find_element_by_id("button-add-abstract"), reverse(URL_ADD_ABSTRACT))
        self._check_link(self.driver.find_element_by_id("button-upload-synopsis"), reverse(URL_UPLOAD_SYOPSIS))
        self._check_link(self.driver.find_element_by_id("button-upload-thesis"), reverse(URL_UPLOAD_THESIS))
        self._check_link(self.driver.find_element_by_id("button-add-keywords"), reverse(URL_ADD_KEYWORDS))
        self._check_link(self.driver.find_element_by_id("button-view-phd-status"), reverse(URL_VIEW_PHD_STATUS))

    def go_to_submit_phd_abstract(self):
        """
        Uses the side navbar to navigate to the Submit PhD Abstract page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            driver: webdriver.Firefox() or webdriver.Chrome(), depending on tests
        """
        timeout = 10    # seconds
        new_page_title = 'Abstract'
        link = self.driver.find_element_by_id("url-phd-abstract")

        if not link.is_displayed():
            self.driver.find_element_by_id("child-menu-abstract").click()
            element = self.driver.find_element_by_class_name('current-page')
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'current-page')))
            
        link.click()
        self.wait_until_page_loads(new_page_title)

    def go_to_upload_synopsis(self):
        """
        Uses the side navbar to navigate to the Upload Synopsis page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            driver: webdriver.Firefox() or webdriver.Chrome(), depending on tests
        """
        timeout = 10    # seconds
        new_page_title = 'Upload Synopsis'
        link = self.driver.find_element_by_id("url-upload-synopsis")

        if not link.is_displayed():
            self.driver.find_element_by_id("child-menu-synopsis").click()
            element = self.driver.find_element_by_class_name('current-page')
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'current-page')))
            
        link.click()
        self.wait_until_page_loads(new_page_title)

    def go_to_view_synopsis(self):
        """
        Uses the side navbar to navigate to the View uploaded Synopsis page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            driver: webdriver.Firefox() or webdriver.Chrome(), depending on tests
        """
        timeout = 10    # seconds
        new_page_title = 'View Synopsis'
        link = self.driver.find_element_by_id("url-view-synopsis")

        if not link.is_displayed():
            self.driver.find_element_by_id("child-menu-synopsis").click()
            element = self.driver.find_element_by_class_name('current-page')
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'current-page')))
            
        link.click()
        self.wait_until_page_loads(new_page_title)

    def go_to_upload_thesis(self):
        """
        Uses the side navbar to navigate to the Upload Thesis document page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            driver: webdriver.Firefox() or webdriver.Chrome(), depending on tests
        """
        timeout = 10    # seconds
        new_page_title = 'Upload Thesis'
        link = self.driver.find_element_by_id("url-upload-thesis")

        if not link.is_displayed():
            self.driver.find_element_by_id("child-menu-thesis").click()
            element = self.driver.find_element_by_class_name('current-page')
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'current-page')))
            
        link.click()
        self.wait_until_page_loads(new_page_title)

    def go_to_view_thesis(self):
        """
        Uses the side navbar to navigate to the Upload Thesis document page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            driver: webdriver.Firefox() or webdriver.Chrome(), depending on tests
        """
        timeout = 10    # seconds
        new_page_title = 'View Thesis'
        link = self.driver.find_element_by_id("url-view-thesis")

        if not link.is_displayed():
            self.driver.find_element_by_id("child-menu-thesis").click()
            element = self.driver.find_element_by_class_name('current-page')
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'current-page')))
            
        link.click()
        self.wait_until_page_loads(new_page_title)

    def go_to_add_keywords(self):
        """
        Uses the side navbar to navigate to the Add Keywords page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            driver: webdriver.Firefox() or webdriver.Chrome(), depending on tests
        """
        timeout = 10    # seconds
        new_page_title = 'Add Keywords'
        link = self.driver.find_element_by_id("url-add-keywords")

        if not link.is_displayed():
            self.driver.find_element_by_id("child-menu-thesis").click()
            element = self.driver.find_element_by_class_name('current-page')
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'current-page')))
            
        link.click()
        self.wait_until_page_loads(new_page_title)

    def go_to_view_phd_status(self):
        """
        Uses the side navbar to navigate to the View PhD status page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            driver: webdriver.Firefox() or webdriver.Chrome(), depending on tests
        """
        timeout = 10    # seconds
        new_page_title = 'Status'
        link = self.driver.find_element_by_id("url-view-phd-status")

        if not link.is_displayed():
            self.driver.find_element_by_id("child-menu-status").click()
            element = self.driver.find_element_by_class_name('current-page')
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'current-page')))
            
        link.click()
        self.wait_until_page_loads(new_page_title)