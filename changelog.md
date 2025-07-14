# Changelog

Beginning with version 0.99.98, the changelog will be maintained in this
file.

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