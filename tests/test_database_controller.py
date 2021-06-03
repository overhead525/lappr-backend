from django.test import TestCase
from controllers.DatabaseController import DatabaseController
from sqlalchemy import text

test_conn_string = "mysql+pymysql://root:alpha298@localhost:3306/test_schema"


class TestDatabaseInitialization(TestCase):
    def test_db_init(self):
        db_controller = DatabaseController()
        curr_tables = db_controller.db_init(test_conn_string)
        expected_tables = ['groups', 'global_transactions', 'portfolio_updates', 'users']
        for table_name in curr_tables:
            sql = text(f"""SELECT * FROM test_schema.{table_name} LIMIT 1""")
            result = db_controller.connection.execute(sql)
            for row in result:
                self.assertIsNone(row, "Should not exist")
        self.assertListEqual(curr_tables, expected_tables, "Database should have the correct tables created")
