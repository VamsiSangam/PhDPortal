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
STATUS_ID_SUBMIT_ABSTRACT = 5

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

    def _update_instance_variables(self):
        """
        Instance variables which are ORM objects need to be updated (queried again)
        if they were externally modified (say, by the application logic instead of test logic)
        This method updates those instance variables
        """
        self.thesis = Thesis.objects.get(student = self.student)
        
    def check_homepage(self):
        """
        Veryifies the contents of the student homepage. Checks if the content displayed is
        valid. Assumes that 'driver' is at the student homepage.
        """

        super(StudentTests, self).check_homepage()

        self._check_element_contents(self.driver.find_element_by_id("user-email"), self.student.email)
        
        if self.thesis.title is not None and len(self.thesis.title) > 0:
            self.assertEqual(self.driver.find_element_by_id("thesis-title").text, self.thesis.title)

        if self.thesis.abstract is not None and len(self.thesis.abstract) > 0:
            self.assertEqual(self.driver.find_element_by_id("thesis-abstract").text, self.thesis.abstract)
    
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

    def go_to_submit_phd_abstract(self, check = False):
        """
        Uses the side navbar to navigate to the Submit PhD Abstract page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.
        Also verifes the contents of the page.

        Args:
            check: False by default, set to True to check the validity of data displayed on the page
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

        if check:
            self.check_abstract_page()

    def go_to_upload_synopsis(self, check = False):
        """
        Uses the side navbar to navigate to the Upload Synopsis page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            check: False by default, set to True to check the validity of data displayed on the page
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

    def go_to_view_synopsis(self, check = False):
        """
        Uses the side navbar to navigate to the View uploaded Synopsis page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            check: False by default, set to True to check the validity of data displayed on the page
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

    def go_to_upload_thesis(self, check = False):
        """
        Uses the side navbar to navigate to the Upload Thesis document page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            check: False by default, set to True to check the validity of data displayed on the page
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

    def go_to_view_thesis(self, check = False):
        """
        Uses the side navbar to navigate to the Upload Thesis document page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            check: False by default, set to True to check the validity of data displayed on the page
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

    def go_to_add_keywords(self, check = False):
        """
        Uses the side navbar to navigate to the Add Keywords page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            check: False by default, set to True to check the validity of data displayed on the page
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

    def go_to_view_phd_status(self, check = False):
        """
        Uses the side navbar to navigate to the View PhD status page by clicking on
        the appropriate links. Assumes that the side navbar is NOT collapsed.

        Args:
            check: False by default, set to True to check the validity of data displayed on the page
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

    def check_edit_profile_page(self):
        """
        Veryifies the contents of the Edit Profile.
        Checks if the content displayed is valid.
        Assumes that driver is already at required page.
        """
        first_name = self.driver.find_element_by_id("first-name")
        last_name = self.driver.find_element_by_id("last-name")
        email = self.driver.find_element_by_id("email")

        self.assertEqual(first_name.get_attribute('value'), self.student.first_name)
        self.assertEqual(first_name.get_attribute('disabled') is not None, True)
        self.assertEqual(last_name.get_attribute('value'), self.student.last_name)
        self.assertEqual(last_name.get_attribute('disabled') is not None, True)
        self.assertEqual(email.get_attribute('value'), self.student.email)
        self.assertEqual(email.get_attribute('disabled') is not None, True)

    def check_abstract_page(self):
        """
        Veryifies the contents of the Add PhD Abstract page.
        Checks if the content displayed is valid.
        Assumes that the driver is at the required page.
        """

        if self.thesis.status.id == STATUS_ID_SUBMIT_ABSTRACT:
            abstract_element = self.driver.find_element_by_id('abstract')
            self.assertEqual(abstract_element.is_displayed(), True)
            self.assertEqual(abstract_element.get_attribute('disabled'), None)

            if self.thesis.abstract is not None:
                self.assertEqual(abstract_element.text, self.thesis.abstract)
        else:
            self.assertEqual(self._check_if_element_exists('#abstract'), False)

    def submit_phd_abstract(self, abstract):
        """
        Submits PhD abstract. Assumes driver is on Submit PhD abstract page.
        Assumes the student can submit a PhD abstract.

        Args:
            abstract: string, abstract text
        """
        abstract_element = self.driver.find_element_by_name('abstract')
        abstract_element.clear()
        abstract_element.send_keys(abstract)

        submit_button = self.driver.find_element_by_id('submit')
        submit_button.click()
        self.wait_until_element_is_invisible((By.NAME, 'abstract'))
        self._update_instance_variables()

    def check_abstract_displayed_on_homepage(self, abstract):
        """
        Checks if the abstract displayed on homepage is equal to the
        given input 'abstract'. Assumes driver is on homepage.

        Args:
            abstract: string, abstract text
        """
        self.assertEqual(self.driver.find_element_by_id("thesis-abstract").text, abstract)

    def _check_if_element_exists(self, css_selector):
        """
        Checks if an element with the specified 'css_selector' exists.
        Returns True / False accordingly.

        Args:
            css_selector: string, css selector string , eg. '#thesis-id .thesis-class input'
        """

        return len(self.driver.find_elements_by_css_selector(css_selector)) > 0

    def check_submission_pages(self, abstract, upload_synopsis, view_synopsis, upload_thesis, view_thesis, keywords, status_id):
        """
        Checks all the submission pages. Eg. - If 'abstract' is True, then method checks if the student has an
        abstract submission box visible. Eg. - If 'upload_synopsis' is False, then method checks if the student
        is restricted from uploading a synopsis file.
        TODO: Add status_id check

        Args:
            abstract: bool, stating whether student should be able to submit abstract
            upload_synopsis: bool, stating whether student should be able to upload synopsis
            view_synopsis: bool, stating whether student should be able to view synopsis
            upload_synopsis: bool, stating whether student should be able to upload synopsis
            upload_thesis: bool, stating whether student should be able to upload thesis
            view_thesis: bool, stating whether student should be able to view thesis
            keywords: bool, stating whether student should be able to add keywords
            status_id: int, to check if status page is dispaying the mentioned status
        """

        # Abstract
        self.go_to_submit_phd_abstract()
        self.assertEqual(self._check_if_element_exists('#abstract'), abstract)

        # Upload Synopsis
        self.go_to_upload_synopsis()
        self.assertEqual(self._check_if_element_exists('#file-upload'), upload_synopsis)
        
        # View synopsis
        self.go_to_view_synopsis()
        self.assertEqual(self._check_if_element_exists('#synopsis'), view_synopsis)

        # Upload thesis
        self.go_to_upload_thesis()
        self.assertEqual(self._check_if_element_exists('#file-upload'), upload_thesis)

        # View thesis
        self.go_to_view_thesis()
        self.assertEqual(self._check_if_element_exists('#thesis'), view_thesis)

        # Add Keywords
        self.go_to_add_keywords()
        self.assertEqual(self._check_if_element_exists('#selected-keywords'), keywords)
        self.assertEqual(self._check_if_element_exists('#keywords-list-group'), keywords)
