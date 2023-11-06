import json
import re
from functools import wraps

import jwt
from fastapi import Request
from configs.mysql_config import My_Connection
from fastapi.responses import JSONResponse


class Auth_Model:

    def token_auth(self):
        def inner1(func):
            @wraps(func)
            def inner2(request: Request, *args):
                endpoint = request.url.path
                authorization = request.headers.get("authorization")
                if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                    token = authorization.split(" ")[1]
                    try:
                        jwt_decoded = jwt.decode(token, "Hieu@123", algorithms="HS256")
                    except jwt.ExpiredSignatureError:
                        return JSONResponse({"error": "token_expired"}, 401)
                    role_id = jwt_decoded['payload']['role_id']
                    with My_Connection() as db_connection:
                        db_connection.cur.execute(f"select roles from accessibility_view where endpoint = '{endpoint}'")
                        result = db_connection.cur.fetchall()
                    if len(result) > 0:
                        allowed_roles = json.loads(result[0]['roles'])
                        if role_id in allowed_roles:
                            return func(request, *args)
                        else:
                            return JSONResponse({"error": "invalid_role"}, 401)
                    else:
                        return JSONResponse({"error": "invalid_endpoint"}, 404)
                else:
                    return JSONResponse({"error": "invalid_token"}, 401)

            return inner2

        return inner1

    @classmethod
    def change_user_password(cls, data, uid):
        with My_Connection() as db_connection:
            db_connection.cur.execute("SELECT * FROM user WHERE id_user = %(uid)s", {"uid": uid})
            result = db_connection.cur.fetchone()

            if result:
                current_password = data.get('current_password')
                new_password = data.get('new_password')
                if result['id_user'] == uid and result['password'] == current_password:
                    db_connection.cur.execute("UPDATE user SET password = %(new_password)s WHERE id_user = %(uid)s",
                                              {"new_password": new_password, "uid": uid})
                    return JSONResponse({"message": "Your password successfully updated"}, 200)
                else:
                    return JSONResponse({"message": "Current password is incorrect"}, 400)
            else:
                return JSONResponse({"message": "User not found"}, 404)

    @classmethod
    def login_user(self, data):
        with My_Connection() as db_connection:
            # Use placeholders in your SQL query to prevent SQL injection
            query = "SELECT * FROM user WHERE (user_name = %s OR email = %s) AND password = %s"
            db_connection.cur.execute(query, (data['username_or_email'], data['username_or_email'], data['password']))
            result = db_connection.cur.fetchall()

            if len(result) == 1:  # Check the length of the result list
                return JSONResponse({"message": "Login successfully", "user": result[0]}, status_code=200)
            else:
                return JSONResponse({"message": "Login failed"}, status_code=401)
