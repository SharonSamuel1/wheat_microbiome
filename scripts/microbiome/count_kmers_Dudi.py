## coding: utf-8
# %load ./Kmers/count_kmers.py
from collections import Counter, defaultdict

from itertools import product
from numba import jit

import numpy as np
import pandas as pd
from gzip import open as gopen


#! By using @jit(nopython=True) we can compile the function to machine code, which makes it run much faster
#! "jit" stands for "Just In Time" compilation, which means that the function is compiled when it is first called
@jit(nopython=True)
def base_to_int(base):
    """
    Convert a base to an integer. For "jit" purposes, we don't use a dictionary, but rather a series of if-else
    This function is used in count_kmers() where the integer representation of the kmer is constructed base-by-base
    based on the integer representation of each base.

    :param base: one of A, C, G, T
    :return: integer representation of the base
    """
    if base == 'A':
        return 0
    elif base == 'C':
        return 1
    elif base == 'G':
        return 2
    elif base == 'T':
        return 3
    else:
        return -1

@jit(nopython=True)
def count_kmers(sequence, k):
    """
    Count the number of occurrences of each kmer in a sequence.
    We use a numpy array to store the counts as they happen (the number of options is 4^k, so we can use a 1D array).

    'index' is the base-4 representation of the kmer. It is initialized to 0 and then constructed base-by-base in the loop.
    For each base (in the current window) we multiply by 4 and add the integer representation of the base.
    This gives a unique integer representation of the kmer which we can use as an index in the counts array.

    :param sequence: a string of A, C, G, T
    :param k: kmer length
    :return: 1D numpy array of counts of the different kmers
    """
    counts = np.zeros(4**k, dtype=np.int64)
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i+k] # sliding window
        index = 0
        valid_kmer = True
        for base in kmer:
            base_int = base_to_int(base)
            if base_int == -1: # the base isn't one of [A, C, G, T]
                valid_kmer = False
                break
            index = index * 4 + base_int
        if valid_kmer:
            counts[index] += 1
    return counts

@jit(nopython=True)
def int_to_base(n):
    """
    Convert an integer to a base. For "jit" purposes, we don't use a dictionary, but rather a series of if-else.
    This function is used in int_to_kmer() where the integer representation of the kmer is converted to a string

    :param n: integer representation of a base
    :return: the base
    """
    if n == 0:
        return 'A'
    elif n == 1:
        return 'C'
    elif n == 2:
        return 'G'
    elif n == 3:
        return 'T'
    else:
        return 'N'

@jit(nopython=True)
def int_to_kmer(n, k):
    """
    Convert an integer to a kmer. We use the fact that the integer representation of the kmer is base-4 (4^k options).
    We construct the kmer base-by-base, starting from the least significant base (the rightmost base).

    :param n: integer representation of a kmer
    :param k: kmer length (for example for tetranucleotides, k=4)
    :return: the kmer as a list of bases
    """
    kmer = []
    # _ is a dummy variable. In each iteration we change *n* so we don't need to keep track of the loop index
    for _ in range(k):
        kmer.append(int_to_base(n % 4))
        n //= 4
    return kmer[::-1] # reverse the list


def translate_counts(counts, k):
    """
    Convert the counts array to a list of tuples of kmers and their counts.
    This function is used in count_file() where we want to convert the counts array to a dictionary of kmers and their counts
    :param counts: numpy array of counts
    :param k: kmer length
    :return: a list of tuples of the kmer and its count
    """
    kmers = []
    for i in range(len(counts)):
        if counts[i] > 0: # only add kmers that appear at least once
            kmer = int_to_kmer(i, k) # list of bases (that's why we use ''.join() later)
            kmers.append((''.join(kmer), counts[i])) # append a tuple of the kmer and its count to the list
    return kmers


