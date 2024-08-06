#!/bin/bash

chmod +x scripts/microbiome/fastp_call.sh

input_dir="/home/projects/zeevid/Data/Samples/2024-WildWheat/20240717_LH00211_0073_B222WKTLT1"
output_dir_logs="/home/projects/zeevid/samuelsh/wheat_microbiome-2024/results/microbiome/logs/fastp"

mkdir -p "$output_dir_logs"

for file in "$input_dir"/*/*_R1.fastq.gz; 
do
    SRR=$(basename $file _R1.fastq.gz)
    bsub -J ${SRR}_fastp -q medium -R "rusage[mem=4G]" -oo "$output_dir_logs/output_%J.o" -eo "$output_dir_logs/error_%J.e" \
    scripts/microbiome/fastp_call.sh $SRR
done
 