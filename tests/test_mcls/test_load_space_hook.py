"""
TestLoadSpaceHook tests 'LoadSpaceHook' from 'worktoy.mcls.space_hooks'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload, Dispatcher, TypeSig
from worktoy.mcls import BaseObject, BaseSpace, BaseMeta
from worktoy.waitaminute.dispatch import DispatchException
from worktoy.waitaminute.meta import OverloadConflict, ReboundOverload
from worktoy.waitaminute.meta import MixedMethodKind, ClaimedName
from . import MclsTest


class TestLoadSpaceHook(MclsTest):
  """
  'LoadSpaceHook' takes every 'overload' from the class body as it is
  bound, records what it declares on the namespace, and builds one
  dispatcher per overloaded name once the body ends. The tests pin the
  claim, the records of every role, the refusals of a mixed, rebound or
  conflicting binding, a deletion in the body, and the names that get
  no dispatcher.
  """

  def test_overload_claimed_and_dispatched(self) -> None:
    class A(BaseObject):
      @overload(int)
      def f(self, n: int) -> str:
        return 'int'

      @overload(str)
      def f(self, s: str) -> str:
        return 'str'

    space = A.__namespace__
    self.assertFalse(dict.__contains__(space, 'f'))
    self.assertIsInstance(space['f'], overload)
    self.assertIsInstance(A.__dict__['f'], Dispatcher)
    self.assertEqual(A().f(1), 'int')
    self.assertEqual(A().f('s'), 'str')
    sigs = [sig.getRawTypes() for sig, _ in space.getOverloads()['f']]
    self.assertEqual(sigs, [(int,), (str,)])
    self.assertEqual(space.getMethodKinds(), {'f': None})
    self.assertNotIn('f', space.getPlainNames())
    self.assertIn('__module__', space.getPlainNames())

  def test_every_role_recorded(self) -> None:
    class A(BaseObject):
      @overload(int)
      def f(self, n: int) -> str:
        return 'int'

      @overload(ARGS[str])
      def f(self, *words: str) -> str:
        return 'words'

      @overload.flex(int, str, float, list)
      def f(self, n: int, s: str, x: float, l: list) -> str:
        return 'flex'

      @overload.fallback
      def f(self, *args) -> str:
        return 'fallback'

      @overload.finalize
      def f(self, *args) -> None:
        """Runs after every call."""

    space = A.__namespace__
    self.assertEqual(len(space.getOverloads()['f']), 1)
    self.assertEqual(len(space.getVariadics()['f']), 1)
    self.assertEqual(len(space.getFlexes()['f']), 1)
    self.assertIn('f', space.getFallbacks())
    self.assertIn('f', space.getFinalizers())
    self.assertEqual(A().f(1), 'int')
    self.assertEqual(A().f('a', 'b'), 'words')
    self.assertEqual(A().f(1, 's', 1.5, []), 'flex')
    self.assertEqual(A().f(1.5), 'fallback')

  def test_signatures_are_copies(self) -> None:
    def f(self, n: int) -> None:
      """Shared."""

    record = overload(int)(f)

    class A(BaseObject):
      g = record

    class B(BaseObject):
      g = record

    recorded = [sig for sig, _ in record][0]
    kept = A.__namespace__.getOverloads()['g'][0][0]
    self.assertIsNot(kept, recorded)
    self.assertEqual(kept, recorded)
    self.assertIsNot(kept, B.__namespace__.getOverloads()['g'][0][0])

  def test_overloads_then_plain_refused(self) -> None:
    with self.assertRaises(OverloadConflict) as context:
      class A(BaseObject):
        @overload(int)
        def f(self, n: int) -> None:
          """Overloaded first."""

        def f(self) -> None:
          """Then plain."""

    self.assertEqual(context.exception.className, 'A')
    self.assertEqual(context.exception.overloadName, 'f')
    self.assertTrue(context.exception.overloadsFirst)
    self.assertIn('then', str(context.exception))

  def test_plain_then_overloads_refused(self) -> None:
    with self.assertRaises(OverloadConflict) as context:
      class A(BaseObject):
        f = 1

        @overload(int)
        def f(self, n: int) -> None:
          """Overloaded second."""

    self.assertFalse(context.exception.overloadsFirst)
    self.assertIn('plain', str(context.exception))

  def test_rebound_overload_refused(self) -> None:
    with self.assertRaises(ReboundOverload) as context:
      class A(BaseObject):
        @overload(int)
        def __add__(self, n: int) -> None:
          """Bound once."""

        __radd__ = __add__

    exception = context.exception
    self.assertEqual(exception.className, 'A')
    self.assertEqual(exception.firstName, '__add__')
    self.assertEqual(exception.newName, '__radd__')
    self.assertIn("'__radd__'", str(exception))

  def test_mixed_kinds_refused(self) -> None:
    with self.assertRaises(MixedMethodKind) as context:
      class A(BaseObject):
        @classmethod
        @overload(int)
        def f(cls, n: int) -> None:
          """A classmethod."""

        @staticmethod
        @overload(str)
        def f(s: str) -> None:
          """Then a staticmethod."""

    exception = context.exception
    self.assertEqual(exception.className, 'A')
    self.assertEqual(exception.overloadName, 'f')
    self.assertEqual(exception.kinds, (classmethod, staticmethod))
    self.assertIn("'A.f'", str(exception))
    self.assertIn("a 'classmethod' and as a 'staticmethod'", str(exception))
    with self.assertRaises(MixedMethodKind) as context:
      class B(BaseObject):
        @staticmethod
        @overload(int)
        @classmethod
        def f(cls, n: int) -> None:
          """Both kinds in one stack."""

    self.assertEqual(context.exception.kinds, (staticmethod, classmethod))
    self.assertEqual(context.exception.className, 'B')
    self.assertEqual(context.exception.overloadName, 'f')
    self.assertIn("'B.f'", str(context.exception))

  def test_kinds_agree_across_layers(self) -> None:
    class A(BaseObject):
      @classmethod
      @overload(int)
      @classmethod
      def f(cls, n: int) -> str:
        return cls.__name__

      @overload(str)
      @classmethod
      def f(cls, s: str) -> str:
        return s

      @staticmethod
      @overload(float)
      def g(x: float) -> float:
        return x

    self.assertEqual(A.f(1), 'A')
    self.assertEqual(A.f('s'), 's')
    self.assertEqual(A.g(1.5), 1.5)
    self.assertEqual(A.__namespace__.getMethodKinds(),
                     {'f': classmethod, 'g': staticmethod})

  def test_deleted_plain_name_may_be_overloaded(self) -> None:
    class A(BaseObject):
      def f(self) -> None:
        """Bound plainly, then deleted."""

      del f

      @overload(int)
      def f(self, n: int) -> str:
        return 'int'

    self.assertEqual(A().f(1), 'int')
    self.assertNotIn('f', A.__namespace__.getPlainNames())

  def test_deleted_overload_refused(self) -> None:
    with self.assertRaises(ClaimedName) as context:
      class A(BaseObject):
        @overload(int)
        def f(self, n: int) -> None:
          """Claimed."""

        del f

    self.assertEqual(context.exception.className, 'A')
    self.assertEqual(context.exception.keyName, 'f')
    self.assertIn("'f'", str(context.exception))

  def test_plain_definition_overrides_inherited_overloads(self) -> None:
    class A(BaseObject):
      @overload(int)
      def f(self, n: int) -> str:
        return 'int'

      @overload(int)
      def g(self, n: int) -> str:
        return 'g'

    class B(A):
      def f(self, *args) -> str:
        return 'plain'

    class C(B):
      pass

    self.assertNotIsInstance(B.__dict__['f'], Dispatcher)
    self.assertNotIn('f', C.__dict__)
    self.assertIsInstance(B.__dict__['g'], Dispatcher)
    self.assertIsNot(B.__dict__['g'], A.__dict__['g'])
    self.assertEqual(B().g(1), 'g')
    self.assertEqual(A().f(1), 'int')
    self.assertEqual(B().f(1), 'plain')
    self.assertEqual(C().f(1), 'plain')
    self.assertEqual(C().f('s'), 'plain')
    self.assertEqual(C.__namespace__.getOverloadNames(), ['f', 'g'])

  def test_subclass_dispatcher_of_its_own(self) -> None:
    class A(BaseObject):
      @overload(int)
      def f(self, n: int) -> str:
        return 'int'

    class B(A):
      pass

    self.assertIn('f', B.__dict__)
    self.assertIsNot(B.__dict__['f'], A.__dict__['f'])
    self.assertEqual(B().f(1), 'int')
    with self.assertRaises(DispatchException) as context:
      B().f('s')
    self.assertIs(context.exception.dispatch, B.__dict__['f'])
    self.assertEqual(context.exception.posArgs, ('s',))
    self.assertEqual(context.exception.keyArgs, {})
    self.assertIn("'B.f'", str(context.exception))

  def test_lone_role_gets_a_dispatcher(self) -> None:
    class A(BaseObject):
      @overload.fallback
      def only(self, *args) -> tuple:
        return 'fallback', args

      @overload.finalize
      def last(self, *args) -> None:
        """A finalizer with nothing to finalize."""

    self.assertIsInstance(A.__dict__['only'], Dispatcher)
    self.assertIsInstance(A.__dict__['last'], Dispatcher)
    self.assertEqual(A().only(1, 'x'), ('fallback', (1, 'x')))

  def test_by_hand(self) -> None:
    space = BaseSpace(BaseMeta, 'A', ())
    hook = BaseSpace.__dict__['loadSpaceHook'].__get__(space, BaseSpace)

    def f(self, n: int) -> None:
      """Plain."""

    self.assertFalse(hook.setItemPhase('f', f))
    self.assertEqual(space.getPlainNames(), ('f',))
    self.assertFalse(hook.delItemPhase('f', f))
    self.assertEqual(space.getPlainNames(), ())
    self.assertTrue(hook.setItemPhase('f', overload(int)(f)))
    self.assertIsNone(hook._buildDispatcher('absent'))
    built = hook._buildDispatcher('f')
    self.assertIsInstance(built, Dispatcher)
    self.assertEqual(built._getDeclaredSigs(), [TypeSig(int)])
    compiled = hook.postCompilePhase({})
    self.assertIsInstance(compiled['f'], Dispatcher)
    kind = hook._getMethodKind('f', (classmethod,), overload(int)(f))
    self.assertIs(kind, classmethod)
