import psycopg2

class PSQLConnector:
    """ PostgreSQL bindings """

    def __init__(self):
        print("PSQL connector initialized")
    
    def set_config(self, host, user, password):
        self.config = {
            "user": user,
            "password": password,
            "host": host
        }
    
    def get_databases(self):
        self.config["database"] = "postgres"
        result = None
        try:
            connection = psycopg2.connect(**self.config)
            cursor = connection.cursor()
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            result = cursor.fetchall()
        except psycopg2.Error as error:
            print(error)
        finally:
            if connection:
                cursor.close()
                connection.close()
        return result

    def get_tables_from_database(self, database):
        self.config["database"] = database
        result = None
        try:
            connection = psycopg2.connect(**self.config)
            cursor = connection.cursor()
            cursor.execute("SELECT table_name, table_schema FROM information_schema.tables WHERE table_schema='public';")
            result = cursor.fetchall()
        except psycopg2.Error as error:
            print(error)
        finally:
            if connection:
                cursor.close()
                connection.close()
        return result
    
    def get_schema(self):
        dbs = self.get_databases()
        db_tables = []
        for db in dbs:
            db_tables.append(self.get_tables_from_database(db[0]))
        return db_tables

if __name__ == "__main__":
    psql_connector = PSQLConnector()
    psql_connector.set_config("127.0.0.1", "gerry", "password")
    print(psql_connector.get_databases())
    print(psql_connector.get_tables_from_database("cpremier"))
    print(psql_connector.get_schema())