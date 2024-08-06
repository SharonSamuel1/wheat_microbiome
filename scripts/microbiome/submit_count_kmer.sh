#!/bin/bash

chmod +x scripts/microbiome/count_kmers_Dudi.py

input_dir="$1" #"results/microbiome/PostFastp"
output_dir="$2" #"results/microbiome/kmer_counts"
mkdir -p "$output_dir"
output_dir_logs="$3" #"results/microbiome/logs/kmer_counts_fastp"
mkdir -p "output_dir_logs"
k=4
for sample in $input_dir/1/*_R1_trrimed_paired.fastq.gz; #change!
    SRR=$(basename "$(dirname "$sample")")
    echo "Processing sample: $SRR"
    bsub -J "${SRR}_kmers" -q medium -R "rusage[mem=1G]" -oo "$output_dir_logs/${SRR}_output.o" -eo "$output_dir_logs/${SRR}_error.e" \
    python scripts/microbiome/count_kmers_Dudi.py "$input_dir/$SRR/" "$output_dir" $k
done

