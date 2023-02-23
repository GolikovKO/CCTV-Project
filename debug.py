from db_connection_settings import DatabaseConnectionSettings, set_db_settings


def get_db_settings():
    settings = []
    with open('settings.txt') as file:
        for line in file:
            settings.append(line.strip())
    return settings


def main():
    settings = get_db_settings()
    print(settings)
    db = set_db_settings()
    print(db.getDbHost())


if __name__ == '__main__':
    main()
