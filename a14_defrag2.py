"""
--- Day 14: Disk Defragmentation ---

Suddenly, a scheduled job activates the system's disk defragmenter. Were the
situation different, you might sit and watch it for a while, but today, you
just don't have that kind of time. It's soaking up valuable system resources
that are needed elsewhere, and so the only option is to help it finish its task
as soon as possible.

The disk in question consists of a 128x128 grid; each square of the grid is
either free or used. On this disk, the state of the grid is tracked by the bits
in a sequence of knot hashes.

A total of 128 knot hashes are calculated, each corresponding to a single row
in the grid; each hash contains 128 bits which correspond to individual grid
squares. Each bit of a hash indicates whether that square is free (0) or used (1).

The hash inputs are a key string (your puzzle input), a dash, and a number
from 0 to 127 corresponding to the row. For example, if your key string were
flqrgnkx, then the first row would be given by the bits of the knot hash of
flqrgnkx-0, the second row from the bits of the knot hash of flqrgnkx-1, and
so on until the last row, flqrgnkx-127.

The output of a knot hash is traditionally represented by 32 hexadecimal digits;
each of these digits correspond to 4 bits, for a total of 4 * 32 = 128 bits.
To convert to bits, turn each hexadecimal digit to its equivalent binary value,
high-bit first: 0 becomes 0000, 1 becomes 0001, e becomes 1110, f becomes 1111,
and so on; a hash that begins with a0c2017... in hexadecimal would begin with
10100000110000100000000101110000... in binary.

Continuing this process, the first 8 rows and columns for key flqrgnkx appear
as follows, using # to denote used squares, and . to denote free ones:

##.#.#..-->
.#.#.#.#   
....#.#.   
#.#.##.#   
.##.#...   
##..#..#   
.#...#..   
##.#.##.-->
|      |   
V      V   
In this example, 8108 squares are used across the entire 128x128 grid.

Given your actual key string, how many squares are used?

Your puzzle input is hxtvlmkl.

--- Part Two ---

Now, all the defragmenter needs to know is the number of regions. A region is a group of used squares that are all adjacent, not including diagonals. Every used square is in exactly one region: lone used squares form their own isolated regions, while several adjacent squares all count as a single region.

In the example above, the following nine regions are visible, each marked with a distinct digit:

11.2.3..-->
.1.2.3.4   
....5.6.   
7.8.55.9   
.88.5...   
88..5..8   
.8...8..   
88.8.88.-->
|      |   
V      V   
Of particular interest is the region marked 8; while it does not appear contiguous in this small view, all of the squares marked 8 are connected when considering the whole 128x128 grid. In total, in this example, 1242 regions are present.

How many regions are present given your key string?


"""

import operator

HEXMAP = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'] 

class Knot(object):
    def __init__(self, length):
        self.length = length
        self.kt = [x for x in range(0,length)]
        self.skip = 0
        self.current_pos = 0

    def reverse(self, revlen):
        """Reverse revlen items starting at self.current_pos."""
        assert revlen <= self.length, "The reverse length is longer than the list!"

        start_pos = self.current_pos
        end_pos = (self.current_pos + revlen) % self.length

        if revlen in (1,0):
            pass
        elif end_pos <= start_pos:
            # we have looped
            revlist = self.kt[start_pos:self.length] + self.kt[0:end_pos]
            revlist = revlist[::-1]
            i = self.current_pos
            for x in revlist:
                self.kt[i] = x
                i = (i + 1) % self.length
        else:
            # not looped
            revlist = self.kt[start_pos:end_pos]
            revlist = revlist[::-1]
            self.kt = self.kt[0:start_pos] + revlist + self.kt[end_pos:]

        self.current_pos = (self.current_pos + revlen + self.skip) % self.length
        self.skip += 1

    def make_dense(self):
        """Calculate the dense hash"""
        dense_hash = []
        for chunk_num in range(0, self.length//16):
            chunk = self.kt[chunk_num * 16: (chunk_num+1) * 16]
            value = chunk[0]
            for x in chunk[1:]:
                value ^= x
            dense_hash.append(value)
        dense_hash
        dense_hash_string = ''
        for value in dense_hash:
            upper, lower = divmod(value, 16)
            dense_hash_string += HEXMAP[upper]
            dense_hash_string += HEXMAP[lower]
        return dense_hash_string

def make_bitstring(s):
    output = ''
    for c in s:
        x = HEXMAP.index(c)
        output += '{:0>4b}'.format(x)
    return output

def sumbits(s):
    """Assumes s is a string of 0s and 1s"""
    count = [0, 0]
    for x in range(len(s)):
        if s[x] == '1':
            count[1] += 1
        else:
            count[0] += 1
    return count    
            
def hash_it(key):
    k = Knot(256)
    moves = [x for x in key.encode('ascii')] + [17, 31, 73, 47, 23]
    rounds = 64
    while rounds > 0:
        rounds -= 1
        for move in moves:
            k.reverse(move)
    return k.make_dense()
    
class Gridscanner(object):
    def __init__(self, grid):
        self.grid = grid

    def at_pointer(self):
        return self.grid[self.seek_pointer[0]][self.seek_pointer[1]]

    def find_1(self):
        for y in range(0, len(self.grid)):
            if 1 in self.grid[y]:
                return [y, self.grid[y].index(1)]
        return None

    def check_for_1(self, y, x):
        if y < 0 or y >= len(self.grid):
            return False
        if x < 0 or x >= len(self.grid[0]):
            return False
        return bool(self.grid[y][x] == 1)

    def paint(self, y, x, color):
        """Paints a contiguous area of 1s starting at x, y"""
        self.grid[y][x] = color
        if self.check_for_1(y-1, x):
            self.paint(y-1, x, color)
        if self.check_for_1(y+1, x):
            self.paint(y+1, x, color)
        if self.check_for_1(y, x-1):
            self.paint(y, x-1, color)
        if self.check_for_1(y, x+1):
            self.paint(y, x+1, color)

if __name__ == "__main__":
    k = Knot(256)
    grid = []
    key = "hxtvlmkl"
    sum_ones = 0
    for row in range(0, 128):
        rowbits = [1 if x=='1' else 0 for x in list(make_bitstring(hash_it(key + '-' + str(row))))]
        grid.append(rowbits)
    print(grid[0:2])
    gs = Gridscanner(grid)
    # starting color
    color = 2
    # paint every distinct section a different color
    while gs.find_1():
        next1 = gs.find_1()
        gs.paint(*next1, color)
        color += 1
    # how many colors did we need to paint each region?
    print(color-2)
    

        

    
    

        





    
