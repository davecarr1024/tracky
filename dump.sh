#!/usr/bin/env bash

for file in $(find tracky -name *.py)
do 
    echo 
    echo \# $file
    cat $file
    echo
done
