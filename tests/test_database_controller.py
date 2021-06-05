from django.test import TestCase
from controllers.DatabaseController import DatabaseController
from sqlalchemy import text

test_conn_string = "mysql+pymysql://root:alpha298@localhost:3306/test_schema"


class BaseDatabaseTester:
    db_controller = None

    def setup(self):
        self.db_controller = DatabaseController()
        self.db_controller.db_init(test_conn_string)
        self.db_controller.initialize_tables()

    def cleanup(self):
        self.db_controller.connection.close()
        self.db_controller.metadata.drop_all(self.db_controller.engine)


class TestDatabaseInitialization(TestCase):
    def test_db_init(self):
        db_controller = DatabaseController()
        db_controller.db_init(test_conn_string)
        self.assertIsNotNone(db_controller.engine)
        self.assertIsNotNone(db_controller.connection)

        # Cleanup
        db_controller.connection.close()
        db_controller.metadata.drop_all(db_controller.engine)

    def test_initialize_tables(self):
        db_controller = DatabaseController()
        db_controller.db_init(test_conn_string)
        db_controller.initialize_tables()
        expected_tables = ['groups', 'global_transactions', 'portfolio_updates', 'users']
        curr_tables = list(db_controller.metadata.tables.keys())
        for table_name in curr_tables:
            sql = text(f"""SELECT * FROM test_schema.{table_name} LIMIT 1""")
            result = db_controller.connection.execute(sql)
            for row in result:
                self.assertIsNone(row, "Should not exist")
        self.assertListEqual(curr_tables, expected_tables, "Database should have the correct tables created")

        # Cleanup
        db_controller.connection.close()
        db_controller.metadata.drop_all(db_controller.engine)


class TestDatabaseAddFeatures(TestCase, BaseDatabaseTester):
    def test_create_new_group(self):
        self.setup()

        group_name = "Jammin"
        group_leader = "marcus254"

        new_group_id = self.db_controller.create_new_group(group_name, group_leader)
        self.assertIn(new_group_id, self.db_controller.later_tables.keys())
        self.assertIn(new_group_id, list(self.db_controller.metadata.tables.keys()))

        self.cleanup()
