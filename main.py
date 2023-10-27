from fastapi import FastAPI

app = FastAPI()

try:
    from controller import *
except Exception as e:
    print(e)
