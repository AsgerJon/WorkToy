"""
TestDispatcherCloneSigs subclasses 'DispatcherTest' and pins that a clone
of a 'Dispatcher' holds signatures of its own. A clone used to hold the
'TypeSig' objects of the original, and placing a clone on a class
rewrites 'THIS' in its signatures in place, so the first class to receive
a clone fixed 'THIS' for the original and every other clone alike.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import THIS, ARGS
from worktoy.dispatch import Dispatcher, TypeSig, overload

from . import DispatcherTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


def _thisLoad(self: Any, other: Any) -> str:
  return 'this'


def _manyLoad(self: Any, *others) -> int:
  return len(others)


class TestDispatcherCloneSigs(DispatcherTest):
  """
  TestDispatcherCloneSigs provides tests for the signatures of a clone of
  a 'Dispatcher'.
  """

  def test_clones_resolve_own_class(self) -> None:
    """Each clone resolves 'THIS' to the class it is placed on."""
    d = Dispatcher()
    d.addSigFunc(TypeSig(THIS), _thisLoad)

    class Foo:
      x = d.clone()

    class Bar:
      y = d.clone()

    self.assertEqual(Foo().x(Foo()), 'this')
    self.assertEqual(Bar().y(Bar()), 'this')

  def test_original_keeps_this(self) -> None:
    """Placing a clone leaves the signatures of the original as they
    were."""
    d = Dispatcher()
    d.addSigFunc(TypeSig(THIS), _thisLoad)

    class Foo:
      x = d.clone()

    (sig, _), = d._getSigFuncList()
    self.assertEqual(sig.getRawTypes(), (THIS,))

  def test_variadic_clones_resolve_own_class(self) -> None:
    """Each clone resolves 'ARGS[THIS]' to its own class as well."""
    d = Dispatcher()
    d.addVariadicSigFunc(TypeSig(ARGS[THIS]), _manyLoad)

    class Foo:
      x = d.clone()

    class Bar:
      y = d.clone()

    self.assertEqual(Foo().x(Foo(), Foo()), 2)
    self.assertEqual(Bar().y(Bar(), Bar(), Bar()), 3)

  def test_copies_are_their_own(self) -> None:
    """The copied signatures, concrete and variadic, equal the originals
    and are objects of their own."""
    d = Dispatcher()
    d.addSigFunc(TypeSig(int), _thisLoad)
    ov = overload(ARGS[str])(_manyLoad)
    for sig, func in ov.getVariadics():
      d.addVariadicSigFunc(sig, func)
    clone = d.clone()
    originals = [sig for sig, _ in d._getSigFuncList()]
    originals += [sig for sig, _ in d._getVariadicFuncs()]
    copies = [sig for sig, _ in clone._getSigFuncList()]
    copies += [sig for sig, _ in clone._getVariadicFuncs()]
    self.assertEqual(copies, originals)
    self.assertEqual(len(copies), 2)
    for original, copied in zip(originals, copies):
      self.assertIsNot(copied, original)
