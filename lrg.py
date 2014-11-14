# Import required modules

import xml.etree.ElementTree as et, argparse

# Get parameters

def main():
    global lrg_file, fasta, tree, root, include_introns
    parser = argparse.ArgumentParser()
    parser.add_argument('LRG_file',  help = 'Input LRG filename')
    parser.add_argument('Out_file', help = 'Output fasta filename')
    parser.add_argument('-i', help = 'Includes 100bp on either side of exon', action = 'store_true')

    args = parser.parse_args()
    lrg_file = args.LRG_file
    fasta = args.Out_file

    if args.i:
        include_introns = True
    else:
        include_introns = False

    tree = et.parse(lrg_file)
    root = tree.getroot()

# Get element text function

def get_element_text(value):
    for element in root.findall(value):
        return element.text

# Get exon coordinates

def get_exon_info(path, value):
    exon_dict = {}
    for element in root.findall(path):
        exon_dict[element.get(value).zfill(3)] = element[0].attrib
    return exon_dict

# Get fasta format

def get_fasta(exon_dict):
    file = open(fasta,'w')
    for exon in sorted(exon_dict):
            start = int(exon_dict[exon]['start'])
            end = int(exon_dict[exon]['end'])
            if include_introns == False:
                file.write('>' + exon + '\n')
                file.write(ref_seq[start-1: end-1] + '\n')
            elif include_introns == True:
                file.write('>' + exon + '\n')
                file.write(ref_seq[start-101: start-2].lower() + ref_seq[start-1: end-1] + ref_seq[end: end+100] + '\n')
    file.close()

# Call main to get inputs
main()
# Call functions to produce output
ref_seq = get_element_text('./fixed_annotation/sequence')
exon_info = get_exon_info('./fixed_annotation/transcript/exon', 'label')
fasta = get_fasta(exon_info)

# Capture transcripts

#def get_transcripts(path, value):
#   for element in root.findall(path):
#       transcripts.append(element.get(value))
#    return transcripts
