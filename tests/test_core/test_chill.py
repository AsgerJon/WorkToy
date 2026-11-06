"""
TestChill tests '_Chill' from 'worktoy.core._meta_type'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import MetaType
from worktoy.core._meta_type import _Chill
from . import CoreTest


class TestChill(CoreTest):
  """
  A plain class statement with a keyword fails in 'object.__init_subclass__'
  with 'takes no keyword arguments', since nothing along the resolution
  order absorbs the keyword. '_Chill' sits before 'object' in every
  worktoy class and absorbs whatever reaches it. The tests show the plain
  failure first, then the same chain of bases under 'MetaType' passing,
  and pin the marks '_Chill' carries.
  """

  def test_plain_python_refuses_unclaimed_keyword(self) -> None:
    class Base:
      def __init_subclass__(cls, mine=None, **kw) -> None:
        cls.mine = mine
        super().__init_subclass__(**kw)

    class Sub(Base, mine=1):
      pass

    self.assertEqual(Sub.mine, 1)
    with self.assertRaises(TypeError):
      class Spilled(Base, mine=1, other=2):
        pass

  def test_chill_absorbs_the_rest(self) -> None:
    class Base(metaclass=MetaType):
      def __init_subclass__(cls, mine=None, **kw) -> None:
        cls.mine = mine
        super().__init_subclass__(**kw)

    class Sub(Base, mine=1, other=2):
      pass

    self.assertEqual(Sub.mine, 1)
    self.assertIs(Sub.__mro__[-2], _Chill)

  def test_chill_takes_any_keywords(self) -> None:
    class Direct(_Chill, a=1, b='two'):
      pass

    self.assertIsSubclass(Direct, _Chill)
    self.assertFalse(hasattr(Direct, 'a'))

  def test_marks(self) -> None:
    self.assertTrue(_Chill.__skip_hash__)
    self.assertIs(type(_Chill), type)
    self.assertEqual(_Chill.__mro__, (_Chill, object))
