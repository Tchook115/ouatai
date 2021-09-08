import os
import io
import sys
import math
import numpy as np
import pandas as pd
import tensorflow as tf
from matplotlib import pyplot as plt
import seaborn as sns
import random
from sketchrnn_ouatai import models, dataset, utils
from PIL import Image
from PIL import ImageDraw

class Raconte_moi_un_bulldozer:
    def __init__(self, scene_size = (2560,1600)):
        self.scene_size = scene_size
        self.list_objects = None

    def get_random_position(hstart,hstop,vstart,vstop):
        hor = random.randint(hstart,hstop)
        vert = random.randint(vstart,vstop)
        return hor,vert

    def dessine_moi_un(word, temperature = 0.2, color = 'black', zoom = 1,lw = 2):
        '''
        This function return a unique generated image of one category, using the pretrained corresponding model.
        '''
        #This is the list of pretrained categories's models available
        model_list = sorted(os.listdir('./raw_data/Models'))
        words = []
        for model in model_list:
            words.append(model.split('.')[0])

        #Test if inputed word is an exiting category
        if word not in words:
            raise 'WordNotFoundError'

        #test de variables random
        images_path = os.path.join('./raw_data/Best_images/', f"best_{word}.npy")
        best_images = np.load(images_path, allow_pickle=True)
        max_seq_len = best_images[0].shape[0]-1
        data_train = [1 for k in range(10000)]

        # SketchRNN Model parameters
        hps = {
            "max_seq_len": max_seq_len,
            'batch_size': 100,
            "num_batches": math.ceil(len(data_train) / 100),
            "epochs": 1,
            "recurrent_dropout_prob": 0.1,
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

        # Instantiate model + initiate parameters
        sketchrnn = models.SketchRNN(hps)
        checkpoint = os.path.join('./raw_data/Models/', f"{word}.hdf5")
        sketchrnn.load_weights(checkpoint)

        # generating a unique image
        best_pic = random.choice(best_images)
        d = np.expand_dims(best_pic,0)
        z = sketchrnn.models['encoder'].predict(d[:,1:])[0]
        strokes = sketchrnn.sample(z=z, temperature=temperature)

        # Generating vectorized unique image
        final_object = utils.to_normal_strokes(strokes)
        figsize = (2*zoom,2*zoom)
        fig, ax = plt.subplots(figsize=figsize);
        utils.plot_strokes(ax, final_object, ec = color, lw = lw);

        # Figure to PIL image
        buf = io.BytesIO()
        fig.savefig(buf, format='png', transparent = True)
        buf.seek(0)
        image = Image.open(buf)
        image = image.copy()
        buf.close()

        return image

    def check_position(hor_pos, vert_pos, imgwidth, imheight, lst_coords):
        x_min_new = hor_pos
        x_max_new = hor_pos + imgwidth
        y_min_new = vert_pos
        y_max_new = vert_pos + imheight
        if lst_coords:
            for elem in lst_coords:
                x_min = elem[0]
                x_max = x_min + elem[2]
                y_min = elem[1]
                y_max = y_min + elem[3]
                cond1 = x_min_new <= x_min and x_max_new > x_min
                cond2 = x_min_new <= x_max and x_max_new > x_max
                cond3 = y_min_new <= y_min and y_max_new > y_min
                cond4 = y_min_new <= y_max and y_max_new > y_max
                cond5 = x_min_new >= x_min and x_max_new < x_max
                cond6 = y_min_new >= y_min and y_max_new < y_max
                if (cond1 and (cond3 or cond4 or cond6)) or (cond2 and (cond3 or cond4 or cond6))\
                 or (cond5 and (cond3 or cond4 or cond6)):
                    return False
        return True

    def construit_calque(self):
        '''
        Create a PIL.image transparent, with all the objects requested in df.
        list_objects = [[img_obj1, position_obj1], ...]
        '''
        if self.list_objects:
            calque = Image.new('RGBA', self.scene_size)
            for obj in self.list_objects:
                calque.paste(obj[0], obj[1])
            return calque
        return False

    def df_to_calque(self, nlp_df, lst_coords=None):
        if lst_coords is None:
            lst_coords = []
        self.list_objects = []
        vertical_positions = {'top' : 0, 'center' : int(self.scene_size[1]/3),'bottom' : int(2*self.scene_size[1]/3)}
        horizontal_positions = {'left' : 0, 'middle' : int(self.scene_size[0]/3), 'right' : int(2*self.scene_size[0]/3)}
        sizes = {'small' : 1/2, 'medium' : 1, 'big' : 2}

        #Inspecting DataFrame and generating images
        for index, row in nlp_df.iterrows():
            for _ in range(int(row['num'])):
                #Call method dessine_moi_un to get a unique image
                category = row['category']
                color = row['color']
                size = sizes[row['size']]
                image = Raconte_moi_un_bulldozer.dessine_moi_un(category, color = color, zoom = size)
                imgwidth, imgheight = image.size

                #Define position limits in the sub-scene
                hstart = horizontal_positions[row['horizontal_position']]
                hstop = hstart + (horizontal_positions['middle'] - imgwidth)
                vstart = vertical_positions[row['vertical_position']]
                vstop = vstart + (vertical_positions['center'] - imgheight)
                #liste de tuple : (hpos,vpos,imwidth,imweight)
                #Check
                for _ in range(10):
                    #Generate random coordinates
                    random_position = Raconte_moi_un_bulldozer.get_random_position(hstart,hstop,vstart,vstop)
                    #check for collision
                    if Raconte_moi_un_bulldozer.check_position(random_position[0],random_position[1],imgwidth,imgheight,lst_coords):
                        #add image and its coordinates to list_objects
                        self.list_objects.append([image, (random_position[0],random_position[1])])
                        lst_coords.append((random_position[0],random_position[1],imgwidth,imgheight))
                        break
        calque = Raconte_moi_un_bulldozer.construit_calque(self)


        #Les traits noirs pour les tests
        # draw = ImageDraw.Draw(calque)
        # for h in range(self.scene_size[0]):
        #     draw.point((h,vertical_positions['center']), fill="black")
        # for h in range(self.scene_size[0]):
        #     draw.point((h,vertical_positions['bottom']), fill="black")
        # for v in range(self.scene_size[1]):
        #     draw.point((horizontal_positions['middle'], v), fill="black")
        # for v in range(self.scene_size[1]):
        #     draw.point((horizontal_positions['right'], v), fill="black")

        return calque, lst_coords

if __name__ == '__main__':

    df = pd.DataFrame(np.array([['cat', 'blue', 'small', 2, 'center', 'middle'],
    ['bulldozer', 'orange', 'medium', 1, 'bottom', 'right'],
    ['rabbit', 'brown', 'small', 1, 'top', 'left'],]),
    columns=['category', 'color', 'size', 'num', 'vertical_position', 'horizontal_position'])
    def main(df):
        illustration = Raconte_moi_un_bulldozer()
        package_output = illustration.df_to_calque(df)
        return package_output

    main(df)
