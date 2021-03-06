#!/usr/bin/env bash

# Create Docker Network
NET_NAME="efk_net"

docker network ls | grep -wq "${NET_NAME}" && echo "The network: ${NET_NAME} already exists" ||
  docker network create "${NET_NAME}" && echo "The network: ${NET_NAME} has been created"

mkdir -p etc log plugins

docker run \
  -h fluentd \
  --name fluentd \
  --net "${NET_NAME}" \
  -u fluent \
  --restart always \
  --cpus ".25" \
  --memory "500m" \
  --memory-swap "500m" \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  -v "${PWD}"/etc:/fluentd/etc \
  -v "${PWD}"/log:/fluentd/log \
  -v "${PWD}"/plugins:/fluentd/plugins \
  -v "${PWD}"/../../logs:/logs \
  -v /var/lib/docker/containers/:/containers \
  -p 24224:24224 \
  -p 24224:24224/udp \
  -p 9880:9880 \
  -p 5160:5160 \
  -p 5160:5160/udp \
  -d \
  fluentd:plugin_es
