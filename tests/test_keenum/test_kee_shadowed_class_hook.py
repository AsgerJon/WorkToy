"""
TestKeeShadowedClassHook subclasses 'KeeTest' and pins that the class
body of a 'KeeNum' or a 'KeeFlags' refuses a routed '__class_*__' hook
for an operation its metaclass implements itself, with
'ShadowedClassHook' at the line binding it. Such a hook used to be
accepted and never called: a 'Weekday' with a '__class_len__' of five
working days still measured seven, and 'monday' was never in it however
its '__class_contains__' read. A '__class_call__' was worse, since
'KeeMeta' creates the members through the inherited '__call__', which
handed the call to the hook before any member existed, and the class
statement failed with an unrelated 'AttributeError'. The hooks for the
operations the metaclass leaves alone keep working.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee, KeeFlags, KeeFlag, KeeMeta
from worktoy.waitaminute.meta import ShadowedClassHook

from . import KeeTest


class TestKeeShadowedClassHook(KeeTest):
  """
  TestKeeShadowedClassHook provides tests for the class hooks an
  enumeration body refuses, and for those it keeps.
  """

  def test_len_hook_refused(self) -> None:
    """A 'Weekday' counting its working days through '__class_len__' is
    refused, since 'KeeMeta' counts the members itself."""
    with self.assertRaises(ShadowedClassHook) as context:
      class Weekday(KeeNum):
        MONDAY = Kee[str]('Mandag')
        TUESDAY = Kee[str]('Tirsdag')
        WEDNESDAY = Kee[str]('Onsdag')
        THURSDAY = Kee[str]('Torsdag')
        FRIDAY = Kee[str]('Fredag')
        SATURDAY = Kee[str]('Loerdag')
        SUNDAY = Kee[str]('Soendag')

        @classmethod
        def __class_len__(cls) -> int:
          return 5  # pragma: no cover
    e = context.exception
    self.assertEqual(e.className, 'Weekday')
    self.assertEqual(e.hookName, '__class_len__')
    self.assertEqual(e.metaclassName, 'KeeMeta')
    self.assertEqual(e.methodName, '__len__')

  def test_contains_hook_refused(self) -> None:
    """A '__class_contains__' taking a day name in any case is refused,
    since 'KeeMeta' decides membership itself."""
    with self.assertRaises(ShadowedClassHook) as context:
      class Weekday(KeeNum):
        MONDAY = Kee[str]('Mandag')
        TUESDAY = Kee[str]('Tirsdag')

        @classmethod
        def __class_contains__(cls, item: object) -> bool:
          return True  # pragma: no cover
    self.assertEqual(context.exception.methodName, '__contains__')

  def test_str_hook_refused(self) -> None:
    """A '__class_str__' listing the days is refused, since 'KeeMeta'
    renders an enumeration itself."""
    with self.assertRaises(ShadowedClassHook) as context:
      class Weekday(KeeNum):
        MONDAY = Kee[str]('Mandag')

        @classmethod
        def __class_str__(cls) -> str:
          return 'Weekday'  # pragma: no cover
    self.assertEqual(context.exception.methodName, '__str__')

  def test_call_hook_refused(self) -> None:
    """A '__class_call__' giving a default colour is refused at its line,
    where the class statement used to fail with an 'AttributeError' from
    the hook running as the members were created."""
    with self.assertRaises(ShadowedClassHook) as context:
      class Color(KeeNum):
        RED = Kee[int](0xFF0000)
        GREEN = Kee[int](0x00FF00)

        @classmethod
        def __class_call__(cls, *args, **kwargs) -> object:
          return cls.RED  # pragma: no cover
    self.assertEqual(context.exception.methodName, '__call__')

  def test_hash_hook_accepted(self) -> None:
    """'KeeMeta' leaves hashing to 'AbstractMetaclass', so a
    '__class_hash__' is accepted and called."""

    class Num(KeeNum):
      A = Kee[int](1)

      @classmethod
      def __class_hash__(cls) -> int:
        return 69

    self.assertEqual(hash(Num), 69)

  def test_class_init_accepted(self) -> None:
    """A '__class_init__' is accepted and sees the members."""

    class Num(KeeNum):
      A = Kee[int](1)
      B = Kee[int](2)

      @classmethod
      def __class_init__(cls, *args, **kwargs) -> None:
        type.__setattr__(cls, 'seen', len(cls))

    self.assertEqual(Num.seen, 2)

  def test_flags_len_hook_refused(self) -> None:
    """A 'Perm' counting its flags through '__class_len__' is refused,
    since 'KeeFlagsMeta' counts the members itself."""
    with self.assertRaises(ShadowedClassHook) as context:
      class Perm(KeeFlags):
        READ = KeeFlag()
        WRITE = KeeFlag()

        @classmethod
        def __class_len__(cls) -> int:
          return len(cls.flags)  # pragma: no cover
    e = context.exception
    self.assertEqual(e.className, 'Perm')
    self.assertEqual(e.metaclassName, 'KeeFlagsMeta')
    self.assertEqual(e.methodName, '__len__')

  def test_flags_str_hook_accepted(self) -> None:
    """'KeeFlagsMeta' leaves 'str()' to 'AbstractMetaclass', so a
    '__class_str__' listing the flags is accepted and called."""

    class Perm(KeeFlags):
      READ = KeeFlag()
      WRITE = KeeFlag()

      @classmethod
      def __class_str__(cls) -> str:
        return 'Perm flags: ' + ', '.join(f.name for f in cls.flags)

    self.assertEqual(str(Perm), 'Perm flags: READ, WRITE')
    self.assertEqual(len(Perm), 4)

  def test_custom_metaclass_names_kee_meta(self) -> None:
    """An enumeration of a metaclass derived from 'KeeMeta' is refused
    the same hooks, and the exception names 'KeeMeta', which implements
    the operation."""

    class FontMeta(KeeMeta):
      pass

    with self.assertRaises(ShadowedClassHook) as context:
      class Font(FontMeta.keeNum):
        ARIAL = Kee[int](1)

        @classmethod
        def __class_len__(cls) -> int:
          return 0  # pragma: no cover
    self.assertEqual(context.exception.metaclassName, 'KeeMeta')
