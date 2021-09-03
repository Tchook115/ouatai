import numpy as np
import os, shutil
import math
from google.cloud import storage
from sketchrnn_ouatai import models, dataset, utils

class Trainer():
    def __init__(self, category):
        self.category = category
        self.checkpoint = None

    def create_working_directories(self,dirs):
        for item in dirs:
            if not os.path.exists(item):
                os.mkdir(item)
                return f'"{item}" folder created.\n'

    def delete_folder_content(self,dirs):
        for item in dirs:
            folder = f'./{item}'
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    def copy_to_gcp(self):
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
        hps = {
            "max_seq_len": max(map(len, np.concatenate([data_train, data_valid, data_test]))),
            'batch_size': 100,
            "num_batches": math.ceil(len(data_train) / 100),
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
            'kl_weight_start': 0.01,}
        return data_train, data_valid, data_test,hps

    def preprocess_data(self,data_train,data_valid, hps):
        scale_factor = dataset.calc_scale_factor(data_train)
        train_dataset = dataset.make_train_dataset(data_train, hps['max_seq_len'], hps['batch_size'], scale_factor)
        val_dataset = dataset.make_val_dataset(data_valid, hps['max_seq_len'], hps['batch_size'], scale_factor)
        return train_dataset,val_dataset

    def train_model(self, train_dataset, val_dataset, hps):
        """ function that trains the model """
        sketchrnn = models.SketchRNN(hps)
        initial_epoch = 0
        #initial_loss = 0.05
        checkpoint_dir = 'checkpoints'
        #log_dir = 'logs'
        self.checkpoint = os.path.join(checkpoint_dir, 'sketch_rnn_' + self.category + '_weights.{:02d}.hdf5')
        sketchrnn.train(initial_epoch, train_dataset, val_dataset, self.checkpoint)

if __name__ == '__main__':
### GOOGLE STORAGE INFO ###
    BUCKET_TRAIN_DATA = "quickdraw_dataset"
    BLOB_TRAIN_DATA = "sketchrnn"
    BUCKET_NAME = "wagon-data-677-noyer"
    BLOB_MODEL = 'models/'
    WORKING_FOLDERS = ['npz_repo','checkpoints','logs']
### MODEL LIST TO TRAIN ###
    modellist = ['axe']
### SCRIPT ###
    #Start training loop over model list
    for model in modellist:
        #Instantiate Trainer
        trainer = Trainer(model)
        print(f"### Training start for model {model} ###\n")
        #Create working directories in the running VM in case they doesn't exist 
        trainer.create_working_directories(WORKING_FOLDERS)
        #copy npz file to local VM
        trainer.copy_to_local()
        #Prepare data
        modeltotrain = trainer.get_data()
        #Preprocess data
        preproc = trainer.preprocess_data(modeltotrain[0],modeltotrain[1], modeltotrain[3])
        #train model
        trainer.train_model(preproc[0], preproc[1], modeltotrain[2],modeltotrain[3])
        #upload model trained back to gstorage
        trainer.copy_to_gcp()
        #Delete directories content
        trainer.delete_folder_content(WORKING_FOLDERS)
        print(f"### Model {model} trained and stored in bucket {BUCKET_NAME}/{BLOB_MODEL} ###\n")
    for item in WORKING_FOLDERS:
        shutil.rmtree(f'./{WORKING_FOLDERS}')