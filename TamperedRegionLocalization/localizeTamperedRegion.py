from keras.models import Model
from keras.layers import Conv2D, Input
from keras.preprocessing.image import array_to_img, img_to_array, load_img
import keras.backend as K
import sys

argvs = sys.argv
argc = len(argvs)
if (argc != 1):
  print('Usage: # python %s' % argvs[0])
  quit()

K.set_image_dim_ordering('th')

def generate_model(model_input):
    x = model_input
    x = Conv2D(64, (3, 3), kernel_initializer='he_normal', padding='same', dilation_rate=1, activation='relu', trainable=False)(x)
    x = Conv2D(64, (3, 3), kernel_initializer='he_normal', padding='same', dilation_rate=2, activation='relu', trainable=False)(x)
    x = Conv2D(64, (3, 3), kernel_initializer='he_normal', padding='same', dilation_rate=3, activation='relu', trainable=False)(x)
    x = Conv2D(64, (3, 3), kernel_initializer='he_normal', padding='same', dilation_rate=4, activation='relu', trainable=False)(x)
    x = Conv2D(64, (3, 3), kernel_initializer='he_normal', padding='same', dilation_rate=3, activation='relu', trainable=False)(x)
    x = Conv2D(64, (3, 3), kernel_initializer='he_normal', padding='same', dilation_rate=2, activation='relu', trainable=False)(x)
    x = Conv2D(2, (3, 3), kernel_initializer='he_normal', padding='same', dilation_rate=1, activation=None, trainable=False)(x)
    model_output = x
    model = Model(inputs=[model_input], outputs=[model_output])
    return model, model_output

def load_image(file_path):
    img = img_to_array(load_img(file_path))
    img = img / 255.0
    height = img.shape[1]
    width = img.shape[2]
    img = img.reshape((1, 3, height, width))
    return img

image = load_image("tampered.bmp")
input = Input(shape=(image.shape[1:]))
model, output = generate_model(input)

model = Model(inputs=[input], outputs=[output])
model.load_weights("../model/trained.hdf5")

result = model.predict(image)[0]
result = result.clip(0, 1)

im = array_to_img(result[1,:,:].reshape(1,result.shape[1],result.shape[2])*255, scale=False)
im.save("localizedTamperedRegion.png")
