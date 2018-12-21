# adventofcode-2018

These are my solutions for the Advent of Code 2018 Challenges (https://adventofcode.com/).

* All of them is written with Python 2.7
* None of the solutions require special packages, only the core Python environment
* All of them are unique solutions that was not done with any peeking on existing ones, there are few exceptions though when I hopelessly got stuck and I went to the Reddit page of solutions to see how people approached the problem
* Many of them take parameters (like the input file to read, or how many cycles to execute, etc...)
* Some of them provide visual representation of the problem (maybe there is code inside but switched off)
* Some of them may be not optimal, but they finish on time, some of them are really quick though


# Challenges

## DAY 1

## DAY 2

## DAY 3

## DAY 4
* Sort the events properly, and observe that the sorted events are fully there, none is missing, so the parsing of them is not hard and there are no edge cases (multiple wakeups, no wakeup, etc...)

## DAY 5
* This is not optimal, but quick enough for Part1.
* For Part2, it is even slower, but finishes in a few minutes, and the answer can be read from the screen only.

## DAY 6
* Now there is a hypothetical 500x500 world boundary in the code, it could be eliminated though to make it a bit better
* For Part1 I used a hypothesys that the areas reaching the edge of the world are the infinite ones, which might not be true if the world is not big enough
* It is a tad slow, but runs in 10 seconds

## DAY 7
* Used a unique graph representation for this type of problem with special notion of which Step depends on which other. From here, a simple poke solves the entire graph.

## DAY 8
* Once one figures out how to correctly read the input in, it is easy.

## DAY 9
* Did not know deque, solved without it, and so it takes a bit long to finish, runs in a minute or so. Provided a deque implementation for comparison purposes and will use deque from now on as it is awesome.

## DAY 10
* Did not consider automating it, so there are a few hardcoded values for my specific solution. Might do something about this later on.
* Spent ages to get the projection right (visualize the sky on a fixed size dotted screen, with shrinking it down without distortion, automatically, in every step)
* This challenge is very pleasing to the eye and heart, when suddenly the solution draws on screen :)

## DAY 11
* Did not know the Summed Area Table structure before, but managed to come up with a very similar structure myself, you can see the evolution and the different approaches in later executables

## DAY 12
* The trick here was that there is a pattern, shifting to infinity, and finding it, and finding the shift factor is key here.

## DAY 13
* The catch here was that the carts are not moving at the same time, on a tick, but one after another, and this results a different solution, so it was painful to realize this. Regardless of this nuance, the program solves the input, so nothing seems wrong.

## DAY 14
* The catch here was that if you check only the end of the list for the 10 digits, you could(!) miss the solution, as at each iteration there is a possibility to increase by two, watch out for this, for my input, this was the case

## DAY 15
* It is a bit slow, but VERY graphical, best challenge this year so far
* Biggest catch was that Breath-First Search gives you shortest path in case all edges are equal, which is the case here. Non need to rely on slower shortest algorithms
* Also, reading order is very important, multiple times, to get the proper moves

## DAY 16
* Decided not to use classes for this one, and it ended up being a good choice, used opcode-function-dictionary instead

## DAY 17
* Tricky thing was to "simulate" the water, used a queue for this, and put the fresh water into it to get the flow, occasionally putting in water elements just to restart the calculation of the flow if required
* Great visual challenge, however very hard to print on screen. Used a projection without any shrinkage
* Misinterpreted the text as the water rises not always to the RIGHT, but only in the example, it raises always to the side the water comes into the clay. This could become tricky if in the clay there are multiple pours.

## DAY 18
* Trick was to observe a repetition in the execution, so use a cache, and see from where there is a cycle. Then calculate with the cycle for 99.999% of the time, as the actual calculations are rather slow
* Very graphical challenge, great to look at

## DAY 19
* Part1 is simply reusing the program from DAY 16, and tailoring to the current problem
* For Part2, observe patterns in the execution, and short-circuit them with register-rewritings. However, you need to understand the code executing in the loop to write the proper values into the registers, and into the right registers. It turned out that I had to factor an 8 digit number, and the code does a double-for loop and adds together all divisors or that number. Not sure how this could have been solved fully automatically.
* For the above reasons, my solution contains hardcoded numbers, for my personal problem. One can modify this by start running the program, and observing the big number in one of the registers (R[5] for me), then rewrite all of the constants in the code, including the prime divisors. There is a version that automatically does this for my input.

## DAY 20
* It was tempting to do it the short way, with only parsing the input once, and figuring out the answer, which worked wurpirisingly well for Part1
* I however have chosen to fully and properly solve it due to some corner cases (multiple paths present with shortest coming later, etc...). First calculating all the possible ways to traverse the map (reduce the regexp to a list of matching strings), then do a Breath-First Search for every endpoint from (0,0). From there, it is easy, we just need to extract the answers from the data.

## DAY 21
* Reuse code from DAY19, but rewrite the register-modification logic so that there is only one kind of loop in the program that can happen endlessly, and it has to be a register-dependent rewrite, so I ended using 'exec'
* This also requires reverse engineering: observer how the program can end. Notice that only IP=28 uses R[0] for reading and otherwise R[0] takes no part in the execution, so that is the cornerpiece of the solution. One needs IP=28 --> IP=16. IP=16 is reachable if R[1]<256, so observe in the execution and determine how IP=28 at the end can provide the halt of the program.
* For Part2, this needs to be further thought about: R[3] and R[0] is compared in order to halt the code, so you need an R[3] written into R[0] that gets you going the longest, so collect what numbers you have seen so far in R[3], and if you find a loop, you need to use the previous one to get the longest execution

## DAY 22

## DAY 23

## DAY 24

## DAY 25

