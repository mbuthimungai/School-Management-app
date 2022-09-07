import mysql.connector as db


class DeleteT:
    """This class is responsible for handling deletion of records from the database"""
    def __init__(self):
        """This is the constructor
                        it creates a connection between the database and the MySQLServer"""
        self.my_database = db.connect(
            host="localhost",
            user="root",
            passwd="mbuthi4390",
            database="School_Demo_2"
        )
        self.database_cursor = self.my_database.cursor()
        self.delete_sql_stmt = "DELETE FROM teachers WHERE user_name = %s "

    def delete_teacher(self, u_name):
        """Responsible for deleting the value selected by the user"""
        value_to_delete = (u_name,)
        print(value_to_delete)
        self.database_cursor.execute(self.delete_sql_stmt, value_to_delete)
        self.my_database.commit()
        self.my_database.close()
