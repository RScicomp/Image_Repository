### Excluding Imports ###
from PIL import Image, ImageOps
import numpy as np
import keras
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16
model = VGG16()
# from classify import process_image, model, predict


def import_and_predict(image_data, model):
    
        size = (224,224)    

        image = ImageOps.fit(image_data, size, Image.ANTIALIAS)
        image = image.convert('RGB')
        image = np.asarray(image)
        print(image.shape)
        image = (image.astype(np.float32) / 255.0)
        
        img_reshape = image[np.newaxis,...]
        
        prediction = model.predict(img_reshape)
        # convert the probabilities to class labels
        prediction = decode_predictions(prediction)
        return prediction

def import_compare(image1,image2):
    import imagehash
    size = (224,224) 
    #grayscale?   
    image1 = imagehash.average_hash(ImageOps.fit(image1,size, Image.ANTIALIAS))
    image2 = imagehash.average_hash(ImageOps.fit(image2,size, Image.ANTIALIAS))
    return(abs(image1-image2))
