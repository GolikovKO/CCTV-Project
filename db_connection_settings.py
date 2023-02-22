class DatabaseConnectionSettings:

    __dbHost = ''
    __dbUser = ''
    __dbPass = ''
    __dbName = ''

    def setDbHost(self, dbHost):
        DatabaseConnectionSettings.__dbHost = dbHost

    def setDbUser(self, dbUser):
        DatabaseConnectionSettings.__dbUser = dbUser

    def setDbPass(self, dbPass):
        DatabaseConnectionSettings.__dbPass = dbPass

    def setDbName(self, dbName):
        DatabaseConnectionSettings.__dbName = dbName

    def getDbHost(self):
        return DatabaseConnectionSettings.__dbHost

    def getDbUser(self):
        return DatabaseConnectionSettings.__dbUser

    def getDbPass(self):
        return DatabaseConnectionSettings.__dbPass

    def getDbName(self):
        return DatabaseConnectionSettings.__dbName

    def setDbSettings(self):

        dbHost = '127.0.0.1'
        dbUser = 'root'
        dbPass = 'Huawei13'
        dbName = 'test'

        DatabaseConnectionSettings.setDbHost(self, dbHost)
        DatabaseConnectionSettings.setDbUser(self, dbUser)
        DatabaseConnectionSettings.setDbPass(self, dbPass)
        DatabaseConnectionSettings.setDbName(self, dbName)
