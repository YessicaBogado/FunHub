#!/bin/sh
local_directory=$(pwd)
mid1=mid1
mid2=mid2
snafu=snafu_dev
function_hub=functionhub
cd $local_directory/marketplace/deployment/
sh build.sh
cd $local_directory/Middleware_1
docker build --rm -t $mid1 .
cd $local_directory/Middleware_2
docker build --rm -t $mid2 .
cd $local_directory
git clone https://github.com/YessicaBogado/snafu
cd $local_directory/snafu
docker build --rm -t $snafu .
