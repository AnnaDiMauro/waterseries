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
    if not os.path.isdir('data/splits/csv_'+fixture):
        os.mkdir('data/splits/csv_'+fixture)

    # This section detects usages and splits the original timeseries
    splitter = SimpleSplitter('data/feed_'+fixture+'.MYD.csv', 'data/splits/csv_'+fixture)
    splitter.split()
