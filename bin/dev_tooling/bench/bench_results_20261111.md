# Bench results, 2026-11-11

Measured with `python -m bench` on worktoy 1.2.0-dev1, on one machine,
Python 3.15.2 and 3.7.12. Each cell is the best of seven runs, with its
ratio against the baseline row of its table. The flags classes are
timed once each, best of five, and the import in fresh interpreters,
best of seven. Absolute times belong to the machine; the ratios are the
part that carries over.

The subjects are written the way a reasonable builder writes with
worktoy. Deprecated features and last-resort fallbacks are not
measured.

## Python 3.15.2

```
worktoy 1.2.0-dev1 on Python 3.15.2

A point with two float attributes
=================================
impl             construct                  read                   write
---------------------------------------------------------------------------------
plain           96.1 ns  x   1.0        11.8 ns  x   1.0        12.8 ns  x   1.0
slots           93.3 ns  x   1.0        11.3 ns  x   1.0        12.3 ns  x   1.0
dataclass       93.1 ns  x   1.0        11.4 ns  x   1.0        12.3 ns  x   1.0
ezdata          2.35 us  x  24.5        23.6 ns  x   2.0       265.9 ns  x  20.7
attribox        4.58 us  x  47.7        2.11 us  x 179.4        1.55 us  x 120.9
field           6.14 us  x  63.9        2.69 us  x 229.0        2.31 us  x 179.9
fastbox        432.5 ns  x   4.5       108.0 ns  x   9.2       142.9 ns  x  11.1

ratios are against the 'plain' row.

One call, by the type of its argument
=====================================
impl                         int                    float              bool, a subclass
------------------------------------------------------------------------------------------
plain method             29.7 ns  x   1.0        30.1 ns  x   1.0        28.5 ns  x   1.0
isinstance by hand       44.1 ns  x   1.5        76.1 ns  x   2.5        47.0 ns  x   1.7
singledispatch          309.9 ns  x  10.4       317.9 ns  x  10.5       317.5 ns  x  11.1
overload                771.0 ns  x  26.0       775.5 ns  x  25.7        1.53 us  x  53.6

ratios are against the 'plain method' row.

The routes of an overload
=========================
impl                              call
-----------------------------------------------
exact type                   762.7 ns  x   1.0
subclass (bool for int)       1.55 us  x   2.0
widened (int for float)       3.19 us  x   4.2
two arguments, exact         837.2 ns  x   1.1

ratios are against the 'exact type' row.

An enumeration of seven members
===============================
impl            Day.TUESDAY            Day['TUESDAY']          Day('tirsdag')             m.value                   d[m]                 list(Day)
---------------------------------------------------------------------------------------------------------------------------------------------------------
enum.Enum       13.1 ns  x   1.0        42.5 ns  x   1.0       216.8 ns  x   1.0        95.5 ns  x   1.0        88.6 ns  x   1.0       625.7 ns  x   1.0
KeeNum          64.8 ns  x   4.9       616.6 ns  x  14.5        1.36 us  x   6.3        11.6 ns  x   0.1        73.0 ns  x   0.8       398.1 ns  x   0.6

ratios are against the 'enum.Enum' row.

Three flags
===========
impl               a | b                   ab & a                  ab ^ a                    ~a                   bool(a)
---------------------------------------------------------------------------------------------------------------------------------
enum.Flag      483.1 ns  x   1.0       501.7 ns  x   1.0       499.8 ns  x   1.0        95.4 ns  x   1.0        73.4 ns  x   1.0
KeeFlags       534.5 ns  x   1.1       572.2 ns  x   1.1       579.3 ns  x   1.2        1.19 us  x  12.5        71.9 ns  x   1.0

ratios are against the 'enum.Flag' row.

A field over an enumeration
===========================
impl                   first read              later read            assign member            assign name
---------------------------------------------------------------------------------------------------------------
plain attribute      160.1 ns  x   1.0        12.0 ns  x   1.0        12.0 ns  x   1.0
AttriBox              8.97 us  x  56.0        2.19 us  x 182.4        1.61 us  x 134.4            4.52 us

ratios are against the 'plain attribute' row.

One class statement
===================
impl                      class statement
---------------------------------------------
plain class                 4.19 us  x   1.0
dataclass                 204.38 us  x  48.8
BaseObject, two boxes     115.22 us  x  27.5
EZData, two fields        238.68 us  x  57.0
enum.Enum, seven           64.10 us  x  15.3
KeeNum, seven             466.85 us  x 111.5

ratios are against the 'plain class' row.

A flags class
=============
impl              2 flags                 4 flags                 6 flags        
---------------------------------------------------------------------------------
enum.Flag     111.15 us  x   1.0      138.98 us  x   1.0      182.67 us  x   1.0 
KeeFlags      254.68 us  x   2.3      456.13 us  x   3.3      971.77 us  x   5.3 

ratios are against the 'enum.Flag' row.

A fresh interpreter, to the end of the import
=============================================
impl                 no bytecode cache        bytecode cached
-----------------------------------------------------------------
interpreter alone      11.44 ms  x   1.0       11.66 ms  x   1.0
standard library       19.40 ms  x   1.7       19.16 ms  x   1.6
worktoy               197.29 ms  x  17.2       94.36 ms  x   8.1

ratios are against the 'interpreter alone' row.
```

