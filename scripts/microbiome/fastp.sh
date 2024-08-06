
#!/bin/bash
#BSUB -J fastp
#BSUB -q medium 
#BSUB -R "rusage[mem=4G]"
mkdir -p "/home/projects/zeevid/samuelsh/wheat_microbiome-2024/results/microbiome/logs/fastp"
output_dir_logs="/home/projects/zeevid/samuelsh/wheat_microbiome-2024/results/microbiome/logs/fastp"

#BSUB -oo "$output_dir_logs"/output_%J.o
#BSUB -eo "$output_dir_logs"/error_%J.e

module load fastp/0.23.4-GCC-12.2.0

input_dir="/home/projects/zeevid/Data/Samples/2024-WildWheat/20240717_LH00211_0074_A222VG2LT1" #run twice for A and B
output_dir="/home/projects/zeevid/samuelsh/wheat_microbiome-2024/results/microbiome/PostFastp"

if [ ! -d "$output_dir" ]; then
        mkdir -p "$output_dir"
fi

for file in  "$input_dir"/*/*_R1.fastq.gz;  #change!
do
    SRR=$(basename $file _R1.fastq.gz)
    mkdir -p "$output_dir"/${SRR}
    echo working on $SRR
    fastp --in1 "$input_dir"/${SRR}/${SRR}_R1.fastq.gz --out1 "$output_dir"/${SRR}/${SRR}_R1_trrimed_paired.fastq.gz \
    --in2 "$input_dir"/${SRR}/${SRR}_R2.fastq.gz --out2 "$output_dir"/${SRR}/${SRR}_R2_trrimed_paired.fastq.gz \
    --unpaired1 "$output_dir"/${SRR}/${SRR}_R1_unpaired.fastq.gz --unpaired2 "$output_dir"/${SRR}/${SRR}_R2_unpaired.fastq.gz \
    -l 50 --low_complexity_filter --trim_poly_g --cut_right --cut_right_window_size 4 --cut_right_mean_quality 15 \
    --cut_front --cut_front_window_size 1 --cut_front_mean_quality 10 \
    --cut_tail --cut_tail_window_size 1 --cut_tail_mean_quality 10 \
    --adapter_fasta /home/projects/zeevid/Bin/Trimmomatic-0.39/adapters/TruSeq3-PE.fa \
    --overrepresentation_analysis --json "$output_dir"/${SRR}/${SRR}_report_fastp.json --html "$output_dir"/${SRR}/${SRR}_report_fastp.html
done


#overrepresented sequence analysis -Overrepresented sequence analysis is disabled by default, you can specify -p or --overrepresentation_analysis to enable it. 
#Quality filtering is enabled by default,
#Length filtering is enabled by default -l 50
#Low complexity filter is disabled by default, and you can enable it by -y or --low_complexity_filter 

#For Illumina NextSeq/NovaSeq data, polyG can happen in read tails since G means no signal in the Illumina two-color systems. 
##fastp can detect the polyG in read tails and trim them. This feature is enabled for NextSeq/NovaSeq data by default,
### and you can specify -g or --trim_poly_g to enable it for any data, or specify -G or --disable_trim_poly_g to disable it.
### NextSeq/NovaSeq data is detected by the machine ID in the FASTQ records. 

#window- -r, --cut_right cut_right_window_size 4 cut_right_mean_quality 15 
#leading -5, --cut_front cut_front_window_size 1 cut_front_mean_quality 10
#trailing -3, --cut_tail cut_tail_window_size 1 cut_tail_mean_quality 10

#--adapter_fasta /home/labs/zeevid/Bin/Trimmomatic-0.39/adapters/TruSeq3-PE.fa


