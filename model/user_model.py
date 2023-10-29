import mysql.connector
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from config.config import dbconfig


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

        self.cur.execute(sql, params)
        result = self.cur.fetchall()
        if result:
            return result
        return {"message": "No data found"}

    def add_user_model(self, data: User):
        sql = "INSERT INTO user (link_avatar, user_name, ip_register, device_register, password, email, count_sukien, count_comment, count_view) " \
              "VALUES (%(link_avatar)s, %(user_name)s, %(ip_register)s, %(device_register)s, %(password)s, %(email)s, 0, 0, 0)"

        try:
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
        self.cur.execute(qry)
        if self.cur.rowcount > 0:
            return JSONResponse({"message": "UPDATED_SUCCESSFULLY"}, 201)
        else:
            return JSONResponse({"message": "NOTHING_TO_UPDATE"}, 204)

    def delete_user_model(self, uid: int):
        self.cur.execute("DELETE FROM user WHERE id_user = %(uid)s", {"uid": uid})
        if self.cur.rowcount > 0:
            return {"message": "DELETED_SUCCESSFULLY"}
        return {"message": "CONTACT_DEVELOPER"}

    def update_user_model(self, data):
        self.cur.execute(
            f"UPDATE user SET link_avatar='{data['link_avatar']}', user_name='{data['user_name']}', ip_register='{data['ip_register']}',"
            f" device_register='{data['device_register']}', password='{data['password']}', email='{data['email']}' WHERE id={data['id']}")
        if self.cur.rowcount > 0:
            return JSONResponse({"message": "UPDATED_SUCCESSFULLY"}, 201)
        else:
            return JSONResponse({"message": "NOTHING_TO_UPDATE"}, 204)
