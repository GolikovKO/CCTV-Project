import json


def get_db_settings():
    file_with_settings = open('../settings.json')
    settings_as_json = json.load(file_with_settings)
    file_with_settings.close()

    return settings_as_json


def create_db_connection():
    settings = get_db_settings()

    db_name = settings.get("db_name")
    db_user = settings.get("db_user")
    db_pass = settings.get("db_pass")
    db_host = settings.get("db_host")

    db_connection = DatabaseConnectionSettings()

    db_connection.set_db_name(db_name)
    db_connection.set_db_user(db_user)
    db_connection.set_db_pass(db_pass)
    db_connection.set_db_host(db_host)

    return db_connection


class DatabaseConnectionSettings:
    def __init__(self):
        self._db_name = None
        self._db_user = None
        self._db_pass = None
        self._db_host = None

    def set_db_name(self, db_name):
        self._db_name = db_name

    def set_db_user(self, db_user):
        self._db_user = db_user

    def set_db_pass(self, db_pass):
        self._db_pass = db_pass

    def set_db_host(self, db_host):
        self._db_host = db_host

    def get_db_host(self):
        return self._db_host

    def get_db_user(self):
        return self._db_user

    def get_db_pass(self):
        return self._db_pass

    def get_db_name(self):
        return self._db_name
