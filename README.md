irrat
=====

*An (ir)rationals library for python.*

(This library is a work in progress, and currently unfinished.)

import the rationals type:

    from irrat import *

and then use rationals:

    r = rat(22, 7)
    r2 = rat(-153, 517)
    r3 = r + r2
    print(r3 > 0.5)

They are designed to delay computation until you ask for it (e.g. via comparison.)

Still some stuff to do, they will try to completely resolve addition and subtraction, I need to find a way to delay that using new `Expression` types.

Another big TODO is computing the decimal number string representation to arbitrary precision.

Finally, we eventually want to add the `irrat` type, which can handle sqrt, PI, e, and other irrational and transcendental numbers inside the expressions.



