from django.test import TestCase
from typing import List
from controllers.DatabaseController import DatabaseController
from sqlalchemy import text, select, Table
from controllers.types import GroupMemberRow
import pprint
import sys

test_conn_string = "mysql+pymysql://root:alpha298@localhost:3306/test_schema"


def handle_error(e: Exception):
    tb = sys.exc_info()[2]
    raise e.with_traceback(tb)


class BaseDatabaseTester:
    db_controller = None
    pp = pprint.PrettyPrinter(indent=4)

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
    group_name = "Jammin"
    group_leader = "marcus254"

    def group_setup(self):
        new_group_id = self.db_controller.create_new_group(self.group_name, self.group_leader)

    def test_create_new_group(self):
        try:
            self.setup()

            group_name = "Jammin"
            group_leader = "marcus254"

            new_group_id = self.db_controller.create_new_group(group_name, group_leader)
            self.assertIn(new_group_id, self.db_controller.later_tables.keys())
            self.assertIn(new_group_id, list(self.db_controller.metadata.tables.keys()))

            self.cleanup()
        except Exception as e:
            self.cleanup()
            handle_error(e)

    def test_add_user_to_group(self):
        try:
            self.setup()
            self.group_setup()

            role = "player"
            username = "sheldon256"
            group_name = "Jammin"

            self.db_controller.add_user_to_group(role, username, group_name)

            # Get group id from group name
            group_id = self.db_controller.get_group_id_from_name(group_name)
            group_table: Table = dict(self.db_controller.metadata.tables)[group_id]
            group_members_sql = select(group_table)
            group_members: List[GroupMemberRow] = list(self.db_controller.connection.execute(group_members_sql))

            # Check if group has the correct members
            expected_members = [
                ('leader', self.group_leader),
                ('player', username)
            ]
            for member_index, member in enumerate(group_members):
                for column_index, column in enumerate(member):
                    if column_index < len(member) - 1:
                        self.assertEqual(column, expected_members[member_index][column_index],
                                         "One leader and one player should be present in the group table")

            self.cleanup()
        except Exception as e:
            self.cleanup()
            handle_error(e)


