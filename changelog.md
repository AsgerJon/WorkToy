# Changelog

# [0.99.126] Additions

**2026 February 20**

## Descriptor Protocol Enhancements

### Background

Python provides the descriptor protocol allowing customization of the
attribute access operations. These operations are set, get and delete,
each customizable by implementing the following methods respectively:

- ```__get__```
- ```__set__```
- ```__delete__```

The ```Object``` class provides a general implementation of those methods,
which defers to the following instance specific methods suitable for
overriding by subclasses:

- ```__instance_get__```
- ```__instance_set__```
- ```__instance_delete__```

A get operation where ```instance is None``` does *not* defer to
```__instance_get__```, but instead returns the descriptor itself. This
behaviour is consistent with how accessing a method through an instance
returns a bound method, while accessing through the class returns the
plain function object.

The ```Object``` implements access methods by deferring to the instance
specific methods. With the introduction of the new hooks, the ```Object```
now runs the pre-hook, the instance specific access method and then the
on-hook.

Additionally, the set operations can now be cancelled during this context
manager block by raising ```SkipSet```. This is the first of a new family
of custom exceptions described below. In short, ```SkipSet``` can be
raised during the ```hookPreSet``` hook to cancel the set operation. This
prevents both ```__instance_set__``` and the ```hookOnSet``` during that
set operation.

### Control Flow Exceptions

Python provides a few special exceptions raised to signal events to the
control flow such as ```StopIteration```, ```StopAsyncIteration``` and
```GeneratorExit```. The new ```ControlFlow``` class provides a base for
a family of custom exceptions used to augment the control flow as
implemented by the ```Object``` implementation of the descriptor protocol.

This introduction includes only the ```SkipSet``` signal. The envisioned
use-case is to stop set operations where the new value is the same as the
existing value.

### Access Hooks

Before and after each access operation a hook allows customization of the
control flow. The hooks are given below along with their signatures and a
use-case example.

#### hookPreGet

```python
def hookPreGet(self, instance: Any, ) -> None: ...
```

Trigger lazy instantiation.

#### hookOnGet

```python
def hookOnGet(self, instance: Any, value: Any) -> None: ...
```

Validate value or type and raise appropriate exceptions where appropriate.

#### hookPreSet

```python
def hookPreSet(self, instance: Any, value: Any) -> None: ...
```

Detect redundant set operations where new and existing values are the
same. This should be done by raising ```SkipSet``` as described above.

#### hookOnSet

```python
def hookOnSet(self, instance: Any, value: Any) -> None: ...
```

Please note, that ```SkipSet``` also prevents this hook from running.
Thus, this hook running guarantees that a new value has been set. This
allows the triggering of updates to dependent attributes.

#### hookPreDelete

```python
def hookPreDelete(self, instance: Any) -> None: ...
```

If a particular attribute cannot be allowed to be deleted, but where the
actual deletion procedure is expensive or otherwise disadvantageous, this
hook allows an even earlier raising of preventative exceptions.

#### hookOnDelete

```python
def hookOnDelete(self, instance: Any) -> None: ...
```

This has the same motivation as ```hookOnSet```.

### Reference Implementation

The ```Object``` class has been updated to include the above hooks, but
does not implement any actual functionality in them. The
```BaseDescriptor``` subclass of ```Object``` does. For each hook, the
following decorators allows class bodies to specify methods to be hooked.
Any number of methods can be hooked to the same place in the control flow.
(The naming of the decorators replace 'hook' with the '@' symbol).

- ```@preGet```
- ```@onGet```
- ```@preSet```
- ```@onSet```
- ```@preDelete```
- ```@onDelete```

The two descriptor ```AttriBox``` and ```Field``` provided by
```worktoy.desc``` now subclass ```BaseDescriptor``` instead of subclassing
```Object```. This supports the effort of exposing advanced features
through simple syntax.

## [0.99.98] - 2025 July 14

### Added

#### ```KeeFlags``` to worktoy.keenum

Introducing a powerful, intuitive flag/bitmask system supporting:

- Clean single-flag and multi-flag declaration.
- Full dunder support (`|`, `&`, `^`, `~`, etc.) for easy bitmask math.
- Flexible key and attribute resolution: combos can be accessed via
  string, dict, or even dot-access, in any order and with any separator.
- Robust, user-friendly error handling.

```KeeFlags``` provides enumerations of flag combinations. For example:

