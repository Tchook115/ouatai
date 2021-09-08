from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse

from rasa_ouatai.actions.actions import ActionDrawing
from rasa_sdk.executor import CollectingDispatcher
from ouatai import illustrator
import requests
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
def main(message):

    actions = ActionDrawing()
    df = actions.run(message, dispatcher = CollectingDispatcher())
    illustration = illustrator.Raconte_moi_un_bulldozer()
    package_output = illustration.df_to_calque(df)
    # package_output[0].save('raw_data/scene.png')
    print('-------------------------------------------------')
    print(package_output)
    print('-------------------------------------------------')

    return {
        'image': FileResponse(package_output[0]),
        'coordinates': package_output[1]
    }
    # return FileResponse('raw_data/scene.png')



# if __name__ == '__main__':
#     url = 'http://127.0.0.1:8000/'
#     message = 'draw me a little blue cat in the top left'
#     response = requests.get(url, params=message)

#     response[0].save('raw_data/scene_requested.png')
#     #=> {wait: 64}
