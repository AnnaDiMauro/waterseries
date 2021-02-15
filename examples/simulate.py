from wateranalysis.learning import cluster, randomforest
# from wateranalysis.vis import clusterview
from wateranalysis.simulation.generator import ProfileGenerator
import numpy as np
import os
import logging
import argparse
from  wateranalysis.models.spline import TSSPline
import glob
from matplotlib import pyplot as plt


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='complete example')
    parser.add_argument('fixture', metavar='FIXTURE', type=str, default="Washbasin",
                        help='the basename of csv timeseries to be analyzed')
    parser.add_argument('--nospline', dest='nospline', action='store_true', default=False,
                        help='skip the spline stage')

    args = parser.parse_args()
    fixture = args.fixture

    data_dir = 'data/csv_'+fixture


    '''
    Simulation of userscd /hspl 
    '''
    if not os.path.isdir(data_dir + "/simulation"):
        os.mkdir(data_dir + "/simulation")
    mg = ProfileGenerator(data_dir, data_dir + "/simulation")
    # GLOBAL
    mg.global_model(fixture, 10)
    mg.monthly_model(fixture, 8, 10)


    simulation_file = data_dir + '/simulation/utilizzi_monthly_8_' + fixture + '.csv'
    runs = np.genfromtxt(simulation_file, delimiter=" ")
    predict = open(data_dir + '/' + fixture+".predict", "w")


    for i in range(1, len(runs)):
        predict.write("Nan," + str(int(runs[i][3])) + ",0,10\n")
    predict.close()

    clusters = randomforest.RandomForest.predict(data_dir+"/model.pkl", data_dir + '/' +fixture+".predict")
    print(clusters)

    userid = None

    for i in range(1, len(runs)):
        cluster_ts = np.genfromtxt(data_dir + "/" + str(int(clusters[i-1])) + "_spline.csv", delimiter=",")
        start_time = runs[i][-2] * 3600 + runs[i][-1] * 60
        cluster_ts[:, 0] += start_time
        if userid is None:
            userid = runs[i][0]
            ts = cluster_ts
        elif userid != runs[i][0]:
            np.savetxt(data_dir +"/simulation/user_" + str(int(userid)) +"_predicted.csv", ts, fmt="%i,%f")
            userid = runs[i][0]
            ts = cluster_ts
        else:
            ts = np.vstack((ts, cluster_ts))
    np.savetxt(data_dir + "/simulation/user_" + str(int(userid)) + "_predicted.csv", ts, fmt="%i,%f")


users_files = glob.glob(data_dir + "/simulation/user_*predicted.csv")
for user_file in users_files:
    plt.figure()
    ts =  np.genfromtxt(user_file, delimiter=",")
    plt.plot(ts[:, 0], ts[:, 1], '-')
    plt.savefig(user_file + ".png")








