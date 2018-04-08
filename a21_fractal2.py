"""
--- Day 21: Fractal Art ---

You find a program trying to generate some art. It uses a strange process that involves repeatedly enhancing the detail of an image through a set of rules.

The image consists of a two-dimensional square grid of pixels that are either on (#) or off (.). The program always begins with this pattern:

.#.
..#
###
Because the pattern is both 3 pixels wide and 3 pixels tall, it is said to have a size of 3.

Then, the program repeats the following process:

If the size is evenly divisible by 2, break the pixels up into 2x2 squares, and convert each 2x2 square into a 3x3 square by following the corresponding enhancement rule.
Otherwise, the size is evenly divisible by 3; break the pixels up into 3x3 squares, and convert each 3x3 square into a 4x4 square by following the corresponding enhancement rule.
Because each square of pixels is replaced by a larger one, the image gains pixels and so its size increases.

The artist's book of enhancement rules is nearby (your puzzle input); however, it seems to be missing rules. The artist explains that sometimes, one must rotate or flip the input pattern to find a match. (Never rotate or flip the output pattern, though.) Each pattern is written concisely: rows are listed as single units, ordered top-down, and separated by slashes. For example, the following rules correspond to the adjacent patterns:

../.#  =  ..
          .#

                .#.
.#./..#/###  =  ..#
                ###

                        #..#
#..#/..../#..#/.##.  =  ....
                        #..#
                        .##.
When searching for a rule to use, rotate and flip the pattern as necessary. For example, all of the following patterns match the same rule:

.#.   .#.   #..   ###
..#   #..   #.#   ..#
###   ###   ##.   .#.
Suppose the book contained the following two rules:

../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
As before, the program begins with this pattern:

.#.
..#
###
The size of the grid (3) is not divisible by 2, but it is divisible by 3. It divides evenly into a single square; the square matches the second rule, which produces:

#..#
....
....
#..#
The size of this enhanced grid (4) is evenly divisible by 2, so that rule is used. It divides evenly into four squares:

#.|.#
..|..
--+--
..|..
#.|.#
Each of these squares matches the same rule (../.# => ##./#../...), three of which require some flipping and rotation to line up with the rule. The output for the rule is the same in all four cases:

##.|##.
#..|#..
...|...
---+---
##.|##.
#..|#..
...|...
Finally, the squares are joined into a new grid:

##.##.
#..#..
......
##.##.
#..#..
......
Thus, after 2 iterations, the grid contains 12 pixels that are on.

How many pixels stay on after 5 iterations?

Your puzzle answer was 205.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

How many pixels stay on after 18 iterations?

Your puzzle answer was 3389823.

Both parts of this puzzle are complete! They provide two gold stars: **


"""

import copy

class Panel(object):

    @classmethod
    def from_thumb(cls, s):
        """Create a panel from the standard string format given by the problem"""
        s = s.strip()
        return Panel([list(r) for r in s.split('/')])

    def __init__(self, pixels):
        """Pixels is an array of the pixels in the pattern, ie:
        [['.','#','.'],['.','.','#'],['#','#','#']]"""
        self.size = len(pixels)
        self.pixels = pixels

    def copy(self):
        return Panel(copy.deepcopy(self.pixels))

    def flip_vertical(self):
        return Panel([x for x in reversed(self.pixels)])

    def flip_horizontal(self):
        return Panel([list(reversed(x)) for x in self.pixels])

    def rotate(self):
        """Rotate 90 degress clockwise"""
        new_pixels = []
        for _ in range(self.size):
            new_pixels.append(list())
        for row in reversed(self.pixels):
            for j, val in enumerate(row):
                new_pixels[j].append(val)
        return Panel(new_pixels)

    def print(self):
        for row in self.pixels:
            print(''.join(row))

    def thumbprint(self):
        return '/'.join([''.join(x) for x in self.pixels])

    def all_rotated_thumbs(self):
        thumbs = set()
        rotated = self
        for i in range(4):
            thumbs.add(rotated.thumbprint())
            rotated = rotated.rotate()
        return thumbs

    def all_thumbs(self):
        thumbs = self.all_rotated_thumbs()
        thumbs = thumbs.union(self.flip_vertical().all_rotated_thumbs())
        thumbs = thumbs.union(self.flip_horizontal().all_rotated_thumbs())
        thumbs = thumbs.union(self.flip_vertical().flip_horizontal().all_rotated_thumbs())
        return thumbs

class Rulebook(object):
    
    def __init__(self):
        self.rules = dict()

    def add(self, panel_from, panel_to):
        """For any dictionary entry, make a from->to entry
        for EACH variation of the from panel, so we never have to rotate
        during the run."""
        for thumb in panel_from.all_thumbs():
            if (thumb in self.rules and
                self.rules[thumb].thumbprint() != panel_to.thumbprint()):
                print('Rule collision! {}'.thumb())
            self.rules[thumb] = panel_to

    def lookup(self, panel):
        thumb = panel.thumbprint()
        if thumb in self.rules:
            # always returns a new Panel,
            # not a pointer to an existing panel object
            return Panel(self.rules[thumb].pixels)
        else:
            raise ValueError("No rule entry for {}".format(thumb))

    def add_from_string(self, s):
        """For rules in the rulebook format:
        ##/.. => ###/.#./###"""
        fs, ts = s.split('=>')
        self.add(Panel.from_thumb(fs), Panel.from_thumb(ts))

class Grid(object):

    def __init__(self, s, rulebook):
        """Builds a grid from a string"""
        self.rulebook = rulebook
        self.pixels = []
        for row in s.split('/'):
            self.pixels.append(list(row))
        self.panels = self.break_into_panels()

    def print(self):
        for row in self.pixels:
            print(''.join(row))

    def ons(self):
        """How many are on? #"""
        on = 0
        for row in self.pixels:
            for pix in row:
                if pix == '#':
                    on += 1
        return on

    def panel_size(self):
        if len(self.pixels)%2 == 0:
            return 2
        else:
            return 3

    def panel_extract(self, row, col):
        """Pull out one panel"""
        ps = self.panel_size()
        panel_pixels = []
        for i in range(ps * row, ps * (row+1)):
            panel_pixels.append(self.pixels[i][ps*col:ps*(col+1)])
        return Panel(panel_pixels)

    def break_into_panels(self):
        panels = []
        panels_per_side = len(self.pixels) // self.panel_size()
        for row in range(0, panels_per_side):
            panel_row = []
            for col in range(0, panels_per_side):
                panel_row.append(self.panel_extract(row, col))
            panels.append(panel_row)
        return panels

    def print_panels(self):
        panels_per_side = len(self.pixels) // self.panel_size()
        for row in self.panels:
            for i in range(0, self.panel_size()):
                printed_row = []
                for panel in row:
                    printed_row.append(''.join(panel.pixels[i]))
                print('|'.join(printed_row))
            print('-'*(len(self.pixels)+panels_per_side-1))

    def cycle(self):
        """Run one map cycle, return an updated grid."""
        new_panels = []
        for row in self.panels:
            new_panels_row = []
            for panel in row:
                new_panels_row.append(rulebook.lookup(panel))
            new_panels.append(new_panels_row)
        self.panels = new_panels
        self.pixels = []
        for row in self.panels:
            for i in range(len(row[0].pixels)):
                pixel_row = []
                for panel in row:
                    pixel_row += panel.pixels[i]
                self.pixels.append(pixel_row)
        self.panels = self.break_into_panels()
        return self

rulebook = Rulebook()
f = open('a21_input.txt')
for line in f:
    rulebook.add_from_string(line)
f.close()

grid = Grid('.#./..#/###', rulebook)
# grid = Grid('#..#/..../..../#..#')
grid.print()
print(grid.ons())
grid.print_panels()
print('Ons after 18 cylces:')
for _ in range(18):
    grid.cycle()
print(grid.ons())




