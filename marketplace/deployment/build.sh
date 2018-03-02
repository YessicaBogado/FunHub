#!/bin/sh

rm -rf _build
mkdir -p _build
cp -r ../index.html ../app Dockerfile _build
cd _build
docker build -t functionhub .
