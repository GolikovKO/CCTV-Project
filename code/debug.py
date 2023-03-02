import datetime
import psycopg2

from code.database.db_connection_settings import create_db_connection, get_db_settings


def load_humans_count_go_outside(db_connection, stop_id, time, x1, y1, x4, y4):
    db_name = db_connection.get_db_name()
    db_user = db_connection.get_db_user()
    db_pass = db_connection.get_db_pass()
    db_host = db_connection.get_db_host()
    print(db_name)

    try:
        connection = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host)
    except Exception as error:
        print('Error occurred trying to connect to database - ', error)
    else:
        try:
            sql = "INSERT INTO humans (stop_id, coord_x1, coord_y1, coord_x4, coord_y4, time, flag) VALUES (" +\
                  str(stop_id) + "," + str(x1) + "," + str(y1) + "," + str(x4) + "," + str(y4) + "," + "'" + str(time) +\
                  "'" + "," + str(1) + ")"

            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as error:
            print('Error occurred trying to save humans count go outside - ', error)


def main():
    #db_connection = create_db_connection()
    #load_humans_count_go_outside(db_connection, 1, datetime.datetime.now(), 1, 1, 1, 1)
    settings = get_db_settings()
    print(settings)
    print(type(settings))
    db_name = settings.get("db_name")
    db_user = settings.get("db_user")
    db_pass = settings.get("db_pass")
    db_host = settings.get("db_host")

    print(db_name)


if __name__ == '__main__':
    main()
