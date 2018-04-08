"""
--- Day 11: Hex Ed ---

Crossing the bridge, you've barely reached the other side of the stream when a program comes up to you, clearly in distress. "It's my child process," she says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be found to the north, northeast, southeast, south, southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \
You have the path the child process took. Starting where he started, you need to determine the fewest number of steps required to reach him. (A "step" means to move from the hex you are in to any adjacent hex.)

For example:

ne,ne,ne is 3 steps away.
ne,ne,sw,sw is 0 steps away (back where you started).
ne,ne,s,s is 2 steps away (se,se).
se,sw,se,sw,sw is 3 steps away (s,s,sw).
"""

def steps_back(N, E):
    N = abs(N)
    E = abs(E)
    steps = E
    N = N - (E * 0.5)
    if N > 0:
        steps += N
    return steps

f = open('a11_hexgrid_input.txt', 'r')
dirs = f.read()
f.close()

dirs = dirs.strip().split(',')

N = 0.0
E = 0.0

for d in dirs:
    if d == 'n':
        N += 1
    elif d == 's':
        N -= 1
    else:
        if 'n' in d:
            N += 0.5
        if 's' in d:
            N -= 0.5
        if 'e' in d:
            E += 1
        if 'w' in d:
            E -= 1

print(N, E)
print(steps_back(N, E))



        
