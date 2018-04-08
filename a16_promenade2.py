"""
--- Day 16: Permutation Promenade ---

You come upon a very unusual sight; a group of programs here appear to be dancing.

There are sixteen programs in total, named a through p. They start by standing in a line: a stands in position 0, b stands in position 1, and so on until p, which stands in position 15.

The programs' dance consists of a sequence of dance moves:

Spin, written sX, makes X programs move from the end to the front, but maintain their order otherwise. (For example, s3 on abcde produces cdeab).
Exchange, written xA/B, makes the programs at positions A and B swap places.
Partner, written pA/B, makes the programs named A and B swap places.
For example, with only five programs standing in a line (abcde), they could do the following dance:

s1, a spin of size 1: eabcd.
x3/4, swapping the last two programs: eabdc.
pe/b, swapping programs e and b: baedc.
After finishing their dance, the programs end up in order baedc.

You watch the dance for a while and record their dance moves (your puzzle input). In what order are the programs standing after their dance?

Your puzzle answer was giadhmkpcnbfjelo.

The first half of this puzzle is complete! It provides one gold star: *
"""

class DanceProgs():
    def __init__(self):
        self.progs = [chr(x) for x in range(ord('a'), ord('a')+16)]
        f = open('a16_promenade_input.txt', 'r')
        rawsteps = f.read()
        f.close
        self.steps = [x.strip() for x in rawsteps.split(',')]

    def spin(self, x):
        """Take x elements off the end and put them in the front"""
        self.progs = self.progs[-x:] + self.progs[0:-x]

    def exchange(self, a, b):
        """Swap the elements at indexes a and b"""
        temp = self.progs[b]
        self.progs[b] = self.progs[a]
        self.progs[a] = temp

    def partner(self, a, b):
        self.exchange(self.progs.index(a), self.progs.index(b))

    def print(self):
        print(''.join(self.progs))

    def full_dance(self):
        for step in self.steps:
            step = step.strip()
            move = step[0]
            elements = step[1:].split('/')
            if move == 's':
                self.spin(int(elements[0]))
            elif move == 'x':
                self.exchange(int(elements[0]), int(elements[1]))
            elif move == 'p':
                self.partner(elements[0], elements[1])
            else:
                raise ValueError('Unknown move: {} in step: {}'.format(move, step))

g = DanceProgs()
g.full_dance()
g.print()

g = DanceProgs()
starting = list(g.progs)
print(starting)
print(g.progs)
iters = 1
g.full_dance()
while g.progs != starting:
    g.full_dance()
    iters += 1
print('Cycles in {} iterations.'.format(iters))


# reset
g = DanceProgs()
for _ in range(1000000000 % iters):
    g.full_dance()
g.print()





