import warnings  
with warnings.catch_warnings():  
    warnings.filterwarnings("ignore",category=FutureWarning)
    import tensorflow as tf  
    import keras.models   
    from keras.models import load_model
    from keras import backend as K


def init():

    K.clear_session()

    model = load_model('Models/model.h5')
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    graph = tf.get_default_graph()
    return model,graph