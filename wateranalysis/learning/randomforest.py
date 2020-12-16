import numpy as np
from argparse import ArgumentParser
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn import metrics
from datetime import datetime
import logging

class RandomForest:

    def __init__(self, folder, fixture, n_clusters):
        self.folder = folder
        self.filename = folder + '/' + fixture
        self.fixture = fixture
        self.n_cluster = n_clusters

    def compute_features(self, clusters):
        # compute the delay since the last occurence of the same program
        # datetime, duration, liters, maxflow
        individuals = np.genfromtxt(self.filename+".individuals", delimiter=" ")
        delay = 0
        j = 2
        while clusters[-j] != clusters[-1] and len(clusters) - j > 0:
            delay += 1
            j += 1

        sequence_f = open(self.filename + ".sequence", "w")
        i = 0
        for j in range(len(individuals)-1):
            ind = individuals[j]
            start_time = ind[1]
            dt = datetime.fromtimestamp(start_time)
            day_week = dt.strftime("%w")
            day_month = dt.strftime("%d")
            hour = dt.strftime("%H")

            sequence_f.write(str(start_time) + "," + str(hour) + "," + str(day_week) + "," + str(day_month) + "," +
                             # str(ind[2]) + ',' + str(ind[3]) + ',' + str(ind[4]) + ',' +
                             str(clusters[i]) + "\n")
            i += 1
        sequence_f.close()

    def evaluate(self):
        dataset = np.genfromtxt(self.filename + ".sequence", delimiter=",")
        splitn = int(len(dataset) * 0.66)

        Y = []
        for i in range(0, len(dataset)):
            Y.append(chr(ord('a') + int(dataset[i, 4])))

        Y = dataset[:, 4]

        clf = RandomForestClassifier(n_estimators=10)
        clf = clf.fit(dataset[:splitn, 1:-1], Y[:splitn])

        labels = list(set(Y))
        labels.sort()

        pred = clf.predict(dataset[splitn:, 1:-1])
        pred = list(pred)

        temp1 = []
        temp2 = []

        logging.info(pred)
        logging.debug(Y[splitn:])
        logging.debug(labels)
        '''
        for i in range(0,len(pred)):
            temp1.append(ord(pred[i])-ord('a'))
            temp2.append(ord(Y[splitn+i]) - ord('a'))

        print(metrics.classification_report(temp2, temp1))

        print metrics.accuracy_score(temp2, temp1)
        print metrics.precision_score(temp2, temp1)
        print metrics.recall_score(temp2, temp1)
        '''
        print(metrics.accuracy_score(Y[splitn:], pred))
        # print(metrics.precision_score(np.array(Y[splitn:]), np.array(pred)))
        # print metrics.recall_score(Y[splitn:], pred)

        print(metrics.classification_report(Y[splitn:], pred))

    def learn(self, data_dir):

        dataset = np.genfromtxt(self.filename + ".sequence", delimiter=",")
        splitn = int(len(dataset) * 0.66)

        Y = []
        for i in range(0, len(dataset)):
            Y.append(chr(ord('a') + int(dataset[i, 4])))

        Y = dataset[:, 4]

        clf = RandomForestClassifier(n_estimators=10)
        temp_ds = dataset[:, 1:-1]
        clf = clf.fit(dataset[:, 1:-1], Y)
        joblib.dump(clf, data_dir+'/model.pkl')

    @staticmethod
    def predict(model_file, file_items):
        clf = joblib.load(model_file)
        dataset = np.genfromtxt(file_items, delimiter=",")
        temp_ds = dataset[:, 1:]
        result = clf.predict(temp_ds)
        return result

