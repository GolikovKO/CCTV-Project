import psycopg2

from db_connection_settings import create_db_connection


def get_arrivals_by_time():
    db_connection = create_db_connection()

    db_name = db_connection.get_db_name()
    db_user = db_connection.get_db_user()
    db_pass = db_connection.get_db_pass()
    db_host = db_connection.get_db_host()

    result = None
    try:
        connection = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host)
    except Exception as error:
        print('Error occurred trying to connect to database - ', error)
    else:
        try:
            sql = "SELECT * FROM podezd JOIN svyaz ON svyaz.svyaz_id = podezd.svyaz_id WHERE svyaz.stop_id = 2"

            connection.autocommit = True
            cursor = connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
        except Exception as error:
            print('Error occurred trying to get arrival - ', error)

    return result


def get_humans_count_by_time():
    db_connection = create_db_connection()

    db_name = db_connection.get_db_name()
    db_user = db_connection.get_db_user()
    db_pass = db_connection.get_db_pass()
    db_host = db_connection.get_db_host()

    result = None
    try:
        connection = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host)
    except Exception as error:
        print('Error occurred trying to connect to database - ', error)
    else:
        try:
            sql = "SELECT `time`, COUNT(`time`) AS `count` FROM `people` WHERE flag = 0 GROUP BY `time` " \
                  "HAVING `count` >= 1"
            connection.autocommit = True
            cursor = connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
        except Exception as error:
            print('Error occurred trying to get time and humans amount - ', error)

    return result


def load_human_go_outside(stop_id, time, coord_x1, coord_y1, coord_x4, coord_y4):
    db_connection = create_db_connection()

    db_name = db_connection.get_db_name()
    db_user = db_connection.get_db_user()
    db_pass = db_connection.get_db_pass()
    db_host = db_connection.get_db_host()

    try:
        connection = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host)
    except Exception as error:
        print('Error occurred trying to connect to database - ', error)
    else:
        try:
            sql = "INSERT INTO humans (stop_id, coord_x1, coord_y1, coord_x4, coord_y4, time, flag) VALUES (" +\
                  str(stop_id) + "," + str(coord_x1) + "," + str(coord_y1) + "," + str(coord_x4) + "," + \
                  str(coord_y4) + "," + "'" + str(time) + "'" + "," + str(0) + ")"

            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as error:
            print('Error occurred trying to save humans count go outside - ', error)


def load_human_go_inside(stop_id, time, coord_x1, coord_y1, coord_x4, coord_y4):
    db_connection = create_db_connection()

    db_name = db_connection.get_db_name()
    db_user = db_connection.get_db_user()
    db_pass = db_connection.get_db_pass()
    db_host = db_connection.get_db_host()

    try:
        connection = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host)
    except Exception as error:
        print('Error occurred trying to connect to database - ', error)
    else:
        try:
            sql = "INSERT INTO humans (stop_id, coord_x1, coord_y1, coord_x4, coord_y4, time, flag) VALUES (" +\
                  str(stop_id) + "," + str(coord_x1) + "," + str(coord_y1) + "," + str(coord_x4) + "," + \
                  str(coord_y4) + "," + "'" + str(time) + "'" + "," + str(1) + ")"

            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as error:
            print('Error occurred trying to save humans count go inside - ', error)
