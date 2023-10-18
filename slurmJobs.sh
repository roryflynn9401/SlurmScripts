#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: $0 <fileName> <iterations> <max_cores>"
    exit 1
fi

fileName="$1"
iterations="$2"
max_cores="$3"

for ((i=1; i<=$max_cores; i*=2)); do
    sbatch  --mem=32G ./runProc.sh "$fileName" "$i" "$iterations"
done 