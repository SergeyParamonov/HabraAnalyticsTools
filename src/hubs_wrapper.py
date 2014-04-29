from reader import Reader
import glob
import operator
import pylab as pl


def jaccard_index(set1,set2):
  set1    = set(set1)
  set2    = set(set2)
  intrsct = float(len(set1.intersection(set2)))
  union   = float(len(set1.union(set2)))
  jaccard_index = intrsct/union
  return round(jaccard_index,3)

#inclusion of set1 into ses2
#not symmetric!!!
def inclusion(set1,set2):
  set1    = set(set1)
  set2    = set(set2)
  intrsct = set1.intersection(set2)
  inclusion = len(intrsct)/float(len(set1))
  return int(100*inclusion)



def compute(hubname,isCompany,fun_name):
  hub_readers     = Reader.check_and_download(hubname, isCompany) 
  hubs_data_dir   = 'data/hubs/'
  tocut           = len(hubs_data_dir)
  hubs            = glob.glob(hubs_data_dir+'*')
  similarity_dict = dict()
  for hub_file in hubs:
    readers = Reader.read_list_of_users(hub_file)
    hub     = hub_file[tocut:]
    #skip itself
    if hub == hubname:
      continue
    if fun_name == "similarity":
      similarity_dict[hub] = jaccard_index(hub_readers,readers)
    if fun_name == "inclusion":
      similarity_dict[hub] = inclusion(hub_readers,readers)
  return similarity_dict


def display_preferences(hubname,isCompany,fun_name,flag,flagopts):
  ylabel            = fun_name
  values = compute(hubname,isCompany,fun_name)
  sorted_values = sorted(values.iteritems(), key=operator.itemgetter(1), reverse=True)
  hubs     = map(lambda x: x[0],sorted_values) 
  y_values = map(lambda x: x[1],sorted_values) 
  if flag is None:
    MAX_HUBS  = 50
    #exclude itself
    hubs     = hubs[:MAX_HUBS]
    y_values = y_values[:MAX_HUBS]
    fig      = pl.figure()
    ax       = pl.subplot(111)
    hub_range = range(0,MAX_HUBS)
    ax.bar(hub_range, y_values)
   # re-write and also show % of intersection, like
   # 50% of space also read this...
    pl.title(hubname + " : " + fun_name, fontsize=22)
    pl.xticks(hub_range, hubs,rotation=80)
    pl.ylabel(ylabel, fontsize=20)
    pl.show()
  elif flag == "max":
    max_hubs = int(flagopts)
    hubs     = hubs[:max_hubs+1]
    y_values = y_values[:max_hubs+1]
    for hub, value in zip(hubs, y_values):
      print("hub:"+hub + " function:" + fun_name + " value:" + str(value))
  elif flag == "min":
    min_hubs = int(flagopts)
    inverse_sorted_values = sorted(values.iteritems(), key=operator.itemgetter(1))
    hubs     = map(lambda x: x[0],inverse_sorted_values)[:min_hubs]
    y_values = map(lambda x: x[1],inverse_sorted_values)[:min_hubs]
    for hub, value in zip(hubs, y_values):
      print("hub:"+hub + " function:" + fun_name + " value:" + str(value))
