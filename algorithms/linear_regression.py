import random
import math
import pandas as pd
import numpy as np

from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

import logging
logging.basicConfig(level=logging.INFO)


class Dataloader:
    def __init__(self, path):
        """ A dataloader class for handling dataset attributes and functions

        Args:
            path (str): path to the dataset csv file

        Attributes:
            data (pd.DataFrame): pandas dataframe containing the entire dataset
            length (int): number of records in dataset
            feature (pd.DataFrame): features dataframe
            label (pd.DataFrame): label dataframe
            num_features (int): number of features in the dataset
        """
        self.data = pd.read_csv(path)
        self.length = len(self.data)
        self.drop_address()
        self.feature, self.label = self.get_feature_label()
        self.normalize()
        self.bias()
        self.num_features = len(self.feature.iloc[0])
        # logging.info(f'Number of features {self.num_features}')

    def train_val_split(self, pval=0.3):
        """Split dataset into trainign and validation

        Args:
            pval (float): ratio of validation / training split

        Returns:
            train, val (dict, dict): training and validation datasets
        """
        slice = math.floor(self.length*pval)
        ind = [i for i in range(self.length)]
        random.shuffle(ind)
        val = {'feature':self.feature.iloc[ind[:slice]], 'label':self.label.iloc[ind[:slice]]}
        train = {'feature':self.feature.iloc[ind[slice:]], 'label':self.label.iloc[ind[slice:]]}
        return train, val

    def drop_address(self):
        self.data.drop(columns=['Address'], inplace=True)

    def get_feature_label(self):
        # feature = self.data['Avg. Area Number of Rooms'].values
        # feature = self.data[['Avg. Area Number of Rooms', 'Avg. Area Income']].values
        feature = self.data.loc[:, self.data.columns != 'Price']
        label = self.data['Price']
        return feature, label

    def normalize(self):
        self.feature = (self.feature-self.feature.min())/(self.feature.max()-self.feature.min())

    def bias(self):
        bias = [1] * self.length
        self.feature['bias'] = bias
        self.label['bias'] = bias


class LinearRegression:
    def __init__(self, path='./data/USA_Housing.csv'):
        """A Linear Regression parent class

        Args:
            path (str): path to the dataset csv file

        Attributes:
            dataloader (obj): a Dataloader object
            train (dict): training dataset with 'feature' and 'label' keys
            val (dict): validation dataset with 'feature' and 'label' keys
        """
        self.dataloader = Dataloader(path)
        self.train, self.val = self.dataloader.train_val_split()
        self.coef = np.zeros(self.dataloader.num_features)

    def get_R2(self):
        y_pred = self.predict(self.val['feature'].values)
        return r2_score(self.val['label'].values,y_pred)

class ManualLR(LinearRegression):
    """A manual linear regression class using numpy

    Attributes:
        coef (numpy.array): a matrix of coefficients for the linear equation
    """
    def __init__(self):
        LinearRegression.__init__(self)
        self.coef = np.zeros(self.dataloader.num_features)

    def fit(self):
        x_train, y_train = self.train['feature'].values, self.train['label'].values
        # Closed form solution
        self.coef = np.linalg.pinv(x_train.T @ x_train) @ x_train.T @ y_train
        # logging.info(f'Learnt coefficients {self.coef}')

    def predict(self, data):
        # predict using coefficients
        return np.dot(data, self.coef)

    def get_rmse(self):
        # Inference validation set
        y_pred = self.predict(self.val['feature'].values)
        y = self.val['label'].values
        # Calculate RMSE
        return np.sqrt((np.sum((y_pred - y)**2)/len(y)))


class SKLearnLR(LinearRegression):
    def __init__(self):
        """A linear regression class using sklearn libraries

        Attributes:
            model (object): a sklearn linear regression model object
        """
        LinearRegression.__init__(self)
        self.model = None

    def fit(self):
        x_train, y_train = self.train['feature'].values, self.train['label'].values
        self.model = linear_model.LinearRegression()
        self.model.fit(x_train, y_train)
        # logging.info(f'Learnt coefficients {self.model.coef_}')

    def predict(self, data):
        return self.model.predict(data)

    def get_rmse(self):
        y_pred = self.predict(self.val['feature'].values)
        y = self.val['label'].values
        return np.sqrt(mean_squared_error(y, y_pred)*len(y))


if __name__ == '__main__':
    # Perform LR manually using closed-form solution
    lr1 = ManualLR()
    lr1.fit()
    logging.info(f'Manual LR: \tRMSE: {lr1.get_rmse()}\t R2: {lr1.get_R2()}')
    del lr1

    # Perform LR using the pre-built sklearn library
    lr2 = SKLearnLR()
    lr2.fit()
    logging.info(f'SKLearn LR: \tRMSE: {lr2.get_rmse()}\t R2: {lr2.get_R2()}')
    del lr2
