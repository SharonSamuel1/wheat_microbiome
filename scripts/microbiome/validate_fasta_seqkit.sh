#!/bin/bash
#BSUB -J fastqc
#BSUB -q short 
#BSUB -R "rusage[mem=10G]"

# Function to convert FASTQ to FASTA
convert_fastq_to_fasta() {
    local fastq_file=$1
    local fasta_file=${fastq_file%.fastq.gz}.fasta

    zcat "$fastq_file" | awk 'NR % 4 == 1 {print ">"substr($0, 2)} NR % 4 == 2 {print}' > "$fasta_file"
    echo "$fasta_file"
}

# Function to validate FASTA sequences using seqkit
validate_fasta_sequences() {
    local fasta_file=$1

    invalid_count=$(seqkit seq --quiet --name --infile "$fasta_file" 2>&1 | grep -c "invalid sequence")
    
    echo "$invalid_count"
}

base_dir_A="/home/projects/zeevid/Data/Samples/2024-WildWheat/20240717_LH00211_0074_A222VG2LT1"
base_dir_b="/home/projects/zeevid/Data/Samples/2024-WildWheat/20240717_LH00211_0073_B222WKTLT1"

for sample_dir in "$base_dir_A"/*/ "$base_dir_B"/*/; do
    echo "Checking sample: $sample_dir"

    total_invalid_reads=0

    for fastq_file in "$sample_dir"*_R1.fastq.gz "$sample_dir"*_R2.fastq.gz; do
        if [[ -f "$fastq_file" ]]; then
            echo "Checking file: $fastq_file"
            
            fasta_file=$(convert_fastq_to_fasta "$fastq_file")
            invalid_reads=$(validate_fasta_sequences "$fasta_file")
            echo "Invalid reads in $fastq_file: $invalid_reads"
            total_invalid_reads=$((total_invalid_reads + invalid_reads))
                        rm "$fasta_file"
        fi
    done

    echo "Total invalid reads in sample $sample_dir: $total_invalid_reads"
    
    if [[ $total_invalid_reads -gt 0 ]]; then
        echo "$sample_dir" >> "$invalid_samples_file"
    fi
    
    echo "------------------------------------------"
done

if [[ -s "$invalid_samples_file" ]]; then
    echo "Samples with invalid reads:"
    cat "$invalid_samples_file"
else
    echo "No samples with invalid reads."
fi


#results- "No samples with invalid reads.- Job 975736"





