# Bench results after the plain read, 2026-11-11

Measured with `python -m bench` on worktoy 1.2.0-dev1 with one change
on top: 'AttriBox.__get__' hands a stored value out without a frame
when no read hook is to run. Same machine and method as
`bench_results_20261111.md`, which holds the numbers before the change.

## Python 3.15.2

```
worktoy 1.2.0-dev1 on Python 3.15.2

A point with two float attributes
=================================
impl             construct                  read                   write
---------------------------------------------------------------------------------
plain           98.6 ns  x   1.0        12.4 ns  x   1.0        13.6 ns  x   1.0
slots           95.8 ns  x   1.0        11.9 ns  x   1.0        12.7 ns  x   0.9
dataclass       97.6 ns  x   1.0        12.3 ns  x   1.0        13.3 ns  x   1.0
ezdata          2.46 us  x  25.0        24.9 ns  x   2.0       268.6 ns  x  19.8
attribox        4.89 us  x  49.6       202.8 ns  x  16.3        1.66 us  x 122.1
field           6.19 us  x  62.8        2.67 us  x 215.5        2.19 us  x 161.4
fastbox        424.7 ns  x   4.3       106.0 ns  x   8.5       139.6 ns  x  10.3

ratios are against the 'plain' row.

One call, by the type of its argument
=====================================
impl                         int                    float              bool, a subclass
------------------------------------------------------------------------------------------
plain method             28.8 ns  x   1.0        30.3 ns  x   1.0        28.5 ns  x   1.0
isinstance by hand       44.5 ns  x   1.5        75.9 ns  x   2.5        45.9 ns  x   1.6
singledispatch          311.4 ns  x  10.8       309.6 ns  x  10.2       321.7 ns  x  11.3
overload                840.8 ns  x  29.2       854.2 ns  x  28.2        1.68 us  x  58.9

ratios are against the 'plain method' row.

The routes of an overload
=========================
impl                              call
-----------------------------------------------
exact type                   850.3 ns  x   1.0
subclass (bool for int)       1.71 us  x   2.0
widened (int for float)       3.22 us  x   3.8
two arguments, exact         863.9 ns  x   1.0

ratios are against the 'exact type' row.

An enumeration of seven members
===============================
impl            Day.TUESDAY            Day['TUESDAY']          Day('tirsdag')             m.value                   d[m]                 list(Day)
---------------------------------------------------------------------------------------------------------------------------------------------------------
enum.Enum       11.9 ns  x   1.0        42.1 ns  x   1.0       224.2 ns  x   1.0        97.4 ns  x   1.0        95.0 ns  x   1.0       667.4 ns  x   1.0
KeeNum          69.6 ns  x   5.8       663.7 ns  x  15.8        1.45 us  x   6.5        12.3 ns  x   0.1        72.2 ns  x   0.8       392.2 ns  x   0.6

ratios are against the 'enum.Enum' row.

Three flags
===========
impl               a | b                   ab & a                  ab ^ a                    ~a                   bool(a)
---------------------------------------------------------------------------------------------------------------------------------
enum.Flag      486.3 ns  x   1.0       491.2 ns  x   1.0       489.5 ns  x   1.0        98.8 ns  x   1.0        79.8 ns  x   1.0
KeeFlags       550.6 ns  x   1.1       595.2 ns  x   1.2       614.6 ns  x   1.3        1.24 us  x  12.6        74.2 ns  x   0.9

ratios are against the 'enum.Flag' row.

A field over an enumeration
===========================
impl                   first read              later read            assign member            assign name
---------------------------------------------------------------------------------------------------------------
plain attribute      164.2 ns  x   1.0        12.5 ns  x   1.0        12.3 ns  x   1.0
AttriBox             10.09 us  x  61.5       204.3 ns  x  16.4        1.66 us  x 135.0            4.60 us

ratios are against the 'plain attribute' row.

One class statement
===================
impl                      class statement
---------------------------------------------
plain class                 4.38 us  x   1.0
dataclass                 212.19 us  x  48.4
BaseObject, two boxes     121.34 us  x  27.7
EZData, two fields        251.49 us  x  57.4
enum.Enum, seven           66.25 us  x  15.1
KeeNum, seven             489.69 us  x 111.7

ratios are against the 'plain class' row.

A flags class
=============
impl              2 flags                 4 flags                 6 flags
---------------------------------------------------------------------------------
enum.Flag      68.44 us  x   1.0       83.93 us  x   1.0       97.66 us  x   1.0
KeeFlags      165.48 us  x   2.4      270.01 us  x   3.2      538.02 us  x   5.5

ratios are against the 'enum.Flag' row.

A fresh interpreter, to the end of the import
=============================================
impl                 no bytecode cache        bytecode cached
-----------------------------------------------------------------
interpreter alone      12.00 ms  x   1.0       11.57 ms  x   1.0
standard library       18.49 ms  x   1.5       19.83 ms  x   1.7
worktoy               199.36 ms  x  16.6       97.17 ms  x   8.4

ratios are against the 'interpreter alone' row.
```

