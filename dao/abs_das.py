from abc import ABCMeta, abstractmethod

from mysql.connector import Error

from db_connection.connection_pool import ConnectionPool


class Dao(metaclass=ABCMeta):
    def __init__(self):
        self.connection_Pool = ConnectionPool.get_instance()

    @abstractmethod
    def insert_item(self, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")

    @abstractmethod
    def update_item(self, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")

    @abstractmethod
    def delete_item(self, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")

    @abstractmethod
    def select_item(self, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")

    def do_query(self, **kwargs):
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            if kwargs['kwargs'] is not None:
                cursor.execute(kwargs['query'], kwargs['kwargs'])
            else:
                cursor.execute(kwargs['query'])
            conn.commit()
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def iter_row(self, cursor, size=5):
        while True:
            rows = cursor.fetchmany(size)
            if not rows:
                break
            for row in rows:
                yield row

    def iter_row_proc(self, cursor):
        for result in cursor.stored_results():
            rows = result.fetchall()
            if not rows:
                break
            for row in rows:
                yield row
