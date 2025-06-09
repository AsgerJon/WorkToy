"""
AbstractDescriptor provides the base class for descriptors in the
'worktoy.attr' module. It inherits the descriptor protocol from the
'worktoy.static.AbstractObject' class and enhances it. Please note that
instances of this class and subclasses are intended to be defined inside a
class body. The class created from this body 'owns' the descriptor instance.

The enhancements include:

# Instance specific accessor functions.

This means that an instance owned by a class can have any callable
assigned to each accessor function. The type signatures expected for these
are as follows:
# #  getter(instance: Any, ) -> Any:
# #  setter(instance: Any, value: Any) -> None:
# #  deleter(instance: Any) -> None:

This allows for two different paths for descriptors that diverge as they
subclass AbstractDescriptor:
#  1. The owning class must explicitly specify each accessor function for
example by use of decorators (foreshadowing). (This is similar to the
builtin 'property' class).

#  2. The descriptor class itself implements each accessor function. This
will always be less flexible than the first option, but can reuse advanced
behaviour across multiple descriptors and even classes. A common use-case
is lazy instantiation of a wrapped class such that the wrapped class is
not instantiated until requested by a '__get__' call.

#  Accessor hooks.
The accessors have hooks in their operation flow. The 'getter' has pre,
fix and post hooks invoked before, during and after the value returns.
'setter' and 'deleter' have pre- and post-hooks invoked before and after
respectively.

#  Use Cases
The hooks surrounding each accessor provide a convenient place to
implement logging, debugging and validation functionality. Other common
use cases are specific to the accessor such as caching. The hooks also
allow for more imaginative behaviour even to the point of being
unconventional. The less conventional the behaviour, the more thorough the
documentation.

#  Hooks
#  #  '__get__'
The 'getter' is a general concept in computer science, requiring the
following two steps:
1.  Retrieval of the object to be returned.
2.  Returning the retrieved object.
The 'setter' and 'deleter' in contrast are single step operations. This
extra step required by the 'getter' is accounted for by the third hook,
'fix' invoked between the retrieval and return steps.

#  #  #  preGET(instance: Any, value: Any=None) -> Any:
Each hook is invoked in order registered. The first hook receives no
value, the remaining hooks receive the value returned by the previous
hook. If the final hook returns a value other than 'None', the normal
retrieval operation is skipped and proceeds with the value.

Please note, that a pre hook returning 'None' after an earlier hook has
returned a value, it is not replaced. If for some reason a pre hook wishes
to cancel a previously set value, it must raise 'BadCache'. When the flow
catches 'BadCache', it ignores values returned by pre hooks and retrieves
the value normally. This is highly discouraged, if a value does need some
adjustment, use the fix hook defined below:

#  #  #  Retrieval of Value
The 'setter' and 'deleter' hooks receive the existing value or the error
encountered when attempting retrieval. By setting keyword argument
'_root', the 'getter' hooks are entirely ignored. To facilitate this,
the underlying retrieval operation must raise 'MissingVariable' which is
the only exception caught in this flow. The alternative of just catching
and returning any 'Exception' object is poor practice. By requiring that
the retrieval procedure is able to recognize an allowable exception,
such as when a value has not been set for the first time, the flow is
safer and cleaner.

Final word: It is highly discouraged to implement a retrieval operation
that deliberately returns 'None' for any reason. Doing so invites
confusion whether the value is set. In particular, the following two
conditions should never both be true:

if getattr(instance, key, None) is None and hasattr(instance, key):
  raise ...  # Bad, awful, terrible!

#  #  #  FIX(instance: Any, value: Any) -> Any:
The hook in between retrieval and return is the 'fix' hook. This hook
allows modification of the value retrieved before it is returned. When
multiple hooks are registered, the value returned by the previous hook is
passed to the next hook. If a hook returns 'None', the previous value is
used. If a hook wants to cancel a previously set value, it must raise
'BadCache'.

#  #  #  Return Value
Following the fix hooks, the value is returned, but it happens in a
try/finally block to allow for post hooks after returning the value. A
common misconception is that nothing further can happen after 'return',
but finally clauses are executed after the return statement. Please note
that this limits what should be done in the finally block. Specifically,
the finally block can raise exceptions where appropriate, which replaces
any waiting exceptions, but this is allowed. What is bad practice is for
the 'finally' clause to: break, continue, yield or return. Beginning in
Python 3.14 doing so triggers a 'SyntaxWarning' (same in the alpha builds
of 3.15 available at the time of writing).

#  #  #  postGET(instance: Any, value: Any) -> None:
After the value has been returned, the post hooks are invoked. These are
not able to change the value returned, but any further processing
involving the returned value is waiting for the finally block. For example:

#  Test script
from __future__ import annotations

import sys

def foo() -> int:
  try:
    return 69
  finally:
    print('Finally block!')

class Num:
  def __get__(self, instance: Any, owner: type) -> Any:
    if instance is None:
      return self
    return getattr(instance, '__test_number__', 0)

  def __set__(self, instance: Any, value: Any) -> None:
    setattr(instance, '__test_number__', value)

class Bar:
  __test_number__ = 420
  num = Num()
  def __init__(self, *args) -> None:
    print('initiating Bar object!')
    for arg in args:
      if isinstance(arg, int):
        self.__test_number__ = arg
        break

  def __setattr__(self, key: str, value: Any) -> None:
    print('Setting %s to %s' % (key, value))
    return object.__setattr__(self, key, value)

  def __str__(self) -> str:
    return 'Bar[num=%d]' % self.num

def main() -> int:
  bar = Bar()
  bar.num = foo()
  print(bar)
  return 0

if __name__ == '__main__':
  sys.exit(main())

The above script receives the following stdout:

  initiating Bar object!
  Finally block!  # The finally block in foo()
  Setting num to 69  #  Public set call
  # The public set call had to wait for the finally block in foo()
  Setting __test_number__ to 69  # Private set call
  Bar[num=69]

In summary, 'ham = eggs()' still waits for the finally block in eggs()
even if it has already returned a value. So the finally block does provide
a place for a 'post' hook, just not post by very much. This leaves the
post hook as more of an academic exercise, as it is quite literally
impossible for anything to have happened in between the return statement
and the 'finally' clause.

#  preGET(instance: Any, value: Any) -> Any:
Next, the value has been retrieved from the normal procedure or is a
cached value. This value is then passed to the fix hooks. These hooks can
further augment the value, or validate it.

#  fixGET(instance: Any, value: Any) -> Any:
Following the fix hooks, the value is returned from '__get__' in a
try/finally with the finally block

#  set
Before invoking the hook, the existing value is retrieved and passed to
the pre hooks along with the new value:
#  preSET(instance: Any, oldValue: Any, newValue: Any) -> None:
After the pre hooks, the new value is set and the post hooks are invoked:
#  postSET(instance: Any, oldValue: Any, newValue: Any) -> None:



Because
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any
