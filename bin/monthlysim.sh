#!/bin/sh
export PYTHONPATH=src
#timeseries="AMPDScut"
# timeseries="AMPDS1Y"
timeseries="Washbasin"
for k in `seq 1 30`
do
  for i in `seq 1 30`
  do
     python3 src/examples/simulate.py --smodel monthly --month 6 --users 1 $timeseries
     dest_file="data/csv_"$timeseries"/simulation/user_"$i"_predicted.csv"
     echo $dest_file
     if test -f "data/csv_"$timeseries"simulation/user_0_predicted.csv"; then
        mv  data/csv_$timeseries/simulation/user_0_predicted.csv $dest_file
     fi
  done
  dest_dir="data/csv_"$timeseries"/simulation"$k
mv data/csv_$timeseries/simulation data/csv_$timeseries/simulation$k
done


