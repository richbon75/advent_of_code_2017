"""
--- Day 19: A Series of Tubes ---

Somehow, a network packet got lost and ended up here. It's trying to follow a routing diagram (your puzzle input), but it's confused about where to go.

Its starting point is just off the top of the diagram. Lines (drawn with |, -, and +) show the path it needs to take, starting by going down onto the only line connected to the top of the diagram. It needs to follow this path until it reaches the end (located somewhere within the diagram) and stop there.

Sometimes, the lines cross over each other; in these cases, it needs to continue going the same direction, and only turn left or right when there's no other option. In addition, someone has left letters on the line; these also don't change its direction, but it can use them to keep track of where it's been. For example:

     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 

Given this diagram, the packet needs to take the following path:

Starting at the only line touching the top of the diagram, it must go down, pass through A, and continue onward to the first +.
Travel right, up, and right, passing through B in the process.
Continue down (collecting C), right, and up (collecting D).
Finally, go all the way left through E and stopping at F.
Following the path to the end, the letters it sees on its path are ABCDEF.

The little packet looks up at you, hoping you can help it find the way. What letters will it see (in the order it would see them) if it follows the path? (The routing diagram is very wide; make sure you view it without line wrapping.)

Your puzzle answer was KGPTMEJVS.

The first half of this puzzle is complete! It provides one gold star: *
"""

class Maze(object):

    # (x,y) diffs
    offset = {
         's': ( 0, 1),
         'n': ( 0,-1),
         'e': ( 1, 0),
         'w': (-1, 0)
        }

    def __init__(self, filename):
        self.rows = []
        f = open(filename, 'r')
        for line in f:
            self.rows.append(line.strip('\n'))
        f.close()
        self.pos = [self.rows[0].index('|'), 0]
        self.heading = 's'
        self.visited = []
        self.finished = False

    def print(self):
        for i, row in enumerate(self.rows):
            if i == self.pos[1]:
                temprow = [x for x in row]
                temprow[self.pos[0]] = chr(174)
                print(''.join(temprow))
            else:
                print(row)

    def charat(self, pos=None):
        if pos is None:
            pos = self.pos
        if (pos[0] < 0 or pos[1] < 0 or pos[0] >= len(self.rows[0])
            or pos[1] >= len(self.rows)):
            return None # off map
        return self.rows[pos[1]][pos[0]]

    def move(self):
        oldpos = self.pos[:]
        self.pos = self.apply_heading()
        # do we have to do anything here?
        here = self.charat()
        if here in ('|','-'):
            pass
        elif here == '+':
            self.new_direction()
        elif here == ' ':
            # end of route
            self.finished = True
            self.pos = oldpos # unmake the move
        else:
            # visiting a letter, record it
            self.visited.append(here)
        # self.print()

    def apply_heading(self, heading = None, pos = None):
        if heading is None:
            heading = self.heading
        if pos is None:
            pos = self.pos
        localpos = pos[:]
        localpos[0] += self.offset[heading][0]
        localpos[1] += self.offset[heading][1]
        return localpos

    def new_direction(self):
        """We're turning.  Which way do we go next?"""
        if self.heading in ('e','w'):
            test = self.charat(self.apply_heading('s'))
            if test is not None and test != ' ':
                self.heading = 's'
            else:
                self.heading = 'n'
        else:
            test = self.charat(self.apply_heading('e'))
            if test is not None and test != ' ':
                self.heading = 'e'
            else:
                self.heading = 'w'

    def travel(self):
        """Traverse the maze until the end is reached."""
        while not self.finished:
            self.move()
        print(''.join(self.visited))

maze = Maze('a19_input.txt')
maze.travel()

