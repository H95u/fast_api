import mysql.connector
from configs.mysql_config import dbconfig
from fastapi.responses import JSONResponse
from contextlib import closing


class Add_Sukien_Model:
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['username'],
                                           password=dbconfig['password'], database=dbconfig['database'])
        self.con.autocommit = True
        self.cur = self.con.cursor(dictionary=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def get_add_sukiens(self):
        with closing(self.con):
            self.cur.execute("select * from add_sukien")
            result = self.cur.fetchall()
            return result

    def delete_add_sukien(self, sid: int):
        with closing(self.con):
            self.cur.execute("DELETE FROM add_sukien WHERE id = %(sid)s", {"sid": sid})
            if self.cur.rowcount > 0:
                return {"message": "DELETED_SUCCESSFULLY"}
            return {"message": "CONTACT_DEVELOPER"}

    def edit_add_sukien(self, sid: int):
        with closing(self.con):
            self.cur.execute("DELETE FROM add_sukien WHERE id = %(sid)s", {"sid": sid})
            if self.cur.rowcount > 0:
                return {"message": "DELETED_SUCCESSFULLY"}
            return {"message": "CONTACT_DEVELOPER"}
