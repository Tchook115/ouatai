
#--------------------------------------------------
from numpy.core.fromnumeric import cumsum
from pkg_resources import require
import streamlit as st
import streamlit.components.v1 as components
import time
import folium
import pandas as pd
import requests
from PIL import Image
import io


@st.cache
def display(content, final):
    message = {'message': content}
    # st.text(message['message'])
    response = requests.get(url, params=message)
    if content != '':
        image_data = response.content
        calque = Image.frombytes('RGBA', size_image, image_data)
        final = calque_merger(calque, final)
    return final
    # imgs[0].style.backgroundColor = 'yellow';


url = 'http://127.0.0.1:8000/'

st.set_page_config(
    page_title="Once Upon A Time AI",  # => Quick reference - Streamlit
    page_icon="📖",
    layout="centered",  # wide
    initial_sidebar_state="auto")
'''
# Once Upon A Time AI

'''

# components.html(
#     """
#     <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
#     <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
#     <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
#     <div id="accordion">
#       <div class="card">
#         <div class="card-header" id="headingOne">
#           <h5 class="mb-0">
#             <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
#             Collapsible Group Item #1
#             </button>
#           </h5>
#         </div>
#         <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordion">
#           <div class="card-body">
#             Collapsible Group Item #1 content
#           </div>
#         </div>
#       </div>
#       <div class="card">
#         <div class="card-header" id="headingTwo">
#           <h5 class="mb-0">
#             <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
#             Collapsible Group Item #2
#             </button>
#           </h5>
#         </div>
#         <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordion">
#           <div class="card-body">
#             Collapsible Group Item #2 content
#           </div>
#         </div>
#       </div>
#     </div>
#     """,
#     height=600,
# )

st.text('draw me a big cat to the top left')
st.text('draw me a big cat to the bottom right')
st.text('draw me a big cat to the top right')
size_image = (2560, 1600)

# if st.button("clear cache"):
#     params = {}
#     st.experimental_set_query_params(**params)


def calque_merger(current_scene, new_scene):
    final = Image.new("RGBA", size_image)
    final.paste(current_scene, (0, 0), current_scene)
    final.paste(new_scene, (0, 0), new_scene)
    return final


if "persisted_variable" not in st.session_state:
    st.session_state.persisted_variable = 0  # initialize the session state variable

if st.session_state.persisted_variable == 0:
    final1 = Image.new("RGBA", size_image)
    final2 = Image.new("RGBA", size_image)
    final3 = Image.new("RGBA", size_image)

#final = calque_merger(calque_merger(final3, final2), final1)
# if st.experimental_get_query_params():
#     st.write(st.experimental_get_query_params())
#     cache = st.experimental_get_query_params()['merged_calque']
#     final = Image.frombytes('RGBA', size_image, cache)

# final = Image.frombytes('RGBA', size_image, final_bytes)

content = st.text_input('Ask for a drawing', '')

message = {'message': content}
st.text(message['message'])

# st.image(final)

response = requests.get(url, params=message)
print(st.session_state.persisted_variable)
if content != '':
    st.text('1')
    st.text(st.session_state.persisted_variable)
    if st.session_state.persisted_variable == 0:
        st.text('2')
        st.session_state.persisted_variable += 1
        st.text(st.session_state.persisted_variable)
        # size_image = eval(response.headers['size_image'])
        # st.write(f"size image : {size_image}")
        # coordinates = eval(response.headers['coordinates'])
        image_data = response.content
        final1 = Image.frombytes('RGBA', size_image, image_data)
final = calque_merger(calque_merger(final3, final2), final1)
#    final1 = Image.new("RGBA", size_image)

st.image(final)
# imgs[0].style.backgroundColor = 'yellow';

content2 = st.text_input('Ask for a second drawing', '')

message = {'message': content2}
# st.text(message['message'])
response = requests.get(url, params=message)
if content2 != '' and st.session_state.persisted_variable == 1:
    st.session_state.persisted_variable += 1
    image_data = response.content
    final2 = Image.frombytes('RGBA', size_image, image_data)

final = calque_merger(calque_merger(final3, final2), final1)
#final = display(content2, final)
st.image(final)

#content3 = st.text_input('Ask for a third drawing',
#  '')
#final = display(content3, final)
#st.image(final)
