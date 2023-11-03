import mysql.connector
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from configs.mysql_config import dbconfig


class Saved_sukien(BaseModel):
    link_nam_goc: str
    link_nu_goc: str
    link_nam_chua_swap: str
    link_nu_chua_swap: str
    link_da_swap: str
    thoigian_swap: str
    ten_su_kien: str
    noidung_su_kien: str


class Saved_Sukien_Model:
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['username'],
                                           password=dbconfig['password'], database=dbconfig['database'])
        self.con.autocommit = True
        self.cur = self.con.cursor(dictionary=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def get_saved_sukiens(self):
        self.cur.execute("select * from saved_sukien")
        result = self.cur.fetchall()
        return result

    def delete_saved_sukien(self, sid: int):
        self.cur.execute("DELETE FROM saved_sukien WHERE id = %(sid)s", {"sid": sid})
        if self.cur.rowcount > 0:
            return {"message": "DELETED_SUCCESSFULLY"}
        return {"message": "CONTACT_DEVELOPER"}
