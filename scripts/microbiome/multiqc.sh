#!/bin/bash

# the directory where the samples are stored
samples_directory="/home/projects/zeevid/samuelsh/2023-Sharon/results/fastqc/"
output_directory="/home/projects/zeevid/samuelsh/2023-Sharon/results/microbiome/multiqc/"
file_list="my_file_list.txt"
for sample_dir in "${samples_directory}"/*/; do
    sample=$(basename "${sample_dir}")
    found_files=$(find "${sample_dir}" -name "*" -exec grep -l "FAIL" {} +)
        if [ -n "${found_files}" ]; then
        echo "${sample_dir}" >> "${file_list}"
        fi
done

# Run multiqc using the file list (in which it found 'FAIL')
if [ -s "${file_list}" ]; then
    echo "Running multiqc for files with FAIL using file list: ${file_list}"
    multiqc --file-list "${file_list}" -o "/home/projects/zeevid/samuelsh/2023-Sharon/results/multiqc"
fi

rm -f "${file_list}"




