#!/bin/bash
#BSUB -J cutadapt
#BSUB -q short 
#BSUB -R "rusage[mem=100MB]"

module load cutadapt/4.2-GCCcore-11.3.0

input_dir="/home/projects/zeevid/samuelsh/wheat_microbiome-2024/results/microbiome/PostTrim"
output_dir="/home/projects/zeevid/samuelsh/wheat_microbiome-2024/results/microbiome/PostCutAdapt"

adapter_seq_rev="G{50}"

SRR=$1

if [ ! -d "$output_dir/${SRR}" ]; then
    mkdir -p "$output_dir/${SRR}"
fi

echo working on $SRR
file_r1="$input_dir/${SRR}/${SRR}_1_paired.fastq.gz"
file_r2="$input_dir/${SRR}/${SRR}_2_paired.fastq.gz"
output_r1="$output_dir/${SRR}/${SRR}_1_paired_cutadapt.fastq.gz"
output_r2="$output_dir/${SRR}/${SRR}_2_paired_cutadapt.fastq.gz"

cutadapt -A "$adapter_seq_rev" -a "$adapter_seq_rev" --overlap 10 --minimum-length 100 -o "$output_r1" -p "$output_r2" "$file_r1" "$file_r2"
