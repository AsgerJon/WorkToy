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

## `worktoy.desc`

### Background

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
    else:  # See explanation below for the unusual for-else statement.
      self.__default_value__ = self.__fallback_value__

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

### Unusual `for-else` statement

The code above features the unusual and under-appreciated for-else
statement in the `__init__` method. If the for loop terminates by the ´break´
keyword, the ´else´ block is skipped. If the for loop completes without
hitting the ´break´ keyword, the ´else´ block is executed. As used here,
the for loop tries to find an integer from the received positional
arguments. If it finds one, it assigns it and hits the ´break´ keyword
and the ´else´ block is skipped. If unable to find an integer, the for
loop will terminate normally, and the ´else´ block will execute, where
the fallback value is conveniently waiting to be assigned.

### The `__set_name__` method

This method is a powerful addition to the descriptor protocol. To
understand its significance, consider that the descriptor class was
instantiated in the class body, during creation of the owning class,
but before the owning class was actually created. When the owning class
is created, every instance of a class that implements this method,
that was assigned to a name in the class body of the newly created
class, will have this method called with the owning class and the
name at which the instance appears in the class body.

### The `__get__` method

This method is called in two different situations that differ
substantially. When the descriptor is accessed through the owning
class and when the descriptor is accessed through an instance of the
owning class. This distinction may be likened to that of accessing a
method. Accessing a method through its owning class returns an
unbound method. In contrast, accessing a method through an instance
of the class returns a method bound to this instance. This is why the
first argument of a method is ´self´ (except for ´classmethods´ and
´staticmethods´).

If the instance is None, it signifies that the descriptor is being
accessed through the owning class. In this case, it is the opinion of
this author that the descriptor should always return itself. This allows
other objects to access the descriptor object itself, instead of the
value it wraps. Choosing this return value also follows the pattern
used by methods. Nevertheless, descriptor classes are allowed to
return any object when accessed through the owning class.

This brings the discussion to the central situation allowing significant
customization of what it even means for a Python class to have an
attribute. This part of the discussion will explain some typical uses
before describing the novel use case provided by the ´AttriBox´ class,
which is the central feature of the ´worktoy.desc´ module.

### Property-like behaviour

A common implementation of the descriptor protocol makes use of a
'private' attribute owned by the instance. Python does not enforce 'private'
attributes, but the convention is to denote attributes intended to remain
'private' with a leading underscore. While convention only, IDEs and
linters will commonly mark as warning or even an error when this
convention is not observed. It is the opinion of this author that issues
caused by failure to observe this convention does not merit fixing, with
the sole exception being security related issues.

Below is an example using a descriptor class to expose a 'private'
attribute through dedicated accessor functions.

```python

class SpacePoint:
  """This class represent an integer valued point in the plane. """
  _x = None
  _y = None
  x = Float(0.)
  y = Float(0.)
```   

Like before, it is the descriptor class more so that the owner class that
is the subject of this discussion:

