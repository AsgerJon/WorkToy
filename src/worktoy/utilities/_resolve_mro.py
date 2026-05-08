"""C3 linearization preview without constructing a class.

The ``resolveMRO`` function returns the C3 linearization of the
given base classes, in the same order CPython would compute when
constructing a class with those bases. The result is the
linearization of the *bases*, not of the hypothetical class
itself: for ``class Foo(*bases): pass``,
``resolveMRO(*bases) == Foo.mro()[1:]``.

Useful for previewing the MRO from inside metaclass machinery,
where actually constructing ``type('_', bases, {})`` would
re-enter the metaclass and recurse."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import joinWords, textFmt


def resolveMRO(*bases: type, **kwargs) -> list[type]:
  """Return the C3 linearization of ``bases``.

  Implements canonical C3: the merge operates on the
  linearizations ``L[Bi]`` of each base plus an auxiliary
  ``[B1, ..., Bn]`` list that pins the bases' relative order.
  The hypothetical most-derived class is *not* included in the
  result; for ``class Foo(*bases): pass``,
  ``resolveMRO(*bases) == Foo.mro()[1:]``.

  Parameters
  ----------
  *bases : type
      The base classes, in the order they would appear in a
      class statement.
  **kwargs
      _initialIterationCount : int, optional
          Test-only hook. Initial value of the merge-loop
          iteration counter; used by the recursion-guard test to
          force the bailout. Do not pass from production code.

  Returns
  -------
  list of type
      The linearized MRO of the bases. For zero bases, an empty
      list. For one base, that base's own ``__mro__`` as a list
      (which already starts with the base itself).

  Raises
  ------
  TypeError
      If the bases admit no consistent linearization.
  RecursionError
      If the iteration counter exceeds the upper bound. Only
      reachable when ``_initialIterationCount`` is set close to
      or above the total length of the input lists.

  Examples
  --------
  >>> class A: pass
  >>> class B(A): pass
  >>> class C(A): pass
  >>> resolveMRO(B, C)
  [<class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>]
  """
  if not bases:
    return []
  if len(bases) == 1:
    return [*bases[0].__mro__]
  #  Canonical C3 input: linearizations plus the base-order list.
  lists = [list(base.__mro__) for base in bases]
  lists.append([*bases])
  maxC = sum(len(seq) for seq in lists)
  count = kwargs.get('_initialIterationCount', 0)
  out = []
  while any(lists):
    for candidate in lists:
      if not candidate:
        continue
      head = candidate[0]
      bad = False
      for other in lists:
        if other and head in other[1:]:
          bad = True
          break
      if not bad:
        break
    else:
      info = """The bases received: (%s) cannot form a consistent
      mro!""" % joinWords(*[b.__name__ for b in bases])
      raise TypeError(textFmt(info))
    out.append(head)
    for seq in lists:
      if seq and seq[0] is head:
        del seq[0]
    count += 1
    if count > maxC:
      raise RecursionError
  return out
