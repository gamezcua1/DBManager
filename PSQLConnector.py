import psycopg2


class PSQLConnector:
    """ PostgreSQL bindings """

    def set_config(self, host, user, password):
        self.config = {
            'user': user,
            'password': password,
            'host': host
        }
        print("PostgreSQL connector initialized")

    def query(self, db, query):
        self.config['database'] = db
        cnx = psycopg2.connect(**self.config)
        cursor = cnx.cursor()

        cursor.execute(query)
        field_names = [i[0] for i in cursor.description]
        tables = [field_names]
        for s in cursor:
            tables.append(list(s))

        cursor.close()
        cnx.close()
        return tables

    def get_databases(self):
        """Get the databases on """
        self.config["database"] = "postgres"
        tables = []
        try:
            connection = psycopg2.connect(**self.config)
            cursor = connection.cursor()
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            result = cursor.fetchall()
            tables =[r[0] for r in result]
        except psycopg2.Error as error:
            print(error)
        finally:
            if connection:
                cursor.close()
                connection.close()
        return tables

    def get_tables_from_database(self, db):
        self.config["database"] = db
        tables = []
        try:
            connection = psycopg2.connect(**self.config)
            cursor = connection.cursor()
            cursor.execute(
                "SELECT table_name, table_schema FROM information_schema.tables WHERE table_schema='public'")
            result = cursor.fetchall()
            tables = [r[0] for r in result]
        except psycopg2.Error as error:
            print(error)
        finally:
            if connection:
                cursor.close()
                connection.close()
        return tables

    def get_columns_from_table(self, db, table):
        self.config['database'] = db
        cnx = psycopg2.connect(**self.config)
        cursor = cnx.cursor()
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND "
                       f"table_name='{table}'")
        columns = [c[0] for c in cursor]

        cursor.close()
        cnx.close()
        return columns

    def get_schema(self):
        excluded = ['postgres', 'roles_on_psql']
        dbs_gotten = self.get_databases()

        dbs = [db for db in dbs_gotten if db not in excluded]
        db_tables = []
        tables_columns = []

        for db in dbs:
            tables = self.get_tables_from_database(db)
            db_tables.append(tables)
            for table in tables:
                columns = self.get_columns_from_table(db, table)
                tables_columns.append(columns)

        schema = {}
        for i in range(0, len(dbs)):
            table_cols = {}
            for j in range(0, len(db_tables[i])):
                table_cols[db_tables[i][j]] = tables_columns[j]
            schema[dbs[i]] = table_cols

        return schema
