"""from DbConnectionSettings import DbConnectionSettings
from mysql.connector import connect
from mysql.connector.errors import Error

class DbService():

    def getPodezd(self):

        dbConnection = DbConnectionSettings()
        dbConnection.setDbSettings()

        dbHost = dbConnection.getDbHost()
        dbUser = dbConnection.getDbUser()
        dbPass = dbConnection.getDbPass()
        dbName = dbConnection.getDbName()

        result = ''

        try:
           with connect(
               host = dbHost,
               user = dbUser,
               password = dbPass,
               database = dbName
           ) as connection:
               sql = "SELECT * FROM podezd JOIN svyaz ON svyaz.svyaz_id = podezd.svyaz_id WHERE svyaz.stop_id = 2"
               with connection.cursor() as cursor:
                   cursor.execute(sql)
                   result = cursor.fetchall()
                   connection.commit()
                   connection.close()
        except Error as e:
           print(e)

        return result

    def getTimeAndPeople(self):

        dbConnection = DbConnectionSettings()
        dbConnection.setDbSettings()

        dbHost = dbConnection.getDbHost()
        dbUser = dbConnection.getDbUser()
        dbPass = dbConnection.getDbPass()
        dbName = dbConnection.getDbName()

        result = ''

        try:
            with connect(
                host = dbHost,
                user = dbUser,
                password = dbPass,
                database = dbName
            ) as connection:
                sql = "SELECT `time`, COUNT(`time`) AS `count` FROM `people` WHERE flag = 0 GROUP BY `time` HAVING `count` >= 1"
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    connection.commit()
                    connection.close()
        except Error as e:
            print(e)

        return result

    def loadPeopleInside(self, stop_id, time, x1, y1, x4, y4):

        dbConnection = DbConnectionSettings()
        dbConnection.setDbSettings()

        dbHost = dbConnection.getDbHost()
        dbUser = dbConnection.getDbUser()
        dbPass = dbConnection.getDbPass()
        dbName = dbConnection.getDbName()

        try:
            with connect(
                host = dbHost,
                user = dbUser,
                password = dbPass,
                database = dbName
            ) as connection:
                sql = "INSERT INTO people (stop_id, coord_x1, coord_y1, coord_x4, coord_y4, time, flag) VALUES (" + str(stop_id) + "," + str(x1) + "," + str(y1) + "," + str(x4) + "," + str(y4) + "," + "'" + str(time) + "'" + "," + str(0) +")"
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    connection.commit()
                    connection.close()
        except Error as e:
            print(e)

    def loadPeopleGetoff(self, stop_id, time, x1, y1, x4, y4, people_getoff_total):

        dbConnection = DbConnectionSettings()
        dbConnection.setDbSettings()

        dbHost = dbConnection.getDbHost()
        dbUser = dbConnection.getDbUser()
        dbPass = dbConnection.getDbPass()
        dbName = dbConnection.getDbName()

        try:
            with connect(
                host = dbHost,
                user = dbUser,
                password = dbPass,
                database = dbName
            ) as connection:
                sql = "INSERT INTO people (stop_id, time, frame, coord_x, coord_y, total_amount) VALUES (" + str(stop_id) + "," + str(x1) + "," + str(y1) + "," + str(x4) + "," + str(y4) + "," + str(time) + "," + str(-1) + "," + str(people_getoff_total) +")"
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    connection.commit()
                    connection.close()
        except Error as e:
            print(e)

    def loadPeopleGetin(self, stop_id, time, x1, y1, x4, y4, people_getin_total):

        dbConnection = DbConnectionSettings()
        dbConnection.setDbSettings()

        dbHost = dbConnection.getDbHost()
        dbUser = dbConnection.getDbUser()
        dbPass = dbConnection.getDbPass()
        dbName = dbConnection.getDbName()

        try:
            with connect(
                host = dbHost,
                user = dbUser,
                password = dbPass,
                database = dbName
            ) as connection:
                sql = "INSERT INTO people (stop_id, coord_x1, coord_y1, coord_x4, coord_y4, time, flag, amount) VALUES (" + str(stop_id) + "," + str(x1) + "," + str(y1) + "," + str(x4) + "," + str(y4) + "," + str(time) + "," + str(1) + "," + str(people_getin_total) +")"
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    connection.commit()
                    connection.close()
        except Error as e:
            print(e)      """