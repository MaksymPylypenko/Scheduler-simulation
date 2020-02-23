# SCHEDULER SIMULATION

## Config

`ROUNDS` - the number of rounds to complete 
  - default is 10 

`TIME SLICE` - the int value of a maximum work at a time
  - default is 5

`SCHEDULER` - type of scheduler

0. Pure Round Robin
1. Priority Round Robin
2. Shortest Job First
3. Shortest Remaining Job First

`RANDOM_SAMPLE`
  - True, a new sample will be generated every run
  - False, will use processes (default file) 

`PRINT_ROUND`
  - True, print statistics for every round
  - False, only the summary of all rounds is printed

`FILE` - if you want to test a specific sample 
  - default is "processes" 
  - ignored if RANDOM_SAMPLE is set to TRUE

## To run:
> python3 main.py <schedulerType>
