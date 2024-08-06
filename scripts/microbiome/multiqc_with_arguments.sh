
#!/bin/bash

module load MultiQC/1.12-foss-2021b

samples_directory="$1"
output_directory="$2"
file_list="my_file_list.txt"

if [ ! -d "$output_directory" ]; then
    mkdir -p "$output_directory"
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


