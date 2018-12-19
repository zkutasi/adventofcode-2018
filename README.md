# adventofcode-2018

These are my solutions for the Advent of Code 2018 Challenges (https://adventofcode.com/).

* All of them is written with Python 2.7
* All of them are unique solutions that was not done with any peeking on existing ones, there are few exceptions though when I hopelessly got stuck and I went to the Reddit page of solutions to see how people approached the problem
* Many of them take parameters (like the input file to read, or how many cycles to execute, etc...)
* Some of them provide visual representation of the problem (maybe there is code inside but switched off)
* Some of them may be not optimal, but they finish on time, some of them are really quick though


# Challenges

## DAY 1

## DAY 2

## DAY 3

## DAY 4
* Sort the events properly, and observe that the sorted events are fully there, none is missing, so the parsing of them is not hard and there are no edge cases

## DAY 5
* This is not optimal, but quick enough for Part1.
* For Part2, it is even slower, but finishes in a few minutes, and the answer can be read from the screen only.

## DAY 6
* Now there is a hypothetical 500x500 world boundary in the code, it could be eliminated though to make it a bit better
* For Part1 I used a hypothesys that the areas reaching the edge of the world are the infinite ones, which might not be true if the world is not big enough
* It is a tad slow, but runs in 10 seconds

## DAY 7
* Used a unique graph representation for this type of problem with special notion of which STep depends on which other

## DAY 8
* Once one figures out how to correctly read the input in, it is easy. Used recursion.

## DAY 9
* Did not know deque at all, solved without it, and so it takes a bit long to finish, runs in a minute or so. Provided a deque implementation for comparison purposes.

## DAY 10
* Did not consider automating it, so there are a few hardcoded values for my specific solution. Might do something about this later on.
* Spent ages to get the projection right (visualize the sky on a fixed size dotted screen, with shrinking it down without distortion, automatically, in every step)

## DAY 11
* Did not know the Summed Area Table structure before, but managed to come up with a very similar structure, you can see the evolution and the different approaches in later executables

## DAY 12
* The trick here was that there is a pattern, shifting to infinity, and finding it, and finding the shift factor is key here, otherwise the implementation never finishes

## DAY 13
* The catch here was that the carts are not moving at the same time, on a tick, but one after another, and this results a different solution, so it was painful to realize this

## DAY 14
* Catch here is if you check only the end of the list for the 10 digits, you will miss the solution, as at each iteration there is a possibility to increase by two, watch out for this

## DAY 15
* It is a bit slow, but VERY graphical, best challenge this year so far
* Biggest catch was that Breath-First Search gives you shortest path in case all edges are equal, which is the case here
* Also, reading order is very important, multiple times, to get the proper moves

## DAY 16
* Decided not to use classes for this one, and it ended up being a good choice, used function-map instead

## DAY 17
* Tricky thing was to "simuate" the water, used a queue for this, and put the fresh water into it to get the flow
* Great visual challenge, however very hard to print on screen. Used a projection without any shrinkage
* Misinterpreted the text as the water rises not always to the RIGHT, but only in the example, it raises always to the side the water comes into the clay. This could become tricky if in the clay there are multiple pours.

## DAY 18
* Trick was to obsevre a repetition, so use a cache, and see from where there is a cycle. Then calculate with the cycle for 99.999 % of the time, as the actual calculations are rather slow
* Very graphical challenge, great to look at

## DAY 19
* Part1 is simply reusing the program from DAY 16, and tailoring to the current problem
* For Part2, observe patterns in the execution, and short-circuit them with register-rewritings. However, you need to understand the code executing in the loop to write the proper values into the registers, and into the right registers. It turned out that I had to factor an 8 digit number, and the code does a double-for loop and adds together all divisors or that number. Not sure how this could have been solved fully automatically.
* For the above reasons, my solution contains hardcoded numbers, for my personal problem. One can modify this by start running the program, and observing the big number in one of the registers (R[5] for me), then rewrite all of the constants in the code, inclusing the prime divisors. There is a version that automatically does this for my input.

## DAY 20

## DAY 21

## DAY 22

## DAY 23

## DAY 24

## DAY 25

