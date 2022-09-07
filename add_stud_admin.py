import mysql.connector as db


class AddStudentAdmin:
    def __init__(self):
        self.my_database = db.connect(
            host="localhost",
            user="root",
            passwd="mbuthi4390",
            database="school_demo_2",
        )
        self.database_cursor = self.my_database.cursor()
        self.database_cursor.execute("CREATE TABLE IF NOT EXISTS student"
                                     "(admission_number VARCHAR(20) NOT NULL,"
                                     "first_name VARCHAR(20) NOT NULL,"
                                     "last_name VARCHAR(20) NOT NULL,"
                                     "city VARCHAR(20),"
                                     "password VARCHAR(80),"
                                     "course VARCHAR(30) ,"
                                     "PRIMARY KEY (admission_number))")
        self.insert_student = "INSERT INTO student(admission_number, first_name, last_name, city)" \
                              "VALUES(%s, %s, %s, %s)"
        self.check_id_query = "SELECT (admission_number) FROM student"
        self.student_id = []

    def add_function(self, admission_number, first_name, last_name, city):
        values = (admission_number, first_name, last_name, city)
        self.database_cursor.execute(self.insert_student, values)
        self.my_database.commit()
        self.my_database.close()

    def check_id_exists(self):
        self.database_cursor.execute(self.check_id_query)
        student_adm_no = self.database_cursor.fetchall()
        return student_adm_no
