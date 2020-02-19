from mysql.connector import Error

from dao.abs_das import Dao

select_sql = "proc_saledetail_orderby"


class SaleDetailDao(Dao):
    def select_item(self, rank):
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            args = [rank, ]
            cursor.callproc(select_sql, args)
            res = []
            [res.append(row) for row in self.iter_row_proc(cursor)]
            return res
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


    def insert_item(self, **kwargs):
        pass

    def update_item(self, **kwargs):
        pass

    def delete_item(self, **kwargs):
        pass
