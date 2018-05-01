import unittest

from flask_monitoringdashboard.test.utils import set_test_environment, clear_db, add_fake_data, get_test_app, \
    test_admin_secure


class TestMeasurement(unittest.TestCase):

    def setUp(self):
        set_test_environment()
        clear_db()
        add_fake_data()
        self.app = get_test_app()

    def test_overview(self):
        """
            Just retrieve the content and check if nothing breaks
        """
        test_admin_secure(self, 'measurements/overview')

    def test_version_usage(self):
        """
            Just retrieve the content and check if nothing breaks
        """
        test_admin_secure(self, 'measurements/version_usage')

    def test_heatmap(self):
        """
            Just retrieve the content and check if nothing breaks
        """
        test_admin_secure(self, 'measurements/heatmap')

    def test_page_number_of_requests_per_endpoint(self):
        """
            Just retrieve the content and check if nothing breaks
        """
        test_admin_secure(self, 'measurements/requests')

    def test_page_boxplot_per_version(self):
        """
            Just retrieve the content and check if nothing breaks
        """
        test_admin_secure(self, 'measurements/versions')

    def test_page_boxplot_per_endpoint(self):
        """
            Just retrieve the content and check if nothing breaks
        """
        test_admin_secure(self, 'measurements/endpoints')
