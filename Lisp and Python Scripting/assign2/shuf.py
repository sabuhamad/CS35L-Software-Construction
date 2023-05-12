#!/usr/bin/python
import random
import sys
import argparse
import string

class RandLine:
    def __init__(self, filename):
            with open(filename, 'r') as f:
              self.lines = f.readlines()

def main():
    usage_msg = """shuf [OPTION]... [FILE]\nor:  shuf -e [OPTION]... [ARG]...\nor:  shuf -i LO-HI [OPTION]..."""
    description_msg = """Write a random permutation of the input lines to standard output.\nWith no FILE, or when FILE is -, read standard input.\nMandatory arguments to long options are mandatory for short options too."""
    parser = argparse.ArgumentParser(description=description_msg,usage=usage_msg)
    parser.add_argument("file", nargs="?", help="File to be shuffled")
    parser.add_argument("-e", "--echo", nargs="*", help="Treat each ARG as an input line")
    parser.add_argument("-i", "--input-range", help="Treat each number LO through HI as an input line")
    parser.add_argument("-n", "--head-count", nargs =None, type=int, help="Output at most COUNT lines")
    parser.add_argument("-r", "--repeat", action="store_true", help="Output lines can be repeated")
    args, unknown = parser.parse_known_args()
   

    num = None 
    lines = []
    if args.head_count:
        num = args.head_count
        if num < 0:
            parser.error("negative count")
    if args.input_range:
        try:
            ir_str = args.input_range
            split_str = ir_str.split("-")
            ir_lo = int(split_str[0])
            ir_hi = int(split_str[1])
            lines = list(range(ir_lo, ir_hi + 1))
        except:
            parser.error("invalid input range")
        if ir_lo < 0 or ir_hi < 0:
            parser.error("negative range")
        if args.file is not None:
            parser.error("extra operand: " + str(args.file))
    if args.echo is not None:
        lines = args.echo
        if args.input_range is not None:
            parser.error("cannot combine -e and -i options")
        if(args.file is not None):
            lines.append(args.file)
            args.file = None
        if (len(unknown) > 0):
            for i in unknown:
                lines.append(i)
            unknown = []
    if unknown:
        parser.error("extra operand: " + str(unknown[0]))
    if args.input_range is None and args.file is None and (args.echo is None):
        lines = sys.stdin.readlines()
    elif args.input_range is None and args.file == '-':
        lines = sys.stdin.readlines()
    elif args.input_range is None and args.file is not None and (args.echo is None):
        try:
            generator = RandLine(args.file)
        except:
            parser.error("No such file or directory: " + str(args.file))
        lines = generator.lines
    random.shuffle(lines)
    if num is None and (not args.repeat):
        num = len(lines)
    if (not args.repeat) and num > len(lines):
        parser.error("count is larger than number of lines")
    if not args.repeat and args.input_range is None and args.echo is None:
        for index in range(0, num):
            sys.stdout.write(lines[index])
    elif not args.repeat and (args.input_range is not None or args.echo is not None):
        for index in range(0, num):
            sys.stdout.write(str(lines[index]) + "\n")
    elif args.repeat:
        if num is None:
            num = True 
        if args.input_range is None and args.echo is None:
            while num != 0:
                sys.stdout.write(lines[0])
                random.shuffle(lines)
                if isinstance(num, bool) is False:
                    num -= 1
        else:
            while num != 0:
                sys.stdout.write(str(lines[0]) + "\n")
                random.shuffle(lines)
                if isinstance(num, bool) is False:
                    num -= 1

if __name__ == "__main__":
    main()