```python
class Float:
  """Descriptor class wrapping a floating point value"""
  __field_name__ = None
  __field_owner__ = None
  __fallback_value__ = 0.0
  __default_value__ = None

  def __init__(self, *args, ) -> None:
    for arg in args:
      if isinstance(arg, float):
        self.__default_value__ = arg
        break
    else:  # See explanation below for the unusual for-else statement.
      self.__default_value__ = self.__fallback_value__

  def __set_name__(self, owner: type, name: str) -> None:
    self.__field_name__ = name
    self.__field_owner__ = owner

  def _getPrivateName(self) -> str:
    """This 'private' method formats the name at which instances of this 
    descriptor class will expect 'private' attributes. """
    if self.__field_name__ is None:
      e = """Unable to format private name, before owning class is 
      created!"""
      raise RuntimeError(e)
    if isinstance(self.__field_name__, str):
      return """_%s""" % self.__field_name__
    e = """Expected field name to be instance of str, but received '%s' 
    of class '%s'!"""
    fieldName = self.__field_name__
    typeName = type(fieldName).__name__
    raise TypeError(e % (fieldName, typeName))

  def __get__(self, instance: object, owner: type, **kwargs) -> object:
    """Getter-function. If instance is None, the descriptor instance 
    returns itself. Otherwise, the descriptor attempts to find a value at 
    the expected private name. If no value is present, the default value 
    of the descriptor is assigned to the expected private name and the 
    getter function is called recursively again. This pattern ensures 
    that if the descriptor lacks permission or is otherwise unable to 
    assign values to owning instances, an error is raised immediately. """
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is not None:
      return getattr(instance, pvtName)
    if kwargs.get('_recursion', False):
      raise RecursionError
    setattr(instance, pvtName, self.__default_value__)
    return self.__get__(instance, owner, _recursion=True)

  def __set__(self, instance: object, value: object) -> None:
    """Setter-function. Although not provided in this example, setter 
    functions provide a convenient place to enforce constraints, in 
    particular type guarding as well as casting and validation. """
    pvtName = self._getPrivateName()
    setattr(instance, pvtName, value)

  def __delete__(self, instance: object) -> None:
    """IMPORTANT! This method is what is called when the 'del' keyword is 
    used on an attribute through an instance. This method is NOT the same 
    as __del__. This latter method is called when the object itself is 
    deleted. Regarding that particular method, this author finds occasion 
    to mention never having observed it implemented in the wild. """
    pvtName = self._getPrivateName()
    if hasattr(instance, pvtName):
      return delattr(instance, pvtName)
    e = """Instance of class '%s' does not have attribute '%s'!"""
    raise AttributeError(e % (instance.__class__.__name__, pvtName))
```

The above describes a common pattern of using the descriptor protocol to
expose 'private' attributes through dedicated accessor functions. The
above is a very straightforward example, but the descriptor protocol is
capable of much more!

### The `property` class

It is likely that some readers are familiar with the `property` class.
Where we are going we do not need the `property` class! Nevertheless, let
us now see a descriptor class that implements the behaviour of the
property class. The property class may seem like advanced or
sophisticated, but as this discussion progresses, the mundane and simple
nature of it will reveal itself.

To avoid confusion, this implementation will be named `Field` as the
name ``property`` is already taken.

