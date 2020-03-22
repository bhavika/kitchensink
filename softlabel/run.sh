#!/usr/bin/env bash

cat data/map.geojson | supermercado burn 20 | sed -E 's/^.|.$//g' | xargs >> data/tiles.csv

cat data/tiles.csv | xargs -n3 curl https://api.mapbox.com/v4/mapbox.satellite/${1}/${2}/${3}@2x.jpg90\?access_token\=$MAPBOX_ACCESS_TOKEN curl-command
