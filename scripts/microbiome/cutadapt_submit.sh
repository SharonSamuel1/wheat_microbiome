#!/bin/bash

input_dir="/home/projects/zeevid/samuelsh/wheat_microbiome-2024/results/microbiome/PostTrim"
mkdir -p "/home/projects/zeevid/samuelsh/wheat_microbiome-2024/results/microbiome/logs/cutadapt"
output_dir_logs="/home/projects/zeevid/samuelsh/wheat_microbiome-2024/results/microbiome/logs/cutadapt"

for file in "$input_dir"/*/*_1_paired.fastq.gz; 
do
    SRR=$(basename "$file" _1_paired.fastq.gz)
    bsub -J ${SRR}_cutadapt -oo "$output_dir_logs"/output_%J.o -eo "$output_dir_logs"/error_%J.e \
    scripts/microbiome/cutadapt.sh $SRR
done
