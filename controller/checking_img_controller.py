from fastapi import Query, Request

from main import app
from service.checking_img import checking_img


@app.post("/api/check-img")
async def check_img(request: Request):
    form_data = await request.form()
    return checking_img(form_data.get("link_img"))
