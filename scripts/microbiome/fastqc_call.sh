#!/bin/bash

module load FastQC/0.12.1-Java-11

SRR=$1
input_dir="$2"
output_dir="$3"
output_dir_sample="$output_dir/$SRR"

if [ ! -d "$output_dir_sample" ]; then
    mkdir -p "$output_dir_sample"
fi

echo "Running FastQC for $SRR"
echo "Input directory: $input_dir"
echo "Output directory: $output_dir_sample"

# Find all paired files for the given SRR
input_files=($(find "$input_dir/$SRR/" -name "*_paired*.fastq.gz"))

if [ ${#input_files[@]} -gt 0 ]; then
    fastqc -o "$output_dir_sample" "${input_files[@]}"
else
    echo "Skipping: No paired fastq.gz files found for $SRR"
fi


