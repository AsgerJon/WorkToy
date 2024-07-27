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

## Table of Contents

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

## Installation

```bash 
pip install worktoy
```

## Usage

### `worktoy.desc`

#### Background

The descriptor protocol in Python allows significant customization of the
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

#### Unusual `for-else` statement

The code above features the unusual and under-appreciated for-else
statement in the `__init__` method. If the for loop terminates by the ´break´
keyword, the ´else´ block is skipped. If the for loop completes without
hitting the ´break´ keyword, the ´else´ block is executed. As used here,
the for loop tries to find an integer from the received positional
arguments. If it finds one, it assigns it and hits the ´break´ keyword
and the ´else´ block is skipped. If unable to find an integer, the for
loop will terminate normally, and the ´else´ block will execute, where
the fallback value is conveniently waiting to be assigned.

#### The `__set_name__` method

This method is a powerful addition to the descriptor protocol. To
understand its significance, consider that the descriptor class was
instantiated in the class body, during creation of the owning class,
but before the owning class was actually created. When the owning class
is created, every instance of a class that implements this method,
that was assigned to a name in the class body of the newly created
class, will have this method called with the owning class and the
name at which the instance appears in the class body.

#### The `__get__` method

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

#### Property-like behaviour

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

#### The `property` class

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

#### The `AttriBox` class - Prologue

This class is the central feature of the `worktoy.desc` module. It is the
logical next step of the implementations hitherto discussed. Before
diving into the implementation, let us begin with a use case.

#### PySide6 - Qt for Python

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

#### The `AttriBox` class - Lazy instantiation

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

#### The `AttriBox` class

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
lazy instantiation. Before discussing further use cases of the `AttriBox`
class, we need to discuss a different module in the WorkToy package.

### `worktoy.meta`

Despite significant vandalism having been done to the word 'meta' in
recent memory, it is no match for the power of the Python metaclass. You
are about to embark on a journey beyond. Beyond all boundaries. No other
programming language conceptualizes what the Python metaclass is. Java
reflections? No, no, no. C# attributes, not even close! C++ templates?
Get it out of here! The Python metaclass is the ultimate power tool. You
have heard about metaclasses. Whispers in the corners. Is it possible to
learn this power? Not from a Java programmer. Not from a C# developer.
Not from a C++ programmer. Welcome to the Python metaclass.

#### What is a metaclass?

You already know what a metaclass is. ``type`` is a metaclass. Recall how
the overconfident "online course" instructor told that 'everything is an
object' in Python. That is correct. In fact, the two classes below are in
fact the same:

```python
class MyClass:
  pass


class OldSchool(object):
  pass
```

The ``OldSchool`` class explicitly inherits from the ``object``, but
``MyClass`` is as much a subclass of ``object`` as ``OldSchool``. If you
suffer the misfortune of encountering Python 2 code, you will see the
explicit inheritance from ``object`` that is now implicit in Python 3.
That is not the only implicit thing happening in Python class creation.
In fact:

```python
class SomeClass(object, metaclass=type):
  pass
```

``type`` is a bit odd. It is a class, a metaclass, but also a function:
``type(69) is int``. A function returning the type of the object:
``type(int) is type``. As an alternative to using ``type`` as a function,
the attribute ``__class__`` also returns the type of the object. In this
discussion, ``type`` denotes the default metaclass. In the next section,
we will implement a custom metaclass that behaves as closely as possible
to ``type``.

#### Your first MetaClass!

We will now be sus. We will implement a metaclass behaving as close to how
``type`` behaves as possible. The metaclass will be named ``MetaClass``.

```python
class MetaClass(type):
  """This metaclass behaves as close to the default metaclass 'type' as 
  possible. """

  @classmethod
  def __prepare__(mcls,
                  name: str,
                  bases: tuple[type, ...],
                  **kwargs) -> dict:
    """This special method creates the namespace object used to create 
    the new class. Before the first line in the class body is even 
    executed, this method is called. At each line in the class body that 
    contains a name assignment, the namespace object is updated. By 
    default, '__prepare__' returns an empty dictionary. Custom metaclasses 
    wishing to override this method should definitely keep reading this 
    documentation!
    
    The __prepare__ method is a classmethod and should be decorated as such.
    """
    return dict()

  def __new__(mcls,
              name: str,
              bases: tuple[type, ...],
              namespace: dict,
              **kwargs) -> type:
    """When the class body is complete and collected in the namespace 
    object, this method is invoked. Like the '__prepare__' method, this 
    is a classmethod, but it must NOT be decorated as such. Doing so 
    results in undefined behaviour. """
    cls = type.__new__(mcls, name, bases, namespace, **kwargs)
    #  cls is the newly created class. When this method returns, the 
    #  '__set_name__' methods on descriptors owned by the class are 
    #  invoked.
    return cls

  def __init__(cls,
               name: str,
               bases: tuple[type, ...],
               namespace: dict,
               **kwargs) -> None:
    """This method is called after the '__new__' method. The '__init__' 
    method defined on 'type', the default metaclass, is a no-op. What is 
    relevant to note here is that this method is invoked after the 
    __set_name__ methods have returned. """
    type.__init__(cls, name, bases, namespace, **kwargs)

  def __call__(cls: type, *args, **kwargs) -> object:
    """This method defines what happens when calling the class. This is 
    typically when the class is instantiated. Please note that 
    metaclasses typically allow their derived classes to implement 
    their own '__new__' and '__init__' methods. """
    self = cls.__new__(cls, *args, **kwargs)
    if isinstance(self, cls):
      cls.__init__(self, *args, **kwargs)
    return self

```

The above implementation of the ``MetaClass`` class is as close to the
default metaclass ``type`` as possible. Let us now proceed examining the
different aspects of the custom metaclass.

#### The `__prepare__` method

As mentioned above, the ``__prepare__`` method creates the namespace
object used when creating new classes. Before proceeding with customizing the
``__prepare__`` method, Python does have two requirements for the
namespace objects: First, the namespace object must not only be a mapping
type, it must outright be a subclass of the ``dict`` class. Secondly and
most importantly: The namespace object must implement ``__getitem__``
such that the method raises a ``KeyError`` when receiving an unknown key.
Why is this so important? Because sometimes class bodies have lines that
do not contain assignments. These lines are passed to the ``__getitem__``
method on the namespace object instead passing the left and right hand
sides to the ``__setitem__`` method. To ensure that no undefined
behaviour starts, Python expects the namespace object to raise a
``KeyError`` when receiving an unknown key. If you reimplement
``__missing__`` in the namespace object, you are going to have a bad time.
This author went through many hours of pain to bring you this information.
Much pain.

Having correctly created a namespace object, let us talk about what
happens when the class body is executed. Each line that contains an
assignment is passed to the ``__setitem__`` method on the namespace. What
is lost by the default namespace object, is its inability handle keys
getting overwritten. So a custom namespace object should implement
functionality that preserves existing values when a key is overwritten.
Then when the namespace object is returned to the metaclass, something like
function overloading (foreshadowing) might be implemented. Besides this
single limitation, there is not any improvements possible on the
namespace object. Once previous key values are preserved, the metaclass
should implement the rest of the functionality.

Despite what might seem obvious, the namespace object cannot actually
change what it means to be a class. At most, it can change how a class
body results in a new class, but the class itself remains a class. To
change what it means to be a class requires changes to the metaclass itself.

#### The `__new__` method

Why? Why should an int not be considered an instance of my newly created
class? Why should a class body result in a new class, why not something
entirely new? By reimplementing methods in the metaclass, in
particular ``__new__``, the metaclass can achieve all of this, albeit
being in a way that some may consider unnatural.

