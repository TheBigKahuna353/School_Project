import keras, numpy
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Flatten, Dense, Dropout, Conv2D, MaxPool2D
from keras.optimizers import sgd
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt

Dir = "C:/Users/jorda/Downloads/OIDv4_ToolKit-master/OID/Dataset/"


size = (128,128,3)

# Our training data will use a wide assortment of transformations to try
# and squeeze as much variety as possible out of our image corpus.
# However, for the validation data, we'll apply just one transformation,
# rescaling, because we want our validation set to reflect "real world"
# performance.
#
train_datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    rescale=1/255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
)
test_datagen = ImageDataGenerator(
    rescale=1/255,
)

# I found that a batch size of 128 offers the best trade-off between
# model training time and batch volatility.
batch_size = 100

# Notice the tiny target size, just 48x48!
train_generator = train_datagen.flow_from_directory(
    Dir + "training",
    target_size=(128,128),
    batch_size=batch_size,
    shuffle = True,
    class_mode='binary',
)
validation_generator = test_datagen.flow_from_directory(
    Dir + "validation",
    target_size=(128,128),
    batch_size=batch_size,
    class_mode='binary',
)

print(train_generator.image_shape)

print("Generators")

#define the model

model = Sequential()
model.add(Conv2D(16, 3, activation='relu', input_shape=size))
model.add(MaxPool2D(pool_size=2))
model.add(Conv2D(32, 3, activation='relu'))
model.add(MaxPool2D(pool_size=2))
model.add(Conv2D(64, 3, activation='relu'))
model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dense(1, activation='sigmoid'))


model.compile(
    optimizer= 'sgd',
    loss='binary_crossentropy',
    metrics=['accuracy']
)
model = load_model("Mymodel.h5")

print("Comiled ai")

print(len(train_generator.filenames) // batch_size)

history = model.fit_generator(
    train_generator,
    steps_per_epoch=len(train_generator.filenames) // batch_size,
    epochs=10,
    validation_data=validation_generator,
    callbacks=[
        EarlyStopping(patience=3, restore_best_weights=True),
        ReduceLROnPlateau(patience=2)
    ]
)

print("trained")

score = model.evaluate_generator(validation_generator, steps=100)

print(score)
model.save("Mymodel.h5")

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()



model.save("Mymodel.h5")



#model = load_model("Mymodel.h5")


#print(model.predict_generator(validation_generator))