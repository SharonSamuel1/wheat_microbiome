"""
A script that runs trimmomatic over the raw files

$$$ This script requiers the loading of env_getting_started env

module load Java/17.0.6
"""

import pathlib as pl
from subprocess import Popen
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input_path')#RawFast
parser.add_argument('-m', '--mem', default=80)
parser.add_argument('-e', '--extension') #.fq.gz
parser.add_argument('-o', '--outpath',) #results/PostTrim
parser.add_argument('-q', '--que', default='new-short')

args = parser.parse_args()

trimmomatic = "/home/labs/zeevid/Bin/Trimmomatic-0.39"
mem = 80
# Getting all the input files
raw_files = pl.Path(args.input_path)
samples_ls = list(raw_files.glob(rf'**/*{args.extension}')) #check if needs "list"
print(len(samples_ls))

#sample_names = set([f.stem.split(f'{args.extension}')[0] for f in samples_ls])
sample_names = set([f.stem.split('_')[0] for f in samples_ls])
print('found' + str(len(sample_names)) + 'samples')
#print (sample_names)

outpath = args.outpath
for samp in sample_names:
    samp_f = f'{raw_files}/{samp}_1{args.extension}'
    samp_r = f'{raw_files}/{samp}_2{args.extension}'
    outpath_dir = pl.Path(f'{outpath}/{samp}')
    if not outpath_dir.is_dir():
        outpath_dir.mkdir()
    command = [
        'java', '-jar', f'{trimmomatic}/trimmomatic-0.39.jar', 'PE', '-phred33', str(samp_f), str(samp_r),
        f'{outpath_dir}/{samp}_1_paired{args.extension}', f'{outpath_dir}/{samp}_1_unpaired{args.extension}',
        f'{outpath_dir}/{samp}_2_paired{args.extension}', f'{outpath_dir}/{samp}_2_unpaired{args.extension}',
        'LEADING:10', 'TRAILING:10', 'SLIDINGWINDOW:4:15', 'MINLEN:50',
        f'ILLUMINACLIP:{trimmomatic}/adapters/TruSeq3-PE.fa:2:30:10'
    ]    
    print(command)
    Popen(command)



#run "python trim_auto.py -i RawFastq -e .fastq.gz -o results/PostTrim" (wd- '2023-Sharon')