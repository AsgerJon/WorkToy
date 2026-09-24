# Changelog

This changelog covers stable releases. Development ('-dev') and release
candidate ('-rc') builds are not logged on their own; their changes are
rolled into the release they lead up to.

## [1.0.1] - unreleased

### AttriBox declarations are settled when the class is created

Several ways of writing an `AttriBox` declaration used to be accepted in
silence and then misbehave later, or never behave at all. Each is now
settled at the declaration itself, which is where the offending line
actually sits.

A subscript naming something other than a plain type, such as
`AttriBox[list[int]]` or `AttriBox[T]`, is handed to the generic
machinery and comes back as a type alias rather than a box. An alias
carries none of the descriptor protocol, so the attribute quietly
answered with the alias object on every read. Such a declaration now
raises `PhantomBoxError` while the class is being built. The subscript
on its own remains legal, because `class Sub(AttriBox[T])` asks for
exactly that alias and a base-class entry is not a namespace value. What
is refused is the alias landing in a class body as an attribute.

A box that never captured a field type, written `AttriBox()` or produced
by calling one of the aliases above, has nothing to build from and no
later chance to learn a field type, since the subscript is the only
place one is ever assigned. It now raises `MissingVariable` as the class
is created, rather than at the first read of the attribute.

A subscript written without its trailing call, `bar = AttriBox[int]`, is
now completed instead of left half-built. The subscript already fixed
the field type, so the only thing the missing parentheses withheld is
the deferred argument list, and an absent list is read as an empty one.
Such a declaration now behaves exactly as `bar = AttriBox[int]()`.

A box installed on a finished class through `setattr` never reaches
`__set_name__`, so both refusals above are repeated on read for that
route.

#### Rationale

A malformed declaration used to surface as a puzzling value or an
exception raised several frames inside the descriptor machinery, at
whatever unrelated line happened to read the attribute first. The class
body that caused it could be in another file entirely. Refusing at class
creation names the attribute, the owning class and the subscript as
written, and does so before any instance exists.

The three spellings are not treated alike, because only one of them
leaves anything to work with. A missing pair of parentheses withholds an
argument list that has an obvious default, so it is completed. A
subscript the box declines to claim, or no subscript at all, leaves no
field type and therefore nothing to construct, so it is refused.

### New exception: PhantomBoxError

`PhantomBoxError` is added to `worktoy.waitaminute.desc` and raised when
a class-body subscript produced a type alias in place of a box. Its
message reports the attribute name, the owning class, and the subscript
as it was written, along with the completed form the declaration wanted.

It subclasses `DescriptorException` and deliberately does not subclass
`AttributeError`. A declaration error that presented as an
`AttributeError` would be swallowed by `hasattr` and by `getattr` with a
default, turning a broken class body into a silently absent attribute.

`AccessError`, `ProtectedError`, `ReadOnlyError` and `PhantomBoxError`
now share the `DescriptorException` base, so a single
`except DescriptorException` still catches all of them.

### Object reports inconsistent state instead of failing obscurely

`Object` now checks the invariants its accessors depend on and reports
the missing piece by name. `getContextInstance` and `getContextOwner`
refuse an absent context stack, which a subclass can produce by
overriding the public `hasContext` in a way that disagrees with the
stack it summarises. `getPrivateName` reports a missing field name
rather than building an attribute name out of `None`, which is reachable
whenever a descriptor is used without having gone through a class body.
The deleted-value guard likewise reports a missing field name rather
than naming the deleted attribute `None`.

## [1.0.0] - 2026 May 29

First stable release. The public API is frozen for the 1.0 series.

### Relicensed from AGPL-3.0 to Apache-2.0

worktoy is now distributed under the Apache License 2.0, replacing the
AGPL-3.0 license used throughout the pre-1.0 development series.

#### Rationale

AGPL-3.0 was originally chosen for one reason: to stop a large company
from folding worktoy into a closed-source product. The clearest version
of that worry is training data, and AGPL was meant to make such use a
copyleft violation rather than a free lunch.

In practice it changed nothing about that threat. Long-removed, renamed
internals of worktoy (for example the abandoned `monoSpace` feature)
already surface in the pre-knowledge of commercial language models,
which means the source was ingested into training weights regardless of
the license. If copying source into training data and model weights is
not treated as derivation, then the one outcome AGPL was chosen to
prevent is simply not prevented.

So the restrictive license bought nothing against the actor it was aimed
at, while it did deter the honest ones: many organizations refuse AGPL
dependencies outright as a matter of policy. A lock that only stops the
law-abiding and waves the scrapers through is not worth keeping.

Apache-2.0 keeps worktoy freely usable, adds an explicit patent grant,
and has clearer terms than a bare permissive license such as MIT.

#### Scope

The `LICENSE` file now holds the canonical Apache-2.0 text. The per-file
license headers, the `pyproject.toml` classifier, the README badge and
license section, and the Code of Conduct were all updated to match.
Copyright remains with Asger Jon Vistisen; only the license terms
changed.

The relicense first shipped in 1.0.0-rc7. Earlier candidates, up to and
including 1.0.0-rc6, remain available under AGPL-3.0; every release from
1.0.0-rc7 onward is Apache-2.0.
