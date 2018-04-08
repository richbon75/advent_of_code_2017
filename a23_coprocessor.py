'''
--- Day 23: Coprocessor Conflagration ---

You decide to head directly to the CPU and fix the printer from there. As you get close, you find an experimental coprocessor doing so much work that the local programs are afraid it will halt and catch fire. This would cause serious issues for the rest of the computer, so you head in and see what you can do.

The code it's running seems to be a variant of the kind you saw recently on that tablet. The general functionality seems very similar, but some of the instructions are different:

set X Y sets register X to the value of Y.
sub X Y decreases register X by the value of Y.
mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
jnz X Y jumps with an offset of the value of Y, but only if the value of X is not zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)
Only the instructions listed above are used. The eight registers here, named a through h, all start at 0.

The coprocessor is currently set to some kind of debug mode, which allows for testing, but prevents it from doing any meaningful work.

If you run the program (your puzzle input), how many times is the mul instruction invoked?

Your puzzle answer was 5929.
'''

import time

class Processor(object):

    def __init__(self, filename):
        self.prog = []
        self.program_counter = 0
        self.registers = {}
        self.mul_invoked = 0
        self.instructions_executed = 0
        f = open(filename, 'r')
        for line in f:
            inst, *args = line.strip().split()
            self.prog.append((inst, args))
        f.close()
        self.instruction_map = {
            'set': self.sets,
            'sub': self.sub,
            'mul': self.mul,
            'jnz': self.jnz
            }

    def decode(self, value):
        try:
            return int(value)
        except ValueError:
            return self.registers.get(value,0)

    def sets(self, x, y):
        self.registers[x] = self.decode(y)
        return True

    def sub(self, x, y):
        value = self.decode(x)
        self.registers[x] = value - self.decode(y)
        return True

    def mul(self, x, y):
        value = self.decode(x)
        self.registers[x] = value * self.decode(y)
        self.mul_invoked += 1
        return True

    def jnz(self, x, y):
        value = self.decode(x)
        if value != 0:
            self.program_counter += self.decode(y) -1
        return True

    def run_instruction(self, debug=False):
        self.instructions_executed += 1
        if self.program_counter < 0 or self.program_counter >= len(self.prog):
            print('Program counter out of bounds. PC = {}'.format(self.program_counter))
            return False
        inst, args = self.prog[self.program_counter]
        if debug:
            print(inst, args)
        self.program_counter += 1
        return self.instruction_map[inst](*args)

p = Processor('a23_input.txt')
activity = True

start_time = time.time()

while p.run_instruction():
    pass

print('elapsed time = ', time.time() - start_time)
print('mul invoked = ', p.mul_invoked)


            
            
            

        
