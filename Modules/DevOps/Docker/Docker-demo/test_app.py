import unittest
from unittest.mock import patch, MagicMock

from app import get_container_details, get_db_connection

class TestContainerDetails(unittest.TestCase):
    def test_get_container_details(self):
        details = get_container_details()
        self.assertIsInstance(details, dict)
        self.assertIn('ip_address', details)
        self.assertIn('hostname', details)
        self.assertIn('os', details)
        self.assertIn('architecture', details)
        self.assertIn('docker_image', details)
        self.assertIn('hosts_file', details)
        self.assertIsInstance(details['os'], str)
        self.assertIsInstance(details['docker_image'], str)
        self.assertIsInstance(details['hosts_file'], str)

    def test_get_container_details_hosts_file(self):
        details = get_container_details()
        self.assertIn('/etc/hosts', details['hosts_file'])

    def test_get_container_details_hosts_file_error(self):
        with unittest.mock.patch('builtins.open', side_effect=Exception('Test Exception')):
            details = get_container_details()
            self.assertEqual(details['hosts_file'], 'Test Exception')

        self.assertIsInstance(details['ip_address'], str)
        self.assertIsInstance(details['hostname'], str)
        self.assertIsInstance(details['os'], str)
        self.assertIsInstance(details['architecture'], str)

    @patch('psycopg2.connect')
    def test_get_db_connection(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        conn = get_db_connection()
        self.assertEqual(conn, mock_conn)
        mock_connect.assert_called_once_with(os.environ['DATABASE_URL'])

if __name__ == '__main__':
    unittest.main()
