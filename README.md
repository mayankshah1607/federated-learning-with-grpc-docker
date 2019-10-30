# Federated Learning with gRPC and Docker
A simple application that uses docker and gRPC to demonstrate fedrated learning

## What is Federated Learning?
<img src="https://1.bp.blogspot.com/-K65Ed68KGXk/WOa9jaRWC6I/AAAAAAAABsM/gglycD_anuQSp-i67fxER1FOlVTulvV2gCLcB/s640/FederatedLearning_FinalFiles_Flow%2BChart1.png"/>

Standard machine learning approaches require centralizing the training data on one machine or in a datacenter. And Google has built one of the most secure and robust cloud infrastructures for processing this data to make our services better. Now for models trained from user interaction with mobile devices, Google is introducing an additional approach: Federated Learning.

Federated Learning enables mobile phones to collaboratively learn a shared prediction model while keeping all the training data on device, decoupling the ability to do machine learning from the need to store the data in the cloud. This goes beyond the use of local models that make predictions on mobile devices (like the Mobile Vision API and On-Device Smart Reply) by bringing model training to the device as well.

[source](https://ai.googleblog.com/2017/04/federated-learning-collaborative.html)

## What's in this repo?
This repo consist of a simple python application that makes use of gRPC and Docker to demonstrate how Federated Learning (kinda) works.

Here's a visualization of the architecture of our application

<img width="400px" src="https://github.com/mayankshah1607/federated-learning-with-grpc-docker/blob/master/static/architecture.jpg">

## Setup
Make sure you have python3, docker and docker-compose setup on your machine.

## Getting started

Start the nodes by running the following commands

```bash
$ cd /node
$ docker-compose up --build
```
You should now have a terminal with the logs from all the nodes in this distributed system.

Open another terminal and run the following commands
```bash
$ cd /interface
$ python3 client.py
```
You should now have a terminal with an interactive menu to play aroud with!
