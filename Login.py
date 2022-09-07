import mysql.connector as db
import bcrypt


class Login:
    """This class is responsible for handling login sessions"""
    def __init__(self):
        """This is the constructor
        it creates a connection between the database and the server"""
        self.my_database = db.connect(
            host='localhost',
            passwd="mbuthi4390",
            user="root",
            database="school_demo_2"
        )
        self.database_cursor = self.my_database.cursor()
        self.sql_select = "SELECT * FROM administrators WHERE user_name = %s"

    def user_validation(self, u_name, u_passwd):
        """This performs validation on the user password
        It takes the password inputed by the user on the text field
        and first hashes it and compares the hashed password with the one stored in the database
        if both of the hashes compare the function returns True otherwise False"""
        param_ = (u_name,)
        self.database_cursor.execute(self.sql_select, param_)
        user_passwd_login = self.database_cursor.fetchone()

        user_passwd_db = user_passwd_login[3].encode()

        valid_passwd = bcrypt.checkpw(u_passwd.encode(), user_passwd_db)

        if valid_passwd:
            return True
        else:
            return False

    def identify_empty_input(self, u_name, u_passwd):
        """This function is responsible for checking where the user has left an empty field"""
        if u_name == "" or u_passwd == "":
            return False
        else:
            return True
