#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")/../"

TAG=event-system-alarm-notifier:package
NAME=event-system-alarm-notifier
docker build . -f package.Dockerfile -t $TAG
docker create --name $NAME $TAG
docker cp $(docker ps -a -q -f name="$NAME" | head -1):/package/verify-event-system-alarm-notifier.zip verify-event-system-alarm-notifier.zip
docker rm $NAME
