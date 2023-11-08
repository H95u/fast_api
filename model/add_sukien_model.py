from fastapi import HTTPException

from configs.mysql_config import My_Connection
from fastapi.responses import JSONResponse


class Add_Sukien_Model:
    def get_add_sukiens(self):
        with My_Connection() as db_connection:
            cur = db_connection.cur
            cur.execute("select * from add_sukien")
            result = cur.fetchall()
            return JSONResponse(result)

    def delete_add_sukien(self, sid: int):
        with My_Connection() as db_connection:
            cur = db_connection.cur
            cur.execute("DELETE FROM add_sukien WHERE id = %(sid)s", {"sid": sid})

            if cur.rowcount > 0:
                return JSONResponse(content={"message": "DELETED_SUCCESSFULLY"})
            else:
                raise HTTPException(status_code=404, detail="No record found for the provided sid")

    def edit_add_sukien(self, sid: int):
        with My_Connection() as db_connection:
            cur = db_connection.cur
            cur.execute("DELETE FROM add_sukien WHERE id = %(sid)s", {"sid": sid})
            if cur.rowcount > 0:
                return {"message": "UPDATED_SUCCESSFULLY"}
            return {"message": "CONTACT_DEVELOPER"}
