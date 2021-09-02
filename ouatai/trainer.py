import numpy as np
from google.cloud import storage

BUCKET_NAME: "wagon-data-677-noyer"
BUCKET_TRAIN_DATA_NAME: "quickdraw_dataset"

def get_data(category_name):
    """ function used in order to get the training data (or a portion of it) from bucket : quickdraw_dataset """
    #input : nom d'une categorie
    #output : return 3 variable : train, valid,test


    client = storage.Client()
    bucket = client.get_bucket('<your-bucket-name>')
    blob = bucket.blob('my-test-file.txt')
    blob.upload_from_string('this is test content!')
    !gsutil cp gs://quickdraw_dataset/sketchrnn/{category_name}.npz .
    data = np.load(f'{category_name}.npz',encoding='latin1',allow_pickle=True)

def preprocess(df):
    """ function that pre-processes the data """
    #input : variables data_train et data_
    printi = f'prepcessing data'
    return printi


def train_model(X_train, y_train):
    """ function that trains the model """
    printi = f'training model'
    return printi


def save_model(reg):
    """ method that saves the model into a .joblib file and uploads it on Google Storage /models folder """
    printi = f'saving model'
    return printi

def pipeline_generator():
    """function used to generate a pipeline for cleaning and training categories gathered in get_data(). Tasks are parallelized between categories"""
    printi = f'creating pipeline'
    return printi

def check_existing_trainings():
    printi = f'this category doesnt exist'
    return printi

if __name__ == '__main__':
    print(" runs a training ")