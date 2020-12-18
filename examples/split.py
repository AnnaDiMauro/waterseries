from wateranalysis.timeseries.splitters import SimpleSplitter
import os
import logging
import argparse

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    parser = argparse.ArgumentParser(description='complete example')
    parser.add_argument('fixture', metavar='FIXTURE', type=str, default="Washbasin",
                        help='the basename of csv timeseries to be analyzed')
    args = parser.parse_args()
    fixture = args.fixture
    if not os.path.isdir('data/csv_'+fixture+'/splits'):
        os.makedirs('data/csv_'+fixture+'/splits')

    # This section detects usages and splits the original timeseries
    splitter = SimpleSplitter('data/feed_'+fixture+'.MYD.csv', 'data/csv_'+fixture+'/splits')
    splitter.split()
