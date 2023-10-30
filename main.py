import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import user_controller, checking_img_controller

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    allow_credentials=False,  # Disable credentials (cookies, auth)
    expose_headers=["*"],  # Expose all headers
)

app.include_router(user_controller.router)
app.include_router(checking_img_controller.router)


