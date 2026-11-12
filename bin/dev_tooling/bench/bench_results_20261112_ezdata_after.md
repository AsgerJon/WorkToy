# Bench results for ezdata after the speed step, 2026-11-12

Measured with `python -m bench ezdata` on worktoy 1.2.0 with the work of
the ezdata tune-up and of the night after it on top. Same machine and
method as `bench_results_20261112_ezdata.md`, which holds the numbers
before the step; the rows and the columns are explained there.

The step changed three things and no answer. The generated constructor
runs its passes over the keywords only when a keyword is given. The
constructor and the assignment store a value whose class is the field
type itself without asking for the cast, which would hand it back as it
is. And two classes are compared for congruence by the types of their
fields directly, where a `TypeSig` of each was built through the getters
of the metaclass.

## Python 3.15.2

```
worktoy 1.2.0 on Python 3.15.2

Making an instance
==================
impl            by position              by keyword               defaults             int for float               frozen                post init
---------------------------------------------------------------------------------------------------------------------------------------------------------
dataclass      125.5 ns  x   1.0       272.4 ns  x   1.0       139.7 ns  x   1.0       122.7 ns  x   1.0       261.0 ns  x   1.0       159.1 ns  x   1.0
EZData          1.78 us  x  14.2        2.30 us  x   8.4        2.11 us  x  15.1        2.41 us  x  19.7        1.79 us  x   6.9        1.30 us  x   8.2
AttriBox        4.69 us  x  37.4                                1.08 us  x   7.8        8.03 us  x  65.4                                3.26 us  x  20.5
FixBox          6.15 us  x  49.0                                1.09 us  x   7.8        9.63 us  x  78.5                                4.08 us  x  25.6

ratios are against the 'dataclass' row.

Using an instance
=================
impl                read                   write                   unpack                as a dict               as a tuple               replace                   repr
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
dataclass       11.4 ns  x   1.0        26.7 ns  x   1.0                               910.1 ns  x   1.0       929.0 ns  x   1.0       835.0 ns  x   1.0       502.4 ns  x   1.0
EZData          23.7 ns  x   2.1       191.1 ns  x   7.2           327.8 ns            226.8 ns  x   0.2       475.9 ns  x   0.5        2.64 us  x   3.2       882.7 ns  x   1.8
AttriBox       188.8 ns  x  16.6        1.54 us  x  57.9
FixBox         189.2 ns  x  16.6

ratios are against the 'dataclass' row.

Comparing two instances
=======================
impl               equal                  unequal            a frozen subclass              hash                 less than              sorted, 100
---------------------------------------------------------------------------------------------------------------------------------------------------------
dataclass       87.5 ns  x   1.0        74.3 ns  x   1.0                               145.9 ns  x   1.0       116.9 ns  x   1.0       58.41 us  x   1.0
EZData         971.9 ns  x  11.1       976.8 ns  x  13.1            2.05 us            548.7 ns  x   3.8       965.6 ns  x   8.3      484.87 us  x   8.3

ratios are against the 'dataclass' row.

An instance and the first read of a built default
=================================================
impl               a list             a nested object
---------------------------------------------------------
dataclass      135.1 ns  x   1.0       254.2 ns  x   1.0
EZData          1.55 us  x  11.5        4.13 us  x  16.2
AttriBox        5.88 us  x  43.5        7.88 us  x  31.0
FixBox          5.85 us  x  43.3        8.04 us  x  31.6

ratios are against the 'dataclass' row.
```

## Python 3.7.12

