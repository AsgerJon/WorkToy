# Changelog

This changelog covers stable releases. Development ('-dev') and release
candidate ('-rc') builds are not logged on their own; their changes are
rolled into the release they lead up to.

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
