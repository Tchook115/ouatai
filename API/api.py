from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse

from rasa_ouatai.actions.actions import ActionDrawing
from rasa_sdk.executor import CollectingDispatcher
from ouatai import illustrator
import requests
import json
import ast
from PIL import Image
import re
import pandas as pd

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
    headers = {'Content-Type': 'application/json'}
    payload = {'message': message}
    r = requests.post('http://localhost:5005/webhooks/rest/webhook',
                      headers=headers,
                      data=json.dumps(payload))
    r = ast.literal_eval(r.text)
    pattern = r"DataFrame:.*"
    text = re.findall(pattern, r[0]['text'])

    if text:
        txt = text[0][10:].split(',')
        df = pd.DataFrame(columns=[
            'category', 'color', 'size', 'num', 'vertical_position',
            'horizontal_position'
        ], data = [txt])
        illustration = illustrator.Raconte_moi_un_bulldozer()
        package_output = illustration.df_to_calque(df)

        byte_calque = io.BytesIO(package_output[0].tobytes())
        # print(str(package_output[1]))
        dict_output = {
            # 'image': byte_calque,
            'size_image' : str(package_output[0].size),
            'coordinates': str(package_output[1])
        }
        return StreamingResponse(
            content=byte_calque,
            headers=dict_output,
            media_type="image/png")
    # print(r[0]['text'])
    return {'text' : r[0]['text']}
