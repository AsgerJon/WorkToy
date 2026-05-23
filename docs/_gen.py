"""Generate the source documentation pages, driven by __all__, with
deterministic line-level cross-references for both library usage and
test usage.

NAVIGATION
----------
Top level of the sidebar: the library packages (built from each
package's __all__), then a 'tests' tree at the bottom mirroring the
tests/ directory. Every leaf shows a whole file, highlighted.

SOURCE RENDERING (Pygments, with line spans)
--------------------------------------------
Each file is highlighted by Pygments into an HTML fragment in which
every line is wrapped in <span id="line-N">. That span is both the
jump target for '#line-N' links and the element a ':target' CSS rule
highlights. The fragment is embedded with '.. raw:: html :file:'.
Nothing is imported; files are read as text.

CROSS-REFERENCES
----------------
For each documented symbol, two sections are appended to its page:

  "Used in"          - where the symbol is used inside src/worktoy.
  "Usage in testing" - where it is used inside tests/.

Both are computed the same deterministic way: an import binds a local
name to a symbol for a whole file, so we resolve every import to its
absolute module, look up (module, name) in a registry of documented
symbols, then list the lines where that bound name actually appears
(the use sites), each linking to that file's page at '#line-N'.

Sphinx only renders the result. generate() is wired to
'builder-inited' in conf.py.
"""
from __future__ import annotations

import ast
import os
import shutil
from pathlib import Path

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

HERE = Path(__file__).parent
REPO_ROOT = HERE.parent
SRC_ROOT = REPO_ROOT / "src"
PKG = SRC_ROOT / "worktoy"
TESTS_ROOT = REPO_ROOT / "tests"
OUT = HERE / "_source"

#  (absolute module dotted, name) -> page stub documenting the symbol.
SYMBOL_PAGE = {}

#  Source/test file (posix path relative to repo root) -> page stub.
FILE_PAGE = {}

_LEXER = PythonLexer()
_FORMATTER = HtmlFormatter(
  cssclass="highlight",
  linenos="inline",
  #  'linespans' wraps each line's content in <span id="line-N">,
  #  the jump target AND the ':target'-styleable element.
  linespans="line",
)


# ============================================================
# Path / rST helpers
# ============================================================

def _title(text: str) -> str:
  """An rST title: text underlined with '=' of equal length."""
  return "%s\n%s" % (text, "=" * len(text))


def _relpath(pyfile: Path) -> str:
  """Repo-relative posix path, e.g. 'src/worktoy/desc/_attri_box.py'
  or 'tests/test_keenum/test_hashing.py'."""
  return pyfile.relative_to(REPO_ROOT).as_posix()


def _src_dotted(path: Path) -> str:
  """Dotted name relative to src/, e.g. 'worktoy.desc._attri_box'.
  Used for symbol/module keys and source stub names."""
  rel = path.relative_to(SRC_ROOT)
  if path.suffix == ".py":
    rel = rel.with_suffix("")
  return ".".join(rel.parts)


def _repo_dotted(path: Path) -> str:
  """Dotted name relative to the repo, e.g. 'tests.test_keenum'.
  Used for test stub names (kept distinct from source stubs)."""
  rel = path.relative_to(REPO_ROOT)
  if path.suffix == ".py":
    rel = rel.with_suffix("")
  return ".".join(rel.parts)


def _render_source(pyfile: Path, stub: str) -> str:
  """Write a highlighted HTML fragment (each line in a
  <span id='line-N'>) and return the rST that embeds it via
  ':file:' so the <pre> content is not re-indented by rST."""
  source = pyfile.read_text(encoding="utf-8")
  (OUT / ("%s.frag.html" % stub)).write_text(
    highlight(source, _LEXER, _FORMATTER), encoding="utf-8")
  return "\n".join([
    "*%s*" % _relpath(pyfile),
    "",
    ".. raw:: html",
    "   :file: %s.frag.html" % stub,
  ])


def _write(stub: str, body: str) -> None:
  """Write one stub file, named '<stub>.rst', into OUT."""
  (OUT / ("%s.rst" % stub)).write_text(body + "\n", encoding="utf-8")


def _record_file_page(pyfile: Path, stub: str) -> None:
  """Remember which page shows a given file (first wins)."""
  FILE_PAGE.setdefault(_relpath(pyfile), stub)


# ============================================================
# Parsing
# ============================================================

def _top_level_defs(pyfile: Path) -> set:
  """Names of classes and functions defined at the top level."""
  tree = ast.parse(pyfile.read_text(encoding="utf-8"))
  names = set()
  for node in tree.body:
    if isinstance(node, (ast.ClassDef, ast.FunctionDef,
                         ast.AsyncFunctionDef)):
      names.add(node.name)
  return names


def _parse_init(init_path: Path):
  """Read a package __init__.py: (all_names, source_map) where
  source_map maps a public name to ('child', child_name) or
  ('from', module, orig_name)."""
  tree = ast.parse(init_path.read_text(encoding="utf-8"))
  all_names = []
  source_map = {}
  for node in tree.body:
    if isinstance(node, ast.Assign):
      is_all = any(isinstance(t, ast.Name) and t.id == "__all__"
                   for t in node.targets)
      if is_all and isinstance(node.value, (ast.List, ast.Tuple)):
        all_names = [e.value for e in node.value.elts
                     if isinstance(e, ast.Constant)]
    elif isinstance(node, ast.ImportFrom) and node.level >= 1:
      if node.module is None:
        for alias in node.names:
          source_map[alias.asname or alias.name] = ("child", alias.name)
      else:
        for alias in node.names:
          key = alias.asname or alias.name
          source_map[key] = ("from", node.module, alias.name)
  return all_names, source_map


# ============================================================
# Library page emission (driven by __all__)
# ============================================================

def _emit_object(pkg_dotted: str, public: str, pyfile: Path) -> str:
  """Leaf page for one public name, showing the whole file."""
  stub = "%s.%s" % (pkg_dotted, public)
  _write(stub, "%s\n\n%s\n" % (_title(public),
                               _render_source(pyfile, stub)))
  _record_file_page(pyfile, stub)
  return stub


def _emit_whole_file(pyfile: Path) -> str:
  """Leaf page for a submodule pulled in via `from . import X`."""
  stub = _src_dotted(pyfile)
  _write(stub, "%s\n\n%s\n" % (_title(pyfile.stem),
                               _render_source(pyfile, stub)))
  _record_file_page(pyfile, stub)
  return stub


def _emit_package(pkg_dir: Path) -> str:
  """Package stub: __init__.py source plus a toctree of __all__."""
  dotted = _src_dotted(pkg_dir)
  init = pkg_dir / "__init__.py"
  all_names, source_map = _parse_init(init)
  own_defs = _top_level_defs(init)
  children = []
  for name in all_names:
    entry = source_map.get(name)
    if entry is None:
      if name in own_defs:
        stub = _emit_object(dotted, name, init)
        SYMBOL_PAGE[(dotted, name)] = stub
        children.append(stub)
      continue
    if entry[0] == "child":
      child = entry[1]
      child_dir = pkg_dir / child
      child_file = pkg_dir / ("%s.py" % child)
      if child_dir.is_dir() and (child_dir / "__init__.py").exists():
        children.append(_emit_package(child_dir))
      elif child_file.exists():
        children.append(_emit_whole_file(child_file))
    else:
      module, origin = entry[1], entry[2]
      modfile = pkg_dir / ("%s.py" % module)
      if modfile.exists():
        stub = _emit_object(dotted, name, modfile)
        SYMBOL_PAGE[(dotted, name)] = stub
        SYMBOL_PAGE[("%s.%s" % (dotted, module), origin)] = stub
        children.append(stub)
  _record_file_page(init, dotted)
  body = "%s\n\n%s\n\n.. toctree::\n   :maxdepth: 1\n\n" % (
    _title(pkg_dir.name), _render_source(init, dotted))
  body += "\n".join("   %s" % child for child in children) + "\n"
  _write(dotted, body)
  return dotted


# ============================================================
# Test tree emission (mirrors the directory layout)
# ============================================================

def _emit_test_file(pyfile: Path) -> str:
  """Leaf page for one test file, shown whole."""
  stub = _repo_dotted(pyfile)
  _write(stub, "%s\n\n%s\n" % (_title(pyfile.stem),
                               _render_source(pyfile, stub)))
  _record_file_page(pyfile, stub)
  return stub


def _emit_test_dir(test_dir: Path) -> str:
  """Directory stub: a title and a toctree of its test files and
  subdirectories. Skips __pycache__, __init__.py, and empty dirs."""
  stub = _repo_dotted(test_dir)
  children = []
  for pyfile in sorted(test_dir.glob("*.py")):
    if pyfile.name != "__init__.py":
      children.append(_emit_test_file(pyfile))
  for sub in sorted(p for p in test_dir.iterdir() if p.is_dir()):
    if sub.name == "__pycache__":
      continue
    if any(sub.rglob("*.py")):
      children.append(_emit_test_dir(sub))
  parts = [_title(test_dir.name), "", ".. toctree::",
           "   :maxdepth: 1", ""]
  parts += ["   %s" % child for child in children]
  _write(stub, "\n".join(parts) + "\n")
  return stub


# ============================================================
# Cross-reference pass
# ============================================================

def _abs_module(pyfile: Path, level: int, module) -> str:
  """Resolve an import target to an absolute dotted module. Relative
  imports (level >= 1) are resolved against the file's package; a
  relative import in a file outside src/ (e.g. a test) cannot name a
  worktoy symbol, so it resolves to ''."""
  if level == 0:
    return module or ""
  try:
    pkg_parts = pyfile.parent.relative_to(SRC_ROOT).parts
  except ValueError:
    return ""
  base = list(pkg_parts[:len(pkg_parts) - (level - 1)])
  if module:
    base += module.split(".")
  return ".".join(base)


def _scan_usages(root: Path):
  """page stub -> {using file (repo-relative posix): [use lines]} for
  every .py file under 'root'. An import binds a local name; the use
  sites are the occurrences of that name. __init__.py is skipped
  (re-export plumbing). Falls back to the import line if a bound name
  is never used in code."""
  usage = {}
  for pyfile in sorted(root.rglob("*.py")):
    if pyfile.name == "__init__.py":
      continue
    try:
      tree = ast.parse(pyfile.read_text(encoding="utf-8"))
    except SyntaxError:
      continue
    rel = _relpath(pyfile)
    bindings = {}
    import_line = {}
    for node in ast.walk(tree):
      if not isinstance(node, ast.ImportFrom):
        continue
      module = _abs_module(pyfile, node.level, node.module)
      for alias in node.names:
        page = SYMBOL_PAGE.get((module, alias.name))
        if page is None or FILE_PAGE.get(rel) == page:
          continue
        bindings[alias.asname or alias.name] = page
        import_line.setdefault(page, node.lineno)
    if not bindings:
      continue
    used = {}
    for node in ast.walk(tree):
      if isinstance(node, ast.Name) and node.id in bindings:
        used.setdefault(bindings[node.id], set()).add(node.lineno)
    for page in set(bindings.values()):
      lines = used.get(page) or {import_line[page]}
      usage.setdefault(page, {})[rel] = sorted(lines)
  return usage


def _append_section(usage, heading: str) -> None:
  """Append a cross-reference section (heading + a raw-HTML list) to
  each symbol page. One row per using file, every use line a link to
  that file's page at '#line-N'."""
  for page, files in usage.items():
    path = OUT / ("%s.rst" % page)
    if not path.exists():
      continue
    items = []
    for rel in sorted(files):
      linenos = files[rel]
      target = FILE_PAGE.get(rel)
      if target:
        links = ", ".join(
          '<a href="%s.html#line-%d">%d</a>' % (target, n, n)
          for n in linenos)
        items.append("   <li>%s: %s</li>" % (rel, links))
      else:
        nums = ", ".join(str(n) for n in linenos)
        items.append("   <li>%s: %s</li>" % (rel, nums))
    block = ["", heading, "-" * len(heading), "", ".. raw:: html", "",
             "   <ul>"] + items + ["   </ul>"]
    with path.open("a", encoding="utf-8") as handle:
      handle.write("\n".join(block) + "\n")


# ============================================================
# Entry point
# ============================================================

def generate(app: object = None) -> None:
  """Regenerate docs/_source/: the library packages, the tests tree,
  and the 'Used in' / 'Usage in testing' cross-references. Wired to
  'builder-inited'; 'app' is supplied by Sphinx and unused."""
  SYMBOL_PAGE.clear()
  FILE_PAGE.clear()
  if OUT.exists():
    shutil.rmtree(OUT)
  OUT.mkdir(parents=True)

  #  Library: top-level entries are worktoy's subpackages.
  all_names, source_map = _parse_init(PKG / "__init__.py")
  entries = []
  for name in all_names:
    entry = source_map.get(name)
    if entry and entry[0] == "child":
      child_dir = PKG / entry[1]
      if child_dir.is_dir() and (child_dir / "__init__.py").exists():
        entries.append(_emit_package(child_dir))

  #  Tests: one bottom entry, the tests/ tree.
  test_entry = None
  if TESTS_ROOT.is_dir():
    test_entry = _emit_test_dir(TESTS_ROOT)

  lines = [".. toctree::", "   :maxdepth: 1", ""]
  lines += ["   _source/%s" % entry for entry in entries]
  if test_entry:
    lines.append("   _source/%s" % test_entry)
  (OUT / "_packages.txt").write_text("\n".join(lines) + "\n",
                                     encoding="utf-8")

  #  Cross-references: library usage first, then test usage.
  _append_section(_scan_usages(PKG), "Used in")
  if TESTS_ROOT.is_dir():
    _append_section(_scan_usages(TESTS_ROOT), "Usage in testing")
