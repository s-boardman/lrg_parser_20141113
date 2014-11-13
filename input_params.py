import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('LRG_file', help = 'Input LRG filename')
    parser.add_argument('Output filename', help = 'Output filename') 
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', help = 'Adds numbers together', action='store_true')
    group.add_argument('-s', help = 'Subtracts second number from first', action='store_true')

	args = parser.parse_args()
	if args.a:
		answer = args.first + args.second
	elif args.s:
		answer = args.first - args.second

main()
