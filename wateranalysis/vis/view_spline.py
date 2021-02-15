from matplotlib import pyplot as plt
import numpy as np
import glob
import os



for i in range(3):
    csv_files = glob.glob("data/spline/C"+str(i)+"*.csv")
    plt.figure()
    for csv_file in csv_files:
        ts = np.genfromtxt(csv_file, delimiter=";")
        plt.plot(ts[:, 0], ts[:, 1], '.', label=os.path.basename(csv_file))
    ts = np.genfromtxt("data/spline/B-splineC" + str(i) + ".csv", delimiter=";")
    plt.plot(ts[:, 0], ts[:, 1], '-', label="spline")
    plt.legend(loc="upper right")
    plt.savefig("data/spline/B-splineC" + str(i) + ".png")

