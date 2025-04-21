import unittest
from app import get_db_connection

class TestDatabaseConnection(unittest.TestCase):
    def test_get_db_connection_valid(self):
        valid_url = "postgresql://user:password@host:port/database"
        conn = get_db_connection(valid_url)
        self.assertIsNotNone(conn)
        conn.close()

    def test_get_db_connection_invalid(self):
        invalid_url = "invalid_url"
        conn = get_db_connection(invalid_url)
        self.assertIsNone(conn)

if __name__ == '__main__':
    unittest.main()
