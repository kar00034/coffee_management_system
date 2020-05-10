from mysql.connector import Error

from dao.abs_das import Dao

insert_sql = "INSERT INTO sale VALUES(NULL, (select code from product where name = %s), %s, default)"
update_sql = "update sale set code=%s, salecnt=%s where no=%s"
delete_sql = "delete from sale where no = %s"
select_sql = "select name,salecnt,sale_price, DATE_FORMAT(date,'%Y-%m-%d %H:%i') from sale s left join sale_detail sd on s.no = sd.no left join product p on s.code = p.code where salecnt != 0"
select_sql_where_year = select_sql + " and DATE_FORMAT(date,'%Y') = %s"
select_sql_where_month = select_sql + " and DATE_FORMAT(date,'%Y %m') = %s"

select_sql2 = "select distinct(DATE_FORMAT(date,'%Y')) from sale s left join product p on s.code = p.code left join sale_detail sd on s.no = sd.no"
select_sql2_where = select_sql2 + " where DATE_FORMAT(date,'%Y') = %s"
select_sql3 = "select distinct(DATE_FORMAT(date,'%m')) from sale s left join product p on s.code = p.code left join sale_detail sd on s.no = sd.no where DATE_FORMAT(date,'%Y') = %s"


class SaleDao(Dao):

    def insert_item(self, name=None, salecnt=None, ):
        args = (name, salecnt,)
        try:
            super().do_query(query=insert_sql, kwargs=args)
            return True
        except Error:
            return False

    def update_item(self, code=None, price=None, saleCnt=None, no=None):
        args = (code, saleCnt, no)
        try:
            super().do_query(query=update_sql, kwargs=args)
            return True
        except Error:
            return False

    def delete_item(self, no=None):
        args = (no,)
        try:
            super().do_query(query=delete_sql, kwargs=args)
            return True
        except Error:
            return False

    def select_item(self, name=None):
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            if name is None:
                cursor.execute(select_sql)
                res = []
                [res.append(row) for row in self.iter_row(cursor, 5)]

            else:
                cursor.execute(select_sql2)
                res = set()

                [res.add(row) for row in self.iter_row(cursor, 5)]
                res = list(res)

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

    def select_date(self, date=None, y=0):
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            if y == 0:  # 연도 별 데이터 찾기
                cursor.execute(select_sql_where_year, (date,))
            elif y == 1:  # 연도 중복 제거
                cursor.execute(select_sql2_where, (date,))
            elif y == 2:  # 연도 별 월 찾기
                cursor.execute(select_sql3, (date,))
            elif y == 3:  # 월 별 데이터 찾기
                cursor.execute(select_sql_where_month, (date,))
            res = []
            [res.append(row) for row in self.iter_row(cursor, 5)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def select_sale_table(self):
        select_sale_sql = "select p.name, c.name, salecnt, sale_price, addtax, margin_price, DATE_FORMAT(date,'%Y-%m-%d %H:%i') " \
                          "from product p left join category c on p.category = c.no left join sale s on p.code = s.code " \
                          "left join sale_detail sd on s.no = sd.no where salecnt is not null and salecnt != 0"
        try:
            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_sale_sql)
            res = []
            [res.append(row) for row in self.iter_row(cursor, 5)]
            return res
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def select_graph(self):
        # p.name에 대해 {%m:salecnt} 의 값을 가지는 딕셔너리 month 와 그 키들을 리스트로 가진 res
        sel_mon_product = "select p.name, sum(sale_price) from sale_detail sd left join sale s on sd.no = s.no left join product p on s.code = p.code GROUP by name"
        try:
            name = []
            price = []

            conn = self.connection_Pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(sel_mon_product)
            for row in self.iter_row(cursor, 12):
                name.append(row[0])
                price.append(row[1])
            return name, price
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()