```python
class Field:
  """Descriptor class wrapping a value"""
  __field_name__ = None
  __field_owner__ = None
  __default_value__ = None
  __getter_function__ = None
  __setter_function__ = None
  __deleter_function__ = None

  def __init__(self, *args) -> None:
    if args:
      self.__default_value__ = args[0]

  def __set_name__(self, owner: type, name: str) -> None:
    self.__field_name__ = name
    self.__field_owner__ = owner

  def _getGetterFunction(self, ) -> Callable:
    """This 'private' method returns the getter-function. This must be
      explicitly defined by the GET decorator for the descriptor to 
      implement getting. This allows significant customization of the 
      attribute access mechanism. """
    if self.__getter_function__ is None:
      e = """The getter-function must be explicitly set by the SET 
      decorator!"""
      raise AttributeError(e)
    if callable(self.__getter_function__):
      return self.__getter_function__
    e = """Expected getter-function to be callable, but received '%s'
        of class '%s'!"""
    func = self.__getter_function__
    typeName = type(func).__name__
    raise TypeError(e % (func, typeName))

  def _getSetterFunction(self, ) -> Callable:
    """This 'private' method returns the setter-function. This must be 
    explicitly defined by the SET decorator for the descriptor to 
    implement setting. Please note, that the setter-function is by no 
    means required and in particular when the descriptor is used to 
    provide a readonly attribute, the setter-function should remain 
    undefined or even defined as a Callable raising an exception. If so, 
    this author suggests raising a TypeError to indicate that this is a 
    readonly object. Alternatively, raising an AttributeError is also 
    observed, although such an error indicates that the instance is not 
    presently capable of supporting this attribute. Not that the object 
    is entirely incapable of supporting setting the attribute. """
    if self.__setter_function__ is None:
      e = """The setter-function must be explicitly set by the SET 
      decorator!"""
      raise AttributeError(e)
    if callable(self.__setter_function__):
      return self.__setter_function__
    e = """Expected setter-function to be callable, but received '%s'
        of class '%s'!"""
    func = self.__setter_function__
    typeName = type(func).__name__
    raise TypeError(e % (func, typeName))

  def _getDeleterFunction(self, ) -> Callable:
    """This 'private' method returns the deleter-function. This is the 
    method called when the 'del' keyword is used on an attribute through
    an instance. This method is NOT the same as __del__ as discussed 
    above. This author notes having never had problem solved by 
    implementation of the deleter-function. """
    if self.__deleter_function__ is None:
      e = """The deleter-function must be explicitly set by the SET 
      decorator!"""
      raise AttributeError(e)
    if callable(self.__deleter_function__):
      return self.__deleter_function__
    e = """Expected deleter-function to be callable, but received '%s'
        of class '%s'!"""
    func = self.__deleter_function__
    typeName = type(func).__name__
    raise TypeError(e % (func, typeName))

  def GET(self, callMeMaybe: Callable) -> Callable:
    """As alluded to above, this method sets the method that should be 
    used as the getter-function. Classes owning instances of this 
    descriptor class should use this method as a decorator to define the 
    method that should be invoked by the __get__ method. Please note, 
    that this method as well as the other method setters return the 
    decorated method as it is without augmenting it. """
    if self.__getter_function__ is not None:
      e = """The getter-function has already been set!"""
      raise AttributeError(e)
    if not callable(callMeMaybe):
      e = """Expected getter-function to be callable, but received '%s'
        of class '%s'!"""
      typeName = type(callMeMaybe).__name__
      raise TypeError(e % (callMeMaybe, typeName))
    self.__getter_function__ = callMeMaybe
    return callMeMaybe

  def SET(self, callMeMaybe: Callable) -> Callable:
    """Similar to the GET method defined above, this method should be 
    used to decorate the desired setter-function on the owning class. """
    if self.__setter_function__ is not None:
      e = """The setter-function has already been set!"""
      raise AttributeError(e)
    if not callable(callMeMaybe):
      e = """Expected setter-function to be callable, but received '%s'
            of class '%s'!"""
      typeName = type(callMeMaybe).__name__
      raise TypeError(e % (callMeMaybe, typeName))
    self.__setter_function__ = callMeMaybe
    return callMeMaybe

  def DELETE(self, callMeMaybe: Callable) -> Callable:
    """Similar to the GET and SET methods defined above, this method 
    defines the method on the owning class that is responsible for 
    deleting the attribute from the owning instance. """
    if self.__deleter_function__ is not None:
      e = """The deleter-function has already been set!"""
      raise AttributeError(e)
    if not callable(callMeMaybe):
      e = """Expected deleter-function to be callable, but received '%s'
            of class '%s'!"""
      typeName = type(callMeMaybe).__name__
      raise TypeError(e % (callMeMaybe, typeName))
    self.__deleter_function__ = callMeMaybe
    return callMeMaybe

  def __get__(self, instance: object, owner: type, **kwargs) -> object:
    """Getter-function. As before, when instance is None, the descriptor 
    returns itself. Otherwise, the dedicated getter-function is used to 
    get the descriptor value. As mentioned, this function should be 
    defined by the owning class using the GET decorator. The function 
    should be a bound method, as this method assumes that the first 
    argument should be the instance itself, or 'self'. 
    
    Please note, that the GET decorator is called before the owning 
    instance is ever created. This means that this descriptor instance 
    does own the getter-function, but as an unbound method, meaning that 
    the getter-function thus defined is common between all instances of 
    the owning class, despite being an instance method.  The same is true 
    for the setter-function and the deleter-function. """
    if instance is None:
      return self
    getter = self._getGetterFunction()
    return getter(instance, )

  def __set__(self, instance: object, value: object) -> None:
    """Setter-function. As before, the setter-function should be defined
    by the owning class using the SET decorator. If the descriptor is 
    not intended to support setting, the setter-function should be 
    explicitly defined to raise an appropriate exception rather than 
    just left undefined, although this is not a strict requirement. """
    setter = self._getSetterFunction()
    setter(instance, value)

  def __delete__(self, instance: object) -> None:
    """Deleter-function. As before, the deleter-function should be 
    defined by the owning class using the DELETE decorator. Although not 
    commonly used, this author suggests either providing an 
    implementation or a method that raises a TypeError. """
    deleter = self._getDeleterFunction()
    deleter(instance, )
```

