from dao.abs_das import Dao
from db_connection.connection_pool import ConnectionPool
from mysql.connector import Error

select_sql = 'select * from product'
select_sql_where = 'select code, name from product where code like %s'
update_sql = 'update product set name = %s, price = %s, margin_rate = %s, category = (select no from category where name = %s) where code = %s'
insert_sql = 'insert into product values(%s, %s, (select no from category where name = %s), %s, %s)'
delete_sql = "delete from product where code = %s"

select_category = 'select name from category'
select_category_sql1 = 'select DISTINCT(p.code), p.name, p.price, p.margin_rate, c.name from product p left join category c on p.category = c.no left join sale s on p.code = s.code where c.name = %s'
select_category_sql2 = 'select DISTINCT(p.code), p.name, p.price, p.margin_rate, c.name from product p left join category c on p.category = c.no left join sale s on p.code = s.code'
select_check_menu_code = 'select code from product where code = %s'
select_check_menu_name = 'select name from product where name = %s'
select_name ='select name from product'

class ProductDao(Dao):
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

    def __iter_row(self, cursor, size=5):
        while True:
            rows = cursor.fetchmany(size)
            if not rows:
                break
            for row in rows:
                yield row

    def select_item(self, code = None):
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            if code is None:
                cursor.execute(select_sql)
            else:
                args = (code,)
                cursor.execute(select_sql_where, args)

            data = []
            [data.append(row) for row in self.__iter_row(cursor, 5)]
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
            return data

    def insert_item(self, code, name, mode, price, margin):
        args = (code, name, mode, price, margin)
        try:
            self.__do_query(query=insert_sql, arg=args)
            return True
        except Error as e:
            return False

    def update_item(self, name, price, margin, category, code):
        args = (name, price, margin, category, code)

        try:
            self.__do_query(query=update_sql, arg=args)
            return True
        except Error as e:
            return False

    def delete_item(self, code):
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute(delete_sql, (code,))
            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()

    def select_category(self):
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_category)
            res = []
            [res.append(row) for row in self.__iter_row(cursor, 1)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def select_check_menu_code(self, code):
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_check_menu_code, (code,))

            res = []
            [res.append(row) for row in self.__iter_row(cursor, 1)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def select_check_menu_name(self, name):
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_check_menu_name, (name,))

            res = []
            [res.append(row) for row in self.__iter_row(cursor, 1)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def select_menu(self, menu=None):
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_category_sql1, (menu,))
            res = []
            [res.append(row) for row in self.__iter_row(cursor, 1)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def select_menu2(self):
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_category_sql2)

            res = []
            [res.append(row) for row in self.iter_row(cursor, 5)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def select_order(self):
        select_sql_order = 'select ca from product'
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_sql_order)

            res = []
            [res.append(row) for row in self.iter_row(cursor, 5)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def select_order_name(self, name):
        select_category = "select p.name from category c join product p on c.no = p.category where c.name = %s"
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_category, (name,))

            res = []
            [res.append(row) for row in self.iter_row(cursor, 5)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def select_order_name_category(self, name):
        select_product_category = "select c.name from category c left join product p on c.no = p.category where p.name =  %s"
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_product_category, (name,))

            res = []
            [res.append(row) for row in self.iter_row(cursor, 5)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def select_name(self):
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_name)
            res = []
            [res.append(row) for row in self.iter_row(cursor, 5)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()