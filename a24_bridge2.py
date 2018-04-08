"""
--- Day 24: Electromagnetic Moat ---

The CPU itself is a large, black building surrounded by a bottomless pit. Enormous metal tubes extend outward from the side of the building at regular intervals and descend down into the void. There's no way to cross, but you need to get inside.

No way, of course, other than building a bridge out of the magnetic components strewn about nearby.

Each component has two ports, one on each end. The ports come in all different types, and only matching types can be connected. You take an inventory of the components by their port types (your puzzle input). Each port is identified by the number of pins it uses; more pins mean a stronger connection for your bridge. A 3/7 component, for example, has a type-3 port on one side, and a type-7 port on the other.

Your side of the pit is metallic; a perfect surface to connect a magnetic, zero-pin port. Because of this, the first port you use must be of type 0. It doesn't matter what type of port you end with; your goal is just to make the bridge as strong as possible.

The strength of a bridge is the sum of the port types in each component. For example, if your bridge is made of components 0/3, 3/7, and 7/4, your bridge has a strength of 0+3 + 3+7 + 7+4 = 24.

For example, suppose you had the following components:

0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
With them, you could make the following valid bridges:

0/1
0/1--10/1
0/1--10/1--9/10
0/2
0/2--2/3
0/2--2/3--3/4
0/2--2/3--3/5
0/2--2/2
0/2--2/2--2/3
0/2--2/2--2/3--3/4
0/2--2/2--2/3--3/5
(Note how, as shown by 10/1, order of ports within a component doesn't matter. However, you may only use each port on a component once.)

Of these bridges, the strongest one is 0/1--10/1--9/10; it has a strength of 0+1 + 1+10 + 10+9 = 31.

What is the strength of the strongest bridge you can make with the components you have available?

Your puzzle answer was 1511.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

The bridge you've built isn't long enough; you can't jump the rest of the way.

In the example above, there are two longest bridges:

0/2--2/2--2/3--3/4
0/2--2/2--2/3--3/5
Of them, the one which uses the 3/5 component is stronger; its strength is 0+2 + 2+2 + 2+3 + 3+5 = 19.

What is the strength of the longest bridge you can make? If you can make multiple bridges of the longest length, pick the strongest one.

Your puzzle answer was 1471.

Both parts of this puzzle are complete! They provide two gold stars: **

"""

links = []
link_id = 0
longest_length = 0
longest_weight = 0
heaviest_weight = 0
chains_tried = 0

class Chain(object):

    def __init__(self, a, b, link_id):
        """Make a new chain link.  How many pins on a, b?"""
        self.pins = [a, b]
        self.next_link = None
        self.root = self
        self.link_id = link_id

    def weight(self):
        w = sum(self.pins)
        if self.next_link:
            w += self.next_link.weight()
        return w

    def length(self):
        l = 1
        if self.next_link:
            l += self.next_link.length()
        return l

    def matches_pin(self, pin):
        return (pin in self.pins)

    def link(self, next_link):
        if not next_link.matches_pin(self.pins[1]):
            raise ValueError("Pin mismatch. {} not found in {}."
                             .format(self.pins[1], next_link.pins))
        self.next_link = next_link
        next_link.pins = sorted(next_link.pins, key=lambda x: abs(x-self.pins[1]))
        next_link.root = self.root
        return self.next_link

    def unlink(self):
        """Returns a link to the prior link"""
        if self.root == self:
            return None
        parent = self.root
        while parent.next_link != self:
            parent = parent.next_link
        self.root = self
        parent.next_link = None
        return parent

    def is_in_chain(self, link):
        """Checks to see if a particular link is in the existing chain."""
        chain = self.root
        while chain:
            if chain == link:
                return True
            else:
                chain = chain.next_link
        return False

    def compatible_links(self):
        """Returns a list of possible next links."""
        global links
        return [z for z in filter(lambda x: (x.matches_pin(self.pins[1])
                                             and not self.is_in_chain(x)) ,links)]

    def print(self):
        print(str(self))

    def __str__(self):
        return '<{} {}>'.format(self.link_id, self.pins)

    def weigh_max_chain(self):
        max_weight = 0
        try_links = [x for x in self.compatible_links()]
        if not try_links:
            myweight = self.root.weight()
            global chains_tried
            chains_tried += 1
            global heaviest_weight
            if myweight > heaviest_weight:
                heaviest_weight = myweight
                print('Weight ', heaviest_weight)
                self.print_chain()
            return myweight
        else:
            for try_link in try_links:
                self.link(try_link)
                max_weight = max(max_weight, try_link.weigh_max_chain())
                try_link.unlink()
        return max_weight

    def make_chains(self):
        try_links = [x for x in self.compatible_links()]
        if not try_links:
            # end of chain reached
            global longest_length
            global longest_weight
            mylength = self.root.length()
            myweight = self.root.weight()
            if mylength > longest_length:
                longest_length = mylength
                longest_weight = myweight
            elif mylength == longest_length and myweight > longest_weight:
                longest_weight = myweight            
        else:
            for try_link in try_links:
                self.link(try_link)
                try_link.make_chains()
                try_link.unlink()
        return

    def print_chain(self):
        outstring = '~~'
        chain = self.root
        while chain:
            outstring += str(chain)
            chain = chain.next_link
        outstring += '~~'
        print(outstring)      
            

link_id = 0
zero_link = Chain(0, 0, link_id)
links.append(zero_link)
link_id = 1

f = open('a24_input.txt')
for line in f:
    links.append(Chain(*tuple(sorted([int(x) for x in line.strip().split('/')])), link_id))
    link_id += 1
f.close()

zero_link.make_chains()

print('Chains tried = ', chains_tried)
print('max length = ', longest_length)
print('weight of longest = ', longest_weight)

    


        

    

    

    

    

    


    



    

    


