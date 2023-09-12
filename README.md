[![wakatime](https://wakatime.com/badge/github/AsgerJon/WorkToy.svg)](
https://wakatime.com/badge/github/AsgerJon/WorkToy)

# WorkToy v0.40.26

```
pip install worktoy
```

## Table of Contents

1. [WorkToyClass](#WorkToyClass)
    1. [maybe](#WorkToyClassmaybe)
    2. [maybeType](#WorkToyClassmaybeType)
    3. [maybeTypes](#WorkToyClassmaybeTypes)
    4. [searchKey](#WorkToyClasssearchKey)
    5. [searchKeys](#WorkToyClasssearchKeys)
    6. [maybeKey](#WorkToyClassmaybeKey)
    7. [maybeKeys](#WorkToyClassmaybeKeys)
2. [WorkToyClass.Guards](#WorkToyClass---Guards)
    1. [noneGuard](#WorkToyClassnoneGuard)
    2. [someGuard](#WorkToyClasssomeGuard)
    3. [overRideGuard](#WorkToyClassoverRideGuard)
    4. [functionGuard](#WorkToyClassfunctionGuard)
    5. [intGuard](#WorkToyClassintGuard)
    6. [strGuard](#WorkToyClassstrGuard)
3. [Descriptors](#Descriptors)
    1. [Field](#Field)
    2. [DataField](#DataField)
    3. [DataClass](#DataClass)
4. [Metaclass](#MetaClass)
    1. [type](#type)
    2. [NameSpace](#NameSpace)
5. [Wait A Minute!](#Wait-A-Minute)
    1. [MetaXcept](#MetaXcept)
    2. [MetaTypeSupportError](#MetaTypeSupportError)
    3. [FieldDecoderException](#FieldDecoderException)
    4. [FieldEncoderException](#FieldEncoderException)
    5. [MissingArgumentException](#MissingArgumentException)
    6. [RecursiveCreateGetError](#RecursiveCreateGetError)
    7. [TypeSupportError](#TypeSupportError)
    8. [UnavailableNameException](#UnavailableNameException)
    9. [UnexpectedEventException](#UnexpectedEventException)
    10. [UnsupportedSubclassException](#UnsupportedSubclassException)
6. [Core](#Core)

## WorkToyClass

Parent class providing general utility functions on the class itself.

```python

from worktoy.worktoyclass import WorkToyClass


class MyClass(WorkToyClass):
  """Example class"""

  def __init__(self, *args, **kwargs) -> None:
    WorkToyClass.__init__(self, *args, **kwargs)
```

By inheriting from the ``WorkToyClass``, instances now have access to a
collection of utility functions:

### WorkToyClass.maybe

```python

from typing import Any

from worktoy.worktoyclass import WorkToyClass


class MyClass(WorkToyClass):
  """Example class"""

  def instanceMethod(self, *args) -> Any:
    """Instance method using ``maybe`` use a default argument value."""
    return self.maybe(*args)


myInstance = MyClass()
myInstance.instanceMethod(None, [], )  # >>> []  

```

### WorkToyClass.maybeType

```python

from worktoy.worktoyclass import WorkToyClass


class MyClass(WorkToyClass):
  """Example class"""

  def instanceMethod(self, *args, **kwargs) -> int:
    """Instance method using ``maybeType`` to extract an integer from the 
    positional arguments."""
    return self.maybeType(int, *args)


myInstance = MyClass()
myInstance.instanceMethod('one', 2, '3', 4, 5)  # >>> 2  

```

### WorkToyClass.maybeTypes

```python

from worktoy.worktoyclass import WorkToyClass


class MyClass(WorkToyClass):
  """Example class"""

  def instanceMethod(self, *args, **kwargs) -> int:
    """Instance method using 'maybeTypes' to extract every integer from the 
    positional arguments."""
    out = self.maybeTypes(int, *args)
    if isinstance(out, int):
      return out


myInstance = MyClass()
myInstance.instanceMethod('one', 2, '3', 4, 5)  # >>> [2, 4, 5] 
```

### WorkToyClass.searchKey

```python

from worktoy.worktoyclass import WorkToyClass


class MyClass(WorkToyClass):
  """Example class"""

  def instanceMethod(self, *keys, **kwargs) -> int:
    """Instance method using ``searchKey`` to search for keyword argument 
    value."""
    return self.searchKey(*keys, **kwargs)


myInstance = MyClass()
myInstance.instanceMethod('count', 'Count', 'amount', count=7)  # >>> 7 
```

### WorkToyClass.searchKeys

```python

from worktoy.worktoyclass import WorkToyClass


class MyClass(WorkToyClass):
  """Example class"""

  def instanceMethod(self, *keys, **kwargs) -> int:
    """Instance method using ``searchKeys`` to search for every keyword 
    argument."""
    return self.searchKeys(*keys, **kwargs)


myInstance = MyClass()
myInstance.instanceMethod('a', 'd', 'e', a=1, b=2, c=3, d=4)  # >>> [1, 4] 
```

### WorkToyClass.maybeKey

```python

from worktoy.worktoyclass import WorkToyClass


class MyClass(WorkToyClass):
  """Example class"""

  def instanceMethod(self, *args, **kwargs) -> int:
    """Instance method using ``maybeKey`` to search for a keyword argument 
    value with a type restriction argument."""
    return self.maybeKey(*args, **kwargs)


myInstance = MyClass()
myInstance.instanceMethod('a', 'b', int, a='1', b=2, c=3, d=4)  # >>> 2 
```

### WorkToyClass.maybeKeys

```python

from worktoy.worktoyclass import WorkToyClass


class MyClass(WorkToyClass):
  """Example class"""

  def instanceMethod(self, *args, **kwargs) -> int:
    """Instance method using ``maybeKeys`` to search for every keyword 
    argument restricted to a certain type."""
    return self.maybeKeys(*args, **kwargs)


myInstance = MyClass()
myInstance.instanceMethod('a', 'b', int, a=1, b=2, c=3, d=4)  # >>> [1, 2] 
```

## WorkToyClass - Guards

The following methods are various type guards.

### WorkToyClass.noneGuard

Raises ``UnavailableNameException`` if the given object is not None.

### WorkToyClass.someGuard

Raises ``MissingArgumentException`` if given object is None

### WorkToyClass.overRideGuard

Raises ``UnavailableNameException`` if given object is not None

### WorkToyClass.functionGuard

Raises ``TypeSupportError`` if given object is not a function

### WorkToyClass.intGuard

Raises ``TypeSupportError`` if given object is None or not an integer

### WorkToyClass.floatGuard

Raises ``TypeSupportError`` if given object is None or not a float

### WorkToyClass.strGuard

Raises ``TypeSupportError`` if given object is None or not a string

## Descriptors

The Descriptors package implements descriptors. These serve as
alternatives to the ``property`` descriptor. WorkToy provides two ways of
using descriptors: ``Attribute`` and ``Field``.

### Field

This class are defined in the class body in the same way as the
attributes mentioned above. Unlike attributes, instances of Field defined
on a class body must also decorate their own accessor methods.

```python

from worktoy.worktoyclass import WorkToyClass
from worktoy.descriptors import Field


class MyClass(WorkToyClass):
  """Example class"""

  area = Field()
  width = Field()
  height = Field()

  def __init__(self, *args, **kwargs) -> None:
    WorkToyClass.__init__(self, *args, **kwargs)
    self._width = 1
    self._height = 1

  @width.GET
  def getWidth(self) -> int:
    """Getter-function for width"""
    return self._width

  @width.SET
  def setWidth(self, width: int) -> None:
    """Setter-function for width."""
    self._width = width

  @height.GET
  def getHeight(self) -> int:
    """Getter-function for height"""
    return self._height

  @height.SET
  def setHeight(self, height: int) -> None:
    """Setter-function for height."""
    self._height = height

  @area.GET
  def getArea(self) -> float:
    """Getter-Function for the area"""
    return self.width * self.height

  @area.SET
  def setArea(self, newArea: float) -> None:
    """Setter-Function for the area."""
    oldArea = self.getArea()
    if not oldArea:
      raise ZeroDivisionError
    scale = (newArea / oldArea) ** 0.5
    self.width *= scale
    self.height *= scale


myInstance = MyClass()
myInstance.width  # >>> 3
myInstance.height  # >>> 4
myInstance.area  # >>> 12
myInstance.area = 48
myInstance.width  # >>> 3
myInstance.height  # >>> 4

```

Notice the flexibility available by defining a setter function for the
``area`` field.

### DataField

This is a subclass of ``Field`` implementing automatic encoding and
decoding to json format. If the instances of DataField contain custom
classes, it is recommended to use the ``ENCODER`` and ``DECODER``
decorators to specify exactly how those values should be encoded.
DataFields holding types directly supported by ``json`` are able to rely
on the default encoder and decoder.

### DataClass

The ``DataField`` class does little on its own, but by decorating owner
classes, the class will be able to encode and decode all of its DataField
instances directly. Keep in mind the default behaviour of relying on the
``json`` package for encoding and decoding. This is sufficient for
builtin types, but custom classes must either implement ``json`` support
directly or the owned instances of ``DataField`` should specify encoding and
decoding as described above.

## MetaClass

Metaclasses are certainly the most powerful tool available in Python
development. The WorkToy package provides a basic skeleton for
implementing custom metaclasses in the form of ``AbstractMetaClass`` and
``AbstractNameSpace``. Before explaining the merits of these, a
examination of how metaclasses work seem appropriate.

### Introduction to metaclasses

You are already familiar with the default baseclass: ``type``. In a
somewhat unfortunate choice of nomenclature, we face an ambiguity here:
do we mean ``type`` as in: ``isinstance(int, type)`` or do we mean:
``type(int)``? The first treats ``type`` as a ``type``, but the second
treats ``type`` as a function. To illustrate how unfortunate this
nomenclature is, consider this expression:

``type(type) is type`` or ``isinstance(type, type) >>> True``

A ``metaclass`` is a custom ``type``. Consider ``TestClass`` defined below:

```python

from worktoy.worktoyclass import WorkToyClass


class TestClass(WorkToyClass):
  """Created with traditional class body."""

  def __init__(self, *args, **kwargs) -> None:
    WorkToyClass.__init__(self, *args, **kwargs)

  def instanceMethod(self, *args, **kwargs) -> int:
    """Instance method"""
    return self.maybeType(int, *args)
```

The above is entirely equivalent to:

```python

from typing import Any

from worktoy.worktoyclass import WorkToyClass


def initFunc(instance: Any, *args, **kwargs) -> None:
  """Init function"""
  WorkToyClass.__init__(instance, *args, **kwargs)


def someFunc(self, *args, **kwargs) -> int:
  """Instance Method"""
  return self._maybeType(int, *args)


name = 'TestClass'
bases = (WorkToyClass,)
nameSpace = dict(__init__=initFunc, instanceMethod=someFunc)
TestClass = type(name, bases, nameSpace)
```

### ``type``

The ``type`` object used above specifies the creation of new classes. By
creating a custom ``metaclass``, we are able to define our own class
creation. Below we define a ``metaclass`` that behaves entirely like
``type`` allowing us to recognize the class creation we are familiar with
and see how we can change this behaviour.

(Please note, the naming convention: ``mcls``: metaclass, ``cls``: new
class, ``self`` new instance).

```python
from typing import Any


class BaseMeta(type):  # metaclasses inherit from type
  """Base metaclass behaving line ``type``"""

  @classmethod
  def __prepare__(mcls, name: str, bases: tuple[type], **kwargs) -> dict:
    """The prepare method creates the empty mapping object providing the 
    namespace for the newly created class. The base implementation 
    returns an empty instance of ``dict``."""
    return {}

  def __new__(mcls, name: str, bases: tuple[type], nameSpace: dict,
              **kwargs) -> type:
    """The ``__new__`` method createds the new class,"""
    cls = type.__new__(mcls, name, bases, nameSpace, **kwargs)
    return cls

  def __init__(cls, name: str, bases: tuple[type], nameSpace: dict,
               **kwargs) -> None:
    """Once the new class is created it is initialised by this method. """
    type.__init__(cls, name, bases, nameSpace, **kwargs)

  def __call__(cls: type, *args, **kwargs) -> Any:
    """This method specifies how the newly creatd class creates instances 
    of itself. The default behaviour is as shown below: The instance is 
    created with the __new__ method on the newly created class, and then 
    it is initialized with the __init__ on the newly created class."""
    self = cls.__new__(cls, )
    cls.__init__(self, *args, **kwargs)
    return self
```

By introducing custom metaclasses, we are free to customize the above
steps to achieve any imaginable functionality. People say that Python
does not support function overloading. What they mean is that function
overloading in Python must be implemented at the metaclass level. (That
is dumb, function overloading should not require custom metaclasses, but
the point stands).

### ``NameSpace``

Customizing the ``__prepare__`` method gives the greatest
opportunity to customize the class creation. Let us examine the
requirements for the namespace object returned by the ``__prepare__``
method. When attempting to use a custom class for this purppose, one is
likely to encounter errors like:

```python
"""TypeError: type.__new__() argument 3 must be dict, not NameSpace"""
"""TypeError: META.__prepare__() must return a mapping, not NameSpace"""
"""TypeError: ``NameSpace`` object does not support item assignment"""
```

It is possible to create a custom class that does not trigger any such
``TypeError``, which is able to create classes without any problem. Until
one day, you introduce a ``staticmethod`` and then receive:

```python
"""
    @staticmethod
     ^^^^^^^^^^^^
TypeError: ``NoneType`` object is not callable"""
```

What even is that error message? The above happens if the ``__getitem__``
method on the namespace object does not raise a KeyError when receiving a
missing key. The expected behaviour from the namespace object receiving a
missing key is to raise a KeyError with the missing key as the message.
For example:

```python
from typing import Any


def __getitem__(self, key: str, ) -> Any:
  try:
    dict.__getitem__(self, key)
  except KeyError as e:
    print(key)
    raise e
```

By including the print statement, we can see that the problems occur
where the class body has a valid expression without an equal sign. For
example when decorating a function. Consider the following example:

```python
from typing import Any, Callable


class NameSpace(dict, ):
  """NameSpace custom class"""

  def __getitem__(self, key: str, ) -> Any:
    """Prints missing keys that are encountered."""
    try:
      return dict.__getitem__(self, key)
    except KeyError as e:
      print(key)
      raise e


class META(type):
  """Metaclass implementing the __prepare__ method which returns an
  instance of the NameSpace class."""

  @classmethod
  def __prepare__(mcls, name, bases, **kwargs) -> Any:
    nameSpace = NameSpace()
    return nameSpace


def func(f: Callable) -> None:
  """Decorator"""
  return f


class TestClass(metaclass=META):
  """TestClass """

  @staticmethod
  @func
  def a(self) -> None:
    pass


if __name__ == '__main__':
  TestClass()
```

When running the above script, we see the following printed to the console:

```python
'__name__'
'staticmethod'
'func'
```

Fortunately, WorkToy provides the ``AbstractNameSpace`` class which
implements all required mapping functionality. Besides implementing
``dict`` methods, it logs every line in the class body.

## Wait A Minute!

In this module, WorkToy provides the custom exceptions used throughout
the entire package.

### MetaXcept

Just like the SYM module, the custom exceptions
implement a custom metaclass inheriting from ``AbstractMetaClass``. This
metaclass ``MetaXcept`` uses a custom namespace class inheriting from the
``AbstractNameSpace`` in its ``__prepare__`` method.

Below is a reference list of the custom exceptions currently implemented:

### MetaTypeSupportError

#### Description

Indicates that an instance is not a member of class derived from the
correct metaclass.

#### Signature

```python

from typing import Any

expMetaClass: type  # The expected metaclass
actualValue: Any  # The actual value received
argName: str  # Argument name
```

### FieldDecoderException

Custom exception raised when an instance of ``DataField`` attempts to decode
with default JSON decoder. The exception catches the ``JSONDecodeError`` and
brings additional information.

### FieldEncoderException

Custom exception raised when an instance of ``DataField`` attempts to
serialize its value to ``JSON`` format, but where the value is not
serializable.

### MissingArgumentException

#### Description

Invoked when a function is called before it is ready.

#### Signature

```python

from typing import Any

missingArgument: str  # Argument name
```

### RecursiveCreateGetError

#### Description

Raised when a getter function calls a creator function a second time.

#### Signature

```python

from worktoy.core import Function

from typing import Any

creator: Function  # The expected type
variableType: type  # The type of the variable
variableName: str  # Argument name
```

### TypeSupportError

#### Description

This exception should be raised when the argument type is not supported.

#### Signature

```python

from typing import Any

expectedType: type  # The expected type
actualValue: Any  # The actual value received
argName: str  # Argument name
```

### UnavailableNameException

#### Description

Exception raised when a name is already occupied. Meaning that the named
argument were expected to be ``None``.

#### Signature

```python

from typing import Any

argName: str  # The unavailable name
existingValue: Any  # The present value at the name
newValue: str  # The new value attempted to set
```

### UnexpectedEventException

#### Description

Raised when receiving a ``QEvent`` of the wrong ``QEvent.Type``. (Please note
that this exception is intended for use with the companion ``WorkSide``
module.)

#### Signature

```python

from typing import Any

expectedQEventType: str  # The expected QEvent.Type
actualEvent: Any  # The actual instance of QEvent received
argumentName: str  # The argument name
```

### UnsupportedSubclassException

#### Description

This exception should be raised when encountering a variable of correct
type, but of incorrect subclass.

#### Signature

```python

from typing import Any

argumentName: str  # The argument name
expectedParent: type  # The actual instance of QEvent received
actualValue: str  # The actual value of the variable
```

## Core

This module provides common types and constants.
