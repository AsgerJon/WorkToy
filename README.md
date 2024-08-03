[![wakatime](https://wakatime.com/badge/github/AsgerJon/WorkToy.svg)](
https://wakatime.com/badge/github/AsgerJon/WorkToy)

# WorkToy v0.99.xx

WorkToy collects common utilities. It is available for installation via pip:

```
pip install worktoy
```

Version 0.99.xx is in final stages of development. It will see no new
features, only bug fixes and documentation updates. Upon completion of
tasks given below, version 1.0.0 will be released.
Navigate with the table of contents below.

# Table of Contents

- [WorkToy v0.99.xx](#worktoy-v099xx)
    - [Table of Contents](#table-of-contents)
    - [Installation](#installation)
    - [Usage](#usage)
        - [desc](#worktoydesc)
        - [ezdata](#worktoyezdata)
        - [keenum](#worktoykeenum)
        - [meta](#worktoymeta)
        - [parse](#worktoyparse)
        - [text](#worktoytext)
        - [yolo](#worktoyyolo)
    - [Development](#development)

# Installation

```bash 
pip install worktoy
```

# Usage

# `worktoy.desc`

## Background - The Python Descriptor Protocol

The descriptor protocol in Python allows significant customisation of the
attribute access mechanism. To understand this protocol, consider a class
body assigning an object to a name. During the class creation process,
when this line is reached, the object is assigned to the name. For the
purposes of this discussion, the object is created when this line is
reached, for example:

```python
class PlanePoint:
  """This class represent an integer valued point in the plane. """
  x = Integer(0)
  y = Integer(0)  # Integer is defined below. In practice, classes should 
  #  be defined in dedicated files.
``` 

The above class ´PlanePoint´ owns a pair of attributes. These are
instances of the ´Integer´ class defined below. The ´Integer´ class is a
descriptor and is thus the focus of this discussion.

```python
class Integer:
  """This descriptor class wraps an integer value. More details will be 
  added throughout this discussion."""
  __fallback_value__ = 0
  __default_value__ = None
  __field_name__ = None
  __field_owner__ = None

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, int):
        self.__default_value__ = arg
        break
    else:
      self.__default_value__ = self.__fallback_value__

  #  The '__init__' method implemented above makes use of the unusual 
  #  'else' clause at the end of a loop. This clause is executed once after 
  #  the loop has completed. Since it is part of the loop, the 'break' 
  #  keyword applies to it as well as the loop itself. The for loop above 
  #  iterates through the positional arguments and if it encounters an 
  #  'int' argument, it assigns it and issues the 'break'. So if the loop 
  #  completes without hitting the 'break', no 'int' could be found in any 
  #  of the positional arguments. Conveniently, the 'else' block then 
  #  assigns the fallback value.

  def __set_name__(self, owner: type, name: str) -> None:
    """Powerful method called automatically when the class owning the 
    descriptor instance is finally created. It informs the descriptor 
    instance of its owner and importantly, it informs the descriptor of 
    the name by which it appears in the class body. """
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: object, owner: type) -> int:
    """Getter-function."""
``` 

## The ``__set_name__`` method

Python 3.6 was released on December 23, 2016. This version introduced
the ``__set_name__`` method, which marks a significant improvement to the
descriptor protocol. It informs instances of descriptor classes of the
class that owns them **and** the name by which they appear in the class
namespace. Much of the functionality found in the ``worktoy.desc`` module
would not be possible without this method.

### The `__get__` method

Consider the code below:

```python
class Descriptor:
  """Descriptor class."""

  def __get__(self, instance: object, owner: type) -> object:
    """Getter-function."""

  def __set_name__(self, owner: type, name: str) -> None:
    """Informs the descriptor instance that the owner is created"""


class OwningClass:
  """Class owning the descriptor."""
  descriptor = Descriptor()


#  At this point in the code, the OwningClass is created, which triggers 
#  the '__set_name__' method on the descriptor instance. 
#  Event 1

if __name__ == '__main__':
  owningInstance = OwningClass()  # Event 2
  print(OwningClass.descriptor)  # Event 3
  print(owningInstance.descriptor)  # Event 4
```

Let us examine each of the four events marked in the above example:

1. **Event 1** - This marks the completion of the class creation process,
   which is described in excruciating detail in later sections. Of
   interest here is the call to the ``__set_name__`` method on the
   descriptor:
   ``Descriptor.__set_name__(descriptor, OwningClass, 'descriptor')``
2. **Event 2** - This marks the creation of an instance of the owning
   class. This event is not of interest to this discussion.
3. **Event 3** - Accessing the descriptor on the OwningClass triggers the
   following function call:
   ``Descriptor.__get__(descriptor, None, OwningClass)``
4. **Event 4** - Accessing the descriptor on an instance of the owning
   class triggers the following function call:
   ``Descriptor.__get__(descriptor, owningInstance, OwningClass)``

The ``__get__`` determines what is returned when the descriptor is
accessed. Please note that this method is what is called every time the
descriptor instance is accessed regardless of how. In the above example,
the following would each result in a call to the ``__get__`` method:

```python
#  Each result in:  Descriptor.__get__(descriptor, None, OwningClass)
OwningClass.descriptor
getattr(OwningClass, 'descriptor')
object.__getattribute__(OwningClass, 'descriptor')
```

The interpreter always refers to the ``__get__`` method. To still allow
access to the descriptor object itself, the common pattern is for the
``__get__`` method to return the descriptor instance when accessed
through the owning class:

```python
class Descriptor:
  """Descriptor class."""

  def __get__(self, instance: object, owner: type) -> object:
    """Getter-function."""
    if instance is None:
      return self
    #  YOLO
```

This author suggests never deviating from this pattern. Perhaps some more
functionality or some hooks may be implemented, but the descriptor
instance itself should always be returned when accessed through the owning
class. When accessed through the instance, the descriptor is free to do
whatever it wants!

### The `__set__` method

The prior section focused on the distinction between accessing on the
class or instance level. The ``__set__`` method defined on the Descriptor
is invoked only when accessed through the instance:

```python
class Descriptor:
  """Descriptor class."""

  #  Code as before
  def __set__(self, instance: object, value: object) -> None:
    """Setter-function."""


if __name__ == '__main__':
  owningInstance = OwningClass()
  owningInstance.descriptor = 69  # Event 1
  print(owningInstance.descriptor)  # Event 2
  OwningClass.descriptor = 420  # Event 3
  print(owningInstance.descriptor)  # Event 4
```

The above code triggers the following function call:

-**Event 1:** ``Descriptor.__set__(descriptor, owningInstance, 7)``
-**Event 2:** ``Descriptor.__get__(descriptor, owningInstance, OwningClass)``
-**Event 3:** This call does not involve the descriptor at all, instead
it simply overwrites the descriptor.
-**Event 4:** The previous event overwrote the descriptor instance so now
it simply returns the value set in Event 3.

Thus, when trying to call ``__set__`` through the owning class, it is
applied to the descriptor object itself. This matches the suggested
implementation of the ``__get__`` method which would return the
descriptor item itself, when accessed through the owning class.

### The ``delete`` method

The most important comment here is this warning: **Do not mistake
``__del__`` and ``__delete__``!** ``__del__`` is a mysterious method
associated with the destruction of an object.

The ``__delete__`` method on the other hand allows instance specific
control over what happens when the ``del`` keyword is used on an
attribute through an instance. If the descriptor class does not
implement it, it will raise an ``AttributeError`` when the interpreter
tries to invoke ``__delete__`` on the descriptor instance. Deleting an
attribute through the owning class does not involve the descriptor at all,
but is managed on the metaclass level. Generally, the descriptor is just
yeeted in this case.

```python
class Descriptor:
  """Descriptor class."""

  #  Code as before
  def __delete__(self, instance: object, ) -> None:
    """Setter-function."""


if __name__ == '__main__':
  owningInstance = OwningClass()
  del owningInstance.descriptor  # event 1
  print(owningInstance.descriptor)  # event 2
```

If a descriptor class does implement the ``__delete__`` method the script
above is expected to trigger the following:

-**Event 1:** ``Descriptor.__delete__(descriptor, owningInstance)``

-**Event 2a:** ``AttributeError: __delete__`` if the descriptor does not
implement the method.

-**Event 2b:** ``AttributeError: 'OwningClass' object has no attribute
'descriptor'!`` if the descriptor does implement the method and allows
deletion to proceed.

-**Event 2c:** A custom implementation of the ``__delete__`` method which
does not allow deletion and thus raises an appropriate exception. In this
case, this author suggests raising a ``TypeError`` to indicate that the
attribute is of a read-only type. This is different than the
``AttributeError`` which generally indicate the absense of the attribute.

If a custom implementation of the ``__delete__`` method is provided, 2b
or 2c as described above should happen, as this is the generally expected
behaviour in Python. Implementing some alternative behaviour might be
cute or something, but when the code is then used elsewhere, the bugs
resulting from this unexpected behaviour are nearly impossible to find.

### Descriptor Protocol Implementations

There are three questions to consider before discussing implementation
details:

1. Is the descriptor class simply a way for owning classes to enhance
   attribute access?
2. Should classes implement the descriptor protocol to define their
   behaviour when owned by other classes?
3. Should a central descriptor class define how one class can own an
   instance of another?

There is certainly a need for classes to specialize access to their
attributes. This is the most common use of the descriptor protocol.
Python itself implements the ``property`` class to provide this control.

When creating a custom class, it seems reasonable to consider that other
classes might own instance of it and to implement descriptor protocol
methods as appropriate. Unfortunately, this is not commonly done meaning
that you can expect to have to own instances of classes that do not
provide for this ownership interaction themselves.

The ``AttriBox`` class provided by the ``worktoy.desc`` module does
implement the descriptor protocol in a way designed to allow one class to
own instances of another without either having to implement anything
related to the descriptor protocol. This class also makes the second
question redundant.

This discussion will now proceed with the following:

1. Usage of the ``property`` class provided by Python.
2. The ``worktoy.desc`` module provides the ``AbstractDescriptor`` class,
   which implements the parts of the descriptor protocol used by both
   ``Field`` and ``AttriBox``.
3. Implementation of the vastly superior ``Field`` class provided by the
   ``worktoy.desc`` module.
   4Usage an examples of the ``AttriBox`` class provided by the
   ``worktoy.desc`` module.

### The `property` class

The `property` class is a built-in class in Python. It allows the use of
a decorator to define getter, setter and deleter functions for a property.
Alternatively, the ``property`` may be instantiated in the class body
with the getter, setter and deleter functions as arguments. The following
example will demonstrate a class owning a number and a name,
demonstrating the two approaches to defining properties.

```python
from __future__ import annotations


class OwningClass:
  """This class uses 'property' to implement the 'name' attribute. """

  __fallback_number__ = 0
  __fallback_name__ = 'Unnamed'
  __inner_number__ = None
  __inner_name__ = None

  def __init__(self, *args, **kwargs) -> None:
    self.__inner_number__ = kwargs.get('number', None)
    self.__inner_name__ = kwargs.get('name', None)
    for arg in args:
      if isinstance(arg, int) and self.__inner_number__ is None:
        self.__inner_number__ = arg
      elif isinstance(arg, str) and self.__inner_name__ is None:
        self.__inner_name__ = arg

  @property
  def name(self) -> str:
    """Name property"""
    if self.__inner_name__ is None:
      return self.__fallback_name__
    return self.__inner_name__

  @name.setter
  def name(self, value: str) -> None:
    """Name setter"""
    self.__inner_name__ = value

  @name.deleter
  def name(self) -> None:
    """Name deleter"""
    del self.__inner_name__

  def _getNumber(self) -> int:
    """Number getter"""
    if self.__inner_number__ is None:
      return self.__fallback_number__
    return self.__inner_number__

  def _setNumber(self, value: int) -> None:
    """Number setter"""
    self.__inner_number__ = value

  def _delNumber(self) -> None:
    """Number deleter"""
    del self.__inner_number__

  number = property(_getNumber, _setNumber, _delNumber, doc='Number')

```

The above example demonstrates the use of the `property` class to enhance
the attribute access mechanism.

### The `AbstractDescriptor` class

The ``AbstractDescriptor`` class provides the ``__set_name__`` method and
delegates accessor functions to the following methods:

- ``__instance_get__``: Getter-function (Required!)
- ``__instance_set__``: Setter-function (Optional)
- ``__instance_del__``: Deleter-function (Optional)

When implementing ``__instance_get__`` to handle a missing value, the
subclass must raise a ``MissingValueException`` passing the instance and
itself to the constructor of it. This missing value situation is one
where no default value is provided and the value has not been set. The
``AbstractDescriptor`` calls ``__instance_get__`` during the ``__set__``
and ``delete__`` methods to collect the old value which is used in the
notification. If it catches such an error during ``__get__``, it raises
an ``AttributeError`` from it.

The ``AbstractDescriptor`` provides descriptors to mark methods to be
notified when the attribute is accessed. The methods are:

- ``ONGET``: Called when the attribute is accessed.
- ``ONSET``: Called when the attribute is set.
- ``ONDEL``: Called when the attribute is deleted.

Both ``Field`` and ``AttriBox`` subclass the ``AbstractDescriptor`` class.
These are discussed below.

### The `Field` class

The ``Field`` class provides descriptors in addition to those implemented
on the ``AbstractDescriptor`` class. These are used by owning classes to
mark accessor methods, much like the ``property`` class. Unlike the
Python ``property`` class, instances of the ``Field`` class must be
defined before the accessor methods in the class body. The decorators
require their field instance to be defined in the lexical scope before
they are available to decorate methods.

Below is an example of a plane point implementing the coordinate
attributes using the ``Field`` class:

```python
from __future__ import annotations
from worktoy.desc import Field


class Point:
  """This class uses the 'Field' descriptor to implement the coordinate
  attributes. """
  __x_value__ = None
  __y_value__ = None

  x = Field()
  y = Field()

  @x.GET
  def _getX(self) -> float:
    return self.__x_value__

  @x.SET
  def _setX(self, value: float) -> None:
    self.__x_value__ = value

  @y.GET
  def _getY(self) -> float:
    return self.__y_value__

  @y.SET
  def _setY(self, value: float) -> None:
    self.__y_value__ = value

  def __init__(self, *args, **kwargs) -> None:
    self.__x_value__ = kwargs.get('x', None)
    self.__y_value__ = kwargs.get('y', None)
    for arg in args:
      if isinstance(arg, int):
        arg = float(arg)
      if isinstance(arg, float):
        if self.__x_value__ is None:
          self.__x_value__ = arg
        elif self.__y_value__ is None:
          self.__y_value__ = arg
          break
    else:
      if self.__x_value__ is None:
        self.__x_value__, self.__y_value__ = 69., 420.
      elif self.__y_value__ is None:

        self.__y_value__ = 420.
```

The ``Field`` class allows classes to implement how attributes are accessed.

### The `AttriBox` class

Where ``Field`` relies on the owning class itself to specify the accessor
functions, the ``AttriBox`` class provides an attribute of a specified
class. This class is not instantiated until an instance of the owning
class calls the ``__get__`` method. Only then will the inner object of
the specified class be created. The inner object is then placed on a
private variable belonging to the owning instance. When the ``__get__``
is next called the inner object at the private variable is returned. When
instantiating the ``AttriBxo`` class, the following syntactic sugar
should be used: ``fieldName = AttriBox[FieldClass](*args, **kwargs)``.
The arguments placed in the parentheses after the brackets are those used
to instantiate the ``FieldClass`` given in the brackets.

Below is an example of a class using the ``AttriBox`` class to implement
a ``Circle`` class. It uses the ``Point`` class defined above to manage
the center of the circle. Notice how the ``Point`` class itself is wrapped
in an ``AttriBox`` instance. The ``area`` attribute is defined using the
``Field`` class and illustrates the use of the ``Field`` class to expose
a value as an attribute. Finally, it used the ``ONSET`` decorator to mark
a method as the validator for the radius attribute. This causes the
method to be hooked into the ``__set__`` method on the ``radius``.

```python
from __future__ import annotations


class Circle:
  """This class uses the 'AttriBox' descriptor to manage the radius and
  center, and it also illustrates a use case for the 'Field' class."""

  radius = AttriBox[float](0)
  center = AttriBox[Point](0, 0)
  area = Field()

  @area.GET
  def _getArea(self) -> float:
    return 3.1415926535897932 * self.radius ** 2

  @radius.ONSET
  def _validateRadius(self, _, value: float) -> None:
    if value < 0:
      e = """Received negative radius!"""
      raise ValueError(e)

  def __init__(self, *args, **kwargs) -> None:
    """Constructor omitted..."""

  def __str__(self) -> str:
    msg = """Circle centered at: (%.3f, %.3f), with radius: %.3f"""
    return msg % (self.center.x, self.center.y, self.radius)


if __name__ == '__main__':
  circle = Circle(69, 420, 1337)
  print(circle)
  circle.radius = 1
  print(circle)
```

Running the code above will output the following:

```terminal
Circle centered at: (69.000, 420.000), with radius: 4.000
Circle centered at: (69.000, 420.000), with radius: 1.000
```

### ``worktoy.desc`` - Summary

As have been demonstrated and explained, the ``worktoy.desc`` module
provides helpful, powerful and flexible implementations of the descriptor
protocol. The ``Field`` allows classes to customize attribute access
behaviour in significant detail. The ``AttriBox`` class provides a way to
set as attribute any class on another class in a single line. As
mentioned briefly, the class contained by the ``AttriBox`` instance is
not instantiated until an instance of the owning class calls the
``__get__`` method. In the following section, the importance of this lazy
instantiation feature will be illustrated with an example involving the
``PySide6`` library.

### PySide6 - Qt for Python

The PySide6 library provides Python bindings for the Qt framework. Despite
involving bindings to a C++ library, the code itself remains Python and
not C++, thank the LORD. Nevertheless, certain errors do not have a
Pythonic representation. The ``AttriBox`` class was envisioned for this
very reason. Its lazy instantiation system prevents something called
'Segmentation Fault'. You can lead a long and happy life not ever
encountering those words again, thanks to the ``AttriBox`` class!

Central to Qt is the main event loop managed by an instance of
``QCoreApplication`` or of a subclass of it. While the application is
running, instances of ``QObject`` provide the actual application
functionality. It is reasonable to regard the ``QObject`` in Qt and the
``object`` object in Python as similar. Every window, every widget, the
running application, managed threads and just about everything else in Qt
is essentially an instance of ``QObject``. Having defined these terms, we
may now discuss the two central rules of Qt:

- Only one instances of ``QCoreApplication`` may be running at any time.
- The first instantiated ``QObject`` must be an instance of the
  ``QCoreApplication`` class.

Instantiating any ``QObject`` before the ``QCoreApplication`` is running
will result in immediate error. Enter the ``AttriBox`` class. The
somewhat inflexible nature of the above rules regains flexibility by
making use of the lazy instantiation provided by the ``AttriBox`` class.

In the following, we will see a simple application consisting of a window
showing a welcome message provided as an instance of the ``QLabel`` class
along with an exit button provided by the ``QPushButton`` class. These
widgets are stacked vertically and are managed by an instance of the
``QVBoxLayout`` class and finally these are managed by an instance of
``QWidget`` which is the parent of the widgets and which owns the layout.
This widget is set as the central widget in the main window. The main
window itself is a subclass of the ``QMainWindow`` class.

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import QSize
from worktoy.desc import AttriBox


class MainWindow(QMainWindow):
  """This subclass of QMainWindow provides the main application window. """

  baseWidget = AttriBox[QWidget]()
  layout = AttriBox[QVBoxLayout]()
  welcomeLabel = AttriBox[QLabel]()
  exitButton = AttriBox[QPushButton]()

  def initUi(self) -> None:
    """This method sets up the user interface"""
    self.setMinimumSize(QSize(480, 320))
    self.setWindowTitle("Welcome to WorkToy!")
    self.welcomeLabel.setText("""Welcome to WorkToy!""")
    self.exitButton.setText("Exit")
    self.layout.addWidget(self.welcomeLabel)
    self.layout.addWidget(self.exitButton)
    self.baseWidget.setLayout(self.layout)
    self.setCentralWidget(self.baseWidget)

  def initSignalSlot(self) -> None:
    """This method connects the signals and slots"""
    self.exitButton.clicked.connect(self.close)

  def show(self) -> None:
    """This reimplementation calls 'initUi' and 'initSignalSlot' before 
    calling the parent implementation"""
    self.initUi()
    self.initSignalSlot()
    QMainWindow.show(self)


if __name__ == '__main__':
  app = QApplication([])
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
```

The above script demonstrates the use of the ``AttriBox`` class to
provide lazy instantiation of the widgets in the PySide6 application.

## Conclusion

To take full advantage of the descriptor protocol requires considerable
boilerplate code if implemented from scratch. The ``worktoy.desc`` module
provides the ``Field`` and ``AttriBox`` classes to minimize boilerplate.
The ``Field`` class requires only the code you actually want to use. The
``AttriBox`` lets you set any class as an attribute in a single line.

## ``worktoy.meta`` - Background

Python is the best programming language. The most important reason is
that the syntax is made to be human-readable. Regardless of your personal
preference for languages, you are never happier than when writing in
Python. The objections to Python are valid. Provided you are talking
about Python from 10 years ago. The final reason is the subject of this
discussion: the Python metaclass. The Python metaclass is the most
powerful single concept in programming. No other programming language has
anything like it. Java reflections? No, no, no. Rust macros? Not even
close! C++ templates? Get it out of here!

Understanding the Python metaclass does require some background. In the
following sections, we will examine:

- **The Python object**
- **Object Extensions**
- **The Python Function**
- **The ``*`` and ``**`` operators**
- **The Python ``lambda`` Function**
- **Class Instantiations**
- **The Custom Class**
- **The Custom Metaclass**
- **The Custom Namespace**

## Understanding the Python metaclass

Readers may associate the word **meta** with crime on account of the hype
created around the term **metaverse**. This author hopes readers will
come to associate the word instead with the Python metaclass. The
**'worktoy.meta'** module provides functions and classes allowing a more
streamlined approach to metaclass programming. This documentation
explains the functionality of metaclasses in general and how this module
provides helpful tools.

### Everything is an object!

Python operates on one fundamental idea: Everything is an object.
Everything. All numbers, all strings, all functions, all modules and
everything that you can reference. Even ``object`` itself is an object.
This means that everything supports a core set of attributes and methods
defined on the core ``object`` type.

### Extensions of ``object``

With everything being an object, it is necessary to extend the
functionalities in the core ``object`` type to create new types,
hereinafter classes. This allows objects to share the base ``object``,
while having additional functionalities depending on their class. Python
provides a number of special classes listed below:

- **``object``** - The base class for all classes. This class provides
  the most basic functionalities.
- **``int``** - Extension for integers. The python interpreter uses
  heavily optimized C code to handle integers. This is the case for
  several classes on this list.
- **``float``** - Extension for floating point numbers. This class
  provides a number of methods for manipulating floating point numbers.
- **``list``** - Extension for lists of objects of dynamic size allowing
  members to be of any type. As the amount of data increases, the greater
  the performance penalty for the significant convenience.
- **``tuple``** - Extension for tuples of objects of fixed size. This
  class is similar to the list class, but the size is fixed. This means
  that the tuple is immutable. While this is inflexible, it does allow
  instances to be used as keys in mappings.
- **``dict``** - Extension for mappings. Objects of this class map keys
  to values. Keys be of a hashable type, meaning that ``object`` itself
  is not sufficient. The hashables on this list are: ``int``, ``float``,
  ``str`` and ``tuple``.
- **``set``** - Extension for sets of objects. This class provides a
  number of methods for manipulating sets. The set class is optimized for
  membership testing.
- **``frozenset``** - Provides an immutable version of ``set`` allowing
  it to be used as a key in mappings.
- **``str``** - Extension for strings. This class provides a number of
  methods for manipulating strings. The ``worktoy.text`` module expands
  upon some of these.

To reiterate, everything is an object. Each object belongs to the
``object`` class but may additionally belong to a class that extends the
``object`` class. For example: ``7`` is an object. It is an instance of
``object`` by being an instance of ``int`` which extends ``object``.
Classes are responsible for defining the instantiation of instances
belonging to them. Generally speaking, classes may be instantiated by
calling the class object treating it like a function. Classes may accept
or even require arguments when instantiated.

Before proceeding, we need to talk about functions. Python provides two
builtin extensions of ``object`` that provide standalone objects that
implement functions: ``function`` and ``lambda``. Both of these have
quite unique instantiation syntax and does not follow the conventions we
shall see later in this discussion.

### Defining a ``function``

Python allows the following syntax for creating a function. Please note
that all functions are still objects, and all functions created with the
syntax below belong to the same class ``function``. Unfortunately, this
class cannot be referred to directly. Which is super weird. Anyway, to
create a function, use the following syntax:

```python
def multiplication(a: int, b: int) -> int:
  """This function returns the product of two integers."""
  return a * b
```

#### RANT

The above function implements multiplication. It also provides the
optional features: type hints and a docstring. The interpreter completely
ignores these, but they are very helpful for humans. It is the opinion of
this author that omitting type hints and docstrings is acceptable only
when running a quick test. If anyone except you or God will ever read
your code, it must have type hints and docstrings!

#### END OF RANT

Below is the syntax that invokes the function:

```python
result = multiplication(7, 8)  # result is 56
```

In the function definition, the positional arguments were named ``a`` and
``b``. In the above invocation, the positional arguments were given
directly. Alternatively, they might have been given as keyword arguments:

```python
result = multiplication(a=7, b=8)  # result is 56
tluser = multiplication(b=8, a=7)  # result is 56
```

When keyword arguments are used instead of positional arguments, the
order is irrelevant, but names are required.

### The star ``*`` and double star ``**`` operators

Suppose the function were to be invoked with the numbers from a
list: ``numbers = [7, 8]``, then we might invoke the ``multiplication``
function as follows:

```python
result = multiplication(numbers[0], numbers[1])  # result is 56
```

Imagine the function took more than two arguments. The above syntax would
still work, but would be cumbersome. Enter the star ``*`` operator:

```python
result = multiplication(*numbers)  # result is 56
```

Wherever multiple positional arguments are expected, and we have a list
or a tuple, the star operator unpacks it. This syntax will seem confusing,
but it is very powerful and is used extensively in Python. It is also
orders of magnitude more readable than the equivalent in C++ or Java.

#### RANT

This rant is left as an exercise to the reader

#### END OF RANT

Besides function calls, the star operator conveniently concatenates lists
and tuples. Suppose we have two lists: ``a = [1, 2]`` and ``b = [3, 4]``
we may concatenate them in several ways:

```python
a = [1, 2]
b = [3, 4]
ab = [a[0], a[1], b[0], b[1]]  # Method 1: ab is [1, 2, 3, 4]
ab = a + b  # Method 2: ab is [1, 2, 3, 4]
ab = [*a, *b]  # Method 3: ab is [1, 2, 3, 4]
a.extend(b)  # Method 4 modifies list 'a' in place. 
a = [1, 2, 3, 4]  # a is extended by b

```

Obviously, don't use the first method. The one relevant for the present
discussion is the third, but the second and fourth have merit as well,
but will not be used here. Finally, list comprehension is quite powerful
as well but is the subject for a different discussion.

### The double star ``**`` operator

The single star is to lists and tuples as the double star is to
dictionaries. Suppose we have a dictionary: ``data = {'a': 1, 'b': 2}``
then we may invoke the ``multiplication`` function as follows:

```python   
data = {'a': 1, 'b': 2}
result = multiplication(**data)  # result is 2
```

Like the star operator, the double star operator can be used to
concatenate two dictionaries. Suppose we have two dictionaries:
``A = {'a': 1, 'b': 2}`` and ``B = {'c': 3, 'd': 4}``. These may be
combined in several ways:

```python
A = {'a': 1, 'b': 2}
B = {'c': 3, 'd': 4}
#  Method 1
AB = {**A, **B}  # AB is {'a': 1, 'b': 2, 'c': 3, 'd': 4}
#  Method 2
AB = A | B
#  Method 3 updates A in place
A |= B
A = {'a': 1, 'b': 2}  # Resetting A
#  Method 4 updates A in place
A.update(B)
```

As before, the first method is the most relevant for the present
discussion. Unlike the example with lists, there is not really a method
that is bad like the first method with lists.

In conclusion, the single and double star operators provide powerful
unpacking of iterables and mappings respectively. Each have reasonable
alternatives, but it is the opinion of this author that the star
operators are preferred as they are unique to this use. The plus and
pipe operators are used for addition and bitwise OR respectively. When
the user first sees the plus or the pipe, they cannot immediately infer
that the code is unpacking the operands. Not before having identified the
types of the operands. In contrast, the star in front of an object
without space immediately says unpacking.

#### RANT

If you have ever had the misfortune of working with C++ or Java, you
would know that the syntax were disgusting, but you didn't know the words
for it. The functionalities coded by C++ and Java cannot be inferred
easily. It is necessary to see multiple parts of the code to infer what
functionality is intended. For example, suppose we have a C++ class with
a constructor.

```C++
class SomeClass {
private:
  int _a;
  int _b;
public:
  int a;
  SomeClass(int a, int b) {
      // Constructor code
  }
  int b {
    return _b;
  }
};
```

Find the constructor above. It does not have a name that means "Hello
there, I am a constructor". Instead, it is named the same as the class
itself. So to find the constructor, you need to identify the class name
first then go through the class to find name again. The decision for this
naming makes sense in that it creates something with the name called. But
it significantly reduces readability. The second attack on human dignity
is the syntax for the function definition. Where the class defines the
public variable 'a', the syntax used is not bad. But because the syntax
is identical for the functions, it increases the amount of code required
to infer that a function is being created.

The two examples of nauseating syntax above do not serve any performance
related purpose. Software engineering and development requires the full
cognitive capability of the human brain. Deliberately obscuring code,
reduces the cognitive capacity left over for actual problem-solving. This
syntax is kept in place for no other purpose than gate-keeping.

#### END OF RANT

### The famous function signature: ``def someFunc(*args, **kwargs)``

Anyone having browsed through Python documentation or code may have
marvelled at the function signature: ``def someFunc(*args, **kwargs)``.
The signature means that the function accepts any number of positional
arguments as well as any number of keyword arguments. This allows one
function to accept multiple different argument signatures. While this may
be convenient, the ubiquitous use of this pattern is likely motivated by
the absense of function overloading in native Python. (Foreshadowing...)

### The ``lambda`` function

Before getting back to class instantiation, we will round off this
discussion of functions with the ``lambda`` function. The ``lambda``
function is basically the anonymous function. The syntax of it is
``lambda arguments: expression``. Whatever the expression on the right
hand side of the colon evaluates to is returned by the function. The
``lambda`` function allows inline function definition which is much more
condensed that the regular function definition as defined above. This
allows it to solve certain problems in one line, for example:

```python
fb = lambda n: ('' if n % 3 else 'Fizz') + ('' if n % 5 else 'Buzz') or n
```

Besides flexing, the ``lambda`` function is useful when working with
certain fields of mathematics, requiring implementation of many functions
that fit on one line. Below is an example of a series of functions
implementing Taylor series expansions. This takes advantage of the fact
that many such functions may be distinguished only by a factor mapped
from the term in the series.

```python
factorial = lambda n: factorial(n - 1) * n if n else 1
recursiveSum = lambda F, n: F(n) + (recursiveSum(F, n - 1) if n else 0)
taylorTerm = lambda x, t: (lambda n: t(n) * x ** n / factorial(n))
expTerm = lambda n: 1
sinTerm = lambda n: (-1 if ((n - 1) % 4) else 1) if n % 2 else 0
cosTerm = lambda n: sinTerm(n + 1)
sinhTerm = lambda n: 1 if n % 2 else 0
coshTerm = lambda n: sinhTerm(n + 1)
exp = lambda x, n: recursiveSum(taylorTerm(x, expTerm), n)
sin = lambda x, n: recursiveSum(taylorTerm(x, sinTerm), n)
cos = lambda x, n: recursiveSum(taylorTerm(x, cosTerm), n)
sinh = lambda x, n: recursiveSum(taylorTerm(x, sinhTerm), n)
cosh = lambda x, n: recursiveSum(taylorTerm(x, coshTerm), n)
```

The above collection of functions implement recursive lambda functions to
calculate function values of common mathematical functions including:

- ``exp``: The exponential function.
- ``sin``: The sine function.
- ``cos``: The cosine function.
- ``sinh``: The hyperbolic sine function.
- ``cosh``: The hyperbolic cosine function.

The lambda functions implement Taylor-Maclaurin series expansions at a
given number of terms and then begin by calculating the last term
adding the previous term to it recursively, until the 0th term is reached.
This implementation demonstrates the power of the recursive lambda
function and is not at all flexing.

### Instantiation of classes

Since this discussion includes class instantiations, the previous section
discussing functions will be quite relevant. We left the discussion of
builtin Python classes having listed common ones. Generally speaking,
Python classes have a general syntax for instantiation except for those
listed. Below is the instantiation of the builtin classes.

- **object**: ``obj = object()`` - This creates an object. Not
  particularly useful but does show the general syntax.
- **int**: ``number = 69`` - This creates an integer.
- **float**: ``number = 420.0`` - This creates a float.
- **str**: ``message = 'Hello World!'`` - This creates a string.
- **list**: ``data = [1, 2, 3]`` - This creates a list.
- **tuple**: ``data = (1, 2, 3)`` - This creates a tuple.
- **?**: ``what = (1337)`` - What does this create? Well, you might
  imagine that this creates a tuple, but it does not. The interpreter
  first removes the redundant parentheses and then the evaluation makes
  it an integer. To create a single element tuple, you must add the
  trailing comma: ``what = (1337,)``. This applies to one element tuples,
  as the comma separating the elements of a multi-element tuple
  sufficiently informs the interpreter that this is a tuple. The empty
  tuple requires no commas: ``empty = ()``.
- **set**: ``data = {1, 2, 3}`` - This creates a set.
- **dict**: ``data = {'key': 'value'}`` - This creates a dictionary. If
  the keys are strings, the general syntax may be of greater convenience:
  ``data = dict(key='value')``. Not requiring quotes around the keys.
  Although this syntax does not support non-string keys.
- **?**: ``data = {}`` - What does this create? Does it create an empty
  set or an empty dictionary. This author is not actually aware, and
  recommends instead ``set()`` or ``dict()`` respectively when creating
  empty sets or dictionaries.

Except for ``list`` and ``tuple``, the general class instantiation syntax
may be applied as seen below:

- **int**: ``number = int(69)``
- **float**: ``number = float(420.0)``
- **str**: ``message = str('Hello World!')``
- **dict**: ``data = dict(key='value')`` - This syntax is quite
  reasonable, but is limited to keys of string type.

Now let's have a look at what happens if we try to instantiate ``tuple``,
``list``, ``set`` or ``frozenset`` using the general syntax:

- **list**: ``data = list(1, 2, 3)`` - NOPE! This does not create the
  list predicted by common sense: ``data = [1, 2, 3]``. Instead, we are
  met by the following error message: "TypeError: list expected at most 1
  argument, got 3". Instead, we must use the following syntax:
  ``data = list((1, 2, 3))`` or ``data = list([1, 2, 3])``. Now the
  attentive reader may begin to object, as one of the above require a list
  to already be defined and the other requires the tuple to be defined.
  Let's see how one might instantiate a tuple directly:
- **tuple**: ``data = tuple(1, 2, 3)`` - NOPE! This does not work either!
  We receive the exact same error message as before. Instead, we must use
  one of the following: ``data = tuple((1, 2, 3))``
  or ``data = tuple([1, 2, 3])``. The logically sensitive readers now see
  a significant inconsistency in the syntax: One cannot in fact
  instantiate a tuple nor a list directly without having a list or tuple
  already created. This author suggests that the following syntax should
  be accepted: ``data = smartTuple(1, 2, 3)`` and even:
  ``data = smartList(1, 2, 3)``. Perhaps this author is just being
  pedantic. The existing syntax is not a problem, and it's not like the
  suggested instantiation syntax is used anywhere else in Python.
- **set**: ``data = set(1, 2, 3,)`` This is correct syntax. So this works,
  but the suggested ``smartList`` and ``smartTuple`` functions does not, OK
  sure, makes sense...
- **frozenset**: ``data = frozenset([69, 420])`` - This is correct syntax.

Let us have another look at the instantiations of ``dict`` and of ``set``,
but not ``list`` and ``tuple``.

```python
def newDict(**kwargs) -> dict:
  """This function creates a new dictionary having the key value pairs 
  given by the keyword arguments. """
  return dict(**kwargs)  # Unpacking the keyword arguments creates the dict.


def newSet(*args) -> set:
  """This function creates a new set having the elements given by the 
  positional arguments. """
  return set(args)  # Unpacking the positional arguments creates the set.


def newList(*args) -> list:
  """As long as we don't use the word 'list', we can actually instantiate 
  a list in a reasonable way."""
  return [*args, ]  # Unpacking the positional arguments creates the list.


def newTuple(*args) -> tuple:
  """Same as for list, but remember the hanging comma!"""
  return (*args,)  # Unpacking the positional arguments creates the tuple.
```

### Custom classes

In the previous section, we examined functions and builtin classes. To
reiterate, in the context of this discussion a class is an extension of
``object`` allowing objects to belong to different classes implementing
different extensions of ``object``. This raises a question: What
extension of ``object`` contains ``object`` extensions? If ``7`` is an
instance of the ``int`` extension of ``object``, of what extension is
``int`` and instance. The answer is the ``type``. This extension of
``object`` provides all extensions of ``object``. This implies the
surprising that ``type`` is an instance of itself.

The introduction of the ``type`` class allows us to make the following
insightful statement:

``7`` is to ``int`` as ``int`` is to ``type``. This means that ``type``
is responsible for instantiating new classes. A few readers may now begin
to see where this is going, but before we get there, let us examine how
``type`` creates a new class.

```python
from worktoy.desc import AttriBox


class PlanePoint:
  """Class representing a point in the plane """

  x = AttriBox[float](0)
  y = AttriBox[float](0)

  def __init__(self, *args, **kwargs) -> None:
    """Constructor omitted..."""

  def magnitude(self) -> float:
    """This method returns the magnitude of the point. """
    return (self.x ** 2 + self.y ** 2) ** 0.5


if __name__ == '__main__':
  P = PlanePoint(69, 420)
```

After the import statement, which is not the subject of the present
discussion, the first line of code encountered by the interpreter is the
``class PlanePoint:``. The line omits some default values shown here:
``class PlanePoint(object, metaclass=type)``. What the interpreter does
next is entirely up to the metaclass. Whatever object the metaclass
returns will be place at the name ``PlanePoint``. We will now look at
what the ``type`` metaclass, which is the default, does when it creates a
class, but keep mind that the metaclass my do whatever it wants.

- **name**: ``PlanePoint`` is recorded as the name of the class about to
  be created.
- **bases**: A tuple of the base classes is created. The ``object`` does
  not actually arrive in this tuple and the ``type`` provides implicitly.

Please note that it is possible to pass keyword arguments similarly to
the metaclass=type, but this is beyond the scope of the present
discussion. With the name and the bases, the metaclass now creates a
namespace object. The ``type`` simply uses an empty dictionary. Then the
interpreter goes through the class body line by line look for assignments,
function definitions and even nested classes. Basically every statement
in the class body that assigns a value to a key and for each such pair
the ``__setitem__`` method is called on the namespace object. The
implication of this is that where the value to be assigned is the return
value of a function, then that function is called during the class
creation process. This means that in the ``PlanePoint`` class above, the
instances of ``AttriBox`` are created before the class object is created.
When the interpreter finishes, it calls the ``__new__`` method on the
metaclass and passes to it: the name, the bases, the namespace and any
keyword arguments initially passed to class creation. The interpreter
then waits for the metaclass to return the class object. When this
happens all the objects that implement ``__set_name__`` has the method
called informing the descriptor instances that their owner has been
created. Finally, the interpreter applies the ``__init__`` method of the
metaclass on the newly created class.

In summary:

- **Setting up class creation** The interpreter records the name of the
  class to be created, the base classes, the keyword arguments and which
  metaclass is responsible for creating the class.
- **Namespace creation** The items collected are passed to the
  ``__prepare__`` method on the metaclass:
  ``namespace = type.__prepare__(name, bases, **kwargs)``
- **Class Body Execution** The interpreter goes through the class body
  line by line and assigns the values to the namespace object:
  ``namespace['x'] = AttriBox[float](0)  # Creates the AttriBox object``
- **Class Object Creation** The namespace object is passed to the
  ``__new__`` method on the metaclass:
  ``cls = type.__new__(type, name, bases, namespace, **kwargs)``
- **Descriptor Class Notification** The objects implementing the descriptor
  protocol are notified that the class object has been created:
  ``AttriBox[float].__set_name__(PlanePoint, 'x')``
- **``type.__init__``** The metaclass is called with the class object:
  ``type.__init__(cls, name, bases, namespace, **kwargs)`` Although on
  ``type`` the ``__init__`` method is a noop.

An impractical alternative to the above syntax is to create the new class
inline: ``PlanePoint = type('PlanePoint', (object,), {})``. Although,
this line has an empty dictionary where the namespace should have been.

### The Custom Metaclass

This brings us to the actual subject of this discussion: The custom
metaclass. Because every step mentioned above may be customized by
subclassing ``type``. Doing so takes away every limitation. The line
discussed before:

```python
class AnyWayUWantIt(metaclass=MyMeta):
  """Class representing a point in the plane """
```

This line can create anything. A class for example, but anything. It can
create a string, it can return ``None``, it can create a new function,
any object possible may be created here.

This present discussion is about creating new classes, but readers are
encouraged to experiment.

As mentioned, the ``type`` object provides a very helpful class creation
process. What it does is defined in the heavily optimized C code of the
Python interpreter. This cannot be inspected as Python code. For the
purposes of this discussion, we will now create a custom metaclass that
does the same as the ``type`` metaclass, but exposed as Python code.

```python

class MetaType(type):
  """This custom metaclass illustrates the class creation process as it 
  is done by the 'type' metaclass. """

  @classmethod
  def __prepare__(mcls, name: str, bases: tuple, **kwargs) -> dict:
    """This method creates the namespace object, which for 'type' is 
    merely an empty dictionary. """
    return dict()

  def __new__(cls, name: str, bases: tuple, namespace: dict, **kw) -> type:
    """This method creates the class object. There is not much to see 
    here, as the 'type' metaclass does most of the work. This is normal 
    in custom metaclasses where this method, if implemented, performs 
    some tasks, creates the class object, possibly does some more tasks, 
    before returning the class object. """
    cls = type.__new__(type, name, bases, namespace)
    return cls

  def __init__(cls, name: str, bases: tuple, namespace: dict, **kw) -> None:
    """A custom metaclass may implement this method. Doing so allows 
    further initialization after the '__set_name__' calls have finished. """
    pass

  def __call__(cls, *args, **kwargs) -> object:
    """This method is called when the class object is called. The 
    expected behaviour even from custom metaclasses, is for it to create 
    a new instance of the class object. Please note, that generally 
    speaking, custom classes are free to implement their own 
    instantiation in the form of the '__new__' and '__init__' methods. If 
    a custom metaclass does not intend to adhere to these, then when 
    encountering a class body that tries to implement them, the namespace 
    object should raise an error. Do not allow classes derived from the 
    custom metaclass to implement a function that you do not intend to 
    actually use. """
    self = cls.__new__(cls, *args, **kwargs)
    if isinstance(self, cls):
      self.__init__(*args, **kwargs)
    return self

  def __instance_check__(cls, instance: object) -> bool:
    """Whenever the 'isinstance' function is called, this method on the 
    metaclass is responsible for determine if the instance should be 
    regarded an instance of the class object. """
    otherCls = type(instance)
    if cls is otherCls:
      return True
    for item in otherCls.__mro__:
      if item is cls:
        return True
    return False

  def __subclass_check__(cls, subclass: type) -> bool:
    """Similar to the above instance check method, this method is 
    responsible for deciding of the subclass provided should be regarded 
    as a subclass of the class object. """
    if cls is subclass:
      return True
    for item in subclass.__mro__:
      if item is cls:
        return True
    return False
```

Since the ``type`` metaclass is heavily optimized in the C code of the
Python interpreter, the above implementation is for illustrative purposes
only. It shows what methods a custom metaclass may customize to achieve a
particular behaviour.

### The Custom Namespace

The custom namespace object must implement ``__getitem__`` and
``__setitem__``. Additionally, it must satisfy the key error preservation
and the ``type.__new__`` method must receive a namespace of ``dict``-type.
This is elaborated below:

#### ``KeyError`` preservation

When a dictionary is accessed with a key that does not exist, a
``KeyError`` is raised. The interpreter relies on this behaviour to
handle lines in the class body that are not directly assignments
correctly. This is a particularly important requirement because failing
to raise the expected ``KeyError`` will affect only classes that happen
to include a non-assignment line. Below is a list of known situations
that causes the issue:

- **Decorators**: Unless the decorator is a function defined earlier in
  the class body as an instance method able to receive a callable at the
  ``self`` argument, the decorator will cause the issue described. Please
  note that a static method would be able to receive a callable at the
  first position, but the static method decorator itself would cause the
  issue even sooner.
- **Function calls**: If a function not defined previously in the class
  body is called during the class body without being assigned to a name,
  the error will occur.

The issue raises an error message that will not bring attention to the
namespace object. Further, classes will frequently work fine, if they
happen to not include any of the above non-assignments. In summary:
failing to raise the expected error must be avoided at all costs, as it
will cause undefined behaviour without any indication as to the to cause.

#### The ``type.__new__`` expects a namespace of ``dict``-type

After the class body is executed the namespace object is passed to the
``__new__`` method on the metaclass. If the metaclass is intended to
create a new class object, the metaclass must eventually call the
``__new__`` method on the parent ``type`` class. The ``type.__new__``
method must receive a namespace object that is a subclass of ``dict``. It
is only at this stage the requirement is enforced. Thus, it is possible
to use a custom namespace object that is not a subclass of ``dict``, but
then it is necessary to implement functionality in the ``__new__`` method
on the metaclass such that a ``dict`` is passed to the ``type.__new__``
call.

### Applications of Custom Namespace

During class body execution the namespace object is passed the key value
pairs encountered. When using the empty dictionary as the namespace,
information is lost when a key receives multiple values as only the most
recently set value is retained. A custom namespace might collect all
values set at each name thus preserving all information. This application
is implemented in the ``worktoy.meta`` module. Beyond the scope of this
module is the potential for the namespace object to dynamically change
during the class body execution. This potential is not explored here, but
readers are encouraged to experiment.

Preserving multiple values on the same key can only be provided for by a
custom namespace. An obvious use case would be function overloading. This
brings up an important distinction: A class implementing function
overloading is in some ways the exact same class as before. Only the
overloaded methods are different. Providing a custom namespace does not
actually result in classes that exhibit different behaviour. Achieving
this requires customization of the metaclass itself beyond the
``__prepare__`` method.

## The ``worktoy.meta`` module

We have discussed class creation by use of ``type``, we have illustrated
what methods might be customized. In particular the custom namespace
returned by the ``__prepare__`` method. This brings us to the
``worktoy.meta`` module. Our discussion will proceed with an examination
of the contents.

### Nomenclature

Below is a list of terms used in the ``worktoy.meta`` module:

- **``cls``** - A newly created class object
- **``self``** - A newly created object that is an instance of the newly
  created class.
- **``mcls``** - The metaclass creating the new class.
- **``namespace``** - This is where the class body is stored during class
  creation.

### Metaclass and Namespace Pattern

The ``worktoy.meta`` module implements a pattern where the metaclass is
responsible for defining the functionality of the class, while the
namespace object is responsible for collecting items from the class body
execution. Rather than simply passing on the namespace object it receives,
the namespace object class is expected to implement a method called
``compile``. The metaclass uses the ``dict`` returned by the ``compile``
when it calls the ``type.__new__`` method.

This pattern is based on the separation of responsibilities: The
namespace object class is responsible for processing the contents of the
class body. The metaclass is responsible for defining the functionality
of the class itself.

### Function Overloading

The ``worktoy.meta`` module provides a decorator factory called
``overload`` used to mark an overloaded method with a type signature. The
``Dispatcher`` class contains a dictionary of functions keyed by their
type signatures. When calling an instance of this class, the types of the
arguments received determine what function to call. The ``BaseNamespace``
class is a custom namespace object that collects overloaded functions and
replaces each such name with a relevant instance of the ``Dispatcher``. The
``BaseMetaclass`` class is a custom metaclass using the ``BaseNamespace``
class as the namespace object. Finally, the ``BaseObject`` class derives
from the ``BaseMetaclass`` and implements function overloading.

### Singleton

Singleton classes are characterized by the fact that they are allowed
only one instance. The ``worktoy.meta`` provides ``Singleton`` class
derived from a custom metaclass. Subclasses of it are singletons. When
calling the class object of a subclass of ``Singleton`` the single
instance of the class is returned. If the subclass implements
``__init__`` then it is called on the single instance. This allows
dynamic behaviour of singletons. If this is not desired, the singleton
subclass should provide functionality preventing the ``__init__`` method
from running more than once.

### Summary

The ``worktoy.meta`` module provides base classes and a pattern for
custom metaclass creation and uses them to implement function overloading
in the ``BaseObject`` class. Additionally, the module provides a
``Singleton`` class for creating singletons, which is based on a custom
metaclass derived from the module. Other parts of the ``worktoy`` module
makes use of the ``worktoy.meta`` in their implementation. This includes
the ``KeeNum`` enumeration module and the ``ezdata`` module.

## The ``worktoy.keenum`` module

The ``worktoy.keenum`` module provides the ``KeeNum`` enumeration class.
This class makes use of the ``worktoy.meta`` module to create the
enumeration class. This discussion will demonstrate how to create
enumerations with this class. Every enumeration class must be indicated
in the class body using the ``worktoy.keenum.auto`` function. Each such
instances may provide a public value by passing it to the ``auto``
function. Please note however, that the public value is not used for any
purpose by the module. The ``KeeNum`` implements a hidden value that it
uses internally.

```python
"""Enumeration of weekdays using KeeNum."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, auto


class Weekday(KeeNum):
  """Enumeration of weekdays."""
  MONDAY = auto()
  TUESDAY = auto()
  WEDNESDAY = auto()
  THURSDAY = auto()
  FRIDAY = auto()
  SATURDAY = auto()
  SUNDAY = auto()
```

In the documentation of the ``worktoy.desc`` module, the **PySide6**
framework were mentioned as a use case for the ``AttriBox`` class. Below
is a use case for the ``KeeNum`` class in the **PySide6** framework. In
fact, the ``Alignment`` class shown below is a truncated version
of a enumeration class included in the ``ezside`` module currently under
development.

```python
"""Enumeration of alignment using KeeNum. """
# AGPL-3.0 license
# Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from worktoy.keenum import KeeNum, auto


class Alignment(KeeNum):
  """Enumeration of alignment."""
  CENTER = auto()

  LEFT = auto()
  RIGHT = auto()
  TOP = auto()
  BOTTOM = auto()

  TOP_LEFT = auto()
  TOP_RIGHT = auto()
  BOTTOM_RIGHT = auto()
  BOTTOM_LEFT = auto()
``` 

The ``KeeNum`` class might also have been used to enumerate the different
accessor functions, which might have been useful in the ``worktoy.desc``.

```python
"""Enumeration of accessor functions using KeeNum."""
# AGPL-3.0 license
# Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, auto


class Accessor(KeeNum):
  """Enumeration of accessor functions."""
  GET = auto(getattr)
  SET = auto(setattr)
  DEL = auto(delattr)
```

In the above, the ``Accessor`` class enumerates the accessor functions
``getattr``, ``setattr`` and ``delattr``. But the ``auto`` function can
also be used to decorate enumerations, which makes their public values
functions.

```python
"""Implementation of math functions using KeeNum"""
# AGPL-3.0 license
# Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, Any
from worktoy.keenum import KeeNum, auto


class Trig(KeeNum):
  """Enumeration of trigonometric functions."""

  @classmethod
  def factorial(cls, n: int) -> int:
    """This function returns the factorial of the argument."""
    if n:
      return n * cls.factorial(n - 1)
    return 1

  @classmethod
  def recursiveSum(cls, callMeMaybe: Callable, n: int) -> float:
    """This function returns the sum of the function F from 0 to n."""
    if n:
      return callMeMaybe(n) + cls.recursiveSum(callMeMaybe, n - 1)
    return callMeMaybe(n)

  @classmethod
  def taylorTerm(cls, x: float, callMeMaybe: Callable) -> Callable:
    """This function returns a function that calculates the nth term of a
    Taylor series expansion."""

    def polynomial(n: int) -> float:
      return callMeMaybe(n) * x ** n / cls.factorial(n)

    return polynomial

  @auto
  def SIN(self, x: float) -> float:
    """This method returns the sine of the argument."""
    term = lambda n: [0, 1, 0, -1][n % 4]
    return self.recursiveSum(self.taylorTerm(x, term), 17)

  @auto
  def COS(self, x: float) -> float:
    """This method returns the cosine of the argument."""
    term = lambda n: [1, 0, -1, 0][n % 4]
    return self.recursiveSum(self.taylorTerm(x, term), 17)

  @auto
  def SINH(self, x: float) -> float:
    """This method returns the hyperbolic sine of the argument."""
    term = lambda n: n % 2
    return self.recursiveSum(self.taylorTerm(x, term), 16)

  @auto
  def COSH(self, x: float) -> float:
    """This method returns the hyperbolic cosine of the argument."""
    term = lambda n: (n + 1) % 2
    return self.recursiveSum(self.taylorTerm(x, term), 16)

  def __call__(self, *args, **kwargs) -> Any:
    """Calls are passed on to the public value"""
    return self.value(self, *args, **kwargs)
```

## The ``worktoy.ezdata`` module

The ``worktoy.ezdata`` module provides the ``EZData`` class, which
provides a dataclass based on the ``AttriBox`` class. This is achieved by
leveraging the custom metaclass provided by the ``worktoy.meta`` module.
The main convenience of the ``EZData`` is the auto generated ``__init__``
method that will populate fields with values given as positional
arguments or keyword arguments. The keys to the keyword arguments are the
field names.

Below is an example of the ``EZData`` class in use:

```python
"""Dataclass for a point in the plane using EZData."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData
from worktoy.desc import AttriBox


class PlanePoint(EZData):
  """Dataclass representing a point in the plane."""
  x = AttriBox[float](0)
  y = AttriBox[float](0)

  def __str__(self, ) -> str:
    """String representation"""
    return """(%.3f, %.3f)""" % (self.x, self.y)


if __name__ == '__main__':
  P = PlanePoint(69, 420)
  print(P)
  P.x = 1337
  print(P)
  P.y = 80085  # Copilot suggested this for reals, lol
  print(P)
```

### Summary of ``worktoy.ezdata`` module

The ``EZData`` class supports fields with ``AttriBox`` instances. As
explained in the documentation of the ``worktoy.desc`` module, the
``AttriBox`` can use any class as the inner class. Thus, subclasses of
``EZData`` may use any number of fields of any class.

## ``worktoy.text`` module

The ``worktoy.text`` module provides a number of functions implementing
text formatting as listed below:

- ``stringList``: This function allows creating a list of strings from a
  single string with separated values. The separator symbol may be
  provided at keyword argument ``separator``, but defaults to ``','``.
  Strings in the returned lists are stripped meaning that spaces are
  removed from the beginning and end of each string.
- ``monoSpace``: This function fixes the frustrating reality of managing
  longer strings in Python. Splitting a string over multiple lines
  provides only one good option for long strings and that is by using
  triple quotes. This option is great except for the fact that it
  preserves line breaks verbatim. The ``monoSpace`` function receives a
  string and returns it with all continuous whitespace replaced by a
  single space. Additionally, strings may specify explicitly where line
  breaks and tabs should occur by include ``'<br>'`` and ``'<tab>'``
  respectively. Once the initial space replacement is done, the function
  replaces the explicit line breaks and tabs with the appropriate symbol.
- ``wordWrap``: This function receives an int specifying the maximum line
  length and a string. The function returns the string with line breaks
  inserted at the appropriate places. The function does not break words
  in the middle, but instead moves the entire word to the next line. The
  function also removes any leading or trailing whitespace.
- ``typeMsg``: This function composes the message to be raised with a
  ``TypeError`` exception when an ``object`` named ``name`` did not
  belong to the expected class ``cls``.
- ``joinWords``: This function receives a list of words which it
  concatenates into a single string, separated by commas except for the
  final two words which are separated by the word 'and'.

Below are examples of each of the above

### ``worktoy.text.stringList``

```python
"""Example of the 'stringList' function."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations
from worktoy.text import stringList

if __name__ == '__main__':
  baseString = """69, 420, 1337, 80085"""
  baseList = stringList(baseString)
  for item in baseList:
    print(item)

```

### ``worktoy.text.monoSpace``

```python
"""Example of the 'monoSpace' function."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace

if __name__ == '__main__':
  baseString = """This is a string that is too long to fit on one line. 
    It is so long that it must be split over multiple lines. This is 
    frustrating because it is difficult to manage long strings in Python. 
    This is a problem that is solved by the 'monoSpace' function."""
  print(baseString.count('\n'))
  oneLine = monoSpace(baseString)
  print(oneLine.count('\n'))
```

### ``worktoy.text.wordWrap``

```python
"""Example of the 'wordWrap' function."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import wordWrap

if __name__ == '__main__':
  baseString = """This is a string that is too long to fit on one line. 
    It is so long that it must be split over multiple lines. This is 
    frustrating because it is difficult to manage long strings in Python. 
    This is a problem that is solved by the 'wordWrap' function."""
  wrapped = wordWrap(40, baseString)
  print(baseString.count('\n'))
  print(len(wrapped))
  print('\n'.join(wrapped))
```

### ``worktoy.text.typeMsg``

```python
"""Example of the 'typeMsg' function."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import typeMsg

if __name__ == '__main__':
  susObject = 69 + 0j
  susName = 'susObject'
  expectedClass = float
  e = typeMsg(susName, susObject, expectedClass)
  print(e)
```

### ``worktoy.text.joinWords``

```python
"""Example of the 'joinWords' function."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import joinWords

if __name__ == '__main__':
  words = ['one', 'two', 'three', 'four', 'five']
  print(joinWords(words))
```

## ``worktoy.parse`` module

This module provides two ``None``-aware functions:

- ``maybe``: This functions returns the first positional argument it
  received that is different from ``None``.
- ``maybeType``: Same as ``maybe`` but ignoring arguments that are not of
  the expected type given as the first positional argument. 
