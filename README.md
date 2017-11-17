daloy
============

[![Docker Automated buil](https://img.shields.io/docker/automated/mtpatter/daloy.svg)](https://hub.docker.com/r/mtpatter/daloy/)

Mock stream producer for time series data using Kafka, converting a csv file into a real-time stream useful for testing streaming analytics.
Example of the data format needed included in the data directory.

This uses [Confluent's Kafka client for Python](https://github.com/confluentinc/confluent-kafka-python), which wraps the librdkafka C library.
The librdkafka C library is installed into the Docker container built with the accompanying Dockerfile.

Requires Docker and Docker Compose for the usage instructions below.

Usage
-------------------

Clone repo, cd into directory, and checkout appropriate branch.

**Bring up Kafka broker and Zookeeper**

From the daloy directory:

```
$ docker-compose up -d
```

This will create a network named `daloy_default` with the default driver over which the other containers will connect.

**Build docker container**

From the daloy directory:

```
$ docker build -t "daloy" .
```

This should now work:

```
$ docker run -it daloy python bin/sendStream.py -h
```

**Start producing a time series stream**

Send time series from data/data.csv to topic “my-stream” with 10 seconds in time series equaling 1 second in real time:

```
$ docker run -it \
      --network=daloy_default \
      daloy python bin/sendStream.py data/data.csv my-stream 10
```

**Consume time series stream**

To start a consumer for printing all messages in real-time from the stream "my-stream":

```
$ docker run -it \
      --network=daloy_default \
      daloy python bin/printStream.py my-stream
```

**Mounting a data volume**

Docker will see a local directory with data by mounting the current path to the container:

```
$ docker run -it \
      --network=daloy_default \
      -v $PWD:/home/daloy:rw \
      daloy python bin/sendStream.py localfile.csv my-stream 1
```

**Shut down and clean up**

Shutdown Kafka broker system:

```
$ docker-compose down
```

Find daloy container names with `docker ps` and shut down with `docker kill [id]`.
