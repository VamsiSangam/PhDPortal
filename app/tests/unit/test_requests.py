from app.tests.testing_utilities import *

class RequestTests(TestCase):
    fixtures = ['test-data.json',]

    def setUp(self):
        self.client = Client()
    
    def check_url(self, url, method, data = None, follow = True, status_code = STATUS_CODE_OK):
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

        self.assertEqual(response.status_code, status_code)

    def test_student_views(self):
        login(self.client, username = 'rit2013063', password = 'HelloWorld')

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

        self.client.logout()