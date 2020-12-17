#! /bin/bash

if [[ -z $1 ]] 
then
    echo "Must provide show to watch"
    exit 1
fi

url=$(python3 get_next_hunter_episode.py $1)

if [[ $? == 1 ]] 
then
    echo "Error running script: $url"
    exit 1
fi

echo $url
# open -a Safari $url
pwd

open -a Safari $url


exit 0

