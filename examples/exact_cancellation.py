from irrat import *

a = rat(5, 7)
b = rat(5476, 1053)

c = a / b
# c = (5 * 1053) / (7 * 5476)
print(str(c))
# 0.1373526035688198
print(repr(c))
# rat(5265, 38332)

# the repr should always be simplified (deliberately use a prime above 23, which means it won't
# be auto-simplified.)

d = rat(47 * 53, 3 * 3 * 23)
e = rat(3 * 19, 53 * 73)
f = d * e

print(str(f))
# 0.17728806829461982
print(repr(f))
# rat(893, 5037)

# TODO use evaluate(precision=100) to generate a long string.
