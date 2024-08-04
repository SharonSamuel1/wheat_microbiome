
#!/bin/bash
#BSUB -J cutadapt
#BSUB -q short 
#BSUB -R "rusage[mem=10G]"


#script adapted from Tamir's script
input_dir="/home/projects/zeevid/samuelsh/wheat_microbiome-2024/results/microbiome/PostTrim"
output_dir="/home/projects/zeevid/samuelsh/wheat_microbiome-2024/results/microbiome/PostCutAdapt"
# Ensure the output directory exists
mkdir -p "$output_dir"
# Adapter sequences to trim
adapter_seq_rev="GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG" # Adapter sequence for reverse reads; adjust if different
# Function to process a single pair of files with Cutadapt
process_files() {
    basename=$1
    file_r1="$input_dir/${basename}_1_paired.fastq.gz"
    file_r2="$input_dir/${basename}_1_paired.fastq.gz"
    output_r1="$output_dir/${basename}_1_paired_cutadapt.fastq.gz"
    output_r2="$output_dir/${basename}_2_paired_cutadapt.fastq.gz"

    cutadapt -A "$adapter_seq_rev" -o "$output_r1" -p "$output_r2" "$file_r1" "$file_r2"
}

echo "Cutadapt processing complete."



