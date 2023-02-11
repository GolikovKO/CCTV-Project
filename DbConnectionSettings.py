class DbConnectionSettings():

    __dbHost = ''
    __dbUser = ''
    __dbPass = ''
    __dbName = ''

    def setDbHost(self, dbHost):
        DbConnectionSettings.__dbHost = dbHost

    def setDbUser(self, dbUser):
        DbConnectionSettings.__dbUser = dbUser

    def setDbPass(self, dbPass):
        DbConnectionSettings.__dbPass = dbPass

    def setDbName(self, dbName):
        DbConnectionSettings.__dbName = dbName 

    def getDbHost(self):
        return DbConnectionSettings.__dbHost 

    def getDbUser(self):
        return DbConnectionSettings.__dbUser

    def getDbPass(self):
        return DbConnectionSettings.__dbPass

    def getDbName(self):
        return DbConnectionSettings.__dbName

    def setDbSettings(self):

        dbHost = '127.0.0.1'
        dbUser = 'root'
        dbPass = 'Huawei13'
        dbName = 'test'

        DbConnectionSettings.setDbHost(self, dbHost)
        DbConnectionSettings.setDbUser(self, dbUser)
        DbConnectionSettings.setDbPass(self, dbPass)
        DbConnectionSettings.setDbName(self, dbName)     