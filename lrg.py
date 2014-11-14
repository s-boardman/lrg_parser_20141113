# Import required modules

import xml.etree.ElementTree as et

# Import file and get root

tree = et.parse('LRG_1.xml')
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
    file = open('LRG_1.fa','w')
    for exon in sorted(exon_dict):
        start = int(exon_dict[exon]['start'])
        end = int(exon_dict[exon]['end'])
        file.write('>' + exon + '\n')
        file.write(ref_seq[start-1: end-1] + '\n')
    file.close()

# Call functions to produce output
ref_seq = get_element_text('./fixed_annotation/sequence')
exon_info = get_exon_info('./fixed_annotation/transcript/exon', 'label')
fasta = get_fasta(exon_info)







# Capture transcripts

#def get_transcripts(path, value):
#   for element in root.findall(path):
#       transcripts.append(element.get(value))
#    return transcripts
