from wateranalysis.learning import cluster, randomforest
# from wateranalysis.vis import clusterview
from wateranalysis.simulation.generator import ProfileGenerator
import numpy as np
import os
import logging
import argparse
from  wateranalysis.models.spline import TSSPline

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




