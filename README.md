# Travelling-Salesman-Genetic-Algorithm
Implementation of a genetic algorithm to find a solution to the travelling salesman problem.  
Currently only uses a hard-coded 2D distance matrix, but will be modified to take any 2D distance  
matrix.

### Main Program
**main.py**: contains the program which provides a solution to the travelling salesman problem.  
It takes three arguments or none, in which case default values are supplied:  
1. argv[1]: output file handle (Default: TSOUT.txt)
2. argv[2]: initial population size (Default: 20)
3. argv[3]: number of generations (Default: 1000)

### Driver
**driver2.sh**: a simple bash script that runs main.py over a sequence of multiple combinations  
of inputs. For each run, it prints to output file the best results for that type of run as well  
as the best overall run.

### Output
**myOutput.txt**: contains all captured output for runs over main.py, including all solutions found  
as well as the average best solution for all combinations of potential inputs  
  
**finalResults.txt**: contains summary of results for each combination