## Python 3.7.12

```
worktoy 1.2.0-dev1 on Python 3.7.12

A point with two float attributes
=================================
impl             construct                  read                   write
---------------------------------------------------------------------------------
plain          185.3 ns  x   1.0        21.2 ns  x   1.0        24.9 ns  x   1.0
slots          157.7 ns  x   0.9        19.9 ns  x   0.9        21.8 ns  x   0.9
dataclass      197.8 ns  x   1.1        21.2 ns  x   1.0        24.8 ns  x   1.0
ezdata          3.67 us  x  19.8        49.0 ns  x   2.3       506.1 ns  x  20.3
attribox        8.73 us  x  47.1       477.5 ns  x  22.5        3.06 us  x 123.1
field          10.79 us  x  58.2        5.11 us  x 240.8        4.05 us  x 163.0
fastbox        628.5 ns  x   3.4       147.6 ns  x   7.0       242.7 ns  x   9.8

ratios are against the 'plain' row.

One call, by the type of its argument
=====================================
impl                         int                    float              bool, a subclass
------------------------------------------------------------------------------------------
plain method             62.0 ns  x   1.0        62.7 ns  x   1.0        62.5 ns  x   1.0
isinstance by hand      119.4 ns  x   1.9       183.8 ns  x   2.9       123.8 ns  x   2.0
singledispatch          532.5 ns  x   8.6       527.0 ns  x   8.4       534.3 ns  x   8.6
overload                 1.20 us  x  19.3        1.20 us  x  19.2        2.27 us  x  36.3

ratios are against the 'plain method' row.

The routes of an overload
=========================
impl                              call
-----------------------------------------------
exact type                    1.20 us  x   1.0
subclass (bool for int)       2.26 us  x   1.9
widened (int for float)       4.86 us  x   4.1
two arguments, exact          1.26 us  x   1.0

ratios are against the 'exact type' row.

An enumeration of seven members
===============================
impl            Day.TUESDAY            Day['TUESDAY']          Day('tirsdag')             m.value                   d[m]                 list(Day)
---------------------------------------------------------------------------------------------------------------------------------------------------------
enum.Enum       75.9 ns  x   1.0       150.1 ns  x   1.0       457.2 ns  x   1.0       223.2 ns  x   1.0       170.7 ns  x   1.0        1.46 us  x   1.0
KeeNum         168.0 ns  x   2.2        1.32 us  x   8.8        2.80 us  x   6.1        49.4 ns  x   0.2       144.0 ns  x   0.8       640.0 ns  x   0.4

ratios are against the 'enum.Enum' row.

Three flags
===========
impl               a | b                   ab & a                  ab ^ a                    ~a                   bool(a)
---------------------------------------------------------------------------------------------------------------------------------
enum.Flag      870.6 ns  x   1.0       864.1 ns  x   1.0       864.6 ns  x   1.0        8.14 us  x   1.0       210.1 ns  x   1.0
KeeFlags        1.06 us  x   1.2        1.11 us  x   1.3        1.13 us  x   1.3        1.85 us  x   0.2       168.6 ns  x   0.8

ratios are against the 'enum.Flag' row.

A field over an enumeration
===========================
impl                   first read              later read            assign member            assign name
---------------------------------------------------------------------------------------------------------------
plain attribute      361.1 ns  x   1.0        21.3 ns  x   1.0        25.3 ns  x   1.0
AttriBox             18.85 us  x  52.2       476.0 ns  x  22.3        3.03 us  x 119.8            9.30 us

ratios are against the 'plain attribute' row.

One class statement
===================
impl                      class statement
---------------------------------------------
plain class                 4.59 us  x   1.0
dataclass                 227.60 us  x  49.6
BaseObject, two boxes     160.66 us  x  35.0
EZData, two fields        349.62 us  x  76.2
enum.Enum, seven           62.99 us  x  13.7
KeeNum, seven             715.63 us  x 156.0

ratios are against the 'plain class' row.

A flags class
=============
impl              2 flags                 4 flags                 6 flags
---------------------------------------------------------------------------------
enum.Flag      52.61 us  x   1.0       62.27 us  x   1.0       74.11 us  x   1.0
KeeFlags      223.46 us  x   4.2      459.25 us  x   7.4      826.48 us  x  11.2

ratios are against the 'enum.Flag' row.

A fresh interpreter, to the end of the import
=============================================
impl                 no bytecode cache
-----------------------------------------
interpreter alone      11.03 ms  x   1.0
standard library       21.99 ms  x   2.0
worktoy               135.28 ms  x  12.3

ratios are against the 'interpreter alone' row.
```
