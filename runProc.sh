#!/bin/bash

# Check if the parameter was provided
if [ $# -lt 3 ]; then
    echo "Usage: $0 <fileName> <cpu_cores> <iterations>"
    exit 1
fi

fileName="$1"
cpu_cores="$2"
iterations="$3"


#SBATCH --cpus-per-task=$"cpu_cores"         # Request CPU cores
#SBATCH --time=00:10:00 

# Define the C source file and the output binary name
source_file="$fileName.c"
output_binary="$fileName"

# Compile the program with -fopenmp and -std=c99
gcc -o "$output_binary" -fopenmp -std=c99 "$source_file"

if [ $? -ne 0 ]; then
  echo "Compilation failed. Exiting."
  exit 1
fi

# Run the program x times and measure the time
for ((i=1; i<=$iterations; i++)); do
  echo "Run $i:"
  /usr/bin/time ./"$output_binary" input-large.raw output"$i" search-1.raw
done

# Clean up the compiled binary
rm "$output_binary"

declare -a md5sums

for ((i=1; i<=$iterations; i++)); do
    file_name="output$i" 
    if [ -f "$file_name" ]; then
        md5sums+=("$(md5sum "$file_name")")
    else
        echo "File $file_name does not exist."
    fi
done

if [ "$(printf '%s\n' "${md5sums[@]}" | sort -u | wc -l)" -eq 1 ]; then
    echo "All MD5 checksums are the same."
else
    echo "MD5 checksums are different."
fi