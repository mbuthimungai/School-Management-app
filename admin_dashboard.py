import mysql.connector as db


class AdminDashboardUpdate:
    def __init__(self):
        self.my_database = db.connect(
            host="localhost",
            user="root",
            passwd="mbuthi4390",
            database="school_demo_2",
        )
        self.database_cursor = self.my_database.cursor()
        self.database_cursor.execute("SELECT COUNT(*) FROM administrators")
        self.number_of_rows = self.database_cursor.fetchall()[0][0]
        self.database_cursor.execute("SELECT COUNT(*) FROM teachers")
        self.number_of_rows_teachers = self.database_cursor.fetchall()[0][0]
        self.database_cursor.execute("SELECT COUNT(*) FROM student")
        self.number_of_rows_students = self.database_cursor.fetchall()[0][0]

