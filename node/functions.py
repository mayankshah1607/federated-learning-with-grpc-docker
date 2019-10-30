import numpy as np
import pandas as pd
from load import *
import base64

def SendModel(modelString):
    try:
        with open("Models/model.h5","wb") as file:
            file.write(base64.b64decode(modelString))
            print("Successfully saved model...")
            return 1
    except:
        print("An error occured!")
        return 0


#Train() is used to re-train the model
def Train():

    print("Starting training...")
    model,graph = init()
    data = pd.read_csv('data/data.csv')
    X = data.iloc[:,1:-1].values
    y = data.iloc[:,-1].values

    with graph.as_default():
        model.fit(X,y,verbose=0)
    print("Done training")
    model.save('Models/model.h5')
    
    with open('Models/model.h5','rb') as file:
        encoded_string = base64.b64encode(file.read())
    print("Model trained and saved successfully!")
    
    return encoded_string
    
#GenerateData() is used for generating new batches of training data
def GenerateData():

    def Sigmoid(z):
        return 1/(1+np.exp(-z))
    
    def eqn(input_vals):

        x1 = input_vals[0]
        x2 = input_vals[1]
        x3 = input_vals[2]
        x4 = input_vals[3]
        
        """Totally random values that the neural network must learn"""
        m1 = 0.5447894
        m2 = 0.007894674
        m3 = 0.012252348
        m4 = 0.007867
        b = 0.03345

        y = m1*x1 + m2*x2 + m3*x3 + m4*x4 + b

        return np.round(Sigmoid(y))

    try:
        data = []
        """Generate 1000 data points"""
        for _ in range(10000):
            row = (np.random.sample(4) * np.random.uniform(5,0.0001)) + np.random.uniform(-5,5) # Generate array of 4 numbers
            row = np.append(row, eqn(row))
            data.append(row)
        df = pd.DataFrame(data, columns=['x1','x2','x3','x4','y'])
        df.reset_index()
        df.to_csv('data/data.csv')
        print("Data generated")
        return 1
    except:
        print("An error occured")
        return 0