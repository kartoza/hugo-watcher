#!/bin/bash
docker build -t kartoza/hugo-watcher:latest .
docker tag kartoza/hugo-watcher:latest kartoza/hugo-watcher:0.86.0
docker tag kartoza/hugo-watcher:latest kartoza/hugo-watcher:main