```
worktoy 1.2.0 on Python 3.7.12

Making an instance
==================
impl            by position              by keyword               defaults             int for float               frozen                post init
---------------------------------------------------------------------------------------------------------------------------------------------------------
dataclass      192.0 ns  x   1.0       263.6 ns  x   1.0       178.3 ns  x   1.0       190.1 ns  x   1.0       410.0 ns  x   1.0       260.1 ns  x   1.0
EZData          2.49 us  x  13.0        3.13 us  x  11.9        4.12 us  x  23.1        4.01 us  x  21.1        2.52 us  x   6.1        2.01 us  x   7.7
AttriBox        8.33 us  x  43.4                                1.61 us  x   9.0       13.44 us  x  70.7                                5.93 us  x  22.8
FixBox         10.58 us  x  55.1                                1.61 us  x   9.0       15.94 us  x  83.9                                7.26 us  x  27.9

ratios are against the 'dataclass' row.

Using an instance
=================
impl                read                   write                   unpack                as a dict               as a tuple               replace                   repr
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
dataclass       21.5 ns  x   1.0        25.6 ns  x   1.0                                3.53 us  x   1.0        3.35 us  x   1.0       977.2 ns  x   1.0       776.0 ns  x   1.0
EZData          48.3 ns  x   2.2       335.2 ns  x  13.1           472.2 ns            485.6 ns  x   0.1       697.0 ns  x   0.2        3.89 us  x   4.0        1.40 us  x   1.8
AttriBox       460.7 ns  x  21.4        2.91 us  x 113.9
FixBox         514.8 ns  x  24.0

ratios are against the 'dataclass' row.

Comparing two instances
=======================
impl               equal                  unequal            a frozen subclass              hash                 less than              sorted, 100
---------------------------------------------------------------------------------------------------------------------------------------------------------
dataclass      205.2 ns  x   1.0       210.1 ns  x   1.0                               228.4 ns  x   1.0       220.6 ns  x   1.0      106.77 us  x   1.0
EZData          1.53 us  x   7.4        1.54 us  x   7.3            3.38 us            792.6 ns  x   3.5        1.48 us  x   6.7      743.62 us  x   7.0

ratios are against the 'dataclass' row.

An instance and the first read of a built default
=================================================
impl               a list             a nested object
---------------------------------------------------------
dataclass      222.0 ns  x   1.0       365.3 ns  x   1.0
EZData          2.27 us  x  10.2        8.07 us  x  22.1
AttriBox       10.76 us  x  48.5       14.62 us  x  40.0
FixBox         11.23 us  x  50.6       15.18 us  x  41.5

ratios are against the 'dataclass' row.
```

## Against the numbers before the step

`EZData` rows only, the cells the step touches.

```
                             3.15.2                  3.7.12
                         before     after       before     after
made by position        2.20 us   1.78 us      3.40 us   2.49 us
made by keyword         2.45 us   2.30 us      3.59 us   3.13 us
made of defaults        2.29 us   2.11 us      4.74 us   4.12 us
an int for a float      2.66 us   2.41 us      4.24 us   4.01 us
frozen                  2.19 us   1.79 us      3.33 us   2.52 us
with a post init        1.54 us   1.30 us      2.62 us   2.01 us
a write                  254 ns    191 ns       483 ns    335 ns
replace                 2.84 us   2.64 us      4.41 us   3.89 us
a frozen subclass      29.53 us   2.05 us     50.90 us   3.38 us
a list default          1.77 us   1.55 us      2.74 us   2.27 us
a nested default        4.68 us   4.13 us      8.96 us   8.07 us
```

No other cell runs changed code. They moved by what the harness moves
between two runs, up to about a tenth either way: `as a dict` on 3.15
reads 227 ns here against 203 before, and the `defaults` cell of the
dataclass row, which is not worktoy at all, 140 against 127.

## What is left

- When the tables above were measured, a class with a `__post_init__`
  still built faster than one without: 1.30 against 1.78 microseconds
  on 3.15. That was settled later the same day: `EZMeta` holds `None`
  at the name, so the lookup of a hook that is not there raises
  nothing. Timed back to back with `timeit` on 3.15.2, a dataclass of
  two floats without the hook builds in 1.50 microseconds where it
  took 1.90, the same as one with a hook (1.52). The tables were not
  measured again.
- About 0.3 microseconds of every construction is
  `AbstractMetaclass.__call__`, which every class built by `BaseMeta`
  pays.
- Equality inside one class, the hash and the ordering are as they
  were: each builds the tuple of the values through the generator
  `__iter__` of the instance.
