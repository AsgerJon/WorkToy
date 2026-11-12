# Bench results for ezdata, 2026-11-12

Measured with `python -m bench ezdata` on worktoy 1.2.0 with the fixes
of the ezdata tune-up of 2026-11-12 on top. Of those only `replace` and
the comparison across a subclass run other code than in 1.2.0. Same
machine and method as `bench_results_20261111_plain_read.md`. These are
the numbers before any work on the speed of `EZData`.

The rows: a dataclass of `dataclasses`, an `EZData`, and the same
classes written with boxes, an `AttriBox` for each attribute or a
`FixBox`, each with the constructor a class of boxes writes itself. The
boxes generate no method, so a box row is blank where a class of boxes
has no such operation.

Some columns compare what a builder writes, not equal work:
`dataclasses.asdict` and `dataclasses.astuple` copy deeply, where
`asDict` and `asTuple` are shallow; an `EZData` and a box convert an
`int` given for a `float`, where a dataclass stores it as it came; and
a box builds its default at the first read, so `defaults` is cheap for
the box rows and the cost shows in the last table.

## Python 3.15.2

```
worktoy 1.2.0 on Python 3.15.2

Making an instance
==================
impl            by position              by keyword               defaults             int for float               frozen                post init
---------------------------------------------------------------------------------------------------------------------------------------------------------
dataclass      125.8 ns  x   1.0       275.2 ns  x   1.0       127.2 ns  x   1.0       124.1 ns  x   1.0       267.9 ns  x   1.0       150.0 ns  x   1.0
EZData          2.20 us  x  17.5        2.45 us  x   8.9        2.29 us  x  18.0        2.66 us  x  21.4        2.19 us  x   8.2        1.54 us  x  10.3
AttriBox        4.51 us  x  35.8                                1.05 us  x   8.2        7.77 us  x  62.6                                3.23 us  x  21.6
FixBox          5.88 us  x  46.8                                1.04 us  x   8.1        9.48 us  x  76.4                                4.02 us  x  26.8

ratios are against the 'dataclass' row.

Using an instance
=================
impl                read                   write                   unpack                as a dict               as a tuple               replace                   repr
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
dataclass       11.4 ns  x   1.0        26.3 ns  x   1.0                               919.9 ns  x   1.0       929.4 ns  x   1.0       833.0 ns  x   1.0       516.0 ns  x   1.0
EZData          23.3 ns  x   2.1       253.7 ns  x   9.6           320.8 ns            203.4 ns  x   0.2       445.4 ns  x   0.5        2.84 us  x   3.4       899.9 ns  x   1.7
AttriBox       188.3 ns  x  16.6        1.52 us  x  57.5
FixBox         186.9 ns  x  16.5

ratios are against the 'dataclass' row.

Comparing two instances
=======================
impl               equal                  unequal            a frozen subclass              hash                 less than              sorted, 100
---------------------------------------------------------------------------------------------------------------------------------------------------------
dataclass       87.5 ns  x   1.0        75.0 ns  x   1.0                               142.3 ns  x   1.0       115.4 ns  x   1.0       57.02 us  x   1.0
EZData         955.0 ns  x  10.9       965.5 ns  x  12.9           29.53 us            547.2 ns  x   3.8       958.4 ns  x   8.3      472.68 us  x   8.3

ratios are against the 'dataclass' row.

An instance and the first read of a built default
=================================================
impl               a list             a nested object
---------------------------------------------------------
dataclass      131.7 ns  x   1.0       252.6 ns  x   1.0
EZData          1.77 us  x  13.5        4.68 us  x  18.5
AttriBox        5.79 us  x  44.0        7.93 us  x  31.4
FixBox          5.92 us  x  44.9        8.01 us  x  31.7

ratios are against the 'dataclass' row.
```

## Python 3.7.12

```
worktoy 1.2.0 on Python 3.7.12

Making an instance
==================
impl            by position              by keyword               defaults             int for float               frozen                post init
---------------------------------------------------------------------------------------------------------------------------------------------------------
dataclass      188.9 ns  x   1.0       258.7 ns  x   1.0       175.9 ns  x   1.0       186.7 ns  x   1.0       404.3 ns  x   1.0       264.9 ns  x   1.0
EZData          3.40 us  x  18.0        3.59 us  x  13.9        4.74 us  x  26.9        4.24 us  x  22.7        3.33 us  x   8.2        2.62 us  x   9.9
AttriBox        8.25 us  x  43.7                                1.67 us  x   9.5       13.56 us  x  72.6                                5.95 us  x  22.5
FixBox         10.57 us  x  56.0                                1.72 us  x   9.8       16.56 us  x  88.7                                7.29 us  x  27.5

ratios are against the 'dataclass' row.

Using an instance
=================
impl                read                   write                   unpack                as a dict               as a tuple               replace                   repr
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
dataclass       22.5 ns  x   1.0        25.0 ns  x   1.0                                3.60 us  x   1.0        3.43 us  x   1.0       974.1 ns  x   1.0       775.8 ns  x   1.0
EZData          49.0 ns  x   2.2       483.3 ns  x  19.4           484.6 ns            487.9 ns  x   0.1       704.7 ns  x   0.2        4.41 us  x   4.5        1.41 us  x   1.8
AttriBox       451.4 ns  x  20.1        2.88 us  x 115.2
FixBox         491.2 ns  x  21.8

ratios are against the 'dataclass' row.

Comparing two instances
=======================
impl               equal                  unequal            a frozen subclass              hash                 less than              sorted, 100
---------------------------------------------------------------------------------------------------------------------------------------------------------
dataclass      207.8 ns  x   1.0       216.0 ns  x   1.0                               220.2 ns  x   1.0       219.0 ns  x   1.0      105.66 us  x   1.0
EZData          1.55 us  x   7.4        1.54 us  x   7.1           50.90 us            794.0 ns  x   3.6        1.49 us  x   6.8      736.80 us  x   7.0

ratios are against the 'dataclass' row.

An instance and the first read of a built default
=================================================
impl               a list             a nested object
---------------------------------------------------------
dataclass      220.3 ns  x   1.0       368.3 ns  x   1.0
EZData          2.74 us  x  12.4        8.96 us  x  24.3
AttriBox       10.67 us  x  48.4       14.39 us  x  39.1
FixBox         11.27 us  x  51.1       15.80 us  x  42.9

ratios are against the 'dataclass' row.
```

## What stands out

- Among the three worktoy ways, an `EZData` is the fastest wherever
  work is done: made by position in 2.2 microseconds against 4.5 for a
  class of `AttriBox` fields and 5.9 for one of `FixBox` fields, read
  in 23 nanoseconds against 188, written in 254 against 1520. The
  boxes are ahead only in `defaults`, where they build nothing until
  the first read; with that read counted, the last table, an `EZData`
  is three times ahead for a list.
- A `FixBox` class costs about a third more to make than an `AttriBox`
  class: each first write also looks whether a value is there already.
- A class with a `__post_init__` builds faster than one without: 1.54
  against 2.20 microseconds on 3.15. The constructor looks the hook up
  and catches the `AttributeError` when there is none, and that costs
  more than calling one.
- Comparing an instance with one of a frozen subclass takes about 30
  microseconds, thirty times a comparison within one class:
  `isCongruent` builds the signature of both classes through the
  metaclass at every call.
- `asDict` and `asTuple` are the two places an `EZData` is ahead of a
  dataclass, by doing less: they are shallow.
