#!/usr/bin/env python 

""" Console interface for Venn diagrams  
    Parses arguments and calls the functions from src/reader.py
"""
import sys
sys.path.append("./src")
from reader import Reader
from analyzeHubs import HubAnalyzer
import argparse
from argparse import RawTextHelpFormatter
from draw import draw, print_stats
from header import print_header

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--hubs', help='Print the list of available hubs from habrahabr',action='store_true', default=False)
  drawgroup = parser.add_argument_group(title='drawing commands')  
  drawgroup.add_argument('--draw','-d', help='Make Venn diagram for the 1st and 2nd hubs (must be given) and optinally the 3rd', nargs="+", metavar=('hubname'))
  drawgroup.add_argument('--stats', '-t', help='Must be used with --draw, print statistics about hubs intersection ', action='store_true', default=False)
  parser.add_argument('--onlystats',"-o", help='Print statistics (at least 2 hubs must be given) and exit', nargs="+", metavar=('hubname'))
  parser.add_argument('--removehubdata', help='Remove the data for the selected hub', nargs=1, metavar=('hubname'))
  parser.add_argument('--removehub', help='Remove the hub\'s name', nargs=1, metavar=('hubname'))
  parser.add_argument('--addhub', help='Add a link for a hub', nargs=2, metavar=('hubname', 'description'))
  parser.add_argument('--updatehub', help='Update user list of a hub', nargs=1, metavar=('hubname'))
  parser.add_argument('--silentheader',"-s", help='Do not show the header about pizza and kittens',  action='store_true', default=False)
  parser.add_argument('--downloadcompany','-c', help='Download the data given company name e.g. yandex', nargs=1, metavar=("company_name")) 
  parser.add_argument('--company', help='If a name is ambiguous, like yandex: it is a hub and a company, then enforce company interpretation', nargs='+', metavar=("argument_index"), type=int, choices=range(1,4)) 
  args = vars(parser.parse_args())

  if len(sys.argv)==1:
    print_header()
    parser.print_help()
    sys.exit(1)
   
  if args['silentheader']:
    pass
  else:
    print_header()

  if args['downloadcompany']:
    Reader.download_company_data(args['downloadcompany'][0])
    print("Data has been downloaded. Now it can be used as a regular hub name")
    exit()

  if args['updatehub']:
    try:
      hubname = args['updatehub'][0]
      Reader.updatehub(hubname)
      print(hubname+ " has been updated. Done.")
      exit(0)
    except Exception as e:
      print(e)

  if args['addhub']: 
    try:
      hubname     = args['addhub'][0]
      description = args['addhub'][1]
      Reader.addhub(hubname, description)
      print("Hub name and link have been added, done. ")
      exit(0)
    except Exception as e:
      print(e)
      print(str(e))

  if args['removehub']:
    try:
      Reader.removehub(args['removehub'][0])
      print("Link deletion: done.")
      exit(0)
    except Exception as e:
      print(str(e))

  if args['removehubdata']:
    try:
      Reader.removehubdata(args['removehubdata'][0])
      print("Data deletion: done.")
      exit(0)
    except Exception as e:
      print(str(e))

  if args['hubs']:
    Reader.print_hubs()

  if args['onlystats']:
    if len(args['onlystats']) >= 2:
      hub1 = args['onlystats'][0].strip()
      hub2 = args['onlystats'][1].strip()
      if len(args['onlystats']) > 2:
        hub3 = args['onlystats'][2]
      else:
        hub3 = None
      try:
        company_flag1 = False
        company_flag2 = False
        company_flag3 = False
        if args['company']:
          for i in args['company']: 
            if i == 1:
              company_flag1 = True  
            if i == 2:
              company_flag2 = True  
            if i == 3:
              company_flag3 = True  
        set1 = Reader.check_and_download(hub1,company_flag1)
        set2 = Reader.check_and_download(hub2,company_flag2)
        set3 = Reader.check_and_download(hub3,company_flag3)
        print_stats(set1,set2,set3,HubAnalyzer.convert_label(hub1, company_flag1),HubAnalyzer.convert_label(hub2, company_flag2), HubAnalyzer.convert_label(hub3, company_flag3))
      except Exception as e:
        print(str(e))
    else:
      print("To get statistics at least two hubs must be specified")

  if args['draw']: 
    if len(args['draw']) >= 2:
      hub1 = args['draw'][0].strip()
      hub2 = args['draw'][1].strip()
      if len(args['draw']) > 2:
        hub3 = args['draw'][2]
      else:
        hub3 = None
      try:
        company_flag1 = False
        company_flag2 = False
        company_flag3 = False
        if args['company']:
          for i in args['company']: 
            if i == 1:
              company_flag1 = True  
            if i == 2:
              company_flag2 = True  
            if i == 3:
              company_flag3 = True  
        set1 = Reader.check_and_download(hub1,company_flag1)
        set2 = Reader.check_and_download(hub2,company_flag2)
        set3 = Reader.check_and_download(hub3,company_flag3)
        if args['stats']:
          print_stats(set1,set2,set3,HubAnalyzer.convert_label(hub1, company_flag1),HubAnalyzer.convert_label(hub2, company_flag2), HubAnalyzer.convert_label(hub3, company_flag3))
        draw(set1,set2,set3,HubAnalyzer.convert_label(hub1, company_flag1),HubAnalyzer.convert_label(hub2, company_flag2), HubAnalyzer.convert_label(hub3, company_flag3))
      except Exception as e:
        print(str(e))
    else:
      print("To draw a diagram at least two hubs must be specified")
  if not args['draw'] and args['stats']:
    print('--stats is used only with draw, use --onlystats hub1 hub2 [hub3] instead')
  #it's ok to have only two hubs


