import sqlite3


class DbSettings:
    db_name = 'sqlite'

    def __init__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.db_create_table(
            "CREATE TABLE IF NOT EXISTS TestingTypes ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT)")
        self.db_create_table(
            "CREATE TABLE IF NOT EXISTS Groups ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT, "
            "orders INTEGER,"
            "type_id INTEGER,"
            "FOREIGN KEY(type_id) REFERENCES TestingTypes(id))")
        self.db_create_table(
            "CREATE TABLE IF NOT EXISTS Tests ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT, "
            "orders INTEGER,"
            "path TEXT,"
            "aegs TEXT,"
            "group_id INTEGER,"
            "FOREIGN KEY(group_id) REFERENCES Groups(id))")

    @staticmethod
    def scrub(table_name):
        return ''.join(symbol for symbol in table_name if symbol.isalnum())

    def db_create_table(self, create_table_sql):
        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
        except TypeError:
            pass

    def db_insert_data(self, table_name, columns, values):
        table_name = self.scrub(str(table_name))
        if columns != '':
            sql = "INSERT INTO {0} ({1}) VALUES ({2})".format(table_name, columns, values)
            self.cursor.execute(sql)
            self.conn.commit()

    def db_select_data(self, table_name, columns):
        table_name = self.scrub(str(table_name))
        sql = "SELECT {0} FROM {1}".format(columns, table_name)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

    def db_delete_data(self, table_name, condition):
        table_name = self.scrub(str(table_name))
        sql = "DELETE FROM {0} WHERE {1}".format(table_name, condition)
        self.cursor.execute(sql)
        self.conn.commit()

    def db_update_data(self, table_name, new_values, condition):
        table_name = self.scrub(str(table_name))
        sql = "UPDATE {0} SET {1} WHERE {2} ".format(table_name, new_values, condition)
        self.cursor.execute(sql)
        self.conn.commit()


class Tests(DbSettings):
    table_name = 'Tests'
    columns = 'name, orders, path, aegs, group_id'

    def insert_data(self, values):
        self.db_insert_data(self.table_name, self.columns, values)

    def select_data(self, col):
        self.db_select_data(self.table_name, col)

    def delete_data(self, condition):
        self.db_delete_data(self.table_name, condition)

    def update_data(self, new_values, condition):
        self.db_update_data(self.table_name, new_values, condition)


class Groups(DbSettings):
    table_name = 'Groups'
    columns = 'name, orders, type_id'

    def insert_data(self, values):
        self.db_insert_data(self.table_name, self.columns, values)

    def select_data(self, col):
        self.db_select_data(self.table_name, col)

    def delete_data(self, condition):
        self.db_delete_data(self.table_name, condition)

    def update_data(self, new_values, condition):
        self.db_update_data(self.table_name, new_values, condition)


class TestingTypes(DbSettings):
    table_name = 'TestingTypes'
    columns = 'name'

    def insert_data(self, values):
        self.db_insert_data(self.table_name, self.columns, values)

    def select_data(self, col):
        self.db_select_data(self.table_name, col)

    def delete_data(self, condition):
        self.db_delete_data(self.table_name, condition)

    def update_data(self, new_values, condition):
        self.db_update_data(self.table_name, new_values, condition)


if __name__ == '__main__':
    test = Tests()

    new_values = "path = 'S'"
    condition = "id = 21"
    test.update_data(new_values, condition)


