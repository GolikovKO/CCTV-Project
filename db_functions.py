from db_connection_settings import DatabaseConnectionSettings
from mysql.connector import connect
from mysql.connector.errors import Error


def getPodezd():
    dbConnection = DatabaseConnectionSettings()
    dbConnection.set_db_settings()

    dbHost = dbConnection.getDbHost()
    dbUser = dbConnection.getDbUser()
    dbPass = dbConnection.getDbPass()
    dbName = dbConnection.getDbName()

    result = ''

    try:
        with connect(host=dbHost, user=dbUser, password=dbPass, database=dbName) as connection:
            sql = "SELECT * FROM podezd JOIN svyaz ON svyaz.svyaz_id = podezd.svyaz_id WHERE svyaz.stop_id = 2"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
                connection.close()
    except Error as e:
        print(e)

    return result


def getTimeAndPeople():
    dbConnection = DatabaseConnectionSettings()
    dbConnection.set_db_settings()

    dbHost = dbConnection.getDbHost()
    dbUser = dbConnection.getDbUser()
    dbPass = dbConnection.getDbPass()
    dbName = dbConnection.getDbName()

    result = ''

    try:
        with connect(host=dbHost, user=dbUser, password=dbPass, database=dbName) as connection:
            sql = "SELECT `time`, COUNT(`time`) AS `count` FROM `people` WHERE flag = 0 GROUP BY `time` " \
                  "HAVING `count` >= 1"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
                connection.close()
    except Error as e:
        print(e)

    return result


def load_human_coords(stop_id, time, x1, y1, x4, y4):
    dbConnection = DatabaseConnectionSettings()
    dbConnection.set_db_settings()

    dbHost = dbConnection.getDbHost()
    dbUser = dbConnection.getDbUser()
    dbPass = dbConnection.getDbPass()
    dbName = dbConnection.getDbName()

    try:
        with connect(host=dbHost, user=dbUser, password=dbPass, database=dbName) as connection:
            sql = "INSERT INTO people (stop_id, coord_x1, coord_y1, coord_x4, coord_y4, time, flag) VALUES (" + str(
                stop_id) + "," + str(x1) + "," + str(y1) + "," + str(x4) + "," + str(y4) + "," + "'" + str(
                time) + "'" + "," + str(0) + ")"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
                connection.close()
    except Error as e:
        print(e)


def load_humans_count_go_outside(stop_id, time, x1, y1, x4, y4, humans_get_off_total_count):
    dbConnection = DatabaseConnectionSettings()
    dbConnection.set_db_settings()

    db_host = dbConnection.getDbHost()
    db_user = dbConnection.getDbUser()
    db_pass = dbConnection.getDbPass()
    db_name = dbConnection.getDbName()

    try:
        with connect(host=db_host, user=db_user, password=db_pass, database=db_name) as connection:
            sql = "INSERT INTO people (stop_id, time, frame, coord_x, coord_y, total_amount) VALUES (" + str(
                stop_id) + "," + str(x1) + "," + str(y1) + "," + str(x4) + "," + str(y4) + "," + str(
                time) + "," + str(-1) + "," + str(humans_get_off_total_count) + ")"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
                connection.close()
    except Error as error:
        print('Error occurred trying to save humans count go outside - ', error)


def load_humans_count_go_inside(stop_id, time, x1, y1, x4, y4, humans_get_in_total_count):
    dbConnection = DatabaseConnectionSettings()
    dbConnection.set_db_settings()

    db_host = dbConnection.getDbHost()
    db_user = dbConnection.getDbUser()
    db_pass = dbConnection.getDbPass()
    db_name = dbConnection.getDbName()

    try:
        with connect(host=db_host, user=db_user, password=db_pass, database=db_name) as connection:
            sql = "INSERT INTO people (stop_id, coord_x1, coord_y1, coord_x4, coord_y4, time, flag, amount) VALUES (" +\
                  str(stop_id) + "," + str(x1) + "," + str(y1) + "," + str(x4) + "," + str(y4) + "," + str(time) + \
                  "," + str(1) + "," + str(humans_get_in_total_count) + ")"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
                connection.close()
    except Error as error:
        print('Error occurred trying to save humans count go inside - ', error)
