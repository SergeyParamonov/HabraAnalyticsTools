#!/usr/bin/env python 

""" Visualization function and basic statistics """
from matplotlib_venn import venn2, venn3
import matplotlib.pyplot as plt
from matplotlib.pyplot import gca
from analyzeHubs import HubAnalyzer
import numpy as np

def percent_of(set1,set2):
  dif = set1 & set2
  return str(int(100*len(dif)/len(set1)))

def print_stats(set1, set2, set3, label1, label2, label3):
  set1 = set(set1)
  set2 = set(set2)
  print(percent_of(set1,set2)+"% of " +label1 +"  intersects with " +label2)
  print(percent_of(set2,set1)+"% of " +label2 +"  intersects with " +label1)
  if label3 is None:
    print("Overall number of unique users: " + str((len(set1.union(set2)))))
    return
  set3 = set(set3)
  print(percent_of(set1,set3)+"% of " +label1 +"  intersects with " +label3)
  print(percent_of(set3,set1)+"% of " +label3 +"  intersects with " +label1)
  print(percent_of(set3,set2)+"% of " +label3 +"  intersects with " +label2)
  print(percent_of(set2,set3)+"% of " +label2 +"  intersects with " +label3)
  print("Overall number of unique users: " + str((len(set1.union(set2.union(set3))))))

def draw(set1, set2, set3, label1, label2, label3):
  set1 = set(set1)
  set2 = set(set2)
  if label3:
    set3 = set(set3)
    v = venn3([set1,set2, set3], (label1, label2, label3))
    plt.title('Venn diagram for hubs: ' + label1 + "," + label2 +"," + label3, fontsize=20)
  else:
    v = venn2([set1, set2], (label1, label2))
    plt.title('Venn diagram for hubs:' + label1 + "," + label2, fontsize=20)
#   if v.get_label_by_id('110'):
#     plt.annotate(percent_of(set1,set2)+"% of " +label1 , xy=v.get_label_by_id('110').get_position() - np.array([0.15, 0.10]))
#     plt.annotate(percent_of(set2,set1)+"% of " +label2 , xy=v.get_label_by_id('110').get_position() - np.array([0.15, 0.15]))
  if v.get_patch_by_id('100'):
    v.get_patch_by_id('100').set_color("blue")
  if v.get_patch_by_id('010'):
    v.get_patch_by_id('010').set_color("red")
  if v.get_patch_by_id('110'):
    v.get_patch_by_id('110').set_color("purple")
  if label3 and v.get_patch_by_id('001'):
    v.get_patch_by_id('001').set_color("green") 
    if v.get_patch_by_id('111'):
      v.get_patch_by_id('111').set_color("black") 
  gca().set_axis_bgcolor('white')
  gca().set_axis_on()
  plt.show()
