
"""Part 2 - It's really counting up all the composite numbers
in a given range."""


def slow_prime(x):
    y = 2
    while x % y != 0 and y < x:
        y += 1
    if y < x:
        return False
    else:
        return True

h = 0
prime = 0
last_g = 0
# for g in range(51, 221+1, 17):
for g in range(107900, 124900+1, 17):
    if not slow_prime(g):
        h += 1
        # print('composite: ', g)
    else:
        prime += 1
        # print('prime: ', g)
    last_g = g

print('composites h: ', h)
print('primes: ', prime) 


