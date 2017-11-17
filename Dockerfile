# Version: 0.0.1
FROM python:3.6
LABEL maintainer "maria.t.patterson@gmail.com"
ENV REFRESHED_AT 2017-11-17

# Install library for confluent-kafka python.
WORKDIR /home
RUN git clone https://github.com/edenhill/librdkafka.git && cd librdkafka && git checkout tags/v0.9.4
WORKDIR /home/librdkafka
RUN ./configure && make && make install
ENV LD_LIBRARY_PATH /usr/local/lib

# Add code.
WORKDIR /home
RUN mkdir daloy
ADD . /home/daloy
WORKDIR /home/daloy
RUN pip install -r requirements.txt

