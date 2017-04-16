from app.tests.testing_utilities import *
from django.test import TestCase

class RequestTests(TestCase):
    fixtures = ['data.json',]

    def setUp(self):
        """
        Initial setup before running any test method in this class
        """
        self.client = Client()
    
    def check_url(self, url, method, data = None, follow = True, status_code = STATUS_CODE_OK):
        """
        Checks a given URL by sending a request of the type specified. The status code
        returned after sending the request is checked with 'status_code'.
        Assertion passess or fails accordingly. "OTHER" in method parameter denotes every
        HTTP request type other than GET or POST, eg. PUT, PATCH, DELETE etc. "ANY" denotes
        all the available HTTP request types.

        Args:
            url: string, url to which a request is to be sent
            method: string, "GET" or "POST" or "OTHER" or "ANY"
            data: dictionary, consisting the request data to be sent
            follow: bool, if the url is redirected to somewhere, should it follow?
            status_code: int, expected status code

        Default val of Args:
            data = None
            follow = True
            status_code = STATUS_CODE_OK, which is 200
        """

        response = None
        
        if method == GET:
            response = self.client.get(url, data = data, follow = follow)
        elif method == POST:
            response = self.client.post(url, data = data, follow = follow)
        elif method == OTHER:     # for testing other HTTP requests, must return BAD_REQUEST
            response = self.client.put(url, data = data, follow = follow)
            self.assertEqual(response.status_code, status_code)
            response = self.client.patch(url, data = data, follow = follow)
            logger.info(response.content)
            self.assertEqual(response.status_code, status_code)
            response = self.client.delete(url, data = data, follow = follow)
            self.assertEqual(response.status_code, status_code)
            response = self.client.head(url, data = data, follow = follow)
            self.assertEqual(response.status_code, status_code)
            response = self.client.options(url, data = data, follow = follow)
            self.assertEqual(response.status_code, status_code)
            response = self.client.trace(url, data = data, follow = follow)
        else:
            response = self.client.get(url, data = data, follow = follow)
            self.assertEqual(response.status_code, status_code)
            response = self.client.post(url, data = data, follow = follow)
            self.assertEqual(response.status_code, status_code)
            response = self.client.put(url, data = data, follow = follow)
            self.assertEqual(response.status_code, status_code)
            response = self.client.patch(url, data = data, follow = follow)
            logger.info(response.content)
            self.assertEqual(response.status_code, status_code)
            response = self.client.delete(url, data = data, follow = follow)
            self.assertEqual(response.status_code, status_code)
            response = self.client.head(url, data = data, follow = follow)
            self.assertEqual(response.status_code, status_code)
            response = self.client.options(url, data = data, follow = follow)
            self.assertEqual(response.status_code, status_code)
            response = self.client.trace(url, data = data, follow = follow)
        
        self.assertEqual(response.status_code, status_code)

        return response

    def test_student_views(self):
        """
        Test method. Sends a request to every URL available to student to
        check if the view is working or not.
        """

        self.check_url('', GET)
        login(self.client, username = 'anshul', password = 'HelloWorld')

        self.check_url('/user/profile/', GET)
        self.check_url('/user/profile/dinesh/', GET)
        self.check_url('/user/notifications/', GET)
        self.check_url('/user/edit_profile/', GET)

        self.check_url('/student/abstract/', GET)
        self.check_url('/student/synopsis/upload/', GET)
        self.check_url('/student/synopsis/view/', GET)
        self.check_url('/student/thesis/upload/', GET)
        self.check_url('/student/thesis/view/', GET)
        self.check_url('/student/keywords/', GET)
        self.check_url('/student/help/procedure/', GET)
        self.check_url('/student/help/contacts/', GET)

        self.check_url('/student/abstract/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/student/synopsis/upload/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/student/synopsis/view/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/student/thesis/upload/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/student/thesis/view/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/student/keywords/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/student/keywords/get/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/student/keywords/get/parent/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/student/keywords/add/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/student/help/procedure/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/student/help/contacts/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)

        self.check_url('/logout/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/logout/', GET)

    def test_guide_views(self):
        """
        Test method. Sends a request to every URL available to Guide to
        check if the view is working or not.
        """
        
        self.check_url('', GET)
        login(self.client, username = 'pavan', password = 'HelloWorld')

        self.check_url('/user/profile/', GET)
        self.check_url('/user/profile/dinesh/', GET)
        self.check_url('/user/notifications/', GET)
        self.check_url('/user/edit_profile/', GET)
        self.check_url('/user/search/', GET)
        self.check_url('/user/search/query/', POST, data = {
            'first_name' : 'Neha',
            'last_name' : 'Mishra',
            'email': 'rse2015002@iiita.ac.in',
            'type' : 'S'
        })

        self.check_url('/guide/abstract/unevaluated/', GET)
        self.check_url('/guide/synopsis/unevaluated/', GET)
        self.check_url('/guide/thesis/unevaluated/', GET)
        self.check_url('/guide/panel/', GET)
        self.check_url('/guide/panel/referees/indian/', GET, data = {'term' : 'a'})
        self.check_url('/guide/panel/referees/foreign/', GET, data = {'term' : 'a'})
        self.check_url('/guide/status/', GET)
        self.check_url('/guide/help/procedure/', GET)
        self.check_url('/guide/help/contacts/', GET)

        self.check_url('/guide/abstract/unevaluated/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/guide/synopsis/unevaluated/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/guide/thesis/unevaluated/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/guide/panel/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/guide/panel/referees/indian/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/guide/panel/referees/foreign/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/guide/status/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/guide/help/procedure/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/guide/help/contacts/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)

        self.check_url('/logout/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/logout/', GET)

    def test_director_views(self):
        """
        Test method. Sends a request to every URL available to Director to
        check if the view is working or not.
        """
        
        self.check_url('', GET)
        login(self.client, username = 'gcnandi', password = 'HelloWorld')

        self.check_url('/user/profile/', GET)
        self.check_url('/user/profile/dinesh/', GET)
        self.check_url('/user/notifications/', GET)
        self.check_url('/user/edit_profile/', GET)
        self.check_url('/user/search/', GET)
        self.check_url('/user/search/query/', POST, data = {
            'first_name' : 'Neha',
            'last_name' : 'Mishra',
            'email': 'rse2015002@iiita.ac.in',
            'type' : 'S'
        })

        self.check_url('/director/students/', GET)
        self.check_url('/director/evaluate/', GET)
        self.check_url('/director/help/procedure/', GET)
        self.check_url('/director/help/contacts/', GET)

        self.check_url('/director/students/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/director/evaluate/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/director/help/procedure/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/director/help/contacts/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)

        self.check_url('/logout/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/logout/', GET)

    def test_referee_views(self):
        """
        Test method. Sends a request to every URL available to Referee to
        check if the view is working or not.
        """

        self.check_url('', GET)
        login(self.client, username = 'dennis', password = 'HelloWorld')

        self.check_url('/user/profile/', GET)
        self.check_url('/user/profile/dinesh/', GET)
        self.check_url('/user/notifications/', GET)
        self.check_url('/user/edit_profile/', GET)

        self.check_url('/referee/synopsis/', GET)
        self.check_url('/referee/thesis/', GET)
        self.check_url('/referee/help/procedure/', GET)
        self.check_url('/referee/help/contacts/', GET)

        self.check_url('/referee/synopsis/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/referee/thesis/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/referee/help/procedure/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/referee/help/contacts/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)

        self.check_url('/logout/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/logout/', GET)

    def test_non_student_views(self):
        """
        Test method. Sends a request to every URL which a student is not
        allowed to access and checks if application responds properly.
        The URLs are accessed by the POV of a Student
        """

        self.check_url('', GET)
        login(self.client, username = 'anshul', password = 'HelloWorld')

        self.check_url('/user/search/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/user/search/query/', ALL, status_code = STATUS_CODE_FORBIDDEN)

        # not allowed to access guide views
        self.check_url('/guide/abstract/unevaluated/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/synopsis/unevaluated/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/thesis/unevaluated/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/panel/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/panel/referees/indian/', ALL, data = {'term' : 'a'}, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/panel/referees/foreign/', ALL, data = {'term' : 'a'}, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/status/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/help/procedure/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/help/contacts/', ALL, status_code = STATUS_CODE_FORBIDDEN)

        # not allowed to access director views
        self.check_url('/director/students/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/director/evaluate/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/director/help/procedure/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/director/help/contacts/', ALL, status_code = STATUS_CODE_FORBIDDEN)

        # not allowed to access referee views
        self.check_url('/referee/synopsis/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/referee/thesis/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/referee/help/procedure/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/referee/help/contacts/', ALL, status_code = STATUS_CODE_FORBIDDEN)

        self.check_url('/logout/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/logout/', GET)

    def test_non_guide_views(self):
        """
        Test method. Sends a request to every URL which a Guide is not
        allowed to access and checks if application responds properly.
        The URLs are accessed by the POV of a Guide
        """

        self.check_url('', GET)
        login(self.client, username = 'pavan', password = 'HelloWorld')

        # not allowed to access student views
        self.check_url('/student/abstract/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/synopsis/upload/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/synopsis/view/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/thesis/upload/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/thesis/view/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/keywords/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/help/procedure/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/help/contacts/', ALL, status_code = STATUS_CODE_FORBIDDEN)

        # not allowed to access director views
        self.check_url('/director/students/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/director/evaluate/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/director/help/procedure/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/director/help/contacts/', ALL, status_code = STATUS_CODE_FORBIDDEN)

        # not allowed to access referee views
        self.check_url('/referee/synopsis/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/referee/thesis/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/referee/help/procedure/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/referee/help/contacts/', ALL, status_code = STATUS_CODE_FORBIDDEN)

        self.check_url('/logout/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/logout/', GET)

    def test_non_director_views(self):
        """
        Test method. Sends a request to every URL which a Director is not
        allowed to access and checks if application responds properly.
        The URLs are accessed by the POV of a Director
        """

        self.check_url('', GET)
        login(self.client, username = 'gcnandi', password = 'HelloWorld')

        # not allowed to access student views
        self.check_url('/student/abstract/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/synopsis/upload/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/synopsis/view/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/thesis/upload/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/thesis/view/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/keywords/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/help/procedure/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/help/contacts/', ALL, status_code = STATUS_CODE_FORBIDDEN)

        # not allowed to access guide views
        self.check_url('/guide/abstract/unevaluated/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/synopsis/unevaluated/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/thesis/unevaluated/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/panel/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/panel/referees/indian/', ALL, data = {'term' : 'a'}, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/panel/referees/foreign/', ALL, data = {'term' : 'a'}, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/status/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/help/procedure/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/help/contacts/', ALL, status_code = STATUS_CODE_FORBIDDEN)

        # not allowed to access referee views
        self.check_url('/referee/synopsis/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/referee/thesis/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/referee/help/procedure/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/referee/help/contacts/', ALL, status_code = STATUS_CODE_FORBIDDEN)

        self.check_url('/logout/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/logout/', GET)

    def test_non_referee_views(self):
        """
        Test method. Sends a request to every URL which a Referee is not
        allowed to access and checks if application responds properly.
        The URLs are accessed by the POV of a Referee
        """
        self.check_url('', GET)
        login(self.client, username = 'dennis', password = 'HelloWorld')

        self.check_url('/user/search/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/user/search/query/', ALL, status_code = STATUS_CODE_FORBIDDEN)

        # not allowed to access student views
        self.check_url('/student/abstract/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/synopsis/upload/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/synopsis/view/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/thesis/upload/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/thesis/view/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/keywords/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/help/procedure/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/student/help/contacts/', ALL, status_code = STATUS_CODE_FORBIDDEN)

        # not allowed to access guide views
        self.check_url('/guide/abstract/unevaluated/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/synopsis/unevaluated/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/thesis/unevaluated/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/panel/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/panel/referees/indian/', ALL, data = {'term' : 'a'}, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/panel/referees/foreign/', ALL, data = {'term' : 'a'}, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/status/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/help/procedure/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/guide/help/contacts/', ALL, status_code = STATUS_CODE_FORBIDDEN)

        # not allowed to access director views
        self.check_url('/director/students/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/director/evaluate/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/director/help/procedure/', ALL, status_code = STATUS_CODE_FORBIDDEN)
        self.check_url('/director/help/contacts/', ALL, status_code = STATUS_CODE_FORBIDDEN)

        self.check_url('/logout/', OTHER, status_code = STATUS_CODE_BAD_REQUEST)
        self.check_url('/logout/', GET)

    def _check_login_redirect(self, response):
        """
        Helper method to check if the user is redirected to the login page
        """

        self.assertEqual(response.redirect_chain[0][0].startswith('/?next='), True)

    def test_login_required_views(self):
        """
        Test method. Sends a request to every URL which expects the
        user to be logged in. The request is sent from the POV of
        a user who has not yet logged in
        """

        response = self.check_url('/user/profile/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/user/profile/dinesh/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/user/notifications/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/user/edit_profile/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/user/search/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/user/search/query/', POST, data = {
            'first_name' : 'Neha',
            'last_name' : 'Mishra',
            'email': 'rse2015002@iiita.ac.in',
            'type' : 'S'
        })
        self._check_login_redirect(response)

        response = self.check_url('/student/abstract/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/student/synopsis/upload/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/student/synopsis/view/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/student/thesis/upload/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/student/thesis/view/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/student/keywords/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/student/help/procedure/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/student/help/contacts/', GET)
        self._check_login_redirect(response)
        
        response = self.check_url('/guide/abstract/unevaluated/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/guide/synopsis/unevaluated/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/guide/thesis/unevaluated/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/guide/panel/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/guide/panel/referees/indian/', GET, data = {'term' : 'a'})
        self._check_login_redirect(response)
        response = self.check_url('/guide/panel/referees/foreign/', GET, data = {'term' : 'a'})
        self._check_login_redirect(response)
        response = self.check_url('/guide/status/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/guide/help/procedure/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/guide/help/contacts/', GET)
        self._check_login_redirect(response)
        
        response = self.check_url('/director/students/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/director/evaluate/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/director/help/procedure/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/director/help/contacts/', GET)
        self._check_login_redirect(response)

        response = self.check_url('/director/students/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/director/evaluate/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/director/help/procedure/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/director/help/contacts/', GET)
        self._check_login_redirect(response)

        response = self.check_url('/referee/synopsis/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/referee/thesis/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/referee/help/procedure/', GET)
        self._check_login_redirect(response)
        response = self.check_url('/referee/help/contacts/', GET)
        self._check_login_redirect(response)

        response = self.check_url('/logout/', GET)
        self._check_login_redirect(response)