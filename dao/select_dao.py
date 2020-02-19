from mysql.connector import Error

from dao.abs_das import Dao


class SelDao(Dao):
    def __init__(self):
        super().__init__()
        self.select_item_where()

    def insert_item(self, **kwargs):
        pass

    def update_item(self, **kwargs):
        pass

    def delete_item(self, **kwargs):
        pass

    def select_item(self, **kwargs):
        pass

    def do_query(self, **kwargs):
        super().do_query(**kwargs)

    def iter_row(self, cursor, size=5):
        return super().iter_row(cursor, size)

    def iter_row_proc(self, cursor):
        return super().iter_row_proc(cursor)

    def select_item_where(self, name='', min_price=0, max_price='', min_date='', max_date=''):
        select_sql = "select p.name, salecnt, sale_price, DATE_FORMAT(date,'%Y-%m-%d %H:%i') from product p left join sale s on s.code = p.code left join sale_detail sd on s.no = sd.no where sale_price is not NULL"
        where_name = " and p.name = %s"
        where_price = " and sale_price between %s and %s"
        where_date = " and (select DATE_FORMAT(date, '%Y-%m-%d')) BETWEEN %s and %s"

        sql = {}
        if max_price=='':
            min_price = ''

        arg = [name, min_price, max_price, min_date,max_date]
        del_list = []
        if min_date != '' and max_date == '':
            max_date = 'default'
        for i in range(len(arg)):
            if arg[i] == '':
                del_list.append(i)
        del_list.reverse()

        for i in del_list:
            del arg[i]

        sql['select'] = select_sql
        sql[name] = where_name
        sql[max_price] = where_price
        sql[min_date] = where_date
        sql[''] = ""
        key = []
        data = ""
        arg = tuple(arg)

        for i in sql.keys():
            key.append(i)
        for i in range(len(sql)):
            data = data + sql[key[i]]

        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            if name is None:
                cursor.execute(select_sql)
                res = []
                [res.append(row) for row in self.iter_row(cursor, 5)]

            else:
                cursor.execute(data,arg)
                res = set()

                [res.add(row) for row in self.iter_row(cursor, 5)]
                res = list(res)
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()