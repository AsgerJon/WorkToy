"""
TestWrongImplementation tests the refusal of an implementation that
cannot take what the abstract method declares.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import abstract, overload
from worktoy.mcls import BaseObject, ABCMeta
from worktoy.waitaminute import WorkToyException
from worktoy.waitaminute.meta import WrongImplementation
from . import MclsTest

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class TestWrongImplementation(MclsTest):
  """
  A method left unwritten leaves its class abstract, but a method
  written wrongly is refused as its class is created, with
  'WrongImplementation'. An implementation is right when it is the same
  kind of method as the abstract one and can receive everything that
  one declares: its positional parameters are counted, a default never
  entering, '*args' taking any number; an abstract '**kwargs' asks for
  '**kwargs', and an abstract keyword-only parameter for the same one
  or for '**kwargs'. The blank function of an abstract declaration is
  held to the same count against each signature stacked on it. The
  tests pin each rule both ways, and every slot and the message of the
  exception.
  """

  def _assertWrong(self, context: Any, *expected: str) -> None:
    """Asserts the slots and the message of the exception caught."""
    exception = context.exception
    self.assertIsInstance(exception, WrongImplementation)
    self.assertIsInstance(exception, SyntaxError)
    className, name, declared, written = expected
    self.assertEqual(exception.className, className)
    self.assertEqual(exception.name, name)
    self.assertEqual(exception.declared, declared)
    self.assertEqual(exception.written, written)
    message = ("The class body of '%s' writes '%s' wrongly: it is "
               "declared as %s, and written as %s.") % expected
    self.assertEqual(str(exception), message)
    self.assertEqual(repr(exception), message)
    self.assertEqual(exception.msg, message)

  @staticmethod
  def _model() -> type:
    class Model(BaseObject, metaclass=ABCMeta):
      @abstract
      def data(self, index: str, role: int) -> tuple: ...

    return Model

  def test_count(self) -> None:
    Model = self._model()

    class Same(Model):
      def data(self, index: str, role: int) -> tuple:
        return index, role

    class Defaulted(Model):
      def data(self, index: str = 'a', role: int = 0) -> tuple:
        return index, role

    class Starred(Model):
      def data(self, *args) -> tuple:
        return args

    class Lead(Model):
      def data(self, index: str, *args) -> tuple:
        return (index, *args)

    self.assertEqual(Same().data('a', 1), ('a', 1))
    self.assertEqual(Defaulted().data('b', 2), ('b', 2))
    self.assertEqual(Starred().data('a', 1), ('a', 1))
    self.assertEqual(Lead().data('a', 1), ('a', 1))
    with self.assertRaises(WrongImplementation) as context:
      class Fewer(Model):
        def data(self, index: str) -> tuple: ...
    self._assertWrong(
        context, 'Fewer', 'data',
        'a method taking 2 by position',
        'a method taking 1 by position',
    )
    with self.assertRaises(WrongImplementation) as context:
      class More(Model):
        def data(self, index: str, role: int = 0, extra: int = 0): ...
    self._assertWrong(
        context, 'More', 'data',
        'a method taking 2 by position',
        'a method taking 3 by position',
    )
    with self.assertRaises(WrongImplementation) as context:
      class Long(Model):
        def data(self, a: int, b: int, c: int, *args) -> tuple: ...
    self._assertWrong(
        context, 'Long', 'data',
        'a method taking 2 by position',
        'a method taking 3 or more by position',
    )

  def test_starred_declaration(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @abstract
      def rest(self, first: int, *args) -> tuple: ...

    class Same(Model):
      def rest(self, first: int, *args) -> tuple:
        return (first, *args)

    class Open(Model):
      def rest(self, *args) -> tuple:
        return args

    self.assertEqual(Same().rest(1, 2), (1, 2))
    self.assertEqual(Open().rest(1, 2), (1, 2))
    with self.assertRaises(WrongImplementation) as context:
      class Fixed(Model):
        def rest(self, first: int) -> tuple: ...
    self._assertWrong(
        context, 'Fixed', 'rest',
        'a method taking 1 or more by position',
        'a method taking 1 by position',
    )

  def test_keywords(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @abstract
      def send(self, text: str, *, urgent: bool, **options) -> str: ...

      @abstract
      def mark(self, *, flag: bool) -> bool: ...

    class Same(Model):
      def send(self, text: str, *, urgent: bool, **options) -> str:
        return text

      def mark(self, *, flag: bool) -> bool:
        return flag

    class Open(Model):
      def send(self, text: str, **kwargs) -> str:
        return text

      def mark(self, **kwargs) -> bool:
        return kwargs['flag']

    self.assertEqual(Same().send('a', urgent=True), 'a')
    self.assertTrue(Same().mark(flag=True))
    self.assertEqual(Open().send('a', urgent=True), 'a')
    self.assertTrue(Open().mark(flag=True))
    declared = ("a method taking 1 by position, 'urgent' by keyword, "
                "any keyword")
    with self.assertRaises(WrongImplementation) as context:
      class Closed(Model):
        def send(self, text: str, *, urgent: bool) -> str: ...
    self._assertWrong(
        context, 'Closed', 'send', declared,
        "a method taking 1 by position, 'urgent' by keyword",
    )
    with self.assertRaises(WrongImplementation) as context:
      class Deaf(Model):
        def send(self, text: str) -> str: ...
    self._assertWrong(
        context, 'Deaf', 'send', declared,
        'a method taking 1 by position',
    )
    with self.assertRaises(WrongImplementation) as context:
      class Other(Model):
        def mark(self, *, other: bool) -> bool: ...
    self._assertWrong(
        context, 'Other', 'mark',
        "a method taking 0 by position, 'flag' by keyword",
        "a method taking 0 by position, 'other' by keyword",
    )

  def test_kind(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @classmethod
      @abstract
      def make(cls) -> object: ...

      @abstract
      def run(self) -> str: ...

      @staticmethod
      @abstract
      def unit(n: int) -> int: ...

    with self.assertRaises(WrongImplementation) as context:
      class Bound(Model):
        def make(self) -> object: ...
    self._assertWrong(
        context, 'Bound', 'classmethod make',
        'a classmethod taking 0 by position',
        'a method taking 0 by position',
    )
    with self.assertRaises(WrongImplementation) as context:
      class Static(Model):
        @staticmethod
        def run() -> str: ...
    self._assertWrong(
        context, 'Static', 'run',
        'a method taking 0 by position',
        'a staticmethod taking 0 by position',
    )
    with self.assertRaises(WrongImplementation) as context:
      class Classed(Model):
        @classmethod
        def unit(cls, n: int) -> int: ...
    self._assertWrong(
        context, 'Classed', 'staticmethod unit',
        'a staticmethod taking 1 by position',
        'a classmethod taking 1 by position',
    )

  def test_no_function(self) -> None:
    Model = self._model()
    for value in (3, classmethod(3), len):
      with self.subTest(value=value):
        with self.assertRaises(WrongImplementation) as context:
          ABCMeta('Valued', (Model,), {'data': value})
        self._assertWrong(
            context, 'Valued', 'data',
            'a method taking 2 by position',
            'no function',
        )

  def test_plain_function_for_overloads(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @overload(str, int)
      @abstract
      def data(self, index: str, role: int) -> tuple: ...

      @overload(bytes)
      @overload(str)
      @abstract
      def data(self, index: object) -> tuple: ...

    with self.assertRaises(WrongImplementation) as context:
      class One(Model):
        def data(self, raw: bytes) -> tuple: ...
    self._assertWrong(
        context, 'One', 'data(str, int)',
        'a method taking 2 by position',
        'a method taking 1 by position',
    )
    with self.assertRaises(WrongImplementation) as context:
      class Defaulted(Model):
        def data(self, index: str, role: int = 0) -> tuple: ...
    self._assertWrong(
        context, 'Defaulted', 'data(str)',
        'a method taking 1 by position',
        'a method taking 2 by position',
    )
    with self.assertRaises(WrongImplementation) as context:
      class Static(Model):
        @staticmethod
        def data(*args) -> tuple: ...
    self._assertWrong(
        context, 'Static', 'data(str, int)',
        'a method taking 2 by position',
        'a staticmethod taking 0 or more by position',
    )

  def test_overload_for_overloads(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @overload(str, int)
      @abstract
      def data(self, index: str, role: int, **options) -> tuple: ...

      @overload(str, ARGS[int])
      @abstract
      def many(self, s: str, *n: int) -> tuple: ...

      @overload.flex(int, str, float, bytes)
      @abstract
      def wide(self, n: int, s: str, x: float, b: bytes) -> tuple: ...

      @overload.flex(int, str)
      @abstract
      def tag(self, n: int, s: str) -> tuple: ...

    declared = 'a method taking 2 by position, any keyword'
    with self.assertRaises(WrongImplementation) as context:
      class Short(Model):
        @overload(str, int)
        def data(self, index: str, **options) -> tuple: ...
    self._assertWrong(
        context, 'Short', 'data(str, int)', declared,
        'a method taking 1 by position, any keyword',
    )
    with self.assertRaises(WrongImplementation) as context:
      class Deaf(Model):
        @overload(str, int)
        def data(self, index: str, role: int) -> tuple: ...
    self._assertWrong(
        context, 'Deaf', 'data(str, int)', declared,
        'a method taking 2 by position',
    )
    with self.assertRaises(WrongImplementation) as context:
      class Static(Model):
        @staticmethod
        @overload(str, int)
        def data(index: str, role: int, **options) -> tuple: ...
    self._assertWrong(
        context, 'Static', 'data(str, int)', declared,
        'a staticmethod taking 2 by position, any keyword',
    )
    with self.assertRaises(WrongImplementation) as context:
      class Fixed(Model):
        @overload(str, ARGS[int])
        def many(self, s: str) -> tuple: ...
    self._assertWrong(
        context, 'Fixed', 'many(str, ARGS[int])',
        'a method taking 1 or more by position',
        'a method taking 1 by position',
    )
    with self.assertRaises(WrongImplementation) as context:
      class Narrow(Model):
        @overload.flex(bytes, float, str, int)
        def wide(self, b: bytes, x: float, s: str) -> tuple: ...
    self._assertWrong(
        context, 'Narrow', 'wide(int, str, float, bytes) in any order',
        'a method taking 4 by position',
        'a method taking 3 by position',
    )
    with self.assertRaises(WrongImplementation) as context:
      class Tagged(Model):
        @overload.flex(int, str)
        def tag(self, *, n: int, s: str) -> tuple: ...
    self._assertWrong(
        context, 'Tagged', 'tag(int, str)',
        'a method taking 2 by position',
        "a method taking 0 by position, 'n' by keyword, 's' by keyword",
    )

  def test_declaration_is_held_to_its_signature(self) -> None:
    with self.assertRaises(WrongImplementation) as context:
      class Model(BaseObject, metaclass=ABCMeta):
        @overload(str)
        @abstract
        def data(self, index: str, role: int) -> tuple: ...
    self._assertWrong(
        context, 'Model', 'data(str)',
        'a method taking 1 by position',
        'a method taking 2 by position',
    )
    with self.assertRaises(WrongImplementation) as context:
      class Tail(BaseObject, metaclass=ABCMeta):
        @abstract
        @overload(str, ARGS[int])
        def many(self, s: str) -> tuple: ...
    self._assertWrong(
        context, 'Tail', 'many(str, ARGS[int])',
        'a method taking 1 or more by position',
        'a method taking 1 by position',
    )
    with self.assertRaises(WrongImplementation) as context:
      class Wide(BaseObject, metaclass=ABCMeta):
        @abstract
        @overload.flex(int, str, float, bytes)
        def wide(self, n: int) -> tuple: ...
    self._assertWrong(
        context, 'Wide', 'wide(int, str, float, bytes) in any order',
        'a method taking 4 by position',
        'a method taking 1 by position',
    )

  def test_overloads_for_a_plain_declaration(self) -> None:
    Model = self._model()
    with self.assertRaises(WrongImplementation) as context:
      class Short(Model):
        @overload(str)
        def data(self, index: str) -> tuple: ...
    self._assertWrong(
        context, 'Short', 'data',
        'a method taking 2 by position',
        'no overload that takes it',
    )
    with self.assertRaises(WrongImplementation) as context:
      class Static(Model):
        @staticmethod
        @overload(str, int)
        def data(index: str, role: int) -> tuple: ...
    self._assertWrong(
        context, 'Static', 'data',
        'a method taking 2 by position',
        'no overload that takes it',
    )
    #  An abstract overload of the body is no implementation, and the
    #  written one after it is still held. The body also binds 'plain', a
    #  name of its own that changes nothing.
    with self.assertRaises(WrongImplementation) as context:
      class Half(Model):
        plain = 'a name of its own'

        @overload(bytes)
        @abstract
        def data(self, raw: bytes) -> tuple: ...

        @overload(str)
        def data(self, index: str) -> tuple: ...
    self._assertWrong(
        context, 'Half', 'data',
        'a method taking 2 by position',
        'no overload that takes it',
    )

    #  A builtin shows nothing of what it takes, so it implements nothing,
    #  though its signature has the declared count.
    with self.assertRaises(WrongImplementation) as context:
      class Builtin(Model):
        data = overload(str, int)(len)
    self._assertWrong(
        context, 'Builtin', 'data',
        'a method taking 2 by position',
        'no overload that takes it',
    )

  def test_sorts_of_signature_at_one_name(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @overload(str)
      @abstract
      def many(self, s: str) -> tuple: ...

      @overload(str, ARGS[int])
      @abstract
      def many(self, s: str, *n: int) -> tuple: ...

    with self.assertRaises(WrongImplementation) as context:
      class Fixed(Model):
        @overload(str, ARGS[int])
        def many(self, s: str, n: int) -> tuple: ...
    self._assertWrong(
        context, 'Fixed', 'many(str, ARGS[int])',
        'a method taking 1 or more by position',
        'a method taking 2 by position',
    )

  def test_name_built_at_runtime(self) -> None:
    Model = self._model()

    def short(self, index: str) -> tuple: ...

    #  A name put together as the program runs is equal to the name of
    #  the declaration and is another object.
    name = ''.join(('da', 'ta'))
    with self.assertRaises(WrongImplementation) as context:
      ABCMeta('Built', (Model,), {name: short})
    self._assertWrong(
        context, 'Built', 'data',
        'a method taking 2 by position',
        'a method taking 1 by position',
    )

  def test_exception(self) -> None:
    exception = WrongImplementation('B', 'data', 'this', 'that')
    self.assertEqual(
        WrongImplementation.__bases__, (WorkToyException, SyntaxError))
    self.assertEqual(
        WrongImplementation.__slots__,
        ('className', 'name', 'declared', 'written'))
    self.assertEqual(
        str(exception),
        "The class body of 'B' writes 'data' wrongly: it is declared as "
        "this, and written as that.")
