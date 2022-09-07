import mysql.connector as db
import bcrypt


class UpdatePasswd:
    """This class is responsible for handling updating the password"""
    def __init__(self):
        """This is the constructor
                it creates a connection between the database and the server"""
        self.my_database = db.connect(
            host="localhost",
            user="root",
            passwd="mbuthi4390",
            database="School_Demo_2"
        )
        self.database_cursor = self.my_database.cursor()
        self.update_query = "UPDATE administrators SET password = %s WHERE user_name = %s"
        self.select_query_ = "SELECT password FROM administrators WHERE user_name=%s"

    def select_u_passwd(self, u_name):
        """Responsible for getting the old password saved in the database
        for the user name provided by the user"""
        vals = (u_name,)
        self.database_cursor.execute(self.select_query_, vals)
        passwd = self.database_cursor.fetchone()
        return passwd[0].encode()

    def update_details(self, old_passwd, new_passwd, user_name):
        """Responsible for getting the new password entered by the user and hashing it
        Then compares the hashed new password entered by the user with the old hashed
        password which is returned by the select_u_password() function
        if the both password hashes matches then the password is updated"""
        old_passwd_hashed = bcrypt.hashpw(old_passwd.encode(), bcrypt.gensalt())
        new_passwd_hashed = bcrypt.hashpw(new_passwd.encode(), bcrypt.gensalt())
        passwd_db = self.select_u_passwd(user_name)
        if bcrypt.checkpw(old_passwd.encode(), passwd_db):

            values = (new_passwd_hashed, user_name)
            self.database_cursor.execute(self.update_query, values)
            self.my_database.commit()
            self.my_database.close()
        else:
            return None

    def verify_inputs(self, old_passwd, new_passwd, user_name_):
        """Responsible for ensuring that the user does not leave any text field empty"""
        if old_passwd == "" or new_passwd == "" or user_name_ == "":
            return False
        else:
            return True
