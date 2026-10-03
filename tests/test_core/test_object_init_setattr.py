"""
TestObjectInitSetattr subclasses 'CoreTest' from the 'tests.test_core'
package and pins that 'Object.__init__' keeps its bookkeeping to itself
when a subclass defines a '__setattr__' refusing private names. It used to
store the constructor arguments and the context stack by plain
assignment, which runs the subclass's '__setattr__', so such a class
could not be constructed at all. The bookkeeping is now stored through
'object.__setattr__', as '__set_name__' and the context stack already
were.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import BaseObject

from . import CoreTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Guarded(BaseObject):
  """Guarded is a class whose '__setattr__' refuses every private name,
  constructed through the inherited 'Object.__init__'."""

  def __setattr__(self, key: str, value: Any) -> None:
    if key.startswith('_'):
      raise AttributeError('private name: %s' % key)
    object.__setattr__(self, key, value)


class TestObjectInitSetattr(CoreTest):
  """
  TestObjectInitSetattr provides tests for 'Object.__init__' on a class
  whose '__setattr__' refuses every private name.
  """

  def test_construction(self) -> None:
    """The class constructs and keeps its arguments."""
    guarded = Guarded(1, 2, key='value')
    self.assertEqual(guarded.getPosArgs(), (1, 2))
    self.assertEqual(guarded.getKeyArgs(), {'key': 'value'})

  def test_context_stack(self) -> None:
    """The context stack starts out empty."""
    self.assertFalse(Guarded().hasContext())

  def test_setattr_still_applies(self) -> None:
    """The class's own '__setattr__' still decides later assignments."""
    guarded = Guarded()
    guarded.public = 1
    self.assertEqual(guarded.public, 1)
    with self.assertRaises(AttributeError):
      guarded._private = 1
