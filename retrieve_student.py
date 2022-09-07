import mysql.connector as db


class RetrieveStudent:
    def __init__(self):
        self.my_database = db.connect(
            user="root",
            host="localhost",
            passwd="mbuthi4390",
            database="school_demo_2"
        )
        self.database_cursor = self.my_database.cursor()
        self.get_student_details_ = "SELECT admission_number, first_name, last_name, city" \
                                    " FROM student"

    def get_student_details(self):
        self.database_cursor.execute(self.get_student_details_)
        # student_details = self.database_cursor.fetchall()
        # print(student_details)
        return self.database_cursor.fetchall()
