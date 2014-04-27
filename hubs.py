#!/usr/bin/env python 

""" Console interface for hub operations
    Parses arguments and calls right functions from src/
"""

#regular import 
import sys
sys.path.append("./src")
import argparse
#my functions and classes
from header import print_header_hubs
from reader import Reader
from hubs_wrapper import *



def main():
  SUCCESS = 0
  #arguments declaration
  parser = argparse.ArgumentParser()
  parser.add_argument('--omitheader','-m', help='Do not show the header about pizza and kittens',  action='store_true', default=False)
  parser.add_argument('--hublist', help='Shows all available hubs',  action='store_true', default=False)
  parser.add_argument('--similar','-s', help='Displays similar hubs as a histogram', nargs=1, metavar=("hub_name"))
  parser.add_argument('--alsoread','-a', help='Displays what else people read from this hub as a histogram', nargs=1, metavar=("hub_name"))
  parser.add_argument('--max', help='Print several hubs that maximize the score function e.g. --similar or --alsoread', nargs=1, metavar=("number_of_hubs"), type=int) 
  parser.add_argument('--min', help='Print several hubs that minimize the score function e.g. --similar or --alsoread', nargs=1, metavar=("number_of_hubs"), type=int)
  parser.add_argument('--company', help='If a name is ambiguous, like yandex: it is a hub and a company, then enforce company interpretation', action="store_true", default=False)

  args = vars(parser.parse_args())

  #check flags and delegate functions to src/reader.py and src/hubs_wrapper.py
  if len(sys.argv)==1:
    print_header_hubs()
    parser.print_help()
    return SUCCESS

  if args['omitheader']:
    pass
  else:
    print_header_hubs()

  if args['hublist']:
    Reader.print_hubs()
    return SUCCESS

  isCompany = False
  if args['company']:
    isCompany = True

  flag = None
  flagopts = None
  if args['max']:
    flag = "max"
    flagopts = args['max'][0]

  if args['min']:
    flag = "min"
    flagopts = args['min'][0]

  if args['similar']:
    hub_name = args['similar'][0]
    display_preferences(hub_name, isCompany, "similarity", flag, flagopts)
    return SUCCESS

  if args['alsoread']:
    hub_name = args['alsoread'][0]
    display_preferences(hub_name, isCompany, "inclusion", flag, flagopts)
    return SUCCESS



if __name__ == "__main__":
  main()
