import numpy as np
import keras
from keras.models import load_model
import tensorflow as tf

# def init():
#     print("Model loading....")
#     model = load_model('VGG_MODEL.h5')
#     print("Model loaded")
#     graph = tf.get_default_graph()
#     return model, graph

def initPsoriasis():
    print("Psoriasis Model loading....")
    model = load_model('VGG_Psoriasis.h5')
    print("Psoriasis Model loaded")
    graph = tf.get_default_graph()
    return model, graph

def initHives():
    print("Hives Model loading....")
    model = load_model('VGG_Hives.h5')
    print("Hives Model loaded")
    graph = tf.get_default_graph()
    return model, graph

def initRingworm():
    print("Ring Worm Model loading....")
    model = load_model('VGG_Ringworm.h5')
    print("Ring Worm Model loaded")
    graph = tf.get_default_graph()
    return model, graph

def initEczema():
    print("Eczema Model loading....")
    model = load_model('VGG_Eczema.h5')
    print("Eczema Model loaded")
    graph = tf.get_default_graph()
    return model, graph

def initShingles():
    print("Shingles model loading.....")
    model = load_model("VGG_Shingles.h5")
    print("Shingles model loaded")
    graph = tf.get_default_graph()
    return model, graph