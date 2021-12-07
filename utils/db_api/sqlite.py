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

    def create_table_answers(self):
        sql = """
        CREATE TABLE Answers (
            answers_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id int NOT NULL,
            mood int NOT NULL,
            tired int NOT NULL,
            energy int NOT NULL,
            productivity int NOT NULL,
            one_hour varchar NOT NULL,
            colleagues int NOT NULL,
            date varchar NOT NULL,
            month int NOT NULL,
            year int NOT NULL
            );
        """
        self.execute(sql, commit=True)

    def create_table_managers(self):
        sql = """
        CREATE TABLE Managers (
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
            f"{item}=?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    # Workers table operations
    def add_worker(self, user_id: int, name: str, surname: str, patronym: str, status: str = "Active"):
        sql = "INSERT INTO Workers(user_id, name, surname, patronym, status) VALUES(?, ?, ?, ?, ?)"
        self.execute(sql, parameters=(user_id, name, surname, patronym, status), commit=True)

    def select_worker_by_id(self, **kwargs):
        sql = "SELECT * FROM Workers WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_all_workers_user_id(self, **kwargs):
        sql = "SELECT user_id FROM Workers WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_all_workers_by_name(self, **kwargs):
        sql = "SELECT * FROM Workers WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def inactivate_worker(self, user_id: int, status: str = "Inactive"):
        sql = f"""
                UPDATE Workers SET status=? WHERE user_id=?
                """
        return self.execute(sql, parameters=(status, user_id), commit=True)

    # Answers table operations
    def add_answer(self, user_id, mood, tired, energy, productivity, one_hour, colleagues, date, month, year):
        sql = """
        INSERT INTO Answers(user_id, mood, tired, energy, productivity, one_hour, colleagues, date, month, year) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql,
                     parameters=(user_id, mood, tired, energy, productivity, one_hour, colleagues, date, month, year),
                     commit=True)

    # Managers table operations
    def select_all_managers_user_id(self, **kwargs):
        sql = "SELECT user_id FROM Managers WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def add_manager(self, user_id: int, name: str, surname: str, patronym: str, status: str = "NotActive"):
        sql = "INSERT INTO Managers(user_id, name, surname, patronym, status) VALUES(?, ?, ?, ?, ?)"
        self.execute(sql, parameters=(user_id, name, surname, patronym, status), commit=True)

    def select_manager_by_user_id(self, **kwargs):
        sql = "SELECT name, surname, patronym FROM Managers WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def update_manager(self, user_id: int, status: str):
        sql = f"""
                UPDATE Managers SET status=? WHERE user_id=?
                """
        return self.execute(sql, parameters=(status, user_id), commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
