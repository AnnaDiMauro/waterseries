from matplotlib import pyplot as plt
import numpy as np
import glob
import datetime as dt
import pandas as pd
import logging
logging.getLogger().setLevel("INFO")


def average_volume(filename, month, sum=True):
    df = pd.read_csv(filename, delimiter=" ", names=["time", "flow"])
    df["time"] = pd.to_datetime(df['time'], unit='s')
    df = df[df['time'].dt.month == month]
    values =np.zeros(24)
    day_count = 0
    volume = np.zeros(24)
    for i in range(1, 31):
        df_day = df[df['time'].dt.day == i]
        if len(df_day) > 0:
            day_count +=1
            for j in (range(0,24)):
                df_hour = df_day[df_day['time'].dt.hour == j]
                if len(df_hour) > 0:
                    df_values = df_hour["flow"].to_numpy()
                    values[j] = np.sum(df_values)
                    volume[j] += values[j]
        var_cum=[values[0]]
        for h in range(1,len(values)):
            var_cum.append(var_cum[-1]+values[h])

    volume = volume / day_count
    vol_cum = [volume[0]]
    for h in range(1, len(volume)):
        vol_cum.append(vol_cum[-1] + volume[h])
    return np.array(vol_cum)



def cumulative_sim_volume(sim_dir, sum=True):

    sim_ts = glob.glob(sim_dir+"/user_*.csv")
    simulated = np.zeros(24)
    for ts_file in sim_ts:
        ts_flow = np.genfromtxt(ts_file, delimiter=",")
        values = [0]
        for i in range(len(ts_flow)):
            increment = ts_flow[i,1]
            values.append(values[i-1] + increment)
            this_hour = int(ts_flow[i-1, 0]/3600)
            if this_hour < 24:
                simulated[int(ts_flow[i-1, 0]/3600)] += increment
        print(values[-1])

    cum = [simulated[0]]
    for i in range(1, len(simulated)):
        cum.append((cum[-1] + simulated[i]))

    for i in range(len(cum)):
        cum[i] /= len(sim_ts)

    return cum


def plot_var(sim_dirs):
    all_ts = None
    for sim_dir in sim_dirs:
        temp_ts = np.genfromtxt(sim_dir+"/cum_average.csv")
        if all_ts is None:
            all_ts =[temp_ts]
        else:
            all_ts = np.vstack((all_ts, temp_ts))

    average = np.average(all_ts, axis=0)
    print(average.shape)
    stderr = np.std(all_ts, axis=0)
    print(stderr.shape)
    return average, stderr, all_ts


def all_sim_average(all_dirs):

    for sim_dir in all_dirs:
        logging.info("processing  " + sim_dir)
        c = cumulative_sim_volume(sim_dir)
        np.savetxt(sim_dir + "/cum_average.csv", c)


if __name__ == "__main__":
    timeseries = "AMPDScut"
    # timeseries = "AMPDS1Y"
    # timeseries = "Shower"
    # timeseries = "Washbasin"
    month = 8
    sim_dirs = glob.glob("data/csv_"+timeseries+"/simulation*")
    all_sim_average(sim_dirs)
    av_volume = average_volume("data/feed_"+timeseries+".MYD.csv", month)
    av, std_av, all_ts = plot_var(sim_dirs)
    all_err = np.abs(all_ts - av_volume)
    std_err = np.std(all_err, axis=0)
    print(std_err)
    print(std_av)
    err = np.abs(av_volume-av)
    x_hours = np.arange(0, 24, 1)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_hours, av, alpha=0.5, color='blue', label=' simulated consumption')
    ax.plot(x_hours, av_volume, alpha=0.5, color='black', label=' measured consumption')
    ax.plot(x_hours, err, alpha=0.5, color='red', label='error')

    y1 = av - std_av
    y2 = av + std_av
    y1[y1 < 0] = 0
    z1 = err - 2 * std_av
    z1[z1 < 0] = 0

    ax.fill_between(x_hours, y1, y2, color='#888888', alpha=0.4)
    #ax.fill_between(x_hours, z1,
    #                 av + 2 * std_Av, color='#888888', alpha=0.)

    '''
    y1 = err - std_err
    y2 = err + std_err
    y1[y1 < 0] = 0
    z1 = err - 2 * std_err
    z1[z1 < 0] = 0
    # ax.fill_between(x_hours, y1, y2, color='#888888', alpha=0.4)
    # ax.fill_between(x_hours, z1,
    #                 err + 2 * std_err, color='#888888', alpha=0.2)
    '''
    ax.set_xlabel("hour")
    ax.set_ylabel("Volume [liters]")
    plt.grid()
    plt.legend()
    plt.show()

    i_max = np.argmax(err)
    i_min = np.argmin(err)

    print(timeseries + ": err_max=", np.max(err), ", ", np.max(err) / av_volume[i_max], ": err_min=", np.min(err), ",",
          np.min(err) / av_volume[i_min], " err_mean=", np.average(err))
    print(timeseries + ": var_max=", np.max(std_err), " var_min=", np.min(std_err), " var_mean=", np.average(std_err))
