from pydantic import BaseModel
from configs.mysql_config import My_Connection
from fastapi.responses import JSONResponse


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
    def get_saved_sukiens(self):
        with My_Connection() as db_connection:
            db_connection.cur.execute("select * from saved_sukien")
            result = db_connection.cur.fetchall()
            return result

    def delete_saved_sukien(self, sid: int):
        with My_Connection() as db_connection:
            db_connection.cur.execute("DELETE FROM saved_sukien WHERE id = %(sid)s", {"sid": sid})
            if db_connection.cur.rowcount > 0:
                return {"message": "DELETED_SUCCESSFULLY"}
            return {"message": "CONTACT_DEVELOPER"}

    def patch_saved_sukien(self, sid: int, data):
        qry = "UPDATE saved_sukien SET "
        for key in data:
            if key != 'id':
                qry += f"{key}='{data[key]}',"
        qry = qry[:-1] + f" WHERE id = {sid}"
        with My_Connection() as db_connection:
            db_connection.cur.execute(qry)
            if db_connection.cur.rowcount > 0:
                return JSONResponse({"message": "UPDATED_SUCCESSFULLY"}, 200)
            else:
                return JSONResponse({"message": "NOTHING_TO_UPDATE"}, 204)
