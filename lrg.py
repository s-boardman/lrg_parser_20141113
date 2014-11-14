# Import required modules

import xml.etree.ElementTree as et, argparse, sys

# Get parameters

def main():
    '''Main function that collects command line arguments and assigns to global variables'''
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

    try:
        tree = et.parse(lrg_file) 
    except:
        print 'Unable to parse/open file'
        sys.exit()
        
    root = tree.getroot()
    assert root.tag == 'lrg', 'Input file is not a valid LRG file'

def get_element_text(value):
    '''Returns text of selected element'''
    for element in root.findall(value):
        assert len(element.text) > 0, 'Element has no associated text' 
        return element.text

def get_file_info(tree):
    '''Creates fasta headers to write into output file'''
    lrg_id = get_element_text('./fixed_annotation/id')
    hgnc_id = get_element_text('./fixed_annotation/hgnc_id')
    file_id = 'LRG ID:' + lrg_id + ' HGNC ID:' + hgnc_id + ' Exon: '
    return file_id

def get_exon_info(path, value):
    '''Gets coordinates of exons'''
    exon_dict = {}
    for element in root.findall(path):
        assert len(element[0].attrib) > 0, 'Exon is missing start/end coordinates'
        exon_dict[element.get(value).zfill(3)] = element[0].attrib
    assert len(exon_dict) > 0, 'No Exons found in file'
    return exon_dict

def get_fasta(exon_dict,file_info):
    '''Collates sequences and outputs fasta files'''
    file = open(fasta,'w')
    for exon in sorted(exon_dict):
            try:
                start = int(exon_dict[exon]['start'])
                end = int(exon_dict[exon]['end'])
            except KeyError:
                print 'Start/End Coordinates not present for at least one exon'
                sys.exit()

            if include_introns == False:
                file.write('>' + get_file_info(tree) + exon + '\n')
                file.write(ref_seq[start-1: end-1] + '\n')
            elif include_introns == True:
                file.write('>' + get_file_info(tree) + exon + '\n')
                file.write(ref_seq[start-101: start-2].lower() + ref_seq[start-1: end-1] + ref_seq[end: end+100].lower() + '\n')
    file.close()

# Call main to get inputs
main()
# Call functions to produce output
ref_seq = get_element_text('./fixed_annotation/sequence')
lrg_info = get_file_info(root)
exon_info = get_exon_info('./fixed_annotation/transcript/exon', 'label')
fasta = get_fasta(exon_info,lrg_info)
