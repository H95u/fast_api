from fastapi import HTTPException

from configs.mysql_config import My_Connection
from fastapi.responses import JSONResponse


class Add_Sukien_Model:
    def get_add_sukiens(self):
        db_connection = None
        try:
            # Create an instance of My_Connection
            db_connection = My_Connection()
            db_connection.establish_connection()

            # Access the connection and cursor
            cur = db_connection.cur
            cur.execute("select * from add_sukien")
            result = cur.fetchall()
            return JSONResponse(result)
        finally:
            db_connection.close_connection()

    def delete_add_sukien(self, sid: int):
        db_connection = None
        try:
            # Create an instance of My_Connection
            db_connection = My_Connection()
            db_connection.establish_connection()

            # Access the connection and cursor
            cur = db_connection.cur
            cur.execute("DELETE FROM add_sukien WHERE id = %(sid)s", {"sid": sid})

            if cur.rowcount > 0:
                return JSONResponse(content={"message": "DELETED_SUCCESSFULLY"})
            else:
                raise HTTPException(status_code=404, detail="No record found for the provided sid")
        except Exception as e:
            # Handle the exception, log it, or return an appropriate response
            return JSONResponse(content={"message": "CONTACT_DEVELOPER", "error": str(e)}, status_code=500)
        finally:
            # Close the connection immediately after the query
            db_connection.close_connection()

    def edit_add_sukien(self, sid: int):
        db_connection = None
        try:
            # Create an instance of My_Connection
            db_connection = My_Connection()
            db_connection.establish_connection()

            # Access the connection and cursor
            cur = db_connection.cur
            cur.execute("DELETE FROM add_sukien WHERE id = %(sid)s", {"sid": sid})
            if cur.rowcount > 0:
                return {"message": "UPDATED_SUCCESSFULLY"}
            return {"message": "CONTACT_DEVELOPER"}
        finally:
            db_connection.close_connection()
