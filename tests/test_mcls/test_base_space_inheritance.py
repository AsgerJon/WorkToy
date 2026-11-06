"""
TestBaseSpaceInheritance tests how a 'BaseSpace' from 'worktoy.mcls'
gathers the declarations a class inherits.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.core._meta_type import _Chill
from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload, TypeSig
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException
from . import MclsTest, Figure, Labelled, Fixed, Badge, Tag


class TestBaseSpaceInheritance(MclsTest):
  """
  A class inherits the overloads of a name as Python's lookup would
  hand it the methods: a plain definition, or a declaration of another
  kind of method, hides what lies behind it on its own branch. The tests
  pin the diamond of the folder from both sides, each helper on the
  namespace of 'Badge', the gathering of every role with its distance,
  and the hiding by kind.
  """

  def test_diamond_overloading_branch_first(self) -> None:
    self.assertEqual(Badge().scale(2), ('figure-int', 2))
    self.assertEqual(Badge().scale('s'), ('labelled-str', 's'))
    self.assertEqual(Labelled().scale(2), ('figure-int', 2))
    with self.assertRaises(DispatchException) as context:
      Badge().scale(1.5)
    self.assertIs(context.exception.dispatch, Badge.__dict__['scale'])
    self.assertEqual(context.exception.posArgs, (1.5,))
    self.assertEqual(context.exception.keyArgs, {})
    self.assertIn("'Badge.scale'", str(context.exception))
    self.assertEqual(Badge.__dict__['scale']._getSigDistances(), [1, 2])

  def test_diamond_plain_branch_first(self) -> None:
    self.assertNotIn('scale', Tag.__dict__)
    self.assertEqual(Tag().scale(2), ('fixed', (2,)))
    self.assertEqual(Tag().scale('s'), ('fixed', ('s',)))
    self.assertEqual(Fixed().scale(2), ('fixed', (2,)))
    self.assertEqual(Tag.__namespace__.getOverloadNames(), ['scale'])
    self.assertEqual(Tag.__namespace__._getInheritedSpaces('scale'), [])

  def test_defines_plainly(self) -> None:
    space = Badge.__namespace__
    self.assertTrue(space._definesPlainly(Fixed, 'scale'))
    self.assertFalse(space._definesPlainly(Labelled, 'scale'))
    self.assertFalse(space._definesPlainly(Figure, 'other'))

  def test_own_space(self) -> None:
    space = Badge.__namespace__
    self.assertIs(space._getOwnSpace(Figure), Figure.__namespace__)
    self.assertIsNone(space._getOwnSpace(object))
    self.assertIsNone(space._getOwnSpace(_Chill))
    self.assertIsNone(space._getOwnSpace(Object))
    self.assertIn('__namespace__', Object.__dict__)

  def test_hides_inherited(self) -> None:
    space = Badge.__namespace__
    self.assertTrue(space._hidesInherited(Fixed, 'scale', ()))
    self.assertFalse(space._hidesInherited(object, 'scale', ()))
    self.assertFalse(space._hidesInherited(Figure, 'scale', ()))
    self.assertFalse(space._hidesInherited(Figure, 'scale', (None,)))
    self.assertTrue(space._hidesInherited(Figure, 'scale', (classmethod,)))
    self.assertFalse(space._hidesInherited(BaseObject, 'scale',
                                           (classmethod,)))

  def test_reached_along(self) -> None:
    space = Badge.__namespace__
    self.assertTrue(space._isReachedAlong([Labelled, Figure], Figure,
                                          'scale', ()))
    self.assertFalse(space._isReachedAlong([Fixed, Figure], Figure,
                                           'scale', ()))
    self.assertFalse(space._isReachedAlong([Labelled], Figure, 'scale', ()))

  def test_inherited_and_lookup_spaces(self) -> None:
    space = Badge.__namespace__
    inherited = space._getInheritedSpaces('scale')
    self.assertEqual(inherited, [
      Labelled.__namespace__, Figure.__namespace__, BaseObject.__namespace__,
    ])
    lookup = space._getLookupSpaces()
    self.assertEqual(lookup, [
      Labelled.__namespace__, Fixed.__namespace__, Figure.__namespace__,
      BaseObject.__namespace__,
    ])
    self.assertEqual(space.getOverloadNames(), ['scale'])

  def test_plain_mixin_ahead_hides_nothing(self) -> None:
    class Mixin:
      tag = 'mixin'

    class Both(Mixin, Figure):
      @overload(str)
      def scale(self, s: str) -> tuple:
        return 'both-str', s

    self.assertIn('scale', Both.__dict__)
    self.assertEqual(Both().scale(2), ('figure-int', 2))
    self.assertEqual(Both().scale('s'), ('both-str', 's'))
    self.assertEqual(Both.__namespace__._getInheritedSpaces('scale'),
                     [Figure.__namespace__, BaseObject.__namespace__])

  def test_hidden_branch_leaves_shared_ancestor_reachable(self) -> None:
    class Z(BaseObject):
      @overload(int)
      def f(self, n: int) -> str:
        return 'z-int'

    class G(Z):
      @overload(str)
      def f(self, s: str) -> str:
        return 'g-str'

    class U(Z):
      @overload(float)
      def f(self, x: float) -> str:
        return 'u-float'

    class Hd(U):
      def f(self, *args) -> None:
        """Hides 'U' on its own branch."""

    class D(G, Hd):
      pass

    order = [cls.__name__ for cls in D.__mro__[1:5]]
    self.assertEqual(order, ['G', 'Hd', 'U', 'Z'])
    self.assertEqual(D().f('s'), 'g-str')
    self.assertEqual(D().f(1), 'z-int')
    with self.assertRaises(DispatchException) as context:
      D().f(1.5)
    self.assertIs(context.exception.dispatch, D.__dict__['f'])
    self.assertEqual(context.exception.posArgs, (1.5,))
    self.assertIn("'D.f'", str(context.exception))
    self.assertEqual(U().f(1.5), 'u-float')
    self.assertEqual(D.__namespace__._getInheritedSpaces('f'), [
      G.__namespace__, Z.__namespace__, BaseObject.__namespace__,
    ])

  def test_collect_overloads(self) -> None:
    collected = Badge.__namespace__.collectOverloads('scale')
    self.assertEqual([(sig, d) for sig, _, d in collected],
                     [(TypeSig(str), 1), (TypeSig(int), 2)])
    declared = Labelled.__namespace__.getOverloads()['scale']
    self.assertIs(collected[0][1], declared[0][1])

  def test_nearer_class_keeps_equal_signature(self) -> None:
    class Big(Figure):
      @overload(int)
      def scale(self, n: int) -> tuple:
        return 'big-int', n

    collected = Big.__namespace__.collectOverloads('scale')
    self.assertEqual([(sig, d) for sig, _, d in collected],
                     [(TypeSig(int), 0)])
    self.assertEqual(Big().scale(2), ('big-int', 2))

  def test_collect_variadics(self) -> None:
    class A(BaseObject):
      @overload(ARGS[int])
      def f(self, *n: int) -> str:
        return 'a-ints'

    class B(A):
      @overload(ARGS[int])
      def f(self, *n: int) -> str:
        return 'b-ints'

      @overload(ARGS[str])
      def f(self, *s: str) -> str:
        return 'b-strs'

    collected = B.__namespace__.collectVariadics('f')
    self.assertEqual([d for _, __, d in collected], [0, 0])
    self.assertEqual(B().f(1, 2), 'b-ints')
    self.assertEqual(B().f('x'), 'b-strs')
    self.assertEqual(A().f(1), 'a-ints')

  def test_collect_flexes(self) -> None:
    class A(BaseObject):
      @overload.flex(int, str, float, list)
      def f(self, n: int, s: str, x: float, l: list) -> str:
        return 'a'

      @overload.flex(int, int, int, int)
      def f(self, a: int, b: int, c: int, d: int) -> str:
        return 'a-ints'

    class B(A):
      @overload.flex(list, float, str, int)
      def f(self, l: list, x: float, s: str, n: int) -> str:
        return 'b'

    class C(A):
      @overload.flex(int, str, float, list, dict)
      def f(self, n: int, s: str, x: float, l: list, d: dict) -> str:
        return 'c'

    class W(BaseObject):
      @overload.flex(int, str, float, list, dict)
      def f(self, n: int, s: str, x: float, l: list, d: dict) -> str:
        return 'w'

    class N(W):
      @overload.flex(int, str, float, list)
      def f(self, n: int, s: str, x: float, l: list) -> str:
        return 'n'

    collected = B.__namespace__.collectFlexes('f')
    self.assertEqual([d for _, __, d in collected], [0, 1])
    self.assertEqual(A().f(1, 's', 1.5, []), 'a')
    self.assertEqual(B().f(1, 's', 1.5, []), 'b')
    self.assertEqual(B().f(1, 2, 3, 4), 'a-ints')
    collected = C.__namespace__.collectFlexes('f')
    self.assertEqual([d for _, __, d in collected], [0, 1, 1])
    self.assertEqual(C().f(1, 's', 1.5, [], {}), 'c')
    self.assertEqual(C().f(1, 's', 1.5, []), 'a')
    collected = N.__namespace__.collectFlexes('f')
    self.assertEqual([d for _, __, d in collected], [0, 1])
    self.assertEqual(N().f(1, 's', 1.5, []), 'n')
    self.assertEqual(N().f(1, 's', 1.5, [], {}), 'w')

  def test_collect_fallback_and_finalizer(self) -> None:
    log = []

    class A(BaseObject):
      @overload(int)
      def f(self, n: int) -> str:
        return 'int'

      @overload.fallback
      def f(self, *args) -> str:
        return 'a-fallback'

      @overload.finalize
      def f(self, *args) -> None:
        log.append(args)

    class B(A):
      @overload(str)
      def f(self, s: str) -> str:
        return 'str'

    class C(B):
      @overload.fallback
      def f(self, *args) -> str:
        return 'c-fallback'

    self.assertIs(B.__namespace__.collectFallback('f'),
                  A.__namespace__.getFallbacks()['f'])
    self.assertIs(C.__namespace__.collectFallback('f'),
                  C.__namespace__.getFallbacks()['f'])
    self.assertIs(C.__namespace__.collectFinalizer('f'),
                  A.__namespace__.getFinalizers()['f'])
    self.assertIsNone(C.__namespace__.collectFinalizer('absent'))
    self.assertEqual(A().f(1), 'int')
    self.assertEqual(B().f(1.5), 'a-fallback')
    self.assertEqual(C().f(1.5), 'c-fallback')
    self.assertEqual(C().f('s'), 'str')
    self.assertEqual(log, [(1,), (1.5,), (1.5,), ('s',)])

  def test_collect_method_kind(self) -> None:
    class A(BaseObject):
      @overload(int)
      def f(self, n: int) -> str:
        return 'instance'

    class B(A):
      @classmethod
      @overload(str)
      def f(cls, s: str) -> str:
        return 'class'

    class C(B):
      pass

    self.assertIsNone(A.__namespace__.collectMethodKind('f'))
    self.assertIs(B.__namespace__.collectMethodKind('f'), classmethod)
    self.assertIs(C.__namespace__.collectMethodKind('f'), classmethod)
    self.assertIsNone(C.__namespace__.collectMethodKind('absent'))
    self.assertEqual(B.__namespace__._getInheritedSpaces('f'), [])
    self.assertEqual(C.__namespace__._getInheritedSpaces('f'),
                     [B.__namespace__])
    self.assertEqual(A().f(1), 'instance')
    self.assertEqual(B.f('s'), 'class')
    self.assertEqual(C.f('s'), 'class')
    with self.assertRaises(DispatchException) as context:
      C.f(1)
    self.assertIs(context.exception.dispatch, C.__dict__['f'])
    self.assertEqual(context.exception.posArgs, (1,))
    self.assertIn("'C.f'", str(context.exception))

  def test_random_distances(self) -> None:
    self.randomInteger.size = 4
    depth = max(self.randomInteger.row) % 5 + 2
    classes = [Figure]
    for level in range(depth):
      class Level(classes[-1]):
        @overload(float)
        def scale(self, x: float) -> int:
          return level

      classes.append(Level)
    distances = classes[-1].__dict__['scale']._getSigDistances()
    self.assertEqual(distances, [0, depth])
    self.assertEqual(classes[-1]().scale(1.5), depth - 1)
