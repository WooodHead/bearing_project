#!/usr/bin/env bash

docker run \
    --name prometheus \
    -d \
    -p 127.0.0.1:9090:9090 \
    quay.io/prometheus/prometheus