```python
from worktoy.keenum import KeeFlags, Kee


class FileAccess(KeeFlags):
  """
  FileAccess demonstrates real-world bitmask flags for file permissions.
  """
  READ = Kee[int](0b0001)
  WRITE = Kee[int](0b0010)
  EXECUTE = Kee[int](0b0100)
  DELETE = Kee[int](0b1000)


if __name__ == "__main__":
  print('_' * 40)
  print("""Iteration over FileAccess:""")
  for permissions in FileAccess:
    print(permissions)
  print('¨' * 40)
  print('_' * 40)
  print("""Flexible resolution of FileAccess flags:""")
  print("""FileAccess.WRITE_READ: %s""" % FileAccess.WRITE_READ)
  print("""FileAccess['execute read']: %s""" % FileAccess['execute read'])
  print("""FileAccess.delete__write: %s""" % FileAccess.delete__write)
  print('¨' * 40)
  print('_' * 40)
  print("""Support of use for KeeFlags as dict keys:""")
  permissions = {
    FileAccess.READ        : 'sure!',
    FileAccess.WRITE       : 'go ahead!',
    FileAccess.EXECUTE     : 'be careful!',
    FileAccess.DELETE      : 'no!',
    FileAccess.NULL        : '... nothing! you lose, good day sir!',
    FileAccess.READ_WRITE  : 'sure, go ahead!',
    FileAccess.READ_EXECUTE: 'sure, but be careful!',
    FileAccess.ALL         : 'yolo!'
    }
  for key, value in permissions.items():
    print("""%s: %s""" % (key, value))
  print('¨' * 40)
  print('_' * 40)
  print("""Implementation of binary operators:""")
  print("""READ | WRITE: %s""" % (FileAccess.READ | FileAccess.WRITE))
  print("""READ & WRITE: %s""" % (FileAccess.READ & FileAccess.WRITE))
  print("""READ ^ WRITE: %s""" % (FileAccess.READ ^ FileAccess.WRITE))
  print("""~DELETE: %s""" % (~FileAccess.DELETE))
  print("""bool(READ): %s""" % bool(FileAccess.READ))
  print("""bool(NULL): %s""" % bool(FileAccess.NULL))
  print('¨' * 40)

```

The above outputs:

```terminaloutput
________________________________________
Iteration over FileAccess:
FileAccess.NULL
FileAccess.READ
FileAccess.WRITE
FileAccess.READ_WRITE
FileAccess.EXECUTE
FileAccess.READ_EXECUTE
FileAccess.WRITE_EXECUTE
FileAccess.READ_WRITE_EXECUTE
FileAccess.DELETE
FileAccess.READ_DELETE
FileAccess.WRITE_DELETE
FileAccess.READ_WRITE_DELETE
FileAccess.EXECUTE_DELETE
FileAccess.READ_EXECUTE_DELETE
FileAccess.WRITE_EXECUTE_DELETE
FileAccess.READ_WRITE_EXECUTE_DELETE
¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
________________________________________
Flexible resolution of FileAccess flags:
FileAccess.WRITE_READ: FileAccess.READ_WRITE
FileAccess['execute read']: FileAccess.READ_EXECUTE
FileAccess.delete__write: FileAccess.WRITE_DELETE
¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
________________________________________
Support of use for KeeFlags as dict keys:
FileAccess.READ: sure!
FileAccess.WRITE: go ahead!
FileAccess.EXECUTE: be careful!
FileAccess.DELETE: no!
FileAccess.NULL: derp
FileAccess.READ_WRITE: sure, go ahead!
FileAccess.READ_EXECUTE: sure, but be careful!
FileAccess.READ_WRITE_EXECUTE_DELETE: yolo!
¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
________________________________________
Implementation of binary operators:
READ | WRITE: FileAccess.READ_WRITE
READ & WRITE: FileAccess.NULL
READ ^ WRITE: FileAccess.READ_WRITE
~DELETE: FileAccess.READ_WRITE_EXECUTE
bool(READ): True
bool(NULL): False
¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
```

## [0.99.97] - 2025 July 13

### Added

#### ```Kee``` to worktoy.keenum

Introduced a dedicated class for marking class body items as
members of the enumeration. This permits **KeeNum** classes to
explicitly set enumeration members, whilst permitting normal methods
and variables as well. ```Kee``` must be used with the following novel
syntax:

```python
from worktoy.keenum import KeeNum, Kee
from worktoy.ezdata import EZData


class RGB(EZData):
  red = 255
  green = 255
  blue = 255
  #  Remaining implementation left as an exercise for try-hard readers


class Color(KeeNum):
  RED = Kee[RGB](255, 0, 0)
  GREEN = Kee[RGB](0, 255, 0)
  BLUE = Kee[RGB](0, 0, 255)
  WHITE = Kee[RGB]()


if __name__ == "__main__":
  print('_' * 40)
  print("""Iteration over Color:""")
  for color in Color:
    print(color)
  print('¨' * 40)
  print('_' * 40)
  print("""Accessing Color.RED:""")
  print(Color.RED)
  print('¨' * 40)
```

The above outputs:

```terminaloutput
________________________________________
Iteration over Color:
Color.RED
Color.GREEN
Color.BLUE
Color.WHITE
¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
________________________________________
Accessing Color.RED:
Color.RED
¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
________________________________________
Values of Color members:
#FF0000
#00FF00
#0000FF
#FFFFFF
¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
```

The above should be familiar to 'worktoy' enjoyers as it uses the same
syntax as the ```AttriBox``` class from 'worktoy.desc'. Declare the type
in the brackets and the arguments to be passed to the constructor of the
type in the parentheses. This allows deferred instantiation of the type,
until invocation of ```__get__```.

The introduction of ```Kee``` joins a complete rewrite from scratch of the
'worktoy.keenum' module.

## [0.99.96] - 2025 July 11

### FIXED

- Removed intended feature supporting ```EZData``` entries with type-hint
  syntax. When the class creation procedure encounters a type-hint in the
  class body, the hooks available to the custom namespace objects could
  not be made aligned with the regular setting of attributes. Support for
  type-hint defined attributes, does not appear to be intended in the
  current Python implementation. Future updates may revisit this feature,
  but new custom namespace techniques would be required.

## [0.99.95] - 2025 July 10

### FIXED

- Removed certain classes and functions in the descriptor implementation.

## [0.99.94] - 2025 July 9

This version marked a major rewrite of the entire 'worktoy' library! Any
version prior to this version, is entirely incompatible with this version.
For this reason, all prior changes have been omitted from this changelog.