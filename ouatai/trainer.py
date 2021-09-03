import numpy as np
import os
import math
from google.cloud import storage
from sketchrnn_ouatai import models, dataset, utils


BUCKET_TRAIN_DATA: "quickdraw_dataset"
BLOB_TRAIN_DATA = "sketchrnn"
BUCKET_NAME: "wagon-data-677-noyer"
BLOB_MODEL = 'models/'

def create_working_directories(self,dirs):
    for item in dirs:
        if not os.path.exists(item):
            os.mkdir(item)
            return True
        else:
            return False

class Trainer():
    def __init__(self, category):
        self.category = category
        self.checkpoint = None

    def upload_model_to_gcp(self):
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(BLOB_MODEL)
        blob.upload_from_filename(self.checkpoint)

    def copy_to_local(self):
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_TRAIN_DATA)
        blob = bucket.blob(BLOB_TRAIN_DATA)
        blob.download_to_filename(f'./{self.category}.npz')
        return True

    def get_data(self):
        """ function used in order to get the training data (or a portion of it) from bucket : quickdraw_dataset """
        self.copy_to_local(BUCKET_TRAIN_DATA,BLOB_TRAIN_DATA,self.category)
        data = np.load(f'./{self.category}.npz',encoding='latin1',allow_pickle=True)
        data_train = [dataset.cleanup(d) for d in data['train']]
        data_valid = [dataset.cleanup(d) for d in data['valid']]
        data_test = [dataset.cleanup(d) for d in data['test']]
        return data_train, data_valid, data_test

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
        checkpoint_dir = 'checkpoints'
        log_dir = 'logs'
        self.checkpoint = os.path.join(checkpoint_dir, 'sketch_rnn_' + self.category + '_weights.{:02d}.hdf5')
        sketchrnn.train(initial_epoch, train_dataset, val_dataset, self.checkpoint)


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
    trainer = Trainer('axe')
    print(" runs a training ")
    create_working_directories(['npz_repo','checkpoints','logs'])

    #copy npz file to local VM
    trainer.copy_to_local()

    #train model
    trainer.train_model(self, train_dataset, val_dataset, test_dataset)
    
    #upload to gstorage
    trainer.upload_model_to_gcp()

    #Delete directories content
