import mysql.connector
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from contextlib import closing
from configs.mysql_config import dbconfig


class ReportComment(BaseModel):
    id_report: int
    id_comment: int
    report_reason: str
    content: str
    id_user_report: int
    id_user_comment: int


class ReportCommentModel:
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['username'],
                                           password=dbconfig['password'], database=dbconfig['database'])
        self.con.autocommit = True
        self.cur = self.con.cursor(dictionary=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def get_comments(self):
        with closing(self.con):
            self.cur.execute("select * from report_comment")
            result = self.cur.fetchall()
            return JSONResponse(result)
