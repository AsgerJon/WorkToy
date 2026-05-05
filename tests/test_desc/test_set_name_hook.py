"""
TestSetNameHook subclasses 'DescTest' from the 'tests.test_desc' module
and provides tests for the 'setNameHook'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox
from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestSetNameHook(DescTest):
  """
  TestSetNameHook subclasses 'DescTest' from the 'tests.test_desc' module
  and provides tests for the 'setNameHook'.
  """

  def test_callback_fires_once(self) -> None:
    """Callback fires exactly once at class creation"""
    callCount: list[int] = [0]

    class Foo:
      bar = AttriBox[int]()

      @classmethod
      @bar.setName
      def _setNameBar(cls: type) -> None:
        callCount[0] += 1

    self.assertIsInstance(Foo.bar, AttriBox)
    self.assertEqual(callCount[0], 1)

  def test_callback_arguments(self) -> None:
    """Callback receives '(owner, descriptor)' positionally"""
    captured: dict[str, Any] = {}

    class Foo:
      bar = AttriBox[int]()

      @classmethod
      @bar.setName
      def _capture(cls: type, desc: AttriBox) -> None:
        captured['cls'] = cls
        captured['desc'] = desc

    self.assertIsInstance(Foo.bar, AttriBox)
    self.assertIs(captured['cls'], Foo)
    self.assertIs(captured['desc'], Foo.bar)

  def test_descriptor_argument_is_attribox(self) -> None:
    """The 'desc' argument is an instance of AttriBox"""
    captured: dict[str, Any] = {}

    class Foo:
      bar = AttriBox[int]()

      @classmethod
      @bar.setName
      def _capture(cls: type, desc: AttriBox) -> None:
        captured['desc'] = desc

    self.assertIsInstance(Foo.bar, AttriBox)
    self.assertIsInstance(captured['desc'], AttriBox)

  def test_multiple_callbacks_all_fire(self) -> None:
    """Every registered callback fires on class creation"""
    fired: list[str] = []

    class Foo:
      bar = AttriBox[int]()

      @classmethod
      @bar.setName
      def _first(cls: type) -> None:
        fired.append('first')

      @classmethod
      @bar.setName
      def _second(cls: type) -> None:
        fired.append('second')

    self.assertIsInstance(Foo.bar, AttriBox)
    self.assertEqual(fired, ['first', 'second'])

  def test_callbacks_fire_in_registration_order(self) -> None:
    """Callbacks fire in the order their decorators ran"""
    fired: list[str] = []

    class Foo:
      bar = AttriBox[int]()

      @classmethod
      @bar.setName
      def _alpha(cls: type) -> None:
        fired.append('alpha')

      @classmethod
      @bar.setName
      def _beta(cls: type) -> None:
        fired.append('beta')

      @classmethod
      @bar.setName
      def _gamma(cls: type) -> None:
        fired.append('gamma')

    self.assertIsInstance(Foo.bar, AttriBox)
    self.assertEqual(fired, ['alpha', 'beta', 'gamma'])

  def test_field_metadata_set_before_callback(self) -> None:
    """
    The descriptor's '__field_name__' and '__field_owner__' are
    populated before the callback runs
    """
    captured: dict[str, Any] = {}

    class Foo:
      bar = AttriBox[int]()

      @classmethod
      @bar.setName
      def _check(cls: type, desc: AttriBox) -> None:
        captured['fieldName'] = desc.__field_name__
        captured['fieldOwner'] = desc.__field_owner__

    self.assertEqual(captured['fieldName'], 'bar')
    self.assertIs(captured['fieldOwner'], Foo)

  def test_per_descriptor_isolation(self) -> None:
    """Each descriptor's callbacks fire only for its own __set_name__"""
    fired: list[tuple[str, str]] = []

    class Foo:
      one = AttriBox[int]()
      two = AttriBox[str]()

      @classmethod
      @one.setName
      def _onOne(cls: type, desc: AttriBox) -> None:
        fired.append(('one', desc.__field_name__))

      @classmethod
      @two.setName
      def _onTwo(cls: type, desc: AttriBox) -> None:
        fired.append(('two', desc.__field_name__))

    self.assertIsInstance(Foo.one, AttriBox)
    self.assertIsInstance(Foo.two, AttriBox)
    self.assertIn(('one', 'one'), fired)
    self.assertIn(('two', 'two'), fired)
    self.assertEqual(len(fired), 2)

  def test_descriptor_without_callbacks_inert(self) -> None:
    """A descriptor with no callbacks does not affect the others"""
    fired: list[str] = []

    class Foo:
      hot = AttriBox[int]()
      cold = AttriBox[str]()

      @classmethod
      @hot.setName
      def _onHot(cls: type, desc: AttriBox) -> None:
        fired.append(desc.__field_name__)

    self.assertEqual(fired, ['hot'])
    self.assertIsInstance(Foo.cold, AttriBox)

  def test_no_callbacks_no_error(self) -> None:
    """A bare descriptor builds without error"""

    class Foo:
      bar = AttriBox[int]()

    self.assertIsInstance(Foo.bar, AttriBox)

  def test_set_name_does_not_fire_on_subclass(self) -> None:
    """
    Python only fires '__set_name__' at the class where the descriptor
    is first assigned. Subclasses inheriting the descriptor do not
    refire the callbacks.
    """
    fired: list[str] = []

    class Foo:
      bar = AttriBox[int]()

      @classmethod
      @bar.setName
      def _record(cls: type) -> None:
        fired.append(cls.__name__)

    self.assertEqual(fired, ['Foo'])

    class Sub(Foo):
      pass

    self.assertIs(Sub.bar, Foo.bar)
    self.assertIsInstance(Sub.bar, AttriBox)
    self.assertEqual(fired, ['Foo'])

  def test_primary_key_example(self) -> None:
    """The README-style example: marking a primary-key field"""

    class User:
      id = AttriBox[int]()
      email = AttriBox[str]()

      @classmethod
      @id.setName
      def _markPrimary(cls: type, desc: AttriBox) -> None:
        cls.__primary_key__ = desc.__field_name__

    self.assertEqual(User.__primary_key__, 'id')
    self.assertIsInstance(User.email, AttriBox)
