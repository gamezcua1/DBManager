import mysql.connector


class MySQLConnector:
    """ MySQL bindings """

    def set_config(self, host, user, password, port=3306):
        self.config = {
            'user': user,
            'password': password,
            'host': host,
            'port': int(port)
        }
        print("MySQL connector initialized")

    def query(self, db, query):
        self.config['database'] = db
        cnx = mysql.connector.connect(**self.config)
        cursor = cnx.cursor()

        cursor.execute(query)
        field_names = [i[0] for i in cursor.description]
        tables = [field_names]
        for s in cursor:
            tables.append(list(s))

        cursor.close()
        cnx.close()
        return tables

    def insert(self, db="", table="", cols=[], values=[]):
        self.config['database'] = db
        cnx = mysql.connector.connect(**self.config)
        cursor = cnx.cursor()

        fix_cols = []
        for col in cols:
            fix_cols.append(col.split(',')[0])

        add = (f"INSERT INTO {table} ({','.join(fix_cols)}) VALUES ({'%s,'*(len(fix_cols)-1)+'%s'})")

        try:
            cursor.execute(add, values)
            cnx.commit()
        except mysql.connector.Error as err:
            cursor.close()
            cnx.close()
            print(err)
            return err
        finally:
            cursor.close()
            cnx.close()

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
        cursor.execute(f"SELECT TABLE_NAME FROM TABLES WHERE TABLE_SCHEMA='{db}'")
        tables = [s[0] for s in cursor]

        cursor.close()
        cnx.close()
        return tables

    def get_columns_from_table(self, db, table):
        self.config['database'] = 'information_schema'
        cnx = mysql.connector.connect(**self.config)
        cursor = cnx.cursor()
        cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM COLUMNS WHERE TABLE_SCHEMA='{db}' and TABLE_NAME='{table}'")
        columns = [f"{c[0]}, ({c[1]})" for c in cursor]

        cursor.close()
        cnx.close()
        return columns

    def get_schema(self):
        excluded = ['information_schema', 'mysql', 'performance_schema']
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
        c_i = 0
        for i in range(0, len(dbs)):
            table_cols = {}
            for j in range(0, len(db_tables[i])):
                table_cols[db_tables[i][j]] = tables_columns[c_i]
                c_i += 1
            schema[dbs[i]] = table_cols

        return schema
