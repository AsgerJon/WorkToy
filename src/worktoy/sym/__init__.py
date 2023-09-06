"""WorkToy - SYM
Symbolic classes (Enum implementation)

Procedure for creation of symbolic classes.

The new class should inherit from a symbolic baseclass such as the 'SYM'
class which may be used directly or as a baseclass for a custom
implementation. In the class body of the new class, create the instances.
The 'SYM' class provides a way of creating instances. The default
implementation uses the 'auto' method. For example,

  class WeekDay(SYM):
    # Symbolic class representation of weekdays
    MONDAY=SYM.auto()
    TUESDAY=SYM.auto()
    ...

Note that the instances are named in upper case as is convention. The base
implementation is case-insensitive, but presents instances in upper case.
This means that:

 WeekDay.Wednesday is 'WeekDay.WEDNESDAY'

The SYM baseclass implements hashing allowing dictionaries to use
instances as keys. The SYM baseclass also implements '__eq__' and '__ne__'.

In the SyMeta metaclass, the SymSpace class is used to provide the
namespace object returned by the '__prepare__' method. The SymSpace class
relies on the SYM-subclass to decide if an entry in the class body denotes
an instance creation. The SymSpace dictionary splits the data to
instanceSpace and to namespace. The namespace data is then used in the
super call as part of the normal class creation process, and the
instanceSpace data is used in the __init__ method on the metaclass to
facilitate instance creation. Finally, the metaclass implements the
__call__ method to restrict instance creation to those instances defined
in the instanceSpace.

A custom implementation of the SYM class must provide the following to be
recognized by the rest of the SYM module:
  - Identification. The custom implementation should explicitly define
  itself as a symbolic baseclass by setting:
    '__symbolic_baseclass__ = True'
  If no baseclass has this variable set, the SymSpace defaults to using
  the default SYM class, even if an intended symbolic baseclass is
  present. This allows symbolic classes to inherit from other classes.

  - Validation. The custom implementation must provide a method called
  'validateInstance' mapping '[str, object] -> bool' which is used by the
  SymSpace instance to determine when an entry in the class body is to
  mean instance of the symbolic class.

  - Differentiation. The custom implementation must set a unique value on
  each instance. By default, this value is an integer assigned in the order
  received in the class body beginning at '0'. Custom implementations are
  free to use any data type and reimplement the '__eq__' method as
  appropriate.

  - Instantiation. The custom implementation is responsible for creating
  the instance given a key, value pair. The default implementation creates
  a base instance of the new class and an instance of itself that wraps
  it. Please note that the default implementation requires the new class
  to support instance creation with: 'instance = NewClass()'. Otherwise,
  necessary arguments must be provided in the class body, for example,
    * 'instance = SYM.auto(420, 69)'
    The above will result in the 'instance' wrapping: 'NewClass(420, 69)'

  - Parsing (OPTIONAL). If provided, the 'parseInstance' method should take
  '*args, **kwargs' and return the instance matching or raise a NameError.
  The default implementation allows for the new class to be callable. By
  default, the instance value ('int') or the instance ('name') may be used
  to retrieve the desired instance by calling the class. For example:
    WeekDay.Tuesday == WeekDay('tuesday')  # case-insensitive
  If the parsing method is not defined, or the new class itself implements
  '__call__' the above will not be available.

  - Decoration (OPTIONAL). The default implementation provides the
  following enhancements of the new class:
    * Iteration:
      for item in 'Weekday':
        - 'Weekday.MONDAY'  # the wrapped instance
        - 'Weekday.TUESDAY'
        ...
      The above is achieved with '__iter__', '__next__' and '__len__'
      implemented as class methods. The '__len__' is taken to mean the
      number of instances on the class.
    * Dictionary-like behaviour:
      - Implementation of 'keys', 'values' and 'items'.
      - Implementation of '__getitem__':
        * 'Weekday[0]' -> 'Weekday.MONDAY'  # 'int' refers to value
        * 'Weekday['monday']' -> 'Weekday.MONDAY'  # 'str' refers to name
      - Implementation of binary arithmetic operations including cases of
        reflected operands.
        * 'Weekday[2] + 3' = 'Weekday.SATURDAY'  # SYM.__add__(self, other)
        * '3 + Weekday[2] = 5'  # SYM.__radd__(self, other)
        * 'Weekday[2] += 1 -> Weekday[3]' # SYM.__iadd__(self, other)
        The arithmetic implementation provides integer like behaviour. So
        when an instance appears as the 'other' operand, it behaves like an
        integer of the same value as itself.
        Instances use modular arithmetic such that:
          - 'Weekday.SATURDAY' + 2 -> 'Weekday.MONDAY'
        In general with n = len(SYM):
          -  'SYM.INSTANCE[a] + SYM.INSTANCE[b] = SYM.INSTANCE[(a + b) % n]'
  The default implementation provides parsing such that:
    Weekday(4) -> 'Weekday.FRIDAY'
    Weekday('friday') -> 'Weekday.FRIDAY'  # Case insensitive by default.
"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._sym import SYM
from ._symspace import SymSpace
from ._symeta import SyMeta, BaseSym
from ._accessor_sym import AccessorSym
from ._weekday import Weekday
from ._month import Month