## Python 3.7.12

Python 3.7 cannot keep its bytecode cache outside the source tree, so
the import is timed without a cache only.

```
worktoy 1.2.0-dev1 on Python 3.7.12

A point with two float attributes
=================================
impl             construct                  read                   write
---------------------------------------------------------------------------------
plain          194.1 ns  x   1.0        22.2 ns  x   1.0        26.4 ns  x   1.0
slots          165.6 ns  x   0.9        19.3 ns  x   0.9        21.1 ns  x   0.8
dataclass      190.4 ns  x   1.0        22.2 ns  x   1.0        24.5 ns  x   0.9
ezdata          3.63 us  x  18.7        71.5 ns  x   3.2       527.8 ns  x  20.0
attribox        8.41 us  x  43.3        4.03 us  x 181.5        2.91 us  x 110.0
field          10.28 us  x  53.0        4.77 us  x 215.0        3.93 us  x 148.7
fastbox        605.2 ns  x   3.1       132.2 ns  x   6.0       218.8 ns  x   8.3

ratios are against the 'plain' row.

One call, by the type of its argument
=====================================
impl                         int                    float              bool, a subclass
------------------------------------------------------------------------------------------
plain method             59.0 ns  x   1.0        59.7 ns  x   1.0        60.3 ns  x   1.0
isinstance by hand      108.9 ns  x   1.8       168.1 ns  x   2.8       113.0 ns  x   1.9
singledispatch          498.5 ns  x   8.5       524.5 ns  x   8.8       564.7 ns  x   9.4
overload                 1.35 us  x  22.9        1.31 us  x  21.9        2.57 us  x  42.6

ratios are against the 'plain method' row.

The routes of an overload
=========================
impl                              call
-----------------------------------------------
exact type                    1.25 us  x   1.0
subclass (bool for int)       2.38 us  x   1.9
widened (int for float)       5.03 us  x   4.0
two arguments, exact          1.32 us  x   1.1

ratios are against the 'exact type' row.

An enumeration of seven members
===============================
impl            Day.TUESDAY            Day['TUESDAY']          Day('tirsdag')             m.value                   d[m]                 list(Day)
---------------------------------------------------------------------------------------------------------------------------------------------------------
enum.Enum       78.0 ns  x   1.0       160.2 ns  x   1.0       466.1 ns  x   1.0       236.5 ns  x   1.0       171.4 ns  x   1.0        1.52 us  x   1.0
KeeNum         190.7 ns  x   2.4        1.32 us  x   8.3        2.83 us  x   6.1        59.5 ns  x   0.3       156.8 ns  x   0.9       640.4 ns  x   0.4

ratios are against the 'enum.Enum' row.

Three flags
===========
impl               a | b                   ab & a                  ab ^ a                    ~a                   bool(a)
---------------------------------------------------------------------------------------------------------------------------------
enum.Flag      879.9 ns  x   1.0       906.5 ns  x   1.0       919.4 ns  x   1.0        8.18 us  x   1.0       220.6 ns  x   1.0
KeeFlags        1.14 us  x   1.3        1.17 us  x   1.3        1.17 us  x   1.3        1.88 us  x   0.2       177.6 ns  x   0.8

ratios are against the 'enum.Flag' row.

A field over an enumeration
===========================
impl                   first read              later read            assign member            assign name
---------------------------------------------------------------------------------------------------------------
plain attribute      376.4 ns  x   1.0        22.0 ns  x   1.0        26.1 ns  x   1.0
AttriBox             18.70 us  x  49.7        4.51 us  x 205.3        3.22 us  x 123.4            9.65 us

ratios are against the 'plain attribute' row.

One class statement
===================
impl                      class statement
---------------------------------------------
plain class                 4.53 us  x   1.0
dataclass                 229.00 us  x  50.6
BaseObject, two boxes     172.67 us  x  38.1
EZData, two fields        354.56 us  x  78.3
enum.Enum, seven           64.67 us  x  14.3
KeeNum, seven             730.00 us  x 161.1

ratios are against the 'plain class' row.

A flags class
=============
impl              2 flags                 4 flags                 6 flags        
---------------------------------------------------------------------------------
enum.Flag      52.09 us  x   1.0       63.71 us  x   1.0       74.81 us  x   1.0 
KeeFlags      234.59 us  x   4.5      397.93 us  x   6.2      811.99 us  x  10.9 

ratios are against the 'enum.Flag' row.

A fresh interpreter, to the end of the import
=============================================
impl                 no bytecode cache
-----------------------------------------
interpreter alone      12.62 ms  x   1.0
standard library       23.96 ms  x   1.9
worktoy               159.27 ms  x  12.6

ratios are against the 'interpreter alone' row.
```
