import grpc
import base64

import functions_pb2
import functions_pb2_grpc

import concurrent.futures
import numpy as np

import warnings  
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=FutureWarning)
    from keras.models import load_model

def encode_file(file_name):
    with open('Models/'+file_name,'rb') as file:
        encoded_string = base64.b64encode(file.read())
    return encoded_string

#declare channels here
#channel<n> is the channel for node 'n'
channel01 = grpc.insecure_channel('localhost:8081')
channel02 = grpc.insecure_channel('localhost:8082')
channel03 = grpc.insecure_channel('localhost:8083')
channel04 = grpc.insecure_channel('localhost:8084')
channel05 = grpc.insecure_channel('localhost:8085')

#declare stubs here
#stub<n> is the stub for channel<n>
stub01 = functions_pb2_grpc.FederatedAppStub(channel01)
stub02 = functions_pb2_grpc.FederatedAppStub(channel02)
stub03 = functions_pb2_grpc.FederatedAppStub(channel03)
stub04 = functions_pb2_grpc.FederatedAppStub(channel04)
stub05 = functions_pb2_grpc.FederatedAppStub(channel05)

# array of all our stubs
stubs = [
    stub01,
    stub02,
    stub03,
    stub04,
    stub05
]

#number of nodes on the network
n = len(stubs)

"""Util functions"""

def genFunc(i):
    empty = functions_pb2.Empty(value = 1)
    res = stubs[i].GenerateData(empty)
    print("node0",i+1,":",res.value)

def sendFunc(i, opt):
    if (opt == 2):
        filename = "InitModel.h5"
    else :
        filename = "optimised_model.h5"
    ModelString = functions_pb2.Model(model=encode_file(filename))
    res = stubs[i].SendModel(ModelString)
    print("node0",i+1,":",res.value, " - file :", filename)

def trainFunc(i):
    empty = functions_pb2.Empty(value = 1)
    res = stubs[i].Train(empty)
    with open("Models/model_"+str(i+1)+".h5","wb") as file:
        file.write(base64.b64decode(res.model))
    print("Saved model from node0",i)

""" Option handlers here """

def generateData():

    executor = concurrent.futures.ProcessPoolExecutor(n)
    futures = [executor.submit(genFunc, i) for i in range(n)]
    concurrent.futures.wait(futures)

def sendModel(opt):

    executor = concurrent.futures.ProcessPoolExecutor(n)
    futures = [executor.submit(sendFunc, i, opt) for i in range(n)]
    concurrent.futures.wait(futures)
    

def train():

    executor = concurrent.futures.ProcessPoolExecutor(n)
    futures = [executor.submit(trainFunc, i) for i in range(n)]
    concurrent.futures.wait(futures)

def optimiseModels():
    models = [load_model("Models/model_"+str(i)+".h5") for i in range(1,6)]
    weights = [model.get_weights() for model in models]

    new_weights = list()

    for weights_list_tuple in zip(*weights):
        new_weights.append(
            [np.array(weights_).mean(axis=0)\
                for weights_ in zip(*weights_list_tuple)])

    new_model = models[0]
    new_model.set_weights(new_weights)
    new_model.save("Models/optimised_model.h5")
    print("Averaged over all models - optimised model saved!")




while True:
    print("1. Generate Data")
    print("2. Initialize model on all nodes")
    print("3. Perform training on all nodes")
    print("4. Average and optimize new model")
    print("5. Send new model to all nodes")
    print("6. Exit")
    print("Enter an option: ")
    option = input()

    if (option == "1"):
        generateData()
    if (option == "2"):
        sendModel(int(option))
    if (option == "3"):
        train()
    if (option == "4"):
        optimiseModels()
    if (option == "5"):
        sendModel(int(option))
