from __future__ import absolute_import, division, print_function, unicode_literals
from metaflow import FlowSpec, step, batch, retry,catch
import tensorflow as tf
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping
import s3fs
from keras.callbacks import ModelCheckpoint
from tensorflow import keras
import numpy as np
import os
import re
from pathlib import Path
import logging
import joblib
import pandas as pd
import tensorflow_hub as hub
import tensorflow_datasets as tfds
import logging
import multiprocessing as mp
import os
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD, Adam, Adadelta, Adagrad
from metaflow import FlowSpec, Parameter, step
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import boto3




#Authenticate the AWS Credentials
s3_client = boto3.client('s3') 
s3_resource = boto3.resource('s3')
s3_fs = s3fs.core.S3FileSystem(anon=False)

input_bucket = "" #Enter Bucket name where output.csv is saved from Part 1
key = 'output.csv'
output_bucket  = "" #output bucket to save the labeled data. 



class LinearFlow(FlowSpec):
    
    @step
    def start(self):
        self.s3_cl = boto3.client('s3')
        self.obj = self.s3_cl.get_object(Bucket=input_bucket, Key=key)
        self.df = pd.read_csv(self.obj['Body'])
        self.X = self.df.iloc[:,0]
        self.y = self.df.iloc[:,1]
        for i in range(len(self.y)):
            if self.y[i]<=0.0:
                self.y[i] = 0
            else:
                self.y[i] = 1  
        self.next(self.a)
 
    @step
    def a(self):
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.y, test_size=0.10, random_state=1)
        self.X_train, self.X_val, self.Y_train, self.Y_val = train_test_split(self.X_train, self.Y_train, test_size=0.10, random_state=1)
        self.X_train = np.asarray(self.X_train)
        self.Y_train = np.asarray(self.Y_train)
        self.X_val = np.asarray(self.X_val)
        self.Y_val = np.asarray(self.Y_val)
        self.X_test = np.asarray(self.X_test)
        self.Y_test = np.asarray(self.Y_test)
        self.next(self.end)
        

    @catch(print_exception=False)
    @step
    def end(self):
        self.embedding = "https://tfhub.dev/google/tf2-preview/nnlm-en-dim50/1"
        self.hub_layer = hub.KerasLayer(self.embedding, input_shape=[], dtype=tf.string, trainable=True)
        self.hub_layer(self.X_train)
        self.model = tf.keras.Sequential()
        self.model.add(self.hub_layer)
        self.model.add(tf.keras.layers.Dense(20, activation='relu'))
        self.model.add(tf.keras.layers.Dense(8, activation='relu'))
        self.model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
        self.model.summary()
        self.es = EarlyStopping(monitor='val_loss', mode='min', verbose=1)
        self.mc = ModelCheckpoint('best_model.h5', monitor='val_accuracy', mode='max', verbose=1, save_best_only=True)
        self.opt = 'adamax'
        self.model.compile(optimizer=self.opt,loss=tf.keras.losses.binary_crossentropy,metrics=['accuracy'])
        self.history = self.model.fit(self.X_train, self.Y_train,epochs=20,validation_data= (self.X_val, self.Y_val),shuffle = True,batch_size = 10,callbacks=[self.es, self.mc],verbose=1)
        model = model.save(s3_fs.put('model.h5',output_bucket))
        print("Saved model to bucket")





if __name__ == '__main__':
    LinearFlow()