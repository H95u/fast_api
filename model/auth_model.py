import mysql.connector
from configs.mysql_config import dbconfig
from fastapi.responses import JSONResponse
from contextlib import closing


class Auth_Model:
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['username'],
                                           password=dbconfig['password'], database=dbconfig['database'])
        self.con.autocommit = True
        self.cur = self.con.cursor(dictionary=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def change_user_password(self, data, uid):
        with closing(self.con):
            self.cur.execute("SELECT * FROM user WHERE id_user = %(uid)s", {"uid": uid})
            result = self.cur.fetchone()

            if result:
                current_password = data.get('current_password')
                new_password = data.get('new_password')
                if result['id_user'] == uid and result['password'] == current_password:
                    self.cur.execute("UPDATE user SET password = %(new_password)s WHERE id_user = %(uid)s",
                                     {"new_password": new_password, "uid": uid})
                    return JSONResponse({"message": "Your password successfully updated"}, 200)
                else:
                    return JSONResponse({"message": "Current password is incorrect"}, 400)
            else:
                return JSONResponse({"message": "User not found"}, 404)

    def login_user(self, data):
        with closing(self.con):
            self.cur.execute("SELECT * FROM user")
            result = self.cur.fetchall()

            for u in result:
                if u['user_name'] == data.get('user_name') and u['password'] == data.get('password'):
                    return JSONResponse({"message": "login successfully", "user": u}, status_code=200)

            return JSONResponse({"message": "Login failed"}, status_code=401)
