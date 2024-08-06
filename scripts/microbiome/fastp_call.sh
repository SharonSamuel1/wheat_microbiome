

#!/bin/bash

module load fastp/0.23.4-GCC-12.2.0

input_dir="/home/projects/zeevid/Data/Samples/2024-WildWheat/20240717_LH00211_0073_B222WKTLT1"
output_dir="/home/projects/zeevid/samuelsh/wheat_microbiome-2024/results/microbiome/PostFastp"

SRR=$1

if [ ! -d "$output_dir/${SRR}" ]; then
    mkdir -p "$output_dir/${SRR}"
fi

echo working on $SRR
fastp --in1 "$input_dir/${SRR}/${SRR}_R1.fastq.gz" --out1 "$output_dir/${SRR}/${SRR}_R1_trrimed_paired.fastq.gz" \
      --in2 "$input_dir/${SRR}/${SRR}_R2.fastq.gz" --out2 "$output_dir/${SRR}/${SRR}_R2_trrimed_paired.fastq.gz" \
      --unpaired1 "$output_dir/${SRR}/${SRR}_R1_unpaired.fastq.gz" --unpaired2 "$output_dir/${SRR}/${SRR}_R2_unpaired.fastq.gz" \
      -l 50 --low_complexity_filter --trim_poly_g --cut_right --cut_right_window_size 4 --cut_right_mean_quality 15 \
      --cut_front --cut_front_window_size 1 --cut_front_mean_quality 10 \
      --cut_tail --cut_tail_window_size 1 --cut_tail_mean_quality 10 \
      --adapter_fasta /home/projects/zeevid/Bin/Trimmomatic-0.39/adapters/TruSeq3-PE.fa \
      --overrepresentation_analysis --json "$output_dir/${SRR}/${SRR}_report_fastp.json" --html "$output_dir/${SRR}/${SRR}_report_fastp.html"
