# Schedualing simulator
# COMP3430 A3
# @author Pylypenko Maksym

import random
import numpy as np
import sys

# config
ROUNDS = 10
SCHEDULER = 0 # rb(0), prb(1), sjf(2), srjb(3)
TIME_SLICE = 5 # >0 
RANDOM_SAMPLE = False # gen random sample each time
PRINT_ROUND = True
FILE = "processes" # ignored when using random sample

if len(sys.argv) == 2:
	SCHEDULER = sys.argv[1]
	SCHEDULER = int(SCHEDULER)
	print("Selected:", SCHEDULER)
else:
	print("Using default scheduler\n")


# process structure
class Process(object):
  # info
  name = ""
  type = 0  # short, medium, long, io
  priority = 0  # high, medium, low
  length = 0  # any?
  oddsIO = 0.0  # 0-100%

  # state
  remaining = 0 # work left
  waiting = 0

  # initializer: p = Process(name, type, priority, length, oddsIO)
  def __init__(self, name, type, priority, length, oddsIO):
    self.name = name
    self.type = int(type)
    self.priority = int(priority)
    self.length = int(length)
    self.oddsIO = float(oddsIO) / 100
    self.remaining = float(self.length)

  # do the work 
  def do(self, slice_work):
    rem = self.remaining
    if rem > 0:
      if slice_work >= rem:
        self.remaining = 0 
        return rem  # do what is needed, not more 
      else:
        self.remaining -= slice_work
        return slice_work # do as much as we can...
    return 0  # we are done

  def isDone(self):
    # assert(remaining>-1)
    return self.remaining<=0


# main work is done here
def scheduler(q):
  finished = []

  while len(q) != 0:

    if SCHEDULER == 0:
      task = q.pop(0)
    elif SCHEDULER == 1:
      task = q.pop(smallestPriority(q))
    else:
      task = q.pop(smallestN(q))      
    
   
    work = checkIO(task.oddsIO)  # might need to cut work
    work = task.do(work)    

    if not task.isDone():  # finish later
      if SCHEDULER < 2: # decrease priority 
        q.append(task) # add to the right       
      else: # do not deacrease priority of sjb & srjf 
        q.insert(0,task)  # add to the left 
      
    else:  # task is done
      task.waiting += work # wait outside Q
      finished.append(task)       
      # print(task.name, "wait =",task.waiting)

    for i in q:
      i.waiting += work  # everybody in Q waits
      
  return finished


# simulates interrupts
def checkIO(odds):
  r = random.randint(0, 100)
  if r / 100 < odds:
    s = random.randint(0, TIME_SLICE)
    #print(s / TIME_SLICE)
    return s
  return TIME_SLICE  #full slice


# used to pop the smallest priority item
def smallestPriority(q):  
  currSmallest = 0
  while currSmallest < 4:
    i = 0
    for task in q:
      if task.priority == currSmallest:
        return i
      else:
        i += 1
    currSmallest += 1

  return 0 


# used to pop the sjf & srjf
def smallestN(q):
  val = sys.maxsize
  ind = 0
  i = 0
  for task in q:
    if SCHEDULER == 2:
      curr = task.length
    else:            
      curr = task.remaining     
    if curr < val: # priority is not decreased (smallest left)
      val = curr
      ind = i
    i += 1
  return ind


# summarize 1 round
def build_summary(finished):
  countP = np.array([0, 0, 0])
  countT = np.array([0, 0, 0, 0])
  waitP = np.array([0, 0, 0])
  waitT = np.array([0, 0, 0, 0])

  for i in finished:
    j = i.priority
    countP[j] += 1
    waitP[j] += i.waiting 

  for i in finished:
    j = i.type
    countT[j] += 1
    waitT[j] += i.waiting

  # print(countT)
  # print(waitT)
  
  # can crash if /0
  averP = waitP / countP
  averT = waitT / countT

  # check
  assert (np.sum(countP) == np.sum(countT))
  # print("Total wait:", np.sum(waitP))

  if PRINT_ROUND:
    print_round(averP,averT)

  return averP,averT


# sexy analysis 
def print_round(averP,averT):
  try:
    print("Average run time per priority:")
    for i in range(len(averP)):
      print("Priority %d average run time: %d" % (i, averP[i]))
    print("Average run time per type:")
    for i in range(len(averT)):
      print("Type %d average run time: %d" % (i, averT[i]))    
  except ValueError:
    print("Insufficient data. Try a different sample of tasks")


def print_summary(averP,averT,stdP,stdT):  
  try:
    print("\n-------------------------------------------")
    print("\nStatistical Analysis for ", end='')
    print_scheduler()
    print("\nMean run time per priority:")
    for i in range(len(averP)):
      print("Priority %d mean run time: %d" % (i, averP[i]))
    print("\nMean run time per type:")
    for i in range(len(averT)):
      print("Type %d mean run time: %d" % (i, averT[i]))  

    print("\nStandart deviation per priority:")
    for i in range(len(averP)):
      print("Priority %d standart deviation: %f" % (i, stdP[i]))
    print("\nStandart deviation per type:")
    for i in range(len(averT)):
      print("Type %d standart deviation: %f" % (i, stdT[i]))   
  except ValueError:
    print("Insufficient data. Try a different sample of tasks")


def print_scheduler():
  if (SCHEDULER == 0):
    print("Pure Round-Robin")
  elif (SCHEDULER == 1):
    print("Priority Round-Robin")
  elif (SCHEDULER == 2):
    print("Shortest job first")
  elif (SCHEDULER == 3):
    print("Shortest remaining job first")
  print("Rounds =",ROUNDS)


# taken from the processmaker.py (provided in the A3)
def genData(file):  
  names = ["short_thread_", "med_thread_", "long_thread_", "io_thread_", ]
  count = [0, 0, 0, 0]
  rand_io_range = [ (10,50), (20, 60), (30, 60), (50,100)]
  rand_time_range = [  (5, 20), (20, 50),  (50, 1000), (10, 1000)]

  with open(file, 'w') as f:
      for _ in range(100):
          t = random.randint(0, 3)
          # thread_name thread_type priority thread_length odds_of_IO
          f.write("%s%d %d %d %d %d\n"%(
              names[t],
              count[t],
              t,
              random.randint(0,2),
              random.randint(rand_time_range[t][0], rand_time_range[t][1]),
              random.randint(rand_io_range[t][0], rand_io_range[t][1])
          ))
          count[t] += 1  


# Main routine starts here...

if RANDOM_SAMPLE:
  FILE = "random"
  genData(FILE) 

# for standart deviation 
summary = [[],[]]

print_scheduler()
for rounds in range(ROUNDS):
  print("\nRound ",rounds+1)
  result, queue = [],[] 
 
  with open(FILE, "r") as f:
    for line in f:
      (name, type, priority, length, oddsIO) = line.split(' ')
      queue.append(Process(name, type, priority, length, oddsIO))
  result = scheduler(queue)

  if len(result) > 0:
    (p,t)=build_summary(result)
    summary[0].append(p)
    summary[1].append(t)


# FEELS GOOD MAN
meanP = np.mean(summary[0], axis=0)
meanT = np.mean(summary[1], axis=0)

stdP = np.std(summary[0], axis=0)
stdT = np.std(summary[1], axis=0)

print_summary(meanP,meanT,stdP,stdT)
