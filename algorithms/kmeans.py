import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial.distance import cdist

import logging
logging.basicConfig(level=logging.INFO)


class KMeans:
    def __init__(self, data, max_iter=100):
        self.data = data
        self.max_iter = max_iter
        self.k = None
        self.centroids = None

    def elbow(self):
        # Fit k-means for k range [0,10]
        distortions = []
        K = range(1,10)
        for k in K:
            logging.info(f'Fitting model for k = {k}')
            # Initialise the centroids
            self.initialize(k=k)
            # Fit the centroids to k clusters
            self.fit()
            d = sum(np.min(cdist(self.data, self.centroids,
                          'euclidean'),axis=1)) / self.data.shape[0]
            distortions.append(d)

        # Plot Elbow
        plt.plot(K, distortions, 'bx-')
        plt.xlabel('Values of K')
        plt.ylabel('Distortion')
        plt.title('The Elbow Method using Distortion')
        plt.show()


    def initialize(self, k):
        # Set the random k centroids
        self.k = k
        idx = np.random.randint(self.data.shape[0], size=k)
        self.centroids = self.data[idx,:]


    def fit(self):
        P, C = self.data.shape[0], self.centroids.shape[0]
        for i in range(self.max_iter):
            # Assign each x in data to the nearest cluster
            distances = np.zeros((P, C), dtype=np.float32)
            for p in range(P):
                for c in range(C):
                    distances[p, c] = np.sum(np.square(self.centroids[c] - self.data[p]))
            assigned = np.argmin(distances, axis=1)
            # Find the new cluster center
            for i in range(self.k):
                cluster_points = self.data[assigned==i,:]
                self.centroids[i,:] = np.mean(cluster_points, axis=0)


    def plot(self):
        plt.plot()
        plt.xlim([-6, 6])
        plt.ylim([-6, 6])
        plt.title(f'K-Means for k = {self.k}')
        plt.xlabel('X1')
        plt.ylabel('X2')
        plt.scatter(self.data[:,0], self.data[:,1], color='blue')
        plt.scatter(self.centroids[:,0], self.centroids[:,1], color='red')
        plt.legend(['Dataset', 'Cluster Centers'])
        plt.show()


class DataGeneration:
    def ambers_random_data(self):
        np.random.seed(1)
        x = 2
        data1 = np.random.normal(size=(100, 2)) + [ x, x]
        data2 = np.random.normal(size=(100, 2)) + [ x,-x]
        data3 = np.random.normal(size=(100, 2)) + [-x,-x]
        data4 = np.random.normal(size=(100, 2)) + [-x, x]
        data  = np.concatenate((data1, data2, data3, data4))
        np.random.shuffle(data)
        return data


if __name__ == "__main__":
    generator = DataGeneration()
    k_means = KMeans(generator.ambers_random_data())
    k_means.elbow()
    k = input("Choose number of clusters: ")
    k_means.initialize(int(k))
    k_means.fit()
    k_means.plot()
