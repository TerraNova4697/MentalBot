import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    # TABLES
    def create_table_workers(self):
        sql = """
        CREATE TABLE Workers (
            user_id int NOT NULL,
            name varchar(255) NOT NULL,
            surname varchar(255) NOT NULL,
            patronym varchar(255) NOT NULL,
            status varchar NOT NULL,
            PRIMARY KEY (user_id)
            );
        """
        self.execute(sql, commit=True)

    # STRINGS FORMATTING
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    # Workers table operations
    def add_worker(self, user_id: int, name: str, surname: str, patronym: str, status: str = "Active"):
        sql = "INSERT INTO Workers(user_id, name, surname, patronym, status) VALUES(?, ?, ?, ?, ?)"
        self.execute(sql, parameters=(user_id, name, surname, patronym, status), commit=True)

    def select_all_workers_user_id(self, **kwargs):
        sql = "SELECT user_id FROM Workers WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")

