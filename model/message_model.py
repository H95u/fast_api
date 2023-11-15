from configs.mysql_config import My_Connection


class MessageModel:
    def get_messages_by_id_user(self, id_user: int):
        conditions = []
        params = {}
        if id_user:
            conditions.append("id_user = %(id_user)s")
            params['id_user'] = f"{id_user}"

        sql = "SELECT * FROM messages"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        with My_Connection() as db_connection:
            db_connection.cur.execute(sql, params)
            result = db_connection.cur.fetchall()
            if result:
                return result
            return {"message": "No data found"}