def count_file(in_fname, k, is_bam=False, is_fasta=False):
    """
    Count the number of occurrences of each kmer in a file (fastq, bam, fasta).
    :param in_fname: file name (path)
    :param k: kmer length
    :param is_bam: is the file a bam file? (default: False)
    :param is_fasta: is the file a fasta file? (default: False)
    :return:
    """
    # we wanted to count kmers for a few options: 10,000 reads, 100,000 reads, 1,000,000 reads, and all reads
    # first we initialize the dictionary with the 'all' key (the other keys will be added later)
    ret = {'all':np.zeros(4**k, dtype=np.int64)}

    if is_bam:
        import pysam
        for i, rec in enumerate(pysam.AlignmentFile(in_fname)):
            if i in [10_000, 100_000, 1_000_000]:
                ret[i] = ret['all'].copy() # checkpoint - save the counts for the current number of reads
            ret['all'] += count_kmers(rec.seq, k) # add the counts of the current read to the total counts
    elif is_fasta:
        from Bio import SeqIO
        # check if file is gzipped:
        opening_func = gopen if in_fname.endswith('.gz') else open
        with opening_func(in_fname,'rt') as fin:
            for rec in SeqIO.parse(fin, 'fasta'):
                ret['all'] += count_kmers(str(rec.seq), k)
    else: # fastq
        import pysam
        for i, rec in enumerate(pysam.FastqFile(in_fname)):
            if i in [10_000, 100_000, 1_000_000]:
                ret[i] = ret['all'].copy()
            ret['all'] += count_kmers(rec.sequence, k)

    clean_ret = {}
    for num_reads in ret.keys():
        clean_ret[num_reads] = {}
        # convert the counts array to a dictionary of kmers and their counts (translate_counts() is defined above)
        temp_dct = dict(translate_counts(ret[num_reads], k))
        all_rc_k = all_kmers_rc(k) # rc stands for reverse complement
        for kpair, kmers in all_rc_k.items():
            # account for reverse complement kmers
            clean_ret[num_reads][kpair] = sum([temp_dct[i] for i in kmers if i in temp_dct]) # the if i in kmers is for cases where there are few reads and some kmers are not represented.
    return clean_ret

def rc(kmer):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return "".join(complement[base] for base in reversed(kmer))

def all_kmers_rc(k):
    letters = 'ACGT'
    kmers = sorted([''.join(perm) for perm in product(letters, repeat=k)])
    new_kmers = defaultdict(list)
    for kmer in kmers:
        new_kmers['{}/{}'.format(*sorted([kmer,rc(kmer)]))].append(kmer)
    return new_kmers

def run(fastq_gz, output_fname_base, ks, is_bam=False, is_fasta=False):
    """
    Run the count_file() function for a few kmer lengths and save the results to csv files.
    :param fastq_gz: file path
    :param output_fname_base: output file name base
    :param ks: kmer options
    :param is_bam: is the file a bam file? (default: False)
    :param is_fasta: is the file a fasta file? (default: False)
    :return:
    """
    for k in ks:
        ret = count_file(fastq_gz, k, is_bam, is_fasta)
        df = pd.DataFrame(ret)
        df.to_csv(output_fname_base + '_' + str(k) + 'mers.csv')

if __name__ == '__main__':
    import sys
    # argument1: fastq.gz file (or fasta or bam)
    # argument2: output file name base
    # argument3: kmer size
    # argument4 (optional): bam / fasta
    if sys.argv[-1] == 'bam':
        is_bam = True
        is_fasta = False
        ks = sys.argv[3:-1]
    elif sys.argv[-1] == 'fasta':
        is_bam = False
        is_fasta = True
        ks = sys.argv[3:-1]
    else:
        is_bam = False
        is_fasta = False
        ks = sys.argv[3:]

    run(sys.argv[1], sys.argv[2],[int(k) for k in ks], is_bam, is_fasta)


    #python script.py input.fastq output 4 -This command uses input.fastq as the input file, output as the base name for output files, and uses k-mer size of 4.