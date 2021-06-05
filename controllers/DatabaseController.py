from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, ForeignKey, Boolean, create_engine, select, text,
                        insert)
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Dict, Tuple
from .types import User, DiffObject, TransactionObject, PortfolioObject, PortfolioDiff
from uuid import uuid4

Base = declarative_base()


class DatabaseController:
    """
    This class is responsible for interfacing any actions to the database
    """

    conn_string = "mysql+pymysql://root:alpha298@localhost:3306/test_schema"
    connection = None
    metadata = MetaData()
    engine = None
    sns_client = None
    later_tables: Dict[str, Table] = {}

    # Default table structure
    groups = Table('groups',
                   metadata,
                   Column('uuid', String(50), primary_key=True),
                   Column('group_name', String(24), index=True),
                   Column('group_leader', String(28))
                   )
    global_transactions = Table('global_transactions',
                                metadata,
                                Column('transaction_id', String(50), primary_key=True),
                                Column('timestamp', DateTime()),
                                Column('order_type', String(8)),
                                Column('currency', String(5)),
                                Column('paid_with', String(5)),
                                Column('order_amount', Numeric(24, 10)),
                                Column('from', String(1028)),
                                Column('to', String(1028))
                                )
    portfolio_updates = Table('portfolio_updates',
                              metadata,
                              Column('portfolio_id', String(50), primary_key=True),
                              Column('portfolio', String(2056)),
                              Column('date_of_update', DateTime()),
                              Column('username', String(28), index=True)
                              )
    users = Table('users',
                  metadata,
                  Column('user_id', String(50), primary_key=True),
                  Column('username', String(28), index=True)
                  )

    def delete_everything(self):
        self.metadata.drop_all(self.engine)
        self.later_tables = {}

    def create_table(self, table_name: str, columns: List[Column]):
        self.later_tables[table_name] = (Table(table_name, self.metadata, *columns))
        self.metadata.create_all(self.engine)

    def db_init(self, conn_string) -> None:
        self.engine = create_engine(conn_string)
        self.connection = self.engine.connect()

    def initialize_tables(self) -> List[str]:
        """
        This resets tables back to default state. No groups. No users. No transactions...
        :return: List of current table names
        """
        self.metadata.create_all(self.engine)
        table_names = list(self.metadata.tables.keys())
        return table_names

    def create_new_group(self, group_name: str, group_leader: str) -> str:
        """
        Creates a new group and appoints a new leader as the first member of the
        newly created group.
        :param group_name: Name of the group
        :param group_leader: User whose role is leader of the group
        :return: UUID of the new group table
        """
        new_uuid = str(uuid4()).replace("-", "_")
        new_group_sql = (insert(self.groups).values(uuid=new_uuid, group_name=group_name, group_leader=group_leader))
        new_table_columns = [
            Column('role', String(6)),
            Column('username', String(28), primary_key=True),
            Column('joined_date', DateTime())
        ]
        self.create_table(new_uuid, new_table_columns)
        self.connection.execute(new_group_sql)
        return new_uuid

    def add_user_to_group(self, role: str, username: str, group_name: str) -> None:
        """
        Adds a user to the group and sets up database tables to
        hold their data
        :param role: The assigned role of this new user, relative to the group
        :param username: The username chosen for this user
        :param group_name: The group the user will join
        :return: Nothing...
        """

    def get_users_from_group(self, group_name: str) -> List[User]:
        """
        Retrieves a list of all of the users
        :param group_name: name of the group to index
        :return: A list containing User objects
        """

    def get_group_id_from_name(self, group_name: str) -> str:
        """
        Returns a groupID that matches the specified groupName
        :param group_name:
        :return: A string representing the groupID of the group
        """

    def delete_group(self, group_id: str) -> None:
        """
        Deletes a group from the database, but not its users.
        :param group_id: The ID of the group to be deleted
        :return: Nothing...
        """

    def delete_user_from_group(self, username: str, groupID: str) -> None:
        """
        Deletes a user from the group, but not from the global system
        :param username: The username of the user
        :param groupID: The ID of the group the user is to be removed from
        :return: Nothing...
        """

    def update_user_role(self, group_name: str, username: str) -> None:
        """
        Changes the role of the user to one of:
            leader (max 1)\n
            player (max 9)
        :param group_name: Name of the group
        :param username: Name of the user
        :return: Nothing...
        """

    def update_username(self, group_name: str, username: str) -> None:
        """
        Changes the username of the user
        :param group_name: name of the group the user belongs to
        :param username: name of the user
        :return: nothing
        """

    def setup_new_user(self, username: str) -> None:
        """
        Create database tables for the new user including:
            1. Adding user to global users table
            2. Creating new transactions table for user
            3. Creating new notifications table for user
        :param username: name of the user
        :return: Nothing...
        """

    def add_new_transaction(self,
                            order_type: str,
                            currency: str,
                            paid_with: str,
                            order_amount: float,
                            from_obj: DiffObject,
                            to_obj: DiffObject) -> None:
        """
        *There are NO 'update' or 'delete' methods for use with transactions*\n
        This method:
            1. Adds a new row to the global transactions table
            2. Creates a new portfolio update for each user involved in the transaction
            3. Add a pair (transaction ID, portfolio update) to each user's individual portfolio update table
        :param order_type: Type of order (BUY or SELL)
        :param currency: Currency that will go to the receiver (BTC, ETH, XLM, etc.)
        :param paid_with: Currency used to make the transaction (USD, EUR, etc.)
        :param order_amount: Number of units bought or sold
        :param from_obj: DiffObject describing the flow of money FROM involved parties
                {
                    'user': 0000.00,
                    'sheldon256: 200
                }
        :param to_obj: DiffObject describing the flow of money TO involved parties
                {
                    'user': 0000.00,
                    'marcus23: 200
                }
        :return: Nothing...
        """

    def add_portfolio_update(self, username: str, portfolio_diff_obj: PortfolioDiff) -> None:
        """
        *There are NO 'update' or 'delete' methods for use with portfolio updates*\n
        Makes a new record for portfolio updates. Auto increments portfolio ID.
        :param username:
        :param portfolio_diff_obj: An object representing the change in the user's currency ownership
        :return: Nothing...
        """

    def get_transaction(self, transaction_id: str) -> TransactionObject:
        """
        Gathers all of the data from a particular transaction, referencing based on the ID of the transaction
        :param transaction_id: the ID of the transaction
        :return: A TransactionObject (Tuple) that holds information on the transaction in question
        """

    def get_latest_portfolio_update(self, username: str) -> PortfolioObject:
        """
        Get the latest portfolio update for a particular user.
        :param username: Name of the user
        :return: A PortfolioObject (Tuple) that holds information about the user's most current portfolio
        """

    def get_portfolio_update(self, username: str, portfolio_id: str) -> PortfolioObject:
        """
        Get a particular portfolio update based on the id.
        :param username: Name of the user
        :param portfolio_id: The ID of the portfolio you'd like to get information on
        :return: A PortfolioObject(Tuple) that holds information about the portfolio you've picked out.
        """

    def get_user_transactions(self, username: str, entire: bool = False) -> List[TransactionObject]:
        """
        Retrieves a list of the user's transactions. Default limit is 10 at a time. However, if
        the *entire* parameter is set to 'True', this method will fetch ALL of the transactions for a specific
        user since the beginning of their account creation.
        :param username: Name of the user
        :param entire: Boolean indicating whether to go above the default limit of 20 transaction records
        :return: List of TransactionObjects
        """

    def get_user_portfolio_updates(self, username: str, entire: bool = False) -> List[PortfolioObject]:
        """
        Retrieves a list of the user's portfolio updates. Default limit is 5 at a time. However, this can be overridden
        using the 'entire' parameter if necessary. Doing so will result in ALL of the user's portfolio updates being
        fetched.
        :param username: Name of the user
        :param entire: Boolean indicating whether to go above the default limit of 5 portfolio updates
        :return: List of PortfolioObjects
        """
