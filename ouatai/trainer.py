import numpy as np
import os, shutil
import math
from google.cloud import storage
from sketchrnn_ouatai import models, dataset, utils

class Trainer():
    def __init__(self, category):
        self.category = category
        self.checkpoint = None
        self.epochnb = 100

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
        filename = f'sketch_rnn_{self.category}_weights.{self.epochnb}.hdf5'
        localpthfile = f'./checkpoints/{filename}'
        blobpathfile = f'models/{filename}'
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(blobpathfile)
        blob.upload_from_filename(localpthfile)

    def copy_to_local(self):
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_TRAIN_DATA)
        blob = bucket.blob(BLOB_TRAIN_DATA)
        blob.download_to_filename(f'./npz_repo/{self.category}.npz')
        return True

    def get_data(self):
        """ function used in order to get the training data (or a portion of it) from bucket : quickdraw_dataset """
        self.copy_to_local()
        data = np.load(f'./npz_repo/{self.category}.npz',encoding='latin1',allow_pickle=True)
        data_train = [dataset.cleanup(d) for d in data['train']]
        data_valid = [dataset.cleanup(d) for d in data['valid']]
        data_test = [dataset.cleanup(d) for d in data['test']]
        hps = {
            "max_seq_len": max(map(len, np.concatenate([data_train, data_valid, data_test]))),
            'batch_size': 100, #100
            "num_batches": math.ceil(len(data_train) / 100),
            "epochs": self.epochnb, #100
            "recurrent_dropout_prob": 0.0, ## 0.0 for gpu lstm
            "enc_rnn_size": 256, #256
            "dec_rnn_size": 512, #512
            "z_size": 128, #128
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
        checkpoint_dir = './checkpoints'
        #log_dir = 'logs'
        self.checkpoint = os.path.join(checkpoint_dir, 'sketch_rnn_' + self.category + '_weights.{}.hdf5')
        sketchrnn.train(initial_epoch, train_dataset, val_dataset, self.checkpoint)

if __name__ == '__main__':
    ### GOOGLE STORAGE INFO ###
    BUCKET_TRAIN_DATA = "quickdraw_dataset"
    BUCKET_NAME = "wagon-data-677-sdb"
    WORKING_FOLDERS = ['npz_repo','checkpoints','logs']
    ### MODEL LIST TO TRAIN ###
    categorielist = [
        'peanut', 'pig', 'pizza', 'rabbit', 'rainbow', 'sailboat', 'scissors',
        'skateboard', 'snail', 'snowman', 'spider'
    ]
    ### SCRIPT ###
    #Start training loop over model list
    for categorie in categorielist:
        BLOB_TRAIN_DATA = f"sketchrnn/{categorie}.npz"
        #Instantiate Trainer
        trainer = Trainer(categorie)
        print(f"### Training start for model {categorie} ###")

        #Create working directories in the running VM in case they doesn't exist
        print(f"### Start create_working_directories ###")
        trainer.create_working_directories(WORKING_FOLDERS)
        print(f"done.\n")
        #quit()
        #copy npz file to local VM
        print(f"### Start copy_to_local ###")
        trainer.copy_to_local()
        print(f"done.\n")

        #Prepare data
        print(f"### Start get_data ###")
        modeltotrain = trainer.get_data()
        print(f"done.\n")

        #Preprocess data
        print(f"### Start preprocess_data ###")
        preproc = trainer.preprocess_data(modeltotrain[0],modeltotrain[1], modeltotrain[3])
        print(f"done.\n")

        #train model
        print(f"### Start train_model ###")
        trainer.train_model(preproc[0], preproc[1],modeltotrain[3])
        BLOB_MODEL = trainer.category
        print(f"done.\n")

        #upload model trained back to gstorage
        trainer.copy_to_gcp()
        #Delete directories content
        trainer.delete_folder_content(WORKING_FOLDERS)
        print(f"### Model {categorie} trained and stored in bucket {BUCKET_NAME}/models/{BLOB_MODEL} ###\nFolders cleaned.")
