#!/bin/bash
#BSUB -J trim
#BSUB -q medium 
#BSUB -R "rusage[mem=50G]"

module load Java/17.0.6

python /home/projects/zeevid/samuelsh/wheat_microbiome-2024/scripts/microbiome/trim_auto.py -i /home/projects/zeevid/Data/Samples/2024-WildWheat/20240717_LH00211_0073_B222WKTLT1 -e .fastq.gz -o results/microbiome/PostTrim

