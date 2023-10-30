from fastapi import FastAPI
from controller import user_controller, checking_img_controller

app = FastAPI()

app.include_router(user_controller.router)
app.include_router(checking_img_controller.router)

