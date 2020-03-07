#!/bin/sh

arrGens=(50 100 200) # number of generations to cycle through
arrPops=(4 8 12 16 20) # initial population sizes to cycle through
numTrials=30 # number of trials to iterate through for each gen/pop combinations

for pop in "${arrPops[@]}" 
do
	overallBest=1000
	for gens in "${arrGens[@]}" 
	do
		results=() # for storing results from each call
		i=0 # for counting number of calls
		mySum=0 # for calculating cumulative path costs over 10 trials
		best=1000 # for finding best member in a given execution
		echo -e "Generations:" $gens", Pop:" $pop"\n" >> myOutput.txt
		
		for i in $(seq 0 $numTrials); # try trials with these parameters
		do
			OUTPUT=$(python main.py myOutput.txt $pop $gens)
			results+=("$OUTPUT")
			i=$(( i + 1 ))
		done
		
		for x in "${results[@]}"	# calculate the sum of these trials
		do
			if [ $x -lt $best ] # find the best of the 10
			then
				best=$x
			fi
			mySum=$(( mySum + x )) # add value to cumulative count
		done
		# push results for this combination to the output file
		average=$(( mySum / i ))
		echo -e "\nFor Generations:" $gens "and Population:" $pop", average path cost over" $numTrials "trials is" $average", and best result was" $best "\n" >> myOutput.txt
		echo -e "For Generations:" $gens "and Population:" $pop", average path cost over" $numTrials" trials is" $average", and best result was" $best >> finalResults.txt
		if [ $best -lt $overallBest ] # track if this best is better than overall best
		then
			overallBest=$best
		fi
	done
done
echo -e "Overall Best was" $overallBest >> myOutput.txt
echo -e "Overall Best was" $overallBest >> finalResults.txt