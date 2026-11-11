"""
The 'promises.deprecations' package holds the promises that end at the
next major update. A deprecated feature is still promised: it works as
it did through every release of the major version that deprecated it,
and it gives a deprecation notice where it is used. Each file is one
deprecation. Its docstring says what is deprecated, since when and why,
and its tests are the promise still owed, moved here from the package
it belongs to. The tests run with warnings silenced, since they use
what is deprecated on purpose.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations
