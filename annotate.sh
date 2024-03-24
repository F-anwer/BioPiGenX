#!/bin/bash

# Set the directories
msa_dir="/home/farah/Pipeline/multiple_sequence_alignment"
annot_dir="annotation"
fastadir="${msa_dir}/fasta"
extension=".fasta"
cpus=2

mkdir -p "$annot_dir"

allfasta=("${fastadir}"/*"${extension}")

for file in "${allfasta[@]}"; do
    bname=$(basename "$file" "$extension")

    prokka --cpus "$cpus" --kingdom Virus --locustag "$bname" \
        --addgenes --outdir "${annot_dir}/${bname}" --prefix "${bname}" \
        --centre YourCenter --compliant "$file"
done

