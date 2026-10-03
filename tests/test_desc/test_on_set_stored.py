"""
TestOnSetStored subclasses 'DescTest' and pins which value each
notification of an assignment receives: a 'preSet' callback the value as
assigned, an 'onSet' callback the value as stored. A box that casts or
builds the value used to hand 'onSet' the value as assigned all the same,
so a callback on an 'AttriBox[float]' saw '2' while the field held '2.0'.
'__instance_set__' reports the value it stored, and a descriptor whose
'__instance_set__' reports nothing hands 'onSet' the value as assigned.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox, Field, FixBox, BaseDescriptor
from worktoy.keenum import KeeNum, Kee, KeeBox
from worktoy.mcls import BaseObject

from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Num(KeeNum):
  """Num is the field type of the 'KeeBox' below."""

  A = Kee[int](1)
  B = Kee[int](2)


class Plain(BaseDescriptor):
  """Plain is a descriptor whose '__instance_set__' reports nothing."""

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> None:
    instance.__dict__['_plain'] = value


class Watched(BaseObject):
  """Watched records what each notification receives."""

  x = AttriBox[float](0.0)
  z = AttriBox[complex](0j)
  fixed = FixBox[float]()
  num = KeeBox[Num]('A')
  field = Field()
  plain = Plain()

  def __init__(self, *args, **kwargs) -> None:
    self.log = []

  @x.preSet
  def _preSetX(self, value: Any) -> None:
    self.log.append(('pre', value))

  @x.onSet
  def _onSetX(self, value: Any) -> None:
    self.log.append(('on', value))

  @z.onSet
  @fixed.onSet
  @num.onSet
  @field.onSet
  @plain.onSet
  def _onSetOther(self, value: Any) -> None:
    self.log.append(('on', value))

  @field.SET
  def _setField(self, value: Any) -> None:
    self.__dict__['_field'] = value * 2


class TestOnSetStored(DescTest):
  """
  TestOnSetStored provides tests for the value 'preSet' and 'onSet'
  callbacks receive.
  """

  def test_cast_value(self) -> None:
    """'preSet' receives the assigned 'int', 'onSet' the stored
    'float'."""
    watched = Watched()
    watched.x = 2
    (preTag, pre), (onTag, on) = watched.log
    self.assertEqual((preTag, onTag), ('pre', 'on'))
    self.assertIs(type(pre), int)
    self.assertIs(type(on), float)
    self.assertEqual(on, 2.0)

  def test_built_value(self) -> None:
    """'onSet' receives the value the field type built from an assigned
    tuple."""
    watched = Watched()
    watched.z = 1, 2
    self.assertEqual(watched.log, [('on', 1 + 2j)])

  def test_value_of_field_type(self) -> None:
    """A value already of the field type reaches 'onSet' itself."""
    watched = Watched()
    value = 3.5
    watched.x = value
    self.assertIs(watched.log[-1][1], value)

  def test_fix_box(self) -> None:
    """The 'onSet' of a 'FixBox' receives the stored value."""
    watched = Watched()
    watched.fixed = 3
    self.assertEqual(watched.log, [('on', 3.0)])
    self.assertIs(type(watched.log[0][1]), float)

  def test_kee_box(self) -> None:
    """The 'onSet' of a 'KeeBox' receives the member."""
    watched = Watched()
    watched.num = 'b'
    self.assertEqual(watched.log, [('on', Num.B)])

  def test_field(self) -> None:
    """The 'onSet' of a 'Field' receives the value its setters received,
    since a 'Field' stores nothing itself."""
    watched = Watched()
    watched.field = 4
    self.assertEqual(watched.log, [('on', 4)])

  def test_reporting_nothing(self) -> None:
    """A descriptor whose '__instance_set__' reports nothing hands
    'onSet' the assigned value."""
    watched = Watched()
    watched.plain = 'value'
    self.assertEqual(watched.log, [('on', 'value')])
