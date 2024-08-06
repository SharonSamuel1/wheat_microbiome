#!/bin/bash
#BSUB -J fastqc
#BSUB -q short 
#BSUB -R "rusage[mem=1000MB]"
module load FastQC/0.12.1-Java-11


for sample in results/microbiome/PostTrim/*/*_1_paired.fastq.gz;
do
    SRR=$(basename $sample _1_paired.fastq.gz)
    echo working on $SRR
    output_dir="results/microbiome/fastqc_after_trim/${SRR}/"

    if [ ! -d "$output_dir" ]; then
        mkdir -p "$output_dir"
    fi
    
    fastqc -o results/microbiome/fastqc_after_trim/${SRR}/ results/microbiome/PostTrim/${SRR}/${SRR}_*_paired.fastq.gz 

done


