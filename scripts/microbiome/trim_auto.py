"""
A script that runs trimmomatic over the raw files

$$$ This script requiers the loading of env_getting_started env

module load Java/17.0.6
"""


import pathlib as pl
from subprocess import Popen
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input_path', required=True, help='Path to the input directory containing sample folders.')
parser.add_argument('-e', '--extension', default='.fastq.gz', help='File extension of the raw files.')
parser.add_argument('-o', '--outpath', required=True, help='Path to the output directory.')
parser.add_argument('-q', '--que', default='new-short')

args = parser.parse_args()

trimmomatic = "/home/projects/zeevid/Bin/Trimmomatic-0.39"
# Getting all the sample directories that are numeric
input_path = pl.Path(args.input_path)
sample_folders = [f for f in input_path.iterdir() if f.is_dir() and f.name.isdigit()]

print('Found ' + str(len(sample_folders)) + ' sample directories.')
print(sample_folders)

outpath = pl.Path(args.outpath)
for sample_folder in sample_folders:
    sample_name = sample_folder.name
    # Locate R1 and R2 files
    samp_f = sample_folder / f'{sample_name}_R1{args.extension}'
    samp_r = sample_folder / f'{sample_name}_R2{args.extension}'

    if not samp_f.exists() or not samp_r.exists():
        print(f"Warning: Missing files for sample {sample_name}.")
        continue
    
    # Create output directory if it doesn't exist
    outpath_dir = outpath / sample_name
    outpath_dir.mkdir(parents=True, exist_ok=True)

    command = [
        'java', '-jar', f'{trimmomatic}/trimmomatic-0.39.jar', 'PE', '-phred33', str(samp_f), str(samp_r),
        f'{outpath_dir}/{sample_name}_1_paired{args.extension}', f'{outpath_dir}/{sample_name}_1_unpaired{args.extension}',
        f'{outpath_dir}/{sample_name}_2_paired{args.extension}', f'{outpath_dir}/{sample_name}_2_unpaired{args.extension}',
        'LEADING:10', 'TRAILING:10', 'SLIDINGWINDOW:4:15', 'MINLEN:50',
        f'ILLUMINACLIP:{trimmomatic}/adapters/TruSeq3-PE.fa:2:30:10'
    ]    
    print(command)
    Popen(command)




#run "python //home/projects/zeevid/samuelsh/wheat_microbiome-2024/scripts/microbiome/trim_auto.py -i /home/projects/zeevid/Data/Samples/2024-WildWheat/20240717_LH00211_0074_A222VG2LT1 -e .fastq.gz -o results/PostTrim" (wd- '2023-Sharon')  

#tun using sh file called trim_run_py.sh 