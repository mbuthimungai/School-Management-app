import mysql.connector as db


class TeacherData:
    def __init__(self):
        self.my_database = db.connect(
            host="localhost",
            user="root",
            passwd="mbuthi4390",
            database="School_Demo_2"
        )
        self.database_cursor = self.my_database.cursor()
        self.sql_stmt = "SELECT user_name,first_name,last_name,phone_number,email_address FROM teachers"
        # self.delete_sql_stmt = "DELETE FROM teachers WHERE user_name = %s "

    def get_teacher_vals(self):
        self.database_cursor.execute(self.sql_stmt)
        teachers_vals = self.database_cursor.fetchall()
        self.my_database.commit()
        self.my_database.close()

        return teachers_vals

