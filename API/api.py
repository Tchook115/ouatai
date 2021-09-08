from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse

from rasa_ouatai.actions.actions import ActionDrawing
from rasa_sdk.executor import CollectingDispatcher
from ouatai import illustrator
import requests
from PIL import Image

import io


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

async def main(message):

    actions = ActionDrawing()
    df = actions.run(message, dispatcher = CollectingDispatcher())
    illustration = illustrator.Raconte_moi_un_bulldozer()
    package_output = illustration.df_to_calque(df)

    byte_calque = io.BytesIO(package_output[0].tobytes())
    print(str(package_output[1]))
    dict_output = {
        # 'image': byte_calque,
        'size_image' : str(package_output[0].size),
        'coordinates': str(package_output[1])
    }
    return StreamingResponse(
        content=byte_calque,
        headers=dict_output,
        media_type="image/png")
