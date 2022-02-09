#!/usr/bin/python
#Darren Wu 405597243 CS35L Assignment 2
"""
"""
import random, sys
import argparse

def shuffle(lines, repeat, maxcount, mc):
    
    out = []
    count = 0

    newlines = lines[:]
   # print(maxcount)

    
    while len(newlines)>0 and count<maxcount:
        #print(newlines)

        if(repeat):
            i = random.randint(0,len(lines)-1)
            out.append(lines[i])
            newlines.pop()
            count+=1
            
        else:
            i = random.randint(0,len(newlines)-1)
            out.append(newlines[i])
            newlines.pop(i)
            count += 1
    return out

def main():
    parser = argparse.ArgumentParser(description='Shuffle')

    parser.add_argument('-e', '--echo',
                        nargs="*",
                        type=str,
                        help='treat each ARG as an input line')
    
    parser.add_argument('-i',
                        '--input-range',
                        type=str,
                        help='treat each number LO through HI as an input line')

    parser.add_argument('-n',
                        '--head-count',
                        type=int,
                        help='output at most COUNT lines')
    
    parser.add_argument('-r',
                        '--repeat',
                        action='store_true',
                        help='output lines can be repeated')

    parser.add_argument('file',
                        nargs='?',
                        default='-',
                        help="input lines")
    
    args = parser.parse_args()
    lines = []
    
    if args.echo or args.input_range:
        if args.echo:
            lines = args.echo
        else:
            try:
                ranges = (args.input_range.split('-'))
               # print(ranges)
                match ranges:
                    case[x,y]:
                        start = int(x)
                        end = int(y)
                        lines = list(range(start,end+1))
                
                #start, end = args.input_range.split('-')
                #lines = list(range(int(start),int(end)+1))
            except:
                print("shuf: invalid input range: "+args.input_range)
               
            
    elif not args.file or args.file == '-':
        while True:
            try:
                lines.append(input())
            except EOFError:
                break
    else:
        f = open(args.file)
        lines = f.read().split('\n')
        lines.pop()
       # for line in lines:
           # print(line)

    #start = 1
    #end = len(lines)
    maxcount = len(lines)
    
    mc = False
    if args.head_count:
        maxcount = args.head_count
        mc = True

    if(args.repeat):
        count = 0
        while count<maxcount:
            output = shuffle(lines,args.repeat, maxcount, mc)
            for line in output:
                print(line)
                if(mc):
                    count += 1
                    if(count>mc):
                        break
            
    else:
        output = shuffle(lines,args.repeat, maxcount, mc)
        for i in range(len(output)):
            print(output[i])
if __name__ == "__main__":
    main()
