
### AbstractAttribute

This is the simpler implementation beginning with ``AbstractAttribute``.
WorkToy provides the following subclasses of this abstract baseclass:

1. ``IntAttribute``
2. ``FloatAttribute``
3. ``StrAttribute``

The above are distinguished only by their type. When instantiating these
a default value may be provided, but is optional.

```python

from worktoy.worktoyclass import WorkToyClass
from worktoy.descriptors import Field, FloatAttribute
from worktoy.descriptors import IntAttribute, StrAttribute


class MyClass(WorkToyClass):
  """Example class"""

  n = IntAttribute(77)
  r = FloatAttribute(0.5)
  name = StrAttribute()

  def __init__(self, *args, **kwargs) -> None:
    WorkToyClass.__init__(self, *args, **kwargs)


myInstance = MyClass()
myInstance.n  # >>> 77
myInstance.n = 7
myInstance.n  # >>> 7
myInstance.r  # 0.5
myInstance.name  # >>> ````
myInstance.name = 'Name'
```
