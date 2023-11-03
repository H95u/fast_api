import mysql.connector
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from contextlib import closing
from configs.mysql_config import dbconfig


class User(BaseModel):
    link_avatar: str
    user_name: str
    ip_register: str
    device_register: str
    password: str
    email: str


class UserModel:
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['username'],
                                           password=dbconfig['password'], database=dbconfig['database'])
        self.con.autocommit = True
        self.cur = self.con.cursor(dictionary=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def get_users(self, email: str, ip_register: str):
        conditions = []
        params = {}

        if email:
            conditions.append("email LIKE %(email)s")
            params['email'] = f"%{email}%"
        if ip_register:
            conditions.append("ip_register LIKE %(ip_register)s")
            params['ip_register'] = f"%{ip_register}%"

        sql = "SELECT * FROM user"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        with closing(self.con):
            self.cur.execute(sql, params)
            result = self.cur.fetchall()
            if result:
                return result
            return {"message": "No data found"}

    def add_user_model(self, data: User):
        sql = "INSERT INTO user (link_avatar, user_name, ip_register, device_register, password, email, count_sukien, count_comment, count_view) " \
              "VALUES (%(link_avatar)s, %(user_name)s, %(ip_register)s, %(device_register)s, %(password)s, %(email)s, 0, 0, 0)"

        try:
            with closing(self.con):
                self.cur.execute(sql, data.dict())  # Use data.dict() to convert the Pydantic model to a dictionary
                if self.cur.rowcount > 0:
                    return JSONResponse(content={"message": "CREATED_SUCCESSFULLY"}, status_code=201)
                else:
                    return JSONResponse(content={"message": "Failed to create user"}, status_code=500)
        except Exception as e:
            # Handle database errors and return an appropriate response
            return JSONResponse(content={"message": "Database error"}, status_code=500)

    def patch_user_model(self, data, uid):
        qry = "UPDATE user SET "
        for key in data:
            if key != 'id_user':
                qry += f"{key}='{data[key]}',"
        qry = qry[:-1] + f" WHERE id_user = {uid}"
        with closing(self.con):
            self.cur.execute(qry)
            if self.cur.rowcount > 0:
                return JSONResponse({"message": "UPDATED_SUCCESSFULLY"}, 201)
            else:
                return JSONResponse({"message": "NOTHING_TO_UPDATE"}, 204)

    def delete_user_model(self, uid: int):
        with closing(self.con):
            self.cur.execute("DELETE FROM user WHERE id_user = %(uid)s", {"uid": uid})
            if self.cur.rowcount > 0:
                return {"message": "DELETED_SUCCESSFULLY"}
            return {"message": "CONTACT_DEVELOPER"}

    def update_user_model(self, data, uid: int):
        sql = (
            "UPDATE user SET link_avatar=%s, user_name=%s, ip_register=%s, "
            "device_register=%s, password=%s, email=%s WHERE id_user=%s"
        )

        values = (
            data.get('link_avatar', None),
            data.get('user_name', None),
            data.get('ip_register', None),
            data.get('device_register', None),
            data.get('password', None),
            data.get('email', None),
            uid
        )
        with closing(self.con):
            self.cur.execute(sql, values)

            if self.cur.rowcount > 0:
                return JSONResponse({"message": "UPDATED_SUCCESSFULLY"}, 201)
            else:
                return JSONResponse({"message": "NOTHING_TO_UPDATE"}, 204)
