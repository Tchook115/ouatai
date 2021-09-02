import numpy as np
from google.cloud import storage

BUCKET_NAME: "wagon-data-677-noyer"
BUCKET_TRAIN_DATA_NAME: "quickdraw_dataset"
from _typeshed import Self
from sketchrnn import models
import math
import os
import numpy as np

    def __init__(self, category):
        self.category = category

    def get_data(list):
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


    def train_model(self, train_dataset, val_dataset, test_dataset):
        """ function that trains the model """
        hps = {
            "max_seq_len": max(map(len, np.concatenate([train_dataset, val_dataset, test_dataset]))),
            'batch_size': 100,
            "num_batches": math.ceil(len(train_dataset) / 100),
            "epochs": 100,
            "recurrent_dropout_prob": 0.1, ## 0.0 for gpu lstm
            "enc_rnn_size": 256,
            "dec_rnn_size": 512,
            "z_size": 128,
            "num_mixture": 20,
            "learning_rate": 0.001,
            "min_learning_rate": 0.00001,
            "decay_rate": 0.9999,
            "grad_clip": 1.0,
            'kl_tolerance': 0.2,
            'kl_decay_rate': 0.99995,
            "kl_weight": 0.5,
            'kl_weight_start': 0.01,
        }
        sketchrnn = models.SketchRNN(hps)
        initial_epoch = 0
        initial_loss = 0.05
        checkpoint_dir = BUCKET_NAME


        #log_dir = '/content/gdrive/My Drive/sketchrnn/logs'
        checkpoint = os.path.join(checkpoint_dir, 'sketch_rnn_' + self.category + '_weights.{:02d}_{:.2f}.hdf5')
        sketchrnn.train(initial_epoch, train_dataset, val_dataset, checkpoint)



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
