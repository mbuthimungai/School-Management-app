import mysql.connector as db
import bcrypt


class SignUp:
    def __init__(self):
        """This is SignUp class constructor
        When the SignUp class is initialized the constructor is responsible for
        establishing a connection with the database """
        # This self.my_database variable is responsible for the connection
        # with the database
        self.my_database = db.connect(host="localhost", user="root",
                                      passwd="mbuthi4390", database="School_Demo_2")
        self.database_cursor = self.my_database.cursor()
        # The self.database_creation variable is responsible for creating the database School_Demo_2
        # if the database does not exist. It is done when this class is initialised
        self.database_creation = self.database_cursor.execute("CREATE DATABASE IF NOT EXISTS"
                                                              " School_Demo_2")
        self.sql_insert_admin = "INSERT INTO administrators(user_name,phone_number,email,password)" \
                                "VALUES(%s, %s,%s,%s) "
        self.count_num = 0
        self.count_chars = 0
        self.count_symbols = 0

    def create_table(self):
        """Responsible for creating administrators table if it does not exist"""
        self.database_cursor.execute("CREATE TABLE IF NOT EXISTS administrators"
                                     "(user_name varchar(100) NOT NULL,"
                                     "phone_number varchar(13) NOT NULL,"
                                     "email VARCHAR(40) NOT NULL,"
                                     "password VARCHAR(80)  NOT NULL,"
                                     "PRIMARY KEY (user_name))")

    def insert_into_administrators(self, u_name, phone_num, email_admin, password_admin):
        """Responsible for inserting data into the database when the administrators enter their
        details. Also passwords are hashed here using the bcrypt library so as to enhance security"""
        password_admin = password_admin.strip()
        hashed_passwd_admin = bcrypt.hashpw(password_admin.encode(), bcrypt.gensalt())
        values = (u_name, phone_num, email_admin, hashed_passwd_admin)
        self.database_cursor.execute(self.sql_insert_admin, values)
        self.my_database.commit()
        self.my_database.close()

    def check_password(self, p_admin) -> bool:
        """Responsible for verifying if the password entered by the user has the correct
        number of symbols, words and numbers. If the passwords satisfies the fields the
        function returns True"""
        p_admin = p_admin.strip()
        for chars in p_admin:
            if chars.isdigit():
                self.count_num += p_admin.count(chars)
            elif chars.isalpha():
                self.count_chars += p_admin.count(chars)
            else:
                self.count_symbols += p_admin.count(chars)
        if self.count_chars >= 3 and self.count_num >= 3 and self.count_symbols >= 3:
            return True
        else:
            return False

    def check_empty_fields(self, u_name, phone_num, email_admin, password_admin, c_password_admin):
        """Responsible for checking whether there are any empty text fields in left
        by the user in the sign up form. If user has left some text fields empty the
        function returns False otherwise True"""
        if u_name == "" or phone_num == "" or email_admin == "" or \
                password_admin == "" or c_password_admin == "":
            return False
        else:
            return True

    def confirm_passwd_equals_main_passwd(self, main_passwd, confirm_passwd):
        """Responsible for confirm whether the password entered in the confirm password field
        actually matches the on entered in the password text fields. If password does  not match the
        function returns False else True"""
        if main_passwd.strip() == confirm_passwd.strip():
            return True
        else:
            return False
