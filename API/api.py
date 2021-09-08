from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from rasa_ouatai import actions


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# define a root `/` endpoint
# @app.get("/")
# def index():
#     return {"greeting": "Hello world"}


@app.get("/")
async def main(query):
    return FileResponse("raw_data/scene.png")
