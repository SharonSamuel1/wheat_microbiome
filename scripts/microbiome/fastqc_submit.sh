
#!/bin/bash
chmod +x scripts/microbiome/fastp_call.sh

input_dir="$1"
output_dir="$2"
if [ ! -d "$3" ]; then
    mkdir -p "$3"
fi
output_dir_logs="$3"


for sample in results/microbiome/PostTrim/*/*_1_paired.fastq.gz; #this is just so it would go over all the samples, does not matter that it's this specific dir
do
    SRR=$(basename "$(dirname "$sample")")
    echo "Processing sample: $SRR"
    bsub -J "${SRR}_fastp" -q medium -R "rusage[mem=1G]" -oo "$output_dir_logs/output_%J.o" -eo "$output_dir_logs/error_%J.e" \
    scripts/microbiome/fastqc_call.sh "$SRR" "$input_dir" "$output_dir"
done
