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

    def get_user_contact_history(self, uid: int):
        with My_Connection() as db_connection:
            db_connection.cur.execute("select link_avatar,user_name,timestamp,content from contact_history_view where receiver_id = %(uid)s",
                                      {"uid": uid})
            result = db_connection.cur.fetchall()
            if result:
                return result
            return {"message": "No data found"}
