"""--- Day 20: Particle Swarm ---

Suddenly, the GPU contacts you, asking for help. Someone has asked it to simulate too many particles, and it won't be able to finish them all in time to render the next frame at this rate.

It transmits to you a buffer (your puzzle input) listing each particle in order (starting with particle 0, then particle 1, particle 2, and so on). For each particle, it provides the X, Y, and Z coordinates for the particle's position (p), velocity (v), and acceleration (a), each in the format <X,Y,Z>.

Each tick, all particles are updated simultaneously. A particle's properties are updated in the following order:

Increase the X velocity by the X acceleration.
Increase the Y velocity by the Y acceleration.
Increase the Z velocity by the Z acceleration.
Increase the X position by the X velocity.
Increase the Y position by the Y velocity.
Increase the Z position by the Z velocity.
Because of seemingly tenuous rationale involving z-buffering, the GPU would like to know which particle will stay closest to position <0,0,0> in the long term. Measure this using the Manhattan distance, which in this situation is simply the sum of the absolute values of a particle's X, Y, and Z position.

For example, suppose you are only given two particles, both of which stay entirely on the X-axis (for simplicity). Drawing the current states of particles 0 and 1 (in that order) with an adjacent a number line and diagram of current X positions (marked in parenthesis), the following would take place:

p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>                         (0)(1)

p=< 4,0,0>, v=< 1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 2,0,0>, v=<-2,0,0>, a=<-2,0,0>                      (1)   (0)

p=< 4,0,0>, v=< 0,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-2,0,0>, v=<-4,0,0>, a=<-2,0,0>          (1)               (0)

p=< 3,0,0>, v=<-1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-8,0,0>, v=<-6,0,0>, a=<-2,0,0>                         (0)   
At this point, particle 1 will never be closer to <0,0,0> than particle 0, and so, in the long run, particle 0 will stay closest.

Which particle will stay closest to position <0,0,0> in the long term?

Your puzzle answer was 364.

"""
class Particle(object):

    def __init__(self, p, v, a):
        """Supply position, velocity, and acceleration as tuples"""
        self.p = list(p)
        self.v = list(v)
        self.a = list(a)
        self.crashed = False

    def print(self):
        print("p={} v={} a={}".format(self.p, self.v, self.a))

    def tick(self):
        """Update particle one time tick."""
        self.v = [v + a for v, a in zip(self.v, self.a)]
        self.p = [p + v for p, v in zip(self.p, self.v)]

    def manhattan(self):
        """Return the manhattan distance to the origin."""
        return sum([abs(x) for x in self.p])

class Swarm(object):

    def __init__(self, filename):
        self.particles = []
        self.ticks = 0
        f = open(filename, 'r')
        for line in f:
            rawp, rawv, rawa = [y.split(',') for y in [x[x.index('<')+1:x.index('>')] for x in line.split()]]
            p = [int(x) for x in rawp]
            v = [int(x) for x in rawv]
            a = [int(x) for x in rawa]
            self.particles.append(Particle(p, v, a))
        self.active_particles = len(self.particles)

    def tick(self, ticks = 1):
        for _ in range(ticks):
            self.ticks += 1
            for part in self.particles:
                part.tick()
            self.collision_scan()

    def collision_scan(self):
        # collect all possible crashes
        crashed = 0
        crashes = {}
        for i, part in enumerate(self.particles):
            if not part.crashed:
                if tuple(part.p) in crashes:
                    crashes[tuple(part.p)].append(i)
                else:
                    crashes[tuple(part.p)] = [i]
        # mark any particles involved in a crash
        for c in crashes:
            if len(crashes[c]) > 1:
                # print('tick {} crashed {}'.format(self.ticks, crashes[c]))
                for x in crashes[c]:
                    self.particles[x].crashed = True
                    crashed += 1
                    self.active_particles -= 1
        return crashed

    def closest(self):
        candidate = 0
        candidate_distance = self.particles[0].manhattan()
        for i, part in enumerate(self.particles):
            if part.manhattan() < candidate_distance:
                candidate = i
                candidate_distance = part.manhattan()
        return candidate

swarm = Swarm('a20_input.txt')
swarm.tick(1000)
print('nearest particle = ', swarm.closest())


