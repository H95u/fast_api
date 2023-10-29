import mysql.connector
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from config.config import dbconfig


class Saved_sukien(BaseModel):
    link_nam_goc: str
    link_nu_goc: str
    link_nam_chua_swap: str
    link_nu_chua_swap: str
    link_da_swap: str
    thoigian_swap: str
    ten_su_kien: str
    noidung_su_kien: str


