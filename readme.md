# LRG Parser Project

## Project Brief

Create code to take an Locus Reference Genome file and return exon sequences in .fasta format.

Include flexibility to return genomic or transcriptomic sequence, with the possibility to select intronic regions if required.

## Usage notes

Exonic sequences only:
- python lrg.py input_file.xml output_file.fa

With user specified intronic region:

- python lrg.py input_file.xml output_file.fa -i 
