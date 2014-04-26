#!/usr/bin/env python 

""" Downloads and parses list of hubs and companies
    After executation and making the list, presence is not required
    This file is NOT called by venn.py or any other script
    For dev/debugging only
"""

from __future__ import print_function
import urllib3
from bs4 import BeautifulSoup

class HubsParser:

  @staticmethod
  def parse(url, output_file, divclass, record_html):
    http = urllib3.PoolManager()
    try:
      response = http.request('GET', url)
    except urllib3.exceptions.HTTPError as err:
      if err.code == 404:
        return None
      else:
        raise Exception("Error: cannot parse the page!")
    html    = response.data.decode("utf-8")
    soup    = BeautifulSoup(html)
    hubsRow = soup.find_all(class_=divclass)
    hubs    = []
    for hubRow in hubsRow:
      title    = hubRow.find(class_=record_html).a.text
      link     = hubRow.find(class_=record_html).a['href']
      print(title.encode('utf-8'), file=output_file, end="")
      print(",", file=output_file, end="")
      print(link, file=output_file)

  @staticmethod
  def generateHubDictionary(filename):
    output_file = open(filename, "w")
    for i in range(1,10):
      url = "http://habrahabr.ru/hubs/page{}/".format(i)
      HubsParser.parse(url,output_file,"hub ", "title")
  
  @staticmethod
  def generateCompanyDictionary(filename):
    last_page = 71
    output_file = open(filename, "w")
    for i in range(1,last_page+1):
      url = "http://habrahabr.ru/companies/page{}/".format(i)
      HubsParser.parse(url,output_file, "company ", "name")
    output_file.close()
   
  @staticmethod
  def format_company_links(filename):
    lines = open(filename, "r").readlines()   
    formatted = open(filename, "w")
    tocut = len("/company/")
    for line in lines:
      name = line.split(',')[0]
      link = line.split(',')[1]
      link = link[tocut:].strip().strip('/')
      print(name, file=formatted, end="")
      print(",", file=formatted, end="")
      print(link, file=formatted)
