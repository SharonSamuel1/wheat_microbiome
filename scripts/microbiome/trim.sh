
#!/bin/bash
#BSUB -J trim
#BSUB -q medium 
#BSUB -R "rusage[mem=5G]"

module load Java/21.0.2

input_dir="/home/projects/zeevid/Data/Samples/2024-WildWheat/20240717_LH00211_0074_A222VG2LT1" 
output_dir="/home/projects/zeevid/samuelsh/wheat_microbiome-2024/results/microbiome/PostTrim"

trimmomatic="/home/projects/zeevid/Bin/Trimmomatic-0.39"

if [ ! -d "$output_dir" ]; then
        mkdir -p "$output_dir"
fi

for file in  "$input_dir"/*/*_R1.fastq.gz;
do
    SRR=$(basename $file _R1.fastq.gz)
    mkdir -p "$output_dir/${SRR}"
    echo working on $SRR
    java -jar "$trimmomatic"/trimmomatic-0.39.jar PE -phred33 "$input_dir"/${SRR}/${SRR}_R1.fastq.gz "$input_dir"/${SRR}/${SRR}_R2.fastq.gz "$output_dir"/${SRR}/${SRR}_1_paired.fastq.gz "$output_dir"/${SRR}/${SRR}_1_unpaired.fastq.gz "$output_dir"/${SRR}/${SRR}_2_paired.fastq.gz "$output_dir"/${SRR}/${SRR}_2_unpaired.fastq.gz ILLUMINACLIP:/home/projects/zeevid/Bin/Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10:2:30:10 LEADING:10 TRAILING:10 SLIDINGWINDOW:4:15 MINLEN:50 
done



