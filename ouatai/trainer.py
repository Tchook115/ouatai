BUCKET_NAME: "wagon-data-677-noyer"
BUCKET_TRAIN_DATA_NAME: "quickdraw_dataset"

def get_data(list):
    """ function used in order to get the training data (or a portion of it) from bucket : quickdraw_dataset """
    printi = f'gathering these models dataset: {list}'
    return printi

def preprocess(df):
    """ function that pre-processes the data """
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