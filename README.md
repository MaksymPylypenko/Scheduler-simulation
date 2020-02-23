# SCHEDULER SIMULATION, A3 COMP3430

* author:     Pylypenko Maksym 7802672
* language:   Python 3.6.1
* date:       2018-06-30

## Configuration section is in the top of main.py and contains the folling parameters:

* ROUNDS - the number of rounds to complete 
  - default is 10 

* TIME SLICE - the int value of a maximum work at a time
  - default is 5

* SCHEDULER - type of scheduler
  0. Pure Round Robin
  1. Priority Round Robin
  2. Shortest Job First
  3. Shortest Remaining Job First

* RANDOM_SAMPLE
  - True, a new sample will be generated every run
  - False, will use processes (default file) 

* PRINT_ROUND 
  - True, print statistics for every round
  - False, only the summary of all rounds is printed

* FILE - if you want to test a specific sample 
  - default is "processes" 
  - ignored if RANDOM_SAMPLE is set to TRUE

## To run on linux machine (always default scheduler):
> make 

## To run on linux machine (choose custom scheduler):
> python3 main.py <schedulerType>

## Analysis 

-------------------------------------------

Statistical Analysis for Pure Round-Robin
Rounds = 10

Mean run time per priority:
Priority 0 mean run time: 9969.518750
Priority 1 mean run time: 8099.451351
Priority 2 mean run time: 11105.703226

Mean run time per type:
Type 0 mean run time: 910.604348
Type 1 mean run time: 2457.400000
Type 2 mean run time: 16644.537037
Type 3 mean run time: 17864.262500

Standart deviation per priority:
Priority 0 standart deviation: 73.487558
Priority 1 standart deviation: 58.559041
Priority 2 standart deviation: 59.830428

Standart deviation per type:
Type 0 standart deviation: 45.442714
Type 1 standart deviation: 77.452377
Type 2 standart deviation: 65.443315
Type 3 standart deviation: 96.288077

-------------------------------------------

Statistical Analysis for Priority Round-Robin
Rounds = 10

Mean run time per priority:
Priority 0 mean run time: 3435.493750
Priority 1 mean run time: 11184.102703
Priority 2 mean run time: 20074.309677

Mean run time per type:
Type 0 mean run time: 7894.226087
Type 1 mean run time: 9227.069231
Type 2 mean run time: 12943.907407
Type 3 mean run time: 15628.945833

Standart deviation per priority:
Priority 0 standart deviation: 24.121502
Priority 1 standart deviation: 13.621009
Priority 2 standart deviation: 16.829025

Standart deviation per type:
Type 0 standart deviation: 10.491130
Type 1 standart deviation: 17.274488
Type 2 standart deviation: 28.334821
Type 3 standart deviation: 27.862149
   

## Are the two distributions generated statistically significantly different?

Yes. 

* The mean run time for priorities:
  - Priority Round-Robin: is in ascending order and has big gaps 
  - Pure Round-Robin: no particular order, small gaps
* The mean run time for types:
  - Priority Round-Robin: is in ascending order and has medium gaps 
  - Pure Round-Robin: is in ascending order and has big gaps 

* The standart deviation for priorities:
  - Priority Round-Robin: slight fluctuations, all priorities tend to run in a predefined way. 
  - Pure Round-Robin: aggressive fluctuations on some (0,2) priorities were spotted 

* The standart deviation for types:
  - Priority Round-Robin: slight fluctuations, all types tend to run in a predefined way. 
  - Pure Round-Robin: aggressive fluctuations on some (2,3) types were spotted 

## How did the two algorithms treat the queue differently, how is that reflected in the data?

Pure Round-Robin: If a process can't finish a task in a given time slice - it is pushed back in a queue. All priorities are equally served, resulting in 8-11k run time units.

Priority Round-Robin: processes with higher priorities are served first. If a process can't finish a task in a given time slice - it is pushed back after the last process with the same priority. Low priority jobs starved, resulting in a 20k run time units. While high priority jobs were completed ~6 times faster.
