import mysql.connector


class MySQLConnector:
    """ MySQL bindings """

    def __init__(self):
        print("MySQL connector initialized")

    def set_config(self, host, user, password):
        self.config = {
            'user': user,
            'password': password,
            'host': host
        }

    def get_databases(self):
        """Get the databases on """
        self.config['database'] = 'information_schema'
        cnx = mysql.connector.connect(**self.config)
        cursor = cnx.cursor()

        cursor.execute("SELECT SCHEMA_NAME AS 'Database' FROM schemata")
        tables = []
        for s in cursor:
            tables.append(s[0])

        cursor.close()
        cnx.close()
        return tables

    def get_tables_from_database(self, db):
        self.config['database'] = 'information_schema'
        cnx = mysql.connector.connect(**self.config)
        cursor = cnx.cursor()
        cursor.execute(f"SELECT TABLE_NAME FROM TABLES WHERE TABLE_SCHEMA={db}")
        tables = []
        for s in cursor:
            print(s)
            # tables.append(s[0])

        cursor.close()
        cnx.close()
        return tables

    def get_schema(self):
        dbs = self.get_databases()
        db_tables = []
        for db in dbs:
            print(db)
            ts = self.get_tables_from_database(db)
            # db_tables.append(self.get_tables_from_database(db))

        print(zip(dbs, db_tables))
