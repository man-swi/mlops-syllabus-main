import unittest
from unittest.mock import patch
from app import app, get_db_connection, create_todos_table_if_not_exists

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_main_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_todos_page_empty(self):
        with patch('app.get_db_connection') as mock_get_db_connection:
            mock_get_db_connection.return_value.cursor.return_value.fetchall.return_value = []
            response = self.app.get('/todos')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b"No todos found.")
    
    def test_todos_page_with_data(self):
        with patch('app.get_db_connection') as mock_get_db_connection:
            mock_get_db_connection.return_value.cursor.return_value.fetchall.return_value = [
                (1, "Todo 1"),
                (2, "Todo 2")
            ]
            response = self.app.get('/todos')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Todo 1", response.data)
            self.assertIn(b"Todo 2", response.data)

    def test_create_todos_table(self):
        with patch('psycopg2.connect') as mock_connect:
            create_todos_table_if_not_exists()
            mock_connect.return_value.cursor.return_value.execute.assert_called_once_with(
                'CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY,description text)'
            )

if __name__ == '__main__':
    unittest.main()
