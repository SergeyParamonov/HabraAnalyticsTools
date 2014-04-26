#!/usr/bin/env python 

"""High level wrapper for functionality of venn.py
   Makes sure data is downloaded and calls draw.py to visualize
"""

from __future__ import print_function
from draw import draw
from analyzeHubs import HubAnalyzer
import os.path
class Reader:
  @staticmethod
  def read_list_of_users(filename):
    user_file = open(filename, "r")
    users     = user_file.readlines()
    users     = [user.strip() for user in users]
    return users


  @staticmethod
  def check_and_download(hubname,company_flag):
    if hubname is None:
      return None
    hubs  = HubAnalyzer.get_hub_names()
    companies = HubAnalyzer.get_company_names()
    if not company_flag:
      if hubname in hubs and hubname in companies:
        print("Name is ambiguous, there is a company and a hub with this name; assuming hub by default.")
        prefix = "hubs/"
      elif hubname in hubs:
        prefix = "hubs/"
      elif hubname in companies:
        prefix = "companies/"
      else:
        print("There is no name record for *" + hubname + "*, assuming it is a hub, not a company.")
    else:
      prefix = "companies/"
    datafile = "data/"+prefix+hubname
    if os.path.isfile(datafile):
      return Reader.read_list_of_users(datafile)
    else:
      print("Data for *" +hubname+ "* is not in the local dataset, downloading it now... ")
      HubAnalyzer.report_downloading_progress = True
      if company_flag:
        HubAnalyzer.getCompanyUsers(hubname)
      else:
        HubAnalyzer.getUsers(hubname)
      return Reader.read_list_of_users(datafile)

  @staticmethod
  def removehubdata(hubname):
    datafile = "data/hubs/"+hubname
    if os.path.isfile(datafile):
      os.remove(datafile)
    else:
      raise Exception("The data file does not exist")

  @staticmethod
  def removehub(hubname_to_delete):
    is_deleted = False
    hubname_to_delete = hubname_to_delete.strip()
    hubs = open("data/meta/hubs_name_link.csv","r")
    lines = hubs.readlines()
    hubs.close()
    hubs = open("data/meta/hubs_name_link.csv","w")
    for line in lines:
      hubname = line.split(',')[1].strip()
      if hubname != hubname_to_delete:
        print(line, file=hubs, end="")
      else:
        is_deleted = True
    hubs.close()
    if not is_deleted:
      raise Exception("Link is not found among available hubs")

  @staticmethod
  def addhub(hubname, description):
    hubs = open("data/meta/hubs_name_link.csv","a")
    print(description+"," + hubname , file=hubs)
    hubs.close()

  @staticmethod
  def updatehub(hubname):
    print("Updating: " + hubname)
    HubAnalyzer.report_downloading_progress = True
    HubAnalyzer.enforce_download_in_presence_of_data = True
    HubAnalyzer.getUsers(hubname)
    HubAnalyzer.enforce_download_in_presence_of_data = False

  @staticmethod
  def download_company_data(name):
    HubAnalyzer.report_downloading_progress = True
    HubAnalyzer.enforce_download_in_presence_of_data = True
    try:
      HubAnalyzer.getCompanyUsers(name)
    except Exception as e:
      print(str(e))
      return

  @staticmethod
  def print_hubs():
    print("companies")
    company_dict = HubAnalyzer.generate_company_dictionary()
    for name, descr in company_dict.items():
      print(name + " <-->  " + descr + "(company)")
    print("hubs")
    hub_dict = HubAnalyzer.generate_hub_dictionary()
    for name, descr in hub_dict.items():
      print(name + " <-->  " + descr)
