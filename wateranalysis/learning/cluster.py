import matplotlib.pylab as plt
import os
from sklearn import mixture
from sklearn.cluster import MeanShift, estimate_bandwidth
import numpy as np
from sklearn import cluster
# from learning import LoadModels as lm
import joblib
import shutil
import glob
import pandas as pd


class TSCluster:

    def __init__(self, folder, filename, runs):
        """

        :param folder:
        :param filename:
        :param runs:
        """
        self.data_dir = folder
        self.n_series = runs
        self.filename = filename

    def meanshift(self, testset):
        # #############################################################################
        # Compute clustering with MeanShift

        # The following bandwidth can be automatically detected using
        bandwidth = estimate_bandwidth(testset, quantile=0.8, n_samples=len(testset))

        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        ms.fit(testset)
        labels = ms.labels_
        cluster_centers = ms.cluster_centers_

        labels_unique = np.unique(labels)
        n_clusters_ = len(labels_unique)
        print("number of estimated clusters : %d" % n_clusters_)

    def find_k1(self, testset):
        lowest_bic = np.infty
        bic = []
        n_components_range = range(1, 4)

        for n_components in n_components_range:
            # Fit a Gaussian mixture with EM
            # gmm = mixture.GMM(n_components=n_components)
            gmm = mixture.GaussianMixture(n_components=n_components)
            gmm.fit(testset)
            bic.append(gmm.bic(testset))
            if bic[-1] < lowest_bic:
                lowest_bic = bic[-1]
                best_gmm = gmm
                best_n = n_components
        return best_n

    def compute_statistics(testset):
        pass

    def get_testset(self):
        individuals = np.genfromtxt(self.data_dir + '/' + self.filename + ".individuals", delimiter=' ')
        individuals = np.delete(individuals, 0, 0)
        testset = individuals[:, 2:]

        # Normalization
        maxduration = np.max(testset[:, 0])
        testset[:, 0] = testset[:, 0] / maxduration

        max_liters = np.max(testset[:, 1])
        testset[:, 1] = testset[:, 1] / max_liters
        maxpower = np.max(testset[:, 2])
        testset[:, 2] = testset[:, 2] / maxpower
        return testset

    def predict(self, file_model,testset):
        model = joblib.load(file_model)
        return model.predict(testset)

    @staticmethod
    def plot_clusters(testset, clusters, axis=[0, 1]):
        plt.scatter(testset[:, axis[0]], testset[:, axis[1]], c=clusters)
        return plt

    def extract_features(self, parameters=[]):
        features = pd.read_csv(self.data_dir + '/' + self.filename + '_usage.csv', sep=' ', header=None,
                               names=['start', 'duration', 'liters', 'month', 'hour', 'day', 'max_flow'])
        features = features[parameters]
        features.to_csv(self.data_dir + '/' + self.filename + '.individuals', header=None, sep=' ', index=True)

    def compute_clusters(self, testset):
        # remove cluster folders if they exit

        cluster_dirs = glob.glob(self.data_dir + '/cluster_*')
        for cluster_dir in cluster_dirs:
            if os.path.isdir(cluster_dir):
                shutil.rmtree(cluster_dir)

        # optimal number of clusters
        k1 = self.find_k1(testset)

        # compute clusters with KMeans
        ml_obj = cluster.KMeans(n_clusters=k1)
        clusters = ml_obj.fit_predict(testset)
        return k1, clusters

    def mk_cluster_folders(self, k1, clusters, n_ts=-1):
        individuals = np.genfromtxt(self.data_dir + '/' + self.filename + ".individuals", delimiter=' ')
        if n_ts == -1:
            n_ts = self.n_series
        selections = []

        for i in range(0,k1):
            os.mkdir(self.data_dir+"/cluster_"+str(i))
            selections.append(n_ts)

        for i in range(0, len(clusters)):
            if selections[clusters[i]] > 0:
                selections[clusters[i]] -= 1
                shutil.copyfile(self.data_dir+"/splits/"+str(int(individuals[i][0]))+".csv",
                                self.data_dir+"/cluster_" + str(clusters[i])+"/"+str(i)+".csv")
            if np.sum(selections) == 0:
                break



