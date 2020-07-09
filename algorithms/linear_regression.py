# https://machinelearningmastery.com/implement-simple-linear-regression-scratch-python/

import csv
import random
import math
import operator
import pandas as pd
import numpy as np

from numpy.linalg import inv

from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt

import logging
logging.basicConfig(level=logging.INFO)


class Dataloader:
    def __init__(self, path):
        self.data = pd.read_csv(path)
        self.length = len(self.data)
        self.drop_address()
        self.normalize()
        self.feature, self.label = self.get_feature_label()
        self.bias()
        try:
            self.num_features = self.feature.shape[1]
        except IndexError:
            self.num_features = 1
        logging.info(f'Number of features {self.num_features}')

    def train_val_split(self):
        X_train, X_test, y_train, y_test = train_test_split(self.feature, self.label, test_size=0.33, random_state=42)
        return np.column_stack((X_train, y_train)), np.column_stack((X_test, y_test))

    def drop_address(self):
        self.data.drop(['Address'], axis=1,  inplace=True)

    def get_feature_label(self):
        # feature = self.data['Avg. Area Number of Rooms'].values
        # feature = self.data[['Avg. Area Number of Rooms', 'Avg. Area Income']].values
        feature = self.data.loc[:, self.data.columns != 'Price'].values
        label = self.data['Price'].values
        return feature, label

    def normalize(self):
        self.mean = self.data.mean()
        self.std = self.data.std()
        self.data=(self.data-self.mean)/self.std

    def bias(self):
        pass


class LinearRegression:
    def __init__(self, path='./USA_Housing.csv'):
        self.dataloader = Dataloader(path)
        self.train, self.val = self.dataloader.train_val_split()
        self.b = None

    def fit(self):
        X, y = self.train[:,:-1], self.train[:,1]
        X = X.reshape((len(X), self.dataloader.num_features))   # Incase of 1D feature array
        # linear least squares
        self.b = inv(X.T.dot(X)).dot(X.T).dot(y)
        logging.info(f'Learnt coefficients {self.b}')


    def predict(self, X):
        # predict using coefficients
        return X.dot(self.b)

    def get_mse(self):
        # Inference validation set
        X, y = self.val[:,:-1], self.val[:,1]
        X = X.reshape((len(X), self.dataloader.num_features))
        y_hat = self.predict(X)
        # Calculate MSE
        return np.mean(np.square(y_hat - y))


if __name__ == '__main__':
    lr = LinearRegression()
    lr.fit()
    print('MSE:', lr.get_mse())
