"""
TestTypeSig tests the TypeSig class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import StaticTest
from worktoy.static import TypeSig
from worktoy.waitaminute.dispatch import HashMismatch
from worktoy.waitaminute.dispatch import FlexMismatch

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Any


class CastMeNot:
  pass


class Castable:
  pass


class TrollCastMe:
  """
  u mad bro?
  """


class Dispatcher:
  """
  Callable class replacing the __init__ methods.
  """

  __field_owner__ = None
  __field_name__ = None
  __current_instance__ = None

  def __get__(self, instance: Any, owner: type) -> Self:
    self.__current_instance__ = instance
    return self

  def __set_name__(self, owner: type, name: str) -> None:
    """
    Set the name and owner of the field.
    """
    self.__field_owner__ = owner
    self.__field_name__ = name

  def __call__(self, *args) -> Any:
    """
    Call method that checks if the argument is an instance of CastMeNot.
    Raises TypeError if it is.
    """
    if self.__field_name__ == '__init__':
      return None
    owner, castMeMaybe = [*args, None][:2]
    if isinstance(castMeMaybe, Castable) or castMeMaybe is None:
      return object.__new__(self.__field_owner__, )
    return castMeMaybe


class HasOverloadDispatcher(Dispatcher):
  __overload_dispatcher__ = True


class HasNoOverloadDispatcher(Dispatcher):
  pass


class Foo:
  __new__ = Dispatcher()
  __init__ = HasNoOverloadDispatcher()


class Bar:
  __new__ = Dispatcher()
  __init__ = HasNoOverloadDispatcher()


class Bad:
  """
  Class that does pretend to be a dispatcher!
  """
  __new__ = Dispatcher()
  __init__ = HasOverloadDispatcher()


class TestTypeSig(StaticTest):
  """
  Unit tests for TypeSig: fast, cast, flex.
  """

  def setUp(self) -> None:
    """
    Creates 'TypeSig' object and argument tuples for testing. Bar pretends
    to be a dispatcher, but Foo does not.
    """
    self.sig = TypeSig(Foo, Bar, Foo, Bar)
    self.badSig = TypeSig(Foo, Bar, Bar, Bad)
    self.fastArgs = (Foo(), Bar(), Foo(), Bar())
    self.castArgs = Castable(), Castable(), Castable(), Castable()
    self.flexArgs = (Bar(), Foo(), Bar(), Foo(),)
    self.flex2 = ((*self.fastArgs,),)
    self.badArgs = (*[TrollCastMe() for _ in self.sig],)

  def test_good_fast(self) -> None:
    """
    Tests that 'TypeSig.fast' works as expected with valid arguments.
    """
    fastArgs = self.sig.fast(*self.fastArgs)
    self.assertEqual(fastArgs, self.fastArgs)

  def test_good_cast(self) -> None:
    """
    Tests that 'TypeSig.cast' works as expected with castable arguments.
    """
    castArgs = self.sig.cast(*self.castArgs, )
    fastArgs = self.sig.fast(*castArgs)
    fasterArgs = self.sig.fast(*fastArgs)
    self.assertEqual(fastArgs, fasterArgs)

  def test_good_flex(self) -> None:
    """
    Tests that 'TypeSig.flex' works as expected with flexible arguments.
    """
    flexArgs = self.sig.flex(*self.flexArgs)
    fastArgs = self.sig.fast(*flexArgs)
    self.assertEqual(fastArgs, flexArgs)

    flexArgs = self.sig.flex(*self.flex2)
    fastArgs = self.sig.fast(*flexArgs)
    self.assertEqual(fastArgs, flexArgs)

  def test_bad_args_fast(self) -> None:
    """
    Tests that 'TypeSig.fast' raises 'HashMismatch' with bad arguments.
    """
    with self.assertRaises(HashMismatch) as context:
      _ = self.sig.fast(*self.badArgs)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.typeSig, self.sig)
    self.assertEqual(e.posArgs, self.badArgs)

  def test_bad_args_cast(self) -> None:
    """
    Tests that 'TypeSig.cast' raises 'CastMismatch' with bad arguments.
    """
    susArgs = self.sig.cast(*self.badArgs)
    with self.assertRaises(HashMismatch) as context:
      _ = self.sig.fast(*susArgs)
    e = context.exception
    self.assertIs(e.typeSig, self.sig)
    self.assertEqual(e.posArgs, susArgs)

  def test_bad_args_flex(self) -> None:
    """
    Tests that 'TypeSig.flex' raises 'FlexMismatch' with bad arguments.
    """
    with self.assertRaises(FlexMismatch) as context:
      susArgs = self.sig.flex(*self.badArgs)
    e = context.exception
    self.assertIs(e.typeSig, self.sig)
    self.assertEqual(e.posArgs, self.badArgs)
    with self.assertRaises(HashMismatch) as context:
      _ = self.sig.fast([])
    e = context.exception
    self.assertIn('hashable', str(e))
  #
  # def test_bad_sig_fast(self) -> None:
  #   """
  #   Tests that 'TypeSig.fast' raises 'HashMismatch' with a bad signature.
  #   """
  #   with self.assertRaises(HashMismatch) as context:
  #     _ = self.badSig.fast(*self.fastArgs)
  #   e = context.exception
  #   self.assertIs(e.typeSig, self.badSig)
  #   self.assertEqual(e.posArgs, self.fastArgs)
  #
  # def test_bad_sig_cast(self) -> None:
  #   """
  #   Tests that 'TypeSig.cast' raises 'CastMismatch' with a bad signature.
  #   """
  #   with self.assertRaises(CastMismatch) as context:
  #     _ = self.badSig.cast(*self.castArgs)
  #   e = context.exception
  #   self.assertIs(e.typeSig, self.badSig)
  #   self.assertEqual(e.posArgs, self.castArgs)
  #
  # def test_bad_sig_flex(self) -> None:
  #   """
  #   Tests that 'TypeSig.flex' raises 'FlexMismatch' with a bad signature.
  #   """
  #   with self.assertRaises(FlexMismatch) as context:
  #     _ = self.badSig.flex(*self.flexArgs)
  #   e = context.exception
  #   self.assertIs(e.typeSig, self.badSig)
  #   self.assertEqual(e.posArgs, self.flexArgs)
  #
  # def test_bad_sig_bad_args_flex(self) -> None:
  #   """
  #   Tests that 'TypeSig.flex' raises 'FlexMismatch' with a bad signature
  #   and
  #   bad arguments.
  #   """
  #   sig = TypeSig(Foo, Bad)
  #   args = ('breh', 69, Foo(), TrollCastMe(), (Castable(), Castable()))
  #   with self.assertRaises(FlexMismatch) as context:
  #     _ = sig.flex(*args)
  #   e = context.exception
  #   self.assertIs(e.typeSig, sig)
  #   self.assertEqual(e.posArgs, unpack(args))
  #   ezArgs = (*[TrollCastMe() if i % 2 else CastMeNot() for i in range(
  #   69)],)
  #   ezSig = TypeSig(Foo, Bar, Bad, Bad, Bad, Bad)
  #   with self.assertRaises(FlexMismatch) as context:
  #     _ = ezSig.flex(*ezArgs)
  #   e = context.exception
  #   self.assertIs(e.typeSig, ezSig)
  #   for arg in e.posArgs:
  #     self.assertIn(arg, ezArgs)
  #
  # def test_not_enough_args_flex(self) -> None:
  #   """
  #   Tests that 'TypeSig.flex' raises 'FlexMismatch' with not enough
  #   arguments.
  #   """
  #   sig = TypeSig(Foo, Bar, Foo, Bar)
  #   args = (Foo(), Bar(), Foo())
  #   with self.assertRaises(FlexMismatch) as context:
  #     _ = sig.flex(*args)
  #   e = context.exception
  #   self.assertIs(e.typeSig, sig)
  #   self.assertEqual(e.posArgs, args)
  #
  # def test_args_missing_for_type_flex(self) -> None:
  #   """
  #   Tests that 'TypeSig.flex' raises 'FlexMismatch' one of the types
  #   cannot find a candidate argument.
  #   """
  #   sig = TypeSig(Foo, Bar, Foo, Bar)
  #   args = [Foo() for _ in sig]
  #   with self.assertRaises(FlexMismatch) as context:
  #     _ = sig.flex(*args)
  #   e = context.exception
  #   self.assertIs(e.typeSig, sig)
  #   for arg in e.posArgs:
  #     self.assertIn(arg, [*args, ])
  #
  # def test_no_args_flex(self) -> None:
  #   """
  #   Tests that 'TypeSig.flex' raises 'FlexMismatch' with no arguments.
  #   """
  #   with self.assertRaises(FlexMismatch) as context:
  #     _ = self.sig.flex()
  #   e = context.exception
  #   self.assertIs(e.typeSig, self.sig)
  #   self.assertFalse(e.posArgs)
  #
  # def test_empty_sig_flex(self) -> None:
  #   """
  #   Tests that 'TypeSig.flex' works with an empty signature.
  #   """
  #   sig = TypeSig()
  #   args = ()
  #   flexArgs = sig.flex(*args)
  #   self.assertFalse(flexArgs, )
  #
  #   with self.assertRaises(FlexMismatch) as context:
  #     _ = sig.flex(69, 420)
  #   e = context.exception
  #   self.assertIs(e.typeSig, sig)
  #   self.assertEqual(e.posArgs, (69, 420))
  #
  # def test_iterable_args_flex(self) -> None:
  #   """
  #   Tests that 'TypeSig.flex' works with iterable arguments.
  #   """
  #   sig = TypeSig(float, float)
  #   args = ((69., 420.),)
  #   flexArgs = sig.flex(*args)
  #   fastArgs = sig.fast(*flexArgs)
  #   self.assertEqual(fastArgs, unpack(args))
  #
  # def test_normal_cast(self) -> None:
  #   """
  #   Tests that 'TypeSig.cast' works with normal casting.
  #   """
  #   sig = TypeSig(float, float)
  #   args = (69, 420)
  #   castArgs = sig.cast(*args)
  #   fastArgs = sig.fast(*castArgs)
  #   for arg, fastArg in zip(args, fastArgs):
  #     self.assertEqual(arg, fastArg)
  #
  # def test_bad_cast(self, ) -> None:
  #   """
  #   Tests that 'TypeSig.cast' raises 'CastMismatch' with bad casting.
  #   """
  #   sig = TypeSig(float, float)
  #   args = (69, 'four-twenty')  # '420' is not a float
  #   with self.assertRaises(CastMismatch) as context:
  #     _ = sig.cast(*args)
  #   e = context.exception
  #   self.assertIs(e.typeSig, sig)
  #   self.assertEqual(e.posArgs, args)
  #
  # def test_iterable_sig(self) -> None:
  #   """
  #   Tests that 'TypeSig' can be created from an iterable of types.
  #   """
  #   sig = TypeSig(tuple, list)
  #   args = ((69, 420), [1337, 80085])
  #   fastArgs = sig.fast(*args)
  #   self.assertEqual(fastArgs, args)
  #
  #   nearArgs = ([69, 420], (1337, 80085))
  #   castArgs = sig.cast(*nearArgs)
  #   fastArgs = sig.fast(*castArgs)
  #   self.assertEqual(fastArgs, castArgs)
  #
  #   flexArgs = sig.flex(nearArgs)
  #   fastArgs = sig.fast(*flexArgs)
  #   self.assertEqual(fastArgs, flexArgs)
  #
  # def test_too_few_args_sig(self) -> None:
  #   """
  #   Tests that 'TypeSig' raises 'FlexMismatch' with too few arguments.
  #   """
  #   sig = TypeSig(float, float, float, float)
  #   args = 0.1337, 0.80085, 0.69
  #   with self.assertRaises(FlexMismatch) as context:
  #     _ = sig.flex(*args)
  #   e = context.exception
  #   self.assertIs(e.typeSig, sig)
  #   self.assertEqual(e.posArgs, args)
  #
  # def test_str_iterable_sig_cast(self) -> None:
  #   """
  #   Tests that 'TypeSig' does not change a 'str' object into an array of
  #   characters.
  #   """
  #   sig = TypeSig(tuple)
  #   args = """you better not turn me into an array of characters!""",
  #   with self.assertRaises(CastMismatch) as context:
  #     _ = sig.cast(*args)
  #   e = context.exception
  #   self.assertIs(e.typeSig, sig)
  #   self.assertEqual(e.posArgs, args)
  #
  #   with self.assertRaises(FlexMismatch) as context:
  #     _ = sig.flex(*args)
  #   e = context.exception
  #   self.assertIs(e.typeSig, sig)
  #   self.assertEqual(e.posArgs, args)
