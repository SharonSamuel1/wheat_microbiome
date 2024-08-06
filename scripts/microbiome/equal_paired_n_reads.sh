#!/bin/bash
#BSUB -J equal
#BSUB -q short 
#BSUB -R "rusage[mem=100MB]"

base_dir="results/microbiome/PostTrim"


mismatched_samples_file="results/mismatched_samples.txt"
> "$mismatched_samples_file" # Clear the file if it exists

# Function to count the number of reads in a FASTQ file
count_reads() {
    local fastq_file=$1
    local read_count=0

    read_count=$(zcat "$fastq_file" | awk 'END {print NR/4}')
    
    echo "$read_count"
}

for sample_dir in "$base_dir"/*/; do
    echo "Checking sample: $sample_dir"

    # Find the paired FASTQ files
    for fastq_file_1 in "$sample_dir"/*_1_paired.fastq.gz; do
        fastq_file_2="${fastq_file_1%_1_paired.fastq.gz}_2_paired.fastq.gz"

        if [[ -f "$fastq_file_1" && -f "$fastq_file_2" ]]; then
            echo "Checking files: $fastq_file_1 and $fastq_file_2"
            
            # Count reads in both files
            read_count_1=$(count_reads "$fastq_file_1")
            read_count_2=$(count_reads "$fastq_file_2")
            
            echo "Read count in $fastq_file_1: $read_count_1"
            echo "Read count in $fastq_file_2: $read_count_2"

            # Compare read counts
            if [[ "$read_count_1" -ne "$read_count_2" ]]; then
                echo "Mismatch found in sample $sample_dir"
                echo "$sample_dir" >> "$mismatched_samples_file"
            fi
        else
            echo "Paired files not found for sample $sample_dir"
        fi
    done

    echo "------------------------------------------"
done

# Display the list of samples with mismatched read counts
if [[ -s "$mismatched_samples_file" ]]; then
    echo "Samples with mismatched read counts:"
    cat "$mismatched_samples_file"
else
    echo "No samples with mismatched read counts."
fi
