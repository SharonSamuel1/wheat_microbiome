
#!/bin/bash

samples_directory="$1"
output_directory="$2"
file_list="my_file_list.txt"

if [ ! -d "$samples_directory" ]; then
    echo "Error: The directory '$samples_directory' does not exist."
    exit 1
fi

if [ ! -d "$output_directory" ]; then
    echo "Error: The directory '$output_directory' does not exist."
    exit 1
fi

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
    multiqc --file-list "${file_list}" -o "${output_directory}"
fi

rm -f "${file_list}"

#before trim-

#./run_multiqc.sh /home/projects/zeevid/samuelsh/2023-Sharon/results/fastqc/ /home/projects/zeevid/samuelsh/2023-Sharon/results/microbiome/multiqc/

#