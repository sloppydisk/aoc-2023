# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 15:57:55 2023

@author: Jasper
"""

"""--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

--- Part Two ---

The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?

"""

import numpy as np
import re

# change comment id from '#' to 'lame', otherwise they get excluded. 
inputs = np.genfromtxt('input.txt', dtype='str', comments= 'lame')
testinput = np.genfromtxt('testinput.txt', encoding = None, dtype='str', comments= 'lame')

test = False

if test:
    inputs = testinput
    print(inputs)

matrix = []
match_dot = '\.'
match_star = '\*'

match_digit = '\d+'
i = 0
answer_1_sum= 0

starts, ends = ([], [])

# first pass for parsing to np array
for el in inputs: 
    starts.append([])
    ends.append([])
    
    # find number indices
    for m in re.finditer(match_digit, el):
        starts[i].append(m.start())
        ends[i].append(m.end())
    
    # sub dots to 0
    el = re.sub(match_dot, '0', el)
 
    vec = []
    for x in el: 
        try: 
            vec.append(int(x))
        # if symbol we parse to -1 or -2 for a *
        except: 
            if x == '*': 
                vec.append(-2)
            else: 
                vec.append(-1)
            
    matrix.append(vec)
    i+=1

# second pass to analyse 
n_row = len(starts)
n_col = len(vec)

npmat = np.array(matrix)

gear_id = np.argwhere(npmat < -1)
gear_ratio = np.ones(np.shape(gear_id)[0])
gear_count = np.zeros(np.shape(gear_id)[0])

for j in range(n_row):
    vec = matrix[j]
    
    # for all numbers 
    for k in range(len(starts[j])): 
        # set up adjacent array
        x = np.array(range(max(starts[j][k]-1, 0), min(ends[j][k]+1, n_col-1)))
        y = np.array(range(max(j-1, 0), min(j+2, n_row)))
        XX, YY = np.meshgrid(x, y)
        
        # Part one: check for negative values
        if (npmat[YY, XX]<0).any():
            num = npmat[j, starts[j][k]: ends[j][k]]
            a = ''
            for x in num:
                a += str(x)
            num = int(a)
            
            answer_1_sum += num
            
        # Part two: check for -2 values
        boolarray = npmat[YY, XX]==-2
        all_bools = np.where(boolarray)
        for i in range(len(all_bools[0])):
            x = all_bools[1][i]
            y = all_bools[0][i]
            
            id_tuple = (YY[y][x], XX[y][x])
            
            row_idx = np.where((gear_id == id_tuple).all(axis=1))
            gear_ratio[row_idx] *= num
            gear_count[row_idx] += 1

print('Answer to part 1: '+str(answer_1_sum))
print('Answer to part 2: '+str(int(sum(gear_ratio[gear_count==2]))))


