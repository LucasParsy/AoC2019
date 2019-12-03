#! /usr/bin/env bash
set -e

if [ $# != 2 ]; then
   echo "$0 day part"
   exit
fi

cp input.txt main.py subject.txt days/d$1/p$2
git add days/d$1/p$2
git commit -m "day $1 part $2"
rm subject.txt
if [[ $2 == 2 ]]; then
    rm input.txt
fi
touch input.txt subject.txt
