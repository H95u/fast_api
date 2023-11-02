from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from controller import user_controller, checking_img_controller, auth_controller

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    allow_credentials=False,  # Disable credentials (cookies, auth)
    expose_headers=["*"],  # Expose all headers
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('Accepting client connection...')
    await websocket.accept()
    while True:
        try:
            # Wait for any message from the client
            data = await websocket.receive_text()

            # Send message to the client
            await websocket.send_text(data)
        except Exception as e:
            print('error:', e)
            break
    print('Bye..')


app.include_router(user_controller.router)
app.include_router(checking_img_controller.router)
app.include_router(auth_controller.router)
