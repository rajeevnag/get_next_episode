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

echo "the url is: $url"

open -a Safari $url

echo "Script completed"

exit 0

