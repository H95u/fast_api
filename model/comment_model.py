import mysql.connector
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from configs.mysql_config import dbconfig


class Comment(BaseModel):
    noi_dung_comment: str
    IP_Comment: str
    device_Comment: str
    id_toan_bo_su_kien: str
    imageattach: str
    thoi_gian_release: str
    id_user: int
    user_name: str
    avatar_user: str
    so_thu_tu_su_kien: int
    location: str


class CommentModel:
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['username'],
                                           password=dbconfig['password'], database=dbconfig['database'])
        self.con.autocommit = True
        self.cur = self.con.cursor(dictionary=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def get_comments(self, content: str, ip_comment: str, user_name: str):
        conditions = []
        params = {}

        if content:
            conditions.append("noi_dung_Comment LIKE %(content)s")
            params['content'] = f"%{content}%"
        if ip_comment:
            conditions.append("IP_Comment LIKE %(ip_comment)s")
            params['ip_comment'] = f"%{ip_comment}%"
        if user_name:
            conditions.append("user_name LIKE %(user_name)s")
            params['user_name'] = f"%{user_name}%"

        sql = "SELECT * FROM comment"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        self.cur.execute(sql, params)
        result = self.cur.fetchall()
        if result:
            return result
        return {"message": "No data found"}

    def delete_comment(self, cid: int):
        self.cur.execute("DELETE FROM comment WHERE id_Comment = %(cid)s", {"cid": cid})
        if self.cur.rowcount > 0:
            return {"message": "DELETED_SUCCESSFULLY"}
        return {"message": "CONTACT_DEVELOPER"}

    def edit_comment(self, data, cid: int):
        sql = (
            "UPDATE comment SET noi_dung_Comment=%s WHERE id_Comment=%s"
        )

        values = (
            data.get('noi_dung_Comment', None),
            cid
        )
        self.cur.execute(sql, values)
        if self.cur.rowcount > 0:
            return JSONResponse({"message": "UPDATED_SUCCESSFULLY"}, 201)
        else:
            return JSONResponse({"message": "NOTHING_TO_UPDATE"}, 204)
