import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('LRG_file', help = 'Input LRG filename')
    parser.add_argument('Out_file', help = 'Output filename') 
    parser.add_argument('-i', help = 'Include flanking intronic regions', nargs = 2, action = 'store_false', default = [0,0])

    args = parser.parse_args()
    lrg_filename = args.LRG_file
    outfile_name = args.Out_file   
    if -i:
        minus, plus  = args.i

    print lrg_filename	
    print outfile_name
    print minus
    print plus
    

main()
