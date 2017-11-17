#!/usr/bin/env python

"""Generates a stream to Kafka from a time series csv file.
"""

import argparse
import csv
import sys
import time
import confluent_kafka
from dateutil.parser import parse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filename', type=str,
                        help='Time series csv file.')
    parser.add_argument('topic', type=str,
                        help='Name of the Kafka topic to stream.')
    parser.add_argument('timeconvert', type=int,
                        help='Number of seconds one second in real time '
                        'corresponds to in the data. '
                        '(Speeds up time series over long periods.)')

    args = parser.parse_args()

    conf = {'bootstrap.servers': 'kafka:9092'}
    topic = args.topic

    producer = confluent_kafka.Producer(conf)

    rdr = csv.reader(open(args.filename))
    next(rdr)  # Skip header
    firstline = True

    while True:

        try:

            if firstline is True:
                line1 = next(rdr, None)
                timestamp, value = line1[0], float(line1[1])
                result = timestamp, value
                firstline = False

                print(result)
                producer.produce(topic, str(result))

            else:
                line = next(rdr, None)
                d1 = parse(timestamp)
                d2 = parse(line[0])
                diff = ((d2 - d1).total_seconds())/args.timeconvert
                time.sleep(diff)
                timestamp, value = line[0], float(line[1])
                result = timestamp, value

                print(result)
                producer.produce(topic, str(result))

            producer.flush()

        except TypeError:
            sys.exit()


if __name__ == "__main__":
    main()
