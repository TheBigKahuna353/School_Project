import keras, numpy
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array

Dir = "C:/Users/jorda/Downloads/OIDv4_ToolKit-master/OID/Dataset/"
size = (128,128,3)

test_datagen = ImageDataGenerator(
    rescale=1/255,
)

batch_size = 64

validation_generator = test_datagen.flow_from_directory(
    Dir + "validation",
    target_size=(128,128),
    batch_size=batch_size,
    class_mode='binary',
)
model = load_model("Mymodel.h5")
#print(model.weights)
img = load_img(Dir + "training/_other/56.jpg", target_size=(128,128))
img = img_to_array(img)

img = img / 255

#print(img.shape)
img = numpy.reshape(img,(1,128,128,3))
print(model.predict(img))

print(model.metrics_names)
print(model.evaluate_generator(validation_generator))