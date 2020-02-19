from dao.abs_das import Dao
from db_connection.connection_pool import ConnectionPool
from mysql.connector import Error


class CateDao(Dao):

    def __init__(self):
        super().__init__()

    def __do_query(self, query=None, arg=None):
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute(query, arg)
            conn.commit()
        except Error as e:
            print(e)
            raise e
        finally:
            cursor.close()
            conn.close()

    def insert_item(self, no, name):
        insert_sql = 'insert into category values (%s, %s)'
        args = no, name

        try:
            self.__do_query(query=insert_sql, arg=args)
            return True
        except Error as e:
            print(e)
            return False

    def update_item(self, name, no):
        update_sql = 'update category set name = %s where no = %s'
        args = (name, no)

        try:
            self.__do_query(query=update_sql, arg=args)
            return True
        except Error as e:
            print(e)
            return False


    def delete_item(self, name):
        delete_sql = 'delete from category where name = %s'
        args = name,
        try:
            self.__do_query(query=delete_sql, arg=args)
        except Error as e:
            print(e)

    def select_item(self):
        select_sql = 'select * from category order by no'
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute(select_sql)

            data = []
            [data.append(row) for row in self.iter_row(cursor, 5)]
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
            return data

    def select_item_no(self,no):
        select_sql = 'select no from category where no=%s'
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute(select_sql,(no,))

            data = []
            [data.append(row) for row in self.iter_row(cursor, 5)]
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
            return data

    def select_item_name(self,name):
        select_sql = 'select name from category where name=%s'
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute(select_sql,(name,))

            data = []
            [data.append(row) for row in self.iter_row(cursor, 5)]
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
            return data

    def do_query(self, **kwargs):
        super().do_query(**kwargs)

    def iter_row(self, cursor, size=5):
        return super().iter_row(cursor, size)

    def iter_row_proc(self, cursor):
        return super().iter_row_proc(cursor)