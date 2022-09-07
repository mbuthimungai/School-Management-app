import mysql.connector as db
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class AddTeacherAdmin:
    def __init__(self):
        self.my_database = db.connect(host="localhost",
                                      user="root",
                                      passwd="mbuthi4390",
                                      database="school_demo_2")
        self.database_cursor = self.my_database.cursor()
        self.database_cursor.execute("CREATE TABLE IF NOT EXISTS teachers"
                                     "(user_name VARCHAR(20) NOT NULL,"
                                     "first_name VARCHAR(20) NOT NULL,"
                                     "last_name VARCHAR(20) NOT NULL,"
                                     "phone_number VARCHAR(20) NOT NULL,"
                                     "email_address VARCHAR(20) ,"
                                     "password VARCHAR(80),"
                                     "PRIMARY KEY (user_name))")

        self.sql_insert_query = "INSERT INTO teachers(user_name,first_name,last_name,phone_number) " \
                                "VALUES(%s, %s,%s,%s)"

    def insert_into_teachers(self, u_name, f_name, l_name, phone_num, ):

        values = (u_name, f_name, l_name, phone_num)

        self.database_cursor.execute(self.sql_insert_query, values)

        self.my_database.commit()
        self.my_database.close()

    def check_empty_field(self, u_name, f_name, l_name, phone_num):
        if u_name == "" or f_name == "" or l_name == "" or phone_num == "":
            return False
        else:
            return True

    def is_field_exists(self):
        pass
