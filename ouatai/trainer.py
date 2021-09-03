BUCKET_NAME: "wagon-data-677-noyer"
BUCKET_TRAIN_DATA_NAME: "quickdraw_dataset"
from _typeshed import Self
from sketchrnn_ouatai import models
import math
import os
import numpy as np
import google.cloud import storage

class Trainer():
    def __init__(self, category):
        self.category = category


    def get_data(list):
        """ function used in order to get the training data (or a portion of it) from bucket : quickdraw_dataset """
        printi = f'gathering these models dataset: {list}'
        return printi

    def preprocess(df):
        """ function that pre-processes the data """
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

        client = storage.Client()
        bucket = client.get_bucket(BUCKET_NAME)
        checkpoint = bucket.blob(f'models/{self.category}')

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
