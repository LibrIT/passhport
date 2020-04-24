#!/bin/bash

file=$1

sed -i "s/bower_components/static\/bower_components/g" $1
sed -i 's:"plugins/:"static/plugins/:g' $1
sed -i 's:"dist/:"static/dist/:g' $1
