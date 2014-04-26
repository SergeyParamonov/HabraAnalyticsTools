#!/usr/bin/env python 

""" Low level functions to parse pages with users
    Transform names into links and back     
"""
from __future__ import print_function
from parseHubs import HubsParser 
import urllib3
from bs4 import BeautifulSoup
import re
import time
import os,os.path
from progress.bar import Bar
import sys

class HubAnalyzer:
  logfile = "data/meta/parsing_log1.txt"
  hubnames = None
  report_downloading_progress = False
  enforce_download_in_presence_of_data = False
  



  @staticmethod
  def getLastPageNumber(url):
    url          = url.strip('/')
    suffix       = "/subscribers/rating/"
    userlist_url = url + suffix
    http       = urllib3.PoolManager()
    response   = http.request('GET', userlist_url)
    html       = response.data
    soup       = BeautifulSoup(html)
    nav_pages   = soup.find(id="nav-pages")
    if not nav_pages:
      return 1
    no_index   = nav_pages.find("noindex")
    if no_index:
      last_page  = no_index.a['href'] 
      num_row    = re.findall(r"/subscribers/rating/page\d+",last_page)[0]
      num        = re.findall(r"\d+", num_row)[0]
    else:
      raw_nums = re.findall("/subscribers/rating/page\d",html)
      nums = [int(num[-1]) for num in raw_nums]
      num = max(nums)
    return num

  
  @staticmethod
  def getCompanyLastPage(name):
    url = "http://habrahabr.ru/company/"+name+"/fans/all/rating/"
    http       = urllib3.PoolManager()
    try:
      response   = http.request('GET', url)
    except Exception as e:
      print(str(e))
      return
    html       = response.data.decode('utf-8')
    soup       = BeautifulSoup(html)
    nav_pages   = soup.find(id="nav-pages")
    if not nav_pages:
      return 1
    no_index   = nav_pages.find("noindex")
    if no_index:
      last_page  = no_index.a['href'] 
      num_row    = re.findall(r"/fans/all/rating/page\d+",last_page)[0]
      num        = int(re.findall(r"\d+", num_row)[0])
    else:
      raw_nums = re.findall("/fans/all/rating/page\d",html)
      nums = [int(num[-1]) for num in raw_nums]
      if nums:
        num = max(nums)
      else:
        raise Exception("Link is broken")
    return num
   
  @staticmethod
  def getCompanyUsers(name):
    url      = "http://habrahabr.ru/company/"+name+"/fans/all/rating/"
    log = open(HubAnalyzer.logfile, "a")
    print("URL: " + url + " ----------------- ", file=log)
    print(time.strftime("%H:%M:%S"), file=log)
    log.flush()
    datapath  = "data/companies/"+name
    if os.path.isfile(datapath) and not HubAnalyzer.enforce_download_in_presence_of_data: 
      print("data is already here, abort this url",file=log)
      return None
    try:
      last_page = HubAnalyzer.getCompanyLastPage(name)
    except Exception as err:
      print("URL is broken, abort the url", file=log)
      print(str(e), file=log)
      log.flush()
      print("Cannot analyze the page, please, check the url below: \n" + url)
      return
    datafile  = open(datapath,"w")
    http = urllib3.PoolManager()
    if HubAnalyzer.report_downloading_progress:
      bar = Bar('Downloading: '+name, max=last_page, suffix='%(percent)d%%')
    for i in range(1,last_page+1):
      user_page  = url +"page" +str(i)
      print(user_page, file=log)
      log.flush()
      try:
        response = http.request('GET', user_page)
      except Exception as e:
        print(str(e),file=log)
        print(str(e))
        log.flush()
        datafile.close()
        os.remove(datapath)
        return 
      html      = response.data
      soup      = BeautifulSoup(html)
      usersRow  = soup.find_all(class_="user ")
      for userRow in usersRow:
        username = userRow.find(class_="username").text
        print(username, file=datafile)
      datafile.flush()
      if HubAnalyzer.report_downloading_progress:
        bar.next() 
    #finalize and close everything
    if HubAnalyzer.report_downloading_progress:
      bar.finish()
    datafile.close()
    log.close()


  @staticmethod
  def getUsers(hubname):
    log = open(HubAnalyzer.logfile, "a")
    print("hub: " + hubname  + " ----------------- ", file=log)
    print(time.strftime("%H:%M:%S"), file=log)
    #clean the file to write users to
    url = HubAnalyzer.hubname2link(hubname)
    output_filename = "data/hubs/"+hubname 
    #if data is here, do nothing
    if os.path.isfile(output_filename) and not HubAnalyzer.enforce_download_in_presence_of_data: 
      print("data is already here, abort this url",file=log)
      return None
    output_file  = open(output_filename, "w")
    try:
      last_page_num = int(HubAnalyzer.getLastPageNumber(url))
    except Exception as err:
      print("URL is broken, abort the url", file=log)
      log.flush()
      os.remove(output_filename)
      raise Exception("Cannot analyze the page, please, check the url below: \n" + url)
    #get connection to habrahabr-hub
    suffix       = "/subscribers/rating/page"
    userlist_url = url + suffix
    http = urllib3.PoolManager()
    if HubAnalyzer.report_downloading_progress:
      HubAnalyzer.get_hub_description(hubname)
      bar = Bar('Downloading: '+ hubname, max=last_page_num, suffix='%(percent)d%%')
    for i in range(1,last_page_num+1):
      user_page  = userlist_url+str(i)
      print(user_page, file=log)
      log.flush()
      try:
        response = http.request('GET', user_page)
      except urllib3.exceptions.HTTPError as err:
        if err.code == 404:
          print(user_page + " !! 404 !!", file=log)
          log.flush()
          output_file.close()
          os.remove(output_filename)
          raise("Hub is not found, please, check the url")
        else:
          print(user_page + " PARSING ERROR ", file=log)
          log.flush()
          output_file.close()
          os.remove(output_filename)
          raise Exception("Error: cannot parse the page!")
      html      = response.data
      soup      = BeautifulSoup(html)
      usersRow  = soup.find_all(class_="user ")
      for userRow in usersRow:
        username = userRow.find(class_="username").text
        print(username, file=output_file)
      output_file.flush()
      if HubAnalyzer.report_downloading_progress:
        bar.next() 
    #finalize and close everything
    if HubAnalyzer.report_downloading_progress:
      bar.finish()
    output_file.close()
    log.close()

  @staticmethod
  def generate_hub_dictionary():
    hub_dict = dict()
    csv_hubs = open("data/meta/hubs_name_link.csv","r")
    for line in csv_hubs.readlines():
      name    = line.split(",")[0].strip()
      hubname = line.split(",")[1].strip()
      hub_dict[hubname] = name
    return hub_dict

  @staticmethod
  def generate_company_dictionary():
    company_dict = dict()
    csv_companies = open("data/meta/companies_name_link.csv","r")
    for line in csv_companies.readlines():
      name    = line.split(",")[0].strip()
      company = line.split(",")[1].strip()
      company_dict[company] = name
    return company_dict
   
  

  @staticmethod
  def hubname2link(hubname):
    prefix = "http://habrahabr.ru/hub/"
    url    = prefix + hubname.strip()
    return url

  @staticmethod
  def get_hub_description(hubname):
    if HubAnalyzer.hubnames is None:
      HubAnalyzer.hubnames = HubAnalyzer.generate_hub_dictionary()   
    return HubAnalyzer.hubnames[hubname]

  @staticmethod
  def get_hub_links():
    if HubAnalyzer.hubnames is None:
      HubAnalyzer.hubnames = HubAnalyzer.generate_hub_dictionary()   
    return [HubAnalyzer.hubname2link(hubnames) for hubnames in HubAnalyzer.hubnames.keys()]

  @staticmethod
  def get_hub_names():
    if HubAnalyzer.hubnames is None:
      HubAnalyzer.hubnames = HubAnalyzer.generate_hub_dictionary()   
    return HubAnalyzer.hubnames.keys()


  @staticmethod
  def get_company_names():
   lines = open("data/meta/companies_name_link.csv","r").readlines()
   names = [line.split(',')[1].strip() for line in  lines]
   return names
  
  @staticmethod
  def convert_label(name, company_flag):
    if company_flag:
      return name + "(company)"
    return name


if __name__ == "__main__":
  reload(sys)
  sys.setdefaultencoding("utf-8")
  HubAnalyzer.report_downloading_progress = True
  for hub in HubAnalyzer.get_hub_names():
    print(hub)
    HubAnalyzer.getUsers(hub)
 #for name in HubAnalyzer.getCompanyNames():
 #  print(name)
 #  HubAnalyzer.getCompanyUsers(name)
