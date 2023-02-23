def get_db_settings():
    settings = []
    with open('settings.txt') as file:
        for line in file:
            settings.append(line.strip())
    return settings


def set_db_settings():
    settings = get_db_settings()

    db_name = settings[0]
    db_user = settings[1]
    db_pass = settings[2]
    db_host = settings[3]

    db_connection = DatabaseConnectionSettings()

    db_connection.setDbName(db_name)
    db_connection.setDbUser(db_user)
    db_connection.setDbPass(db_pass)
    db_connection.setDbHost(db_host)

    return db_connection


class DatabaseConnectionSettings:
    __db_name = ''
    __db_user = ''
    __db_pass = ''
    __db_host = ''

    def setDbHost(self, dbHost):
        DatabaseConnectionSettings.__db_host = dbHost

    def setDbUser(self, dbUser):
        DatabaseConnectionSettings.__db_user = dbUser

    def setDbPass(self, dbPass):
        DatabaseConnectionSettings.__db_pass = dbPass

    def setDbName(self, dbName):
        DatabaseConnectionSettings.__db_name = dbName

    def getDbHost(self):
        return DatabaseConnectionSettings.__db_host

    def getDbUser(self):
        return DatabaseConnectionSettings.__db_user

    def getDbPass(self):
        return DatabaseConnectionSettings.__db_pass

    def getDbName(self):
        return DatabaseConnectionSettings.__db_name