Having implemented the `Field` class, some readers will certainly
recognize its use as identical, more or less, to that of the `property`.
One exception to note however is that instances of ``Field`` should be
defined at the top of the class body, unlike the `property` class.

```python
class Server:
  """This example class uses instances of the Field class to define the 
  address and port attributes typically used in server classes. """

  __fallback_address__ = 'localhost'
  __fallback_port__ = 12345

  __private_address__ = None
  __private_port__ = None

  address = Field()
  port = Field()

  @address.GET
  def _getAddress(self, ) -> str:
    """Getter-function responsible for returning the address."""
    if self.__private_address__ is None:
      return self.__fallback_address__
    return self.__private_address__

  @address.SET
  def _setAddress(self, value: str) -> None:
    """Setter-function responsible for setting the address."""
    self.__private_address__ = value

  @address.DELETE
  def _deleteAddress(self, ) -> Never:
    """For the sake of example, let us disable the deleter-function to 
    illustrate how the accessor provide a convenient protection against 
    inadvertent deletion of attributes. Please note the use of the 
    'Never' type hint. This is meant to indicate that this method will 
    never return. Once this method is invoked, the program will certainly 
    raise an exception. """
    e = """The address attribute is read-only!"""
    raise TypeError(e)

  @port.GET
  def _getPort(self) -> int:
    """Getter-function responsible for returning the port."""
    if self.__private_port__ is None:
      return self.__fallback_port__
    return self.__private_port__

  @port.SET
  def _setPort(self, port: int) -> None:
    """Setter-function responsible for setting the port."""
    self.__private_port__ = port

  @port.DELETE
  def _delPort(self, ) -> Never:
    """Disabled deleter-function for the port attribute. The same as for 
    the address attribute."""
    e = """The port attribute is read-only!"""
    raise TypeError(e)
```

The above ``Server`` class does have an unfortunate boilerplate to
functionality ratio. Hopefully it provides a helpful illustration of the
descriptor protocol. While implementing all methods of the descriptor
protocol, the ``Field`` class could be further enhanced by implementing
strong type checking or even casting. This is left as an exercise for
those readers who have read the guidelines in the contribution section.

### The `AttriBox` class - Prologue

This class is the central feature of the `worktoy.desc` module. It is the
logical next step of the implementations hitherto discussed. Before
diving into the implementation, let us begin with a use case.

### PySide6 - Qt for Python

The PySide6 library provides Python bindings for the Qt framework. What
is Qt? For the purposes of this discussion, Qt is a framework for
developing professional and high-quality graphical user interfaces.
Entirely with Python. Below is a very simple script that opens an empty
window and nothing more.

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QSize


