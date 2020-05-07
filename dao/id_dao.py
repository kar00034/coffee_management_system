from mysql.connector import Error

from dao.abs_das import Dao


class IDDao(Dao):
    def insert_item(self, user_id=None, password=None, mode=None, name=None, email=None):
        insert_sql = "INSERT INTO user_data VALUES(%s, password(%s), %s, %s, %s)"
        insert_mode = "INSERT INTO user_mode VALUES((select no from user_mode where mode = %s), %s)"
        args = (user_id, password, mode, name, email)
        mode_args = (mode,mode )
        try:
            super().do_query(query=insert_sql, kwargs=args)
            # super().do_query(query=insert_mode, kwargs=mode_args)
            return True
        except Error:
            return False

    def update_item(self, user_id, mode, name, email):
        update_sql = "update user_data set user_id=%s, mode=%s, name=%s, email=%s where user_id = %s"
        args = (user_id, mode, name, email, user_id)
        try:
            super().do_query(query=update_sql, kwargs=args)
            return True
        except Error:
            return False

    def delete_item(self, user_id=None):
        delete_sql = "delete from user_data where user_id = %s"
        args = (user_id,)
        try:
            super().do_query(query=delete_sql, kwargs=args)
            return True
        except Error:
            return False

    def select_item(self, user_id=None):
        select_sql = "select user_id, mode, name from user_data"
        select_sql_where = select_sql + " where name = %s"
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_sql) if user_id is None else cursor.execute(select_sql_where, (user_id,))
            res = []
            [res.append(list(row)) for row in self.iter_row(cursor, 5)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def select_password_item(self, user_id=None, password=None):
        select_pass_sql = "select pass=password(%s) from user_data where user_id = %s"
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor(buffered=True)
            cursor.execute(select_pass_sql, (password,user_id))
            res = []
            [res.append(row) for row in self.iter_row(cursor, 1)]
            return res
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

    def select_item_mode(self):
        select_mode = "select user_id,name,mode,email from user_data"
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_mode)
            res = []
            [res.append(list(row)) for row in self.iter_row(cursor, 1)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def select_grant(self,id):
        select_grant = "SELECT user_grant from mode_grant g left join user_data u on g.name = u.mode where u.mode = %s"
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_grant, (id,))
            res = []
            [res.append(list(row)) for row in self.iter_row(cursor, 1)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def select_mode(self):
        select_mode = "SELECT mode from user_mode"
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_mode)
            res = []
            [res.append(list(row)) for row in self.iter_row(cursor, 1)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def find_pass(self, password , id, name, email):
        change_pass = "update user_data set pass = password(%s) where user_id = %s and name = %s and email = %s"
        args = (password, id, name, email)

        try:
            super().do_query(query=change_pass, kwargs=args)
            return True
        except Error:
            return False




    def select_data (self, data, type='user_id'):
        select_sql = "select user_id, name, email from user_data"
        select_sql_id = select_sql + " where user_id = %s"
        select_sql_name = select_sql + " where name = %s"
        select_sql_email = select_sql + " where email = %s"
        args = (data,)

        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            if type == 'user_id':
                cursor.execute(select_sql_id, args)
            if type == 'name':
                cursor.execute(select_sql_name, args)
            if type == 'email':
                cursor.execute(select_sql_email, args)
            res = []
            [res.append(row) for row in self.iter_row(cursor, 5)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def update_setting(self, user_id, name, password, email):
        update_sql = "update user_data set name=%s,pass=password(%s), email=%s where user_id = %s"
        args = (name, password, email, user_id)
        try:
            super().do_query(query=update_sql, kwargs=args)
            return True
        except Error:
            return False

    def select_item_id(self, user_id=None):
        select_sql = "select name,mode from user_data"
        select_sql_where = select_sql + " where name = %s"
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_sql) if user_id is None else cursor.execute(select_sql_where, (user_id,))
            res = []
            [res.append(list(row)) for row in self.iter_row(cursor, 5)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()