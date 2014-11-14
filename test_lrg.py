# Import required modules

import xml.etree.ElementTree as et, argparse, sys

# Get parameters

def test_main():
    '''Main function that collects command line arguments and assigns to global variables'''
    # Establish global parameters to be used
    global lrg_file, fasta, tree, root, include_introns, intron
    parser = argparse.ArgumentParser()
    parser.add_argument('LRG_file',  help = 'Input LRG filename')
    parser.add_argument('Out_file', help = 'Output fasta filename')
    parser.add_argument('-i', help = 'Includes user defined length flanking intronic sequence. Parameter must be integer', default = '0')

    args = parser.parse_args()
    lrg_file = args.LRG_file
    fasta = args.Out_file
    
    # Check a valid integer value has been provided for flanking intron sequences
    try:
        intron = int(args.i)
    except:
        print 'Please provide an integer value for flanking sequence'
        sys.exit()

    # Set flag to be used for including intronic sequence in output
    if args.i:
        include_introns = True
    else:
        include_introns = False

    # Check file is available and a valid .xml file
    try:
        tree = et.parse(lrg_file) 
    except:
        print 'Unable to parse/open file'
        sys.exit()
    
    # Check file is an lrg file and establish root    
    root = tree.getroot()
    assert root.tag == 'lrg', 'Input file is not a valid LRG file'

def test_get_element_text(value):
    '''Returns text of selected element'''
    for element in root.findall(value):
        # Check element has associated text
        assert len(element.text) > 0, 'Element has no associated text' 
        return element.text

def test_get_file_info(tree):
    '''Creates fasta headers to write into output file'''
    lrg_id = test_get_element_text('./fixed_annotation/id')
    if  len(test_get_element_text('./fixed_annotation/hgnc_id')) > 0:
	hgnc_id = test_get_element_text('.fixed_annotation/hgnc_id')
	file_id = 'LRG_ID:' + lrg_id + '_HGNC_ID:' + hgnc_id + '_Exon:'
    else:
        file_id = 'LRG_ID:' + lrg_id + '_Exon:'
    return file_id

def test_get_exon_info(path, value):
    '''Gets coordinates of exons'''
    exon_dict = {}
    for element in root.findall(path):
        exon_dict[element.get(value).zfill(3)] = element[0].attrib
    # Check we have collected exons 
    assert len(exon_dict) > 0, 'No Exons found in file'
    return exon_dict

def test_get_fasta(exon_dict,file_info):
    '''Collates sequences and outputs fasta files'''
    with open(fasta,'w+') as file:
        for exon in sorted(exon_dict):
                # Check we have start and end coordinates for all exons
                try:
                    start = int(exon_dict[exon]['start'])
                    end = int(exon_dict[exon]['end'])
                except KeyError:
                    print 'Start/End Coordinates not present for at least one exon'
                    sys.exit()
                
                # Include flanking intronic regions as specified in fasta output if requested     
                if include_introns == False:
                    file.write('>' + test_get_file_info(tree) + exon + '\n')
                    file.write(ref_seq[start-1: end] + '\n')
                elif include_introns == True:
                    file.write('>' + test_get_file_info(tree) + exon + '\n')
                    file.write(ref_seq[start-(intron+1): start-1].lower() + ref_seq[start-1: end] + ref_seq[end: end+intron].lower() + '\n')
        print 'Fasta file (' + fasta + ') written to file.'

# Call main to get inputs
test_main()
# Call functions to produce output
ref_seq = test_get_element_text('./fixed_annotation/sequence')
lrg_info = test_get_file_info(root)
exon_info = test_get_exon_info('./fixed_annotation/transcript/exon', 'label')
fasta = test_get_fasta(exon_info,lrg_info)
