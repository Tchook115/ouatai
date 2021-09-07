# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from pandas._config.config import reset_option
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from nltk.stem import WordNetLemmatizer
import pandas as pd
import random
#
#


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello Alex!")

        return []

class ActionDrawing(Action):
    def name(self) -> Text:
        return "action_drawing"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #dispatcher.utter_message(text="I can draw")
        message = tracker.latest_message.get('text')
        text = message.lower()
        for punctuation in string.punctuation:
            text = text.replace(punctuation, '')

        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        text = [w for w in word_tokens if not w in stop_words]
        lemmatizer = WordNetLemmatizer()
        text = [lemmatizer.lemmatize(word) for word in text]


        #ground/sky categories
        lst_ground = ['apple','bread','candle','cat','church',\
            'crab','cup','envelope','face','firetruck',\
            'frog','grass','hammer','knife','leaf','lollipop','mushroom',\
            'pants','pear','postcard','radio','sheep','skull','snake','square',\
            'sword','t-shirt','teddy-bear','train','windmill',\
            'The Eiffel Tower','banana','bear','bench','book','broom',\
            'bulldozer','bus','cactus','camel','car','cello','circle',\
            'cookie','crocodile','donut','drums','eraser','flower','giraffe',\
            'guitar','harp','hedgehog','hourglass','jail','ladder','lighter',\
            'mailbox','palm tree','pencil','pineapple', 'potato','mountain',\
            'rifle', 'school bus', 'shorts','smiley face','sock', 'stairs',
            'syringe', 'telephone', 'tree']

        lst_sky = [
            'airplane', 'bat',  'cloud',
            'dragon', 'owl', 'angel', 'diamond', 'moon',
            'parachute', 'rain', 'snowflake', 'zigzag']

        lst_all = [
            'bee', 'bird', 'butterfly', 'dolphin', 'feather', 'fish', 'ocean',
            'submarine', 'umbrella','whale']

        all_categories = lst_ground.extend(lst_all)
        all_categories = all_categories.extend(lst_sky)

        i = 0

        #default values
        size = 'medium'
        color = 'black'
        num = 1
        horizontal_position = random.choice(['middle', 'left', 'right'])
        vertical_position = 'center'



        #possible choices
        size_lst = ['medium', 'small', 'big']
        color_lst = ['black','red','blue','green','brown', 'yellow',
                 'orange', 'purple', 'gray', 'white', 'gold']
        num_lst = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

        num_lst_word = ['one', 'two', "three", 'four', 'five', 'six', 'seven', 'eight',
                    'nine', 'ten']
        vertical_position_lst = ['center', 'top', 'bottom']
        horizontal_position_lst = ['middle', 'left', 'right']


        for word in all_categories:
            if word in text:
                i = 1
                category = word
                if category in lst_ground:
                    vertical_position = random.choice(['center', 'bottom'])
                elif category in lst_sky:
                    vertical_position = 'top'
                elif category in lst_all:
                    vertical_position = random.choice(vertical_position_lst)

        if i == 0:
            dispatcher.utter_message(text="I don't know this category")
        else:
            for word in text:
                if word in size_lst:
                    size = word
                if word in color_lst:
                    color = word
                if word in num_lst:
                    num = num_lst.index(word) + 1
                if word in num_lst_word:
                    num = num_lst_word.index(word) + 1
                if word in vertical_position_lst:
                    vertical_position = word
                if word in horizontal_position_lst:
                    horizontal_position = word

            df = pd.DataFrame({
                    'category': category,
                    'color': color,
                    'size': size,
                    'num': num,
                    'vertical_position': vertical_position,
                    'horizontal_position': horizontal_position
                }, index=[0])
            print(df)
            dispatcher.utter_message(text=' '.join(text))


        return []

# draw = drawing()
# draw.run(CollectingDispatcher,
#             Tracker,
#             Dict[Text, Any])
