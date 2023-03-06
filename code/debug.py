from code.database.db_connection_settings import create_db_connection


# Collect events until released
def main():
    db_connection = create_db_connection()

    db_name = db_connection.get_db_name()
    db_user = db_connection.get_db_user()
    db_pass = db_connection.get_db_pass()
    db_host = db_connection.get_db_host()


if __name__ == '__main__':
    main()
