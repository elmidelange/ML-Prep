import csv
import random
import math
import operator
import pandas as pd


class DataLoader:
    def __init__(self):
        self.data = self._load_data()
        self.folds = None

    def _load_data(self):
        # 0 setosa	1 versicolor 2 virginica
        data = pd.read_csv('data/iris.csv')
        data.columns = ['seplen', 'sepwid', 'petlen', 'petwid', 'label']
        features = ['seplen', 'sepwid', 'petlen', 'petwid']
        # Noramlise features between 0 and 1
        data[features] = data[features].apply(lambda x: x - x.min(), axis=0)
        data[features] = data[features].apply(lambda x: x / x.max(), axis=0)
        return data

    # Saves the indexes for the k-folds
    def split(self, k):
        self.data = self.data.sample(frac=1)   # random shuffle
        num_samples = int(len(self.data) / k)
        folds = {}
        for i in range(k):
            folds[i] = self.data.iloc[i*num_samples:(i+1)*num_samples, :].index
        self.folds = folds
        print(self.folds)

    # Returns the train and test set for the k-th fold
    def get_train_test(self, fold):
        print(f'Getting fold {fold}')
        # Get test set
        test = self.data.iloc[self.folds[fold]]
        # Get train set from remaning folds
        folds = list(self.folds.keys())
        folds.remove(fold)
        train = self.data[~self.data.index.isin(self.folds[fold])]
        print(train.head())
        return train.values, test.values


class KNN:
    def __init__(self, dataloader):
        self.dataloader = dataloader
        self.k_cross_val = 5

    # Fit the KNN model
    def fit(self, num_neighbors):
        # 5-fold cross validation
        self.dataloader.split(self.k_cross_val)
        accuracy = 0
        for k in range(self.k_cross_val):
            train, test = dataloader.get_train_test(fold=k)
            preds = []
            for test_row in test:
                preds.append(self._predict(train, test_row, num_neighbors))
            accuracy += self._accuracy(preds, test[:,-1])
        accuracy = (accuracy / self.k_cross_val) * 100
        print('Accuracy: %.3f%%' % accuracy)

    # Predict the class for a given test sample
    def _predict(self, train, test_row, num_neighbors):
        neighbors = self._get_neighbors(train, test_row, num_neighbors)
        labels = [x[-1] for x in neighbors]
        return max(set(labels), key=labels.count)

    # Return the nearest neighbors to the test data point
    def _get_neighbors(self, train, test_row, num_neighbors):
        distances = []
        for train_row in train:
            distance = self._euclidean_distance(train_row, test_row)
            distances.append((train_row, distance))
        distances.sort(key=lambda item: item[1])
        return [distances[i][0] for i in range(num_neighbors)]

    # Calculate the euclidean distance
    def _euclidean_distance(self, vec1, vec2):
        distance = 0.0
        for i in range(len(vec1) - 1):
            distance += (vec1[i] - vec2[i])**2
        return math.sqrt(distance)

    # Calcualte the accuracy
    def _accuracy(self, prediction, actual):
        correct = 0
        for y1, y2 in zip(prediction, actual):
            correct += int(y1 == y2)
        return correct / len(prediction)


if __name__ == "__main__":
    dataloader = DataLoader()
    knn = KNN(dataloader)
    # for n in [1,2,5,10,20,50,100]:
    n = 2
    knn.fit(num_neighbors=n)
