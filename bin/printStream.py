#!/usr/bin/env python

"""Consumes stream for printing all messages to the console.
"""

import os
import argparse
import sys
import time
import confluent_kafka


class EopError(Exception):
    """Exception raised when reaching end of partition.

    Parameters
    ----------
    msg : Kafka message
        The Kafka message result from consumer.poll().
    """
    def __init__(self, msg):
        try:
            message = 'topic:%s, partition:%d, status:end, ' \
                'offset:%d, key:%s, time:%.3f\n' \
                % (msg.topic(), msg.partition(),
                   msg.offset(), str(msg.key()), time.time())
        except TypeError:
            message = 'topic:%s, partition:%d, status:end, ' \
                      'offset:%d, key:%s, time:%.3f\n' \
                      % (msg.topic(), msg.partition(),
                         0, str(msg.key()), time.time())
        self.message = message


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('topic', type=str,
                        help='Name of the Kafka topic to stream.')

    args = parser.parse_args()

    conf = {'bootstrap.servers': 'kafka:9092',
            'default.topic.config': {'auto.offset.reset': 'smallest'},
            'group.id': os.environ['HOSTNAME']}

    consumer = confluent_kafka.Consumer(conf)

    consumer.subscribe([args.topic])

    while True:
        try:
            msg = consumer.poll()

            if msg.error():
                raise EopError(msg)
            else:
                print(msg.value())

        except EopError as e:
            # Write when reaching end of partition
            sys.stderr.write(e.message)


if __name__ == "__main__":
    main()