class MainWindow(QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setWindowTitle("Hello, World!")
    self.setMinimumSize(QSize(480, 320))


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
```

From here, the window class can be extended to include buttons, text boxes,
and other widgets. Qt provides off-the-shelf widgets for much common use.
These widgets may be subclassed further customizing their appearance or
behaviour. Actually advanced users may even create entirely new widgets
from the ground up. The possibilities are endless.

Before we get carried away, we need to keep one very important quirk in
mind. Qt provides a vast array of classes that all inherit from the
`QObject` class. This class has an odd, but very unforgiving requirement.
No instances of `QObject` may be instantiated without a running
QCoreApplication. This immediately presents a problem to our otherwise
elegant descriptor protocol: We are not permitted to instantiate
instances before the main script runs. Such as during class creation. For
this reason, the `AttriBox` class was created to implement lazy
instantiation! Let us now see how we might create a more advanced
graphical user interface whilst adhering to the `QObject` requirement.

### The `AttriBox` class - Lazy instantiation

```python
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import QSize

from worktoy.desc import AttriBox, THIS


class MainWindow(QMainWindow):
  """Subclass of QMainWindow. This class provides the main window for the 
  application. """

  baseWidget = AttriBox[QWidget](THIS)
  verticalLayout = AttriBox[QVBoxLayout]()
  welcomeLabel = AttriBox[QLabel]()

  def show(self) -> None:
    """Before invoking the parent method, we will setup the window. """
    self.setMinimumSize(QSize(480, 320))
    self.setWindowTitle("WorkToy!")
    self.welcomeLabel.setText("""Welcome to AttriBox!""")
    self.verticalLayout.addWidget(self.welcomeLabel)
    self.baseWidget.setLayout(self.verticalLayout)
    self.setCentralWidget(self.baseWidget)
    QMainWindow.show(self)


if __name__ == "__main__":
  app = QApplication([])
  window = MainWindow()
  window.show()
  app.exec()
```

The above script makes use of the lazy instantiation provided by the
`AttriBox` class. While some readers may have recognized the
similarities between ``Field`` and ``property``, many readers are presently
picking jaws up from the floor, pinching themselves or seeking spiritual
guidance. The `AttriBox` not only implements an enhanced version of the
descriptor protocol, but it does so on a single line, where it even
provides syntactic sugar for defining the class intended for lazy
instantiation. Let us examine ``AttriBox`` in more detail.

### The `AttriBox` class

```python
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import QSize

from worktoy.desc import AttriBox, THIS


class MainWindow(QMainWindow):
  """Subclass of QMainWindow. This class provides the main window for the 
    application. """

  baseWidget = AttriBox[QWidget](THIS)
  #  The above line creates a descriptor at name 'baseWidget' that will 
  #  instantiate a QWidget instance. When the __get__ on the descriptor
  #  tries to retrieve the value it owns, only then will the value be 
  #  instantiated. When instantiating the value, the arguments in the 
  #  parentheses are passed to the constructor of the class. That brings 
  #  us to the 'THIS' token. When instantiating the value, the 'THIS' token
  #  is replaced with the instance of the owning class. This is convenient 
  #  for the 'baseWidget' attribute, as it allows the instance created to 
  #  set its parent to the owning instance.
```

The use case pertaining to the PySide6 library makes great use of the
lazy instantiation. In fact, the motivation that led to the creation of
the ``AttriBox`` class was this need for lazy instantiation.

### ``worktoy.desc.AttriBox`` - Advanced Instantiation

PENDING...
WorkToy v1 will not release until this documentation is complete.

## worktoy.meta - Understanding the Python metaclass

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
``type`` creates a new class. In the example below, we create a simple
class and we will examine the exact steps that the ``type`` class takes
during class creation.

```python
from worktoy.desc import AttriBox


class PlanePoint:
  """Class representing a point in the plane """

  x = AttriBox[float]()
  y = AttriBox[float]()

  def __init__(self, *args) -> None:
    """Constructor for the PlanePoint class. """
    floatArgs = [float(arg) for arg in args if isinstance(arg, (int, float))]
    self.x, self.y = [*floatArgs, 0.0, 0.0][:2]

  def __abs__(self, ) -> float:
    """Returns the distance from the origin. """
    return (self.x ** 2 + self.y ** 2) ** 0.5


if __name__ == '__main__':
  P = PlanePoint(69, 420)
```

When the Python interpreter encounters the line beginning with the
reserved keyword ``class``, it creates a new class object, it begins a
new lexical scope and the contents parentheses after the name determine
what happens next. If no such parentheses are present, the default
behaviour is to create a new instance of ``type``, meaning an extension
of ``object``. This starts the following process:

- **namespace**: ``type`` creates a namespace object that the interpreter
  will use to build the new class. This object is simply an empty
  instance of ``dict``.
- **Class Body Execution**: The interpreter goes through the class body
  line by line from top to bottom. When encountering an assignment, it
  updates the namespace accordingly.
- **Class Object Creation**: The interpreter passes the namespace object
  back to ``type`` that creates the new class object. This happens when
  the ``__new__`` method of ``type`` returns.
- **Descriptor Class Notification**: All ``__set_name__`` methods on
  objects owned by the class are notified, receiving the class object as
  the first argument and the name by which the object is assigned to the
  owning class. In the above example, the ``AttriBox`` objects are
  notified: ``PlanePoint.x.__set_name__(PlanePoint, 'x')`` and
  ``PlanePoint.y.__set_name__(PlanePoint, 'y')``.
- **``type.__init__``:** This is the final step before the ``type`` is
  complete and the class object is returned. Please note that the
  interpreter uses highly optimized C code during this whole procedure,
  and the ``type.__init__`` has no C code implementation making it a noop.
- **Class Instantiation**: Once the class object is created, instances of
  the class may now be created. This begins with a call the ``__call__``
  method on the class object. This method is defined by ``type``. If the
  class itself defines ``__call__``, that method is invoked only when an
  instance of the class is called.
- **``type.__call__(cls, *args, **kwargs)``**: This call on the ``type``
  object creates the new instance of the class.
- **``cls.__new__(cls, *args, **kwargs)``**: This method is responsible
  for creating the new instance of the class. Please note that it makes
  use of the ``__new__`` method defined on the class object. This means
  that new classes are able to customize how new instances are created,
  however implementing the ``__init__`` method defined below is more
  common and quite sufficient for most purposes.
- **``cls.__init__(self, *args, **kwargs)``**: When the new instance is
  created, it is passed to the ``__init__`` method on the class. When
  coding custom classes implementing the ``__init__`` method is the most
  convenient way to define how new instances are initialized.

### What is a metaclass?

In the previous section, we examined how ``type`` creates a new class.
What exactly is ``type`` though? ``type`` is an ``object``, but is also
an extension of ``object`` whose instances themselves are extensions of
``object``. But what if we extended ``type``? We can do that because
``type`` itself extends ``object``. This is what a metaclass is. An
extension of the ``type`` extension of ``object``.

Each of the steps in the class creation process described above may be
customized by extending the ``type`` class. Below is a list of the
methods defined on ``type`` that a custom class may override:

- **``__prepare__``**: In the previous
  section when the namespace object was created, this is done by the
  ``__prepare__`` method on the metaclass. The ``type`` implementation of
  ``__prepare__`` returns an empty dictionary. A metaclass can change
  this by prepopulating the items in this dictionary or even return a
  custom namespace object.
- **``__new__``**: This method is responsible for creating the object
  that will be created at the name after the class definition. This is
  where a new class is conventionally created, but this is by no means a
  requirement for a custom metaclass. It is possible to implement a
  metaclass that creates some other object than a new class.
- **``__init__``**: After the metaclass has created the new class object,
  or whatever object is created, it is passed to the ``__init__`` method.
  Please note that this method is called after the ``__set_name__`` has
  been applied to the objects implementing the descriptor protocol. When
  this method returns the new class object is created.

After the metaclass has created the new class and has returned the
``__init__``, the metaclass is still called by the class object under
certain circumstances. Below is a list of methods that on the metaclass
that may be called during class lifetime:

- **``__call__``**: When an instance of the class is called, the
  ``__call__`` method on the metaclass is invoked. By default, the
  ``__new__`` on the created class object is called, and the object
  returned is passed to the ``__init__`` method on the class object. The
  metaclass may override this behaviour.
- **``__instance_check__``**: When the ``isinstance`` function is called,
  the metaclass is called with create class and the instance. Thus, the
  metaclass may specify how classes derived from it determine if an
  instance is an instance of it. For example, a custom metaclass creating
  Numerical classes might recognize instances of ``float`` or ``int`` as
  their own.
- **``__subclass_check__``**: This is the method called when
  ``issubclass`` is called on a class object derived from the metaclass.
  It allows the metaclass to customize what classes it regards as
  subclasses. Similar to the ``__instance_check__``.
- **``__str__``: When printing a class object, the resulting text is
  frequently more confusing than helpful. I defined a class named
  ``TestClass`` in the main script and printed it. The output was:
  ``<class '__main__.TestClass'>``. But suppose we used a custom
  metaclass ``MetaType`` and derived from it a class called ``TestClass``,
  then the default output would be: ``<class '[MODULE].TestClass'>``, but
  it will not make reference to the metaclass. Instead, let us have the
  metaclass improve this output: ``[MODULE].TestClass(MetaType)``.
- **``__iter__`` and ``__next__``**: Conventionally, iterating over an
  object happens on the instance level, and only by implementing the
  iteration protocol on the metaclass level can the class object itself
  become iterable.
- **``__getitem__``**: This method allows a metaclass to define handling
  of ``cls[key]``. Please note that as of Python version 3.9, Python
  classes may implement a method called ``__class_getitem__``, which is
  intended for the same use. In case both the metaclass and the class
  itself implement these classes respectively, the metaclass
  implementation is used and the class version is ignored.
- **``__setitem__``**: This method allows a metaclass to define handling
  of ``cls[key] = value``.

Above is a non-exhaustive list of ``type`` methods that a custom metaclass
may override. Before proceeding, we must discuss the role of the
namespace object. A significant aspect of the custom metaclass is the
ability to provide a custom namespace object.

### Custom Namespace

Going back to the class creation procedure, the interpreter requests a
namespace object from the metaclass. A custom metaclass may reimplement
the ``__prepare__`` method responsible for creating the custom namespace
and have it return an instance of a custom namespace class. Doing so
places a few subtle requirements on this class.

### Preservation of ``KeyError``

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

### Subclass of ``dict``

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

### Required functionalities

Please note that this section pertains only to functionalities whose
absense will cause the interpreter to raise an exception. The
functionalities described here cannot be said to be sufficient for any
degree of functionality. A custom namespace class must additionally
implement whatever functionality is required for its intended purpose.

- **``__getitem__``**: This method must implement this method such that
  if a normal dictionary would raise an error on receiving a key, then
  that error must still be raised. Please note, that the interpreter
  handles this exception silently. Other than this situation, the
  ``__getitem__`` method are otherwise free to do anything it wants.
- **``__setitem__``**: The namespace object must return a callable object
  at name ``__setitem__``, that accepts three positional arguments: the
  namespace instance at the ``self`` argument, as well as the ``key`` and
  the ``value``. As long as a callable is at the name, and it does not
  raise an error upon receiving three arguments, the namespace object can
  do whatever it wants. It does not even have to remember anything.

### Potential functionalities

This section describes functionalities that is certain to preserve all
information received in the class body. This is an enhancement compared
to the default namespace object. It permits the ``__new__`` in the
metaclass access to all information encountered in the class body. As
long as this is satisfied, there is little additional functionality the
namespace object may provide to the ``__new__`` method. Nevertheless,
readers are encouraged to experiment with custom namespace classes beyond
this.

### Custom Metaclass Requirements

This section illustrates the immense flexibility of the custom metaclass,
by just how little is actually required for the interpreter to go through
the class creation process without raising an exception. This author has
found only two requirements for the custom metaclass:

- **Callable**: The object used as ``metaclass`` must be callable.
- **Accept three positional arguments**: As well as being callable, three
  positional arguments are passed to it. As long as doing so does not
  raise an exception, the metaclass is free to do whatever it wants.

And that is all that is required. The metaclass is typically a subclass
of ``type``, but is not required. Conventionally, some kind of class
object is created, but is not required. The metaclass is not even
required to return anything in which case, the ``None`` object will
appear at the given class name. Thus, the custom metaclass can be used to
create new classes, but in reality it can be used to create anything. It
could be used to replace functions defined with the ``def`` keyword.
Readers are encouraged to dream up new uses for the custom metaclass.

The remainder of this documentation focus on the ``worktoy.meta`` module
and the classes and functions defined therein. These focus on the more
conventional applications of the custom metaclass, that is, creation of
classes having functionalities beyond the default Python classes.

## The ``worktoy.meta`` module

### Nomenclature

Before proceeding, let us define terms:

- **``cls``** - A newly created class object
- **``self``** - A newly created object that is an instance of the newly
  created class.
- **``mcls``** - The metaclass creating the new class.
- **``namespace``** - This is where the class body is stored during class
  creation.

### ``AbstractMetaclass`` and ``AbstractNamespace``

These abstract baseclass illustrates an elegant metaclass pattern. The
namespace class records every assignment in the class body, even if a
name is assigned a value for the second time. The namespace class also
implements a method called ``compile`` which returns a regular dictionary
with the items the metaclass should pass on to the ``type.__new__``
method. Without further subclassing, instances of this namespace class,
will provide behaviour indistinguishable from the default behaviour.

The abstract metaclass implements the ``__prepare__`` class method which
returns creates an instance of the abstract namespace class defined above.
In the ``__new__`` method the metaclass retrieves the final namespace
dictionary by calling the ``compile`` method on the namespace object.
With this it calls the ``type.__new__`` method with the thus obtained
namespace object. The class object returned from the call to
``type.__new__`` is returned by the abstract metaclass.

This pair of abstract classes provides a solid pair of baseclasses. The
pattern is convenient, the metaclass instantiates the namespace object.
Without loss of information, the namespace object is returned to the
metaclass. Here the metaclass obtains the final namespace dictionary from
the ``compile`` method on the namespace object.

### Singleton

The singleton term is well understood as a class having only one
instance. Typically, such a class is callable, but instead of creating a
new instance, the same singleton instance is returned. However, when the
singleton class is called the singleton instance will have its
``__init__`` repeated with whatever arguments are passed. This allows the
singleton instance to update itself. If this is undesirable, the
singleton class should itself prevent its ``__init__`` method from
updating values intended to immutable.

``worktoy.meta`` provides a metaclass called ``SingletonMeta`` and a
derived class called ``Singleton``. Custom singleton classes may either
set ``SingletonMeta`` as the metaclass or subclass ``Singleton``. The
metaclass subclasses the ``BaseMetaclass`` discussed below.

### Zeroton

The ``Zeroton`` class is a novelty. What specified the singleton class is
the fact that it has only one instance. The ``Zeroton`` class in contrast
has not even one instance. Such a class is essentially a token. The
purpose of it is to retain itself across multiple modules. Presently, it
finds use in the ``AttriBox`` implementation of the ``worktoy.desc``
module. For more information, readers are referred to the section on
"Advanced Instantiation" in the ``worktoy.desc`` documentation.

### Function overloading in Python

When creating a new class using the default ``type``, only the most
recent assigned value at each name is retained. As such, implementing
overloading of methods in the class body requires a custom metaclass
providing a custom namespace. The ``worktoy.meta`` module provides the
``BaseObject`` class derived from the ``BaseMetaclass``, which implements
function overloading of the methods in the class body. Before
demonstrating the syntactic use of the ``BaseObject`` class, an
explanation of the implementation is provided. To skip directly to the
usage, see section **worktoy.meta.overload - Usage**.

### Background

The main issue with function overloading is that multiple callables are
now present on the same name. Thus, a new step is required to determine
which available implementation to invoke, given the arguments received.
The procedure chosen here is to contain the pairs of type signatures and
callables in a dictionary. When the overloaded function is called, the
type signature of the arguments is determined and used to look up the
appropriate callable in the dictionary, before invoking it with the
argument values. This step does add some overhead, but in testing has not
exceeded 20 %.

### Type Decoration

When a class body is to define multiple callables at the same name, but
with different functions, the ``worktoy.meta.overload`` decorator factory
is used. When calling it with types as positional arguments, it returns a
decorator. When this decorator is called it sets the type signature of
the decorated function at the attribute named
``__overloaded_signature__`` to the type signature given the factory.

### Function Dispatcher

The ``BaseNamespace`` uses a dedicated class called ``Dispatcher`` to
encapsulates the type signature to callable mapping. The ``Dispatcher``
class implements both the descriptor protocol and the ``__call__`` method
allowing it to emulate the behaviour of bounded and unbounded methods as
appropriate. When called it determines the type signature of the
arguments received, resolve the matching callable, invokes it with the
arguments received and returns the return value.

### Namespace Compilation

The ``BaseMetaclass`` implements the pattern described previously, where
the namespace class provides functionality for creating a dictionary to
be used in the ``type.__new__`` method. This ``compile`` method retrieves
the callables encountered during class body execution that were decorated
with by the overload decorator and for each name creates a ``Dispatcher``
instance as described above, which is placed in the final dictionary at
the appropriate name.

```python
from worktoy.meta import BaseObject

```

### ``worktoy.meta.overload`` - Usage