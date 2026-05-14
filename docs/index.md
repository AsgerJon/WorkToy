# worktoy

`worktoy` is a Python utilities library that adds runtime type
enforcement, declarative attributes, function overloading, and
custom-metaclass infrastructure on top of stock Python. It targets
Python 3.7 through 3.14.

## Installation

```bash
pip install worktoy
```

## Layout

The library is organized into layered subpackages. Each layer
imports only from earlier ones; the order below is the canonical
dependency chain:

| Subpackage | Purpose |
| --- | --- |
| [utilities](api/utilities.md) | Leaf-level helpers with no internal dependencies. |
| [waitaminute](api/waitaminute.md) | Custom exception hierarchy. |
| [core](api/core.md) | Primitive runtime types and sentinels. |
| [dispatch](api/dispatch.md) | `@overload` decorator and supporting machinery. |
| [desc](api/desc.md) | Descriptor protocol: `Field`, `AttriBox`, `View`. |
| [mcls](api/mcls.md) | Metaclass framework and `BaseObject`. |
| [lorem_ipsum](api/lorem_ipsum.md) | Text generation. |
| [keenum](api/keenum.md) | Enum framework: `KeeNum`, `KeeFlags`. |
| [ezdata](api/ezdata.md) | `EZData` dataclass. |
| [work_io](api/work_io.md) | Filesystem helpers. |
| [work_test](api/work_test.md) | `BaseTest` and contract scaffolding. |

## License

AGPL-3.0. See the
[LICENSE](https://github.com/AsgerJon/WorkToy/blob/main/LICENSE)
file for full text.
