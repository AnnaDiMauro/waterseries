import numpy as np
import glob
import os
import logging


class TSFilter:

    @staticmethod
    def liters(ts):
        total_lits = 0
        for i in range(1, len(ts)):
            total_lits += ts[i, 1] * (ts[i, 0]-ts[i-1, 0])
        return total_lits

    @staticmethod
    def outlayers(ts_dir, min_dur_const=0, min_lit_const=0, min_samp_const=1, sep=' '):
        ts_files = glob.glob(ts_dir + '/*.csv')
        parameters = {}
        durations = []
        all_liters = []
        parameters["i_min_duration"] = []
        parameters["i_min_liters"] = []
        parameters["i_min_samples"] = []
        for i in range(len(ts_files)):
            ts_file = ts_files[i]
            ts = np.genfromtxt(ts_file, delimiter=sep)
            duration = ts[-1, 0] - ts[0, 0]
            lits = TSFilter.liters(ts)
            durations.append(duration)
            all_liters.append(lits)
            fname = int(os.path.basename(ts_file)[:-4])
            if duration < min_dur_const:
                parameters["i_min_duration"].append(fname)
            if lits < min_lit_const:
                parameters["i_min_liters"].append(fname)
            if len(ts) <= min_samp_const:
                parameters["i_min_samples"].append(fname)

        parameters["min_duration"] = np.min(durations)
        parameters["min_liters"] = np.min(all_liters)

        return parameters

    @staticmethod
    def check_fixtures(filename):
        # filename includes start datetime, duration, liters, month, hour, day
        usages = np.genfromtxt(filename, delimiter=" ")
        parameters = {}
        parameters["min_duration"] = np.min(usages[:, 2])
        parameters["i_min_duration"] = np.where(usages[:, 2] == parameters["min_duration"])
        parameters["max_duration"] = np.max(usages[:, 2])
        parameters["i_max_duration"] = np.where(usages[:, 2] == parameters["max_duration"])
        parameters["min_liters"] = np.min(usages[:, 3])
        parameters["i_min_liters"] = np.where(usages[:, 3] == parameters["min_liters"])
        parameters["max_liters"] = np.max(usages[:, 3])
        parameters["i_max_liters"] = np.where(usages[:, 3] == parameters["max_liters"])

        return

    '''
    @staticmethod
    def rename_usages(ts_dir):
        ts_files = glob.glob(ts_dir + "/*.csv")
        name_sequence = []
        for ts_file in ts_files:
            name_sequence.append(int(os.path.basename(ts_file)[:-4]))
        sorted_sequence = np.sort(name_sequence)
        for i in range(len(name_sequence)):
            if i != sorted_sequence[i]:
                os.rename(ts_dir + "/" + str(sorted_sequence[i])+".csv", ts_dir + "/" + str(i)+".csv")

    '''


    @staticmethod
    def remove_outlayers(ts_dir,  outlayers):

        logging.debug("deleting " + str(len(outlayers["i_min_samples"])) + "files")
        for i in outlayers["i_min_samples"]:
            os.remove(ts_dir + "/" + str(i) + ".csv")


if __name__ == "__main__":
    # checks =TSChecks.check_fixtures("data/washbasin_usage.csv")
    # print(checks)
    checks = TSFilter.outlayers("data/splits/csv_washbasin", 10, 250, 5)
    print(checks)
    print(len(checks["i_min_duration"]))
    print(len(checks["i_min_liters"]))
    print(len(checks["i_min_samples"]))
