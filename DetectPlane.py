from keras.models import load_model
from numpy import resize




model = load_model("Mymodel.h5")

def Detect(image):
    img = resize(image,(1,128,128,3))
    print(model.predict(img))