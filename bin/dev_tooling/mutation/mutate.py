"""
A mutation run of a worktoy package must survive anything short of the
disk going away: a runner that dies, a session that ends, a mutant that
hangs. Every result is appended to a file in this folder the moment it
is known, the files of a run carry the package and the start time in
their names, every mutant has an ID that is the same on every run, and
a runner started on an unfinished run skips every mutant already
recorded. The source under 'src/' is never mutated: each mutant is
written into a copy of the whole 'src' tree under the run's own
'runs/<package>_<stamp>_sandbox/' beside this file,
and the tests under 'tests/' run against that copy.

  python bin/dev_tooling/mutation/mutate.py list --package worktoy.utilities
  python bin/dev_tooling/mutation/mutate.py check --package worktoy.utilities --id ID
  python bin/dev_tooling/mutation/mutate.py run --package worktoy.utilities --jobs 4
  python bin/dev_tooling/mutation/mutate.py run --package worktoy.utilities --pass 1
  python bin/dev_tooling/mutation/mutate.py show --package worktoy.utilities --id ID
  python bin/dev_tooling/mutation/mutate.py report --package worktoy.utilities

Implementation
--------------

The mutants of a file are found by walking its syntax tree, in source
order, and each is a closure that changes one node of that tree; a
mutant is applied by parsing the file again, walking it the same way,
and calling the closure with the same index. The ID of a mutant is
'file:line:column:kind:variant', with the file relative to the package
and the variant counting the mutations of one kind at one position, so
the ID holds for as long as the source does. The kinds are listed on
'_describeKinds' below.

A run is the files 'runs/<package>_<YYYYMMDD-HHMMSS>_<kind>' beside this
file, a folder the repo ignores:
'meta.json' with the mutant table, 'results.jsonl' with one line per
finished mutant, 'attempts.jsonl' with one line per started mutant,
'progress.txt' with a single line rewritten after every start and
finish, 'survivors.md' with the report, and 'verdicts.json' and
'notes.md', written by hand, which the report reads. A result line
carries the pass it belongs to: pass 0 is the sweep over every mutant,
pass 1 and up rerun the mutants whose latest result is 'survived'. The
latest line of a mutant is its current result. A mutant started twice
in one pass without a result crashed the runner twice and is recorded
as 'crashed'; one started once without a result is rerun alone before
the rest, so a crash names its mutant. Ctrl-C ends a run the same way:
the queued mutants never start, the running ones keep their attempt
and lose their result, and the same command resumes. 'meta.json' also
holds a hash of every file of the package, and a run whose source has
changed since is refused, because an ID is a position and would name
another mutant; '--fresh' sweeps the current source.

The tests run as a subprocess of the Python running this script, with
'pytest' pointed at 'tests/', its configured 'addopts' and 'pythonpath'
replaced so coverage is off and the sandbox copy of 'src' is imported.
Exit code 0 or 5 is 'survived', 1 to 3 is 'killed', a timeout is
'timeout' and anything else is 'error'. The baseline runs on the
pristine copy before any run file is written; a baseline that fails
refuses the run, and so does one that collects no tests (exit code 5),
since a sweep against no tests marks every mutant survived and
measures nothing: until the first test exists the map is the listing
of 'list --verbose', not a sweep. The timeout is ten times the
baseline, at least twenty seconds, unless given. Each worker has a
sandbox of its own, so jobs run side by side.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import argparse
import ast
import difflib
import hashlib
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SRC = os.path.join(REPO, 'src')
RUNS = os.path.join(HERE, 'runs')
#  The tests run on the project environment and nothing else.
PYTHON = os.path.expanduser('~/miniforge3/envs/worktoy_env/bin/python')
IGNORE_CACHE = shutil.ignore_patterns('__pycache__')

SURVIVED = 'survived'
KILLED = 'killed'
TIMEOUT = 'timeout'
ERROR = 'error'
CRASHED = 'crashed'
STATUSES = (KILLED, SURVIVED, TIMEOUT, ERROR, CRASHED)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  FILES  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def readText(path: str) -> str:
  handle = None
  try:
    handle = open(path, 'r', encoding='utf-8')
  except OSError as osError:
    raise osError
  else:
    return handle.read()
  finally:
    if handle is not None:
      handle.close()


def writeText(path: str, text: str) -> None:
  """
  The text goes to a sibling file first and is moved into place, so a
  reader never sees a half-written file.
  """
  tmp = '%s.tmp' % path
  handle = None
  try:
    handle = open(tmp, 'w', encoding='utf-8')
  except OSError as osError:
    raise osError
  else:
    handle.write(text)
    handle.flush()
    os.fsync(handle.fileno())
  finally:
    if handle is not None:
      handle.close()
  os.replace(tmp, path)


def appendLine(path: str, line: str) -> None:
  handle = None
  try:
    handle = open(path, 'a', encoding='utf-8')
  except OSError as osError:
    raise osError
  else:
    handle.write(line)
    handle.write('\n')
    handle.flush()
    os.fsync(handle.fileno())
  finally:
    if handle is not None:
      handle.close()


def readJsonLines(path: str) -> list:
  """A line that does not parse, as the last line of a file cut short
  could be, is skipped."""
  if not os.path.exists(path):
    return []
  out = []
  for line in readText(path).splitlines():
    if not line.strip():
      continue
    try:
      out.append(json.loads(line))
    except ValueError:
      continue
  return out


def readJson(path: str, fallback: object) -> object:
  if not os.path.exists(path):
    return fallback
  return json.loads(readText(path))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  MUTANTS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Mutant:
  """
  One mutation of one source file: where it is, what it does, and the
  change it makes to the parsed tree it was collected from.
  """

  __slots__ = (
    'file', 'line', 'col', 'kind', 'variant', 'description', 'apply',
  )

  def __init__(
      self,
      file: str,
      line: int,
      col: int,
      kind: str,
      variant: int,
      description: str,
      apply: object,
  ) -> None:
    self.file = file
    self.line = line
    self.col = col
    self.kind = kind
    self.variant = variant
    self.description = description
    self.apply = apply

  @property
  def id(self) -> str:
    return '%s:%d:%d:%s:%d' % (
      self.file, self.line, self.col, self.kind, self.variant,
    )

  def record(self) -> dict:
    return dict(
        id=self.id,
        file=self.file,
        line=self.line,
        col=self.col,
        kind=self.kind,
        variant=self.variant,
        description=self.description,
    )


_SYMBOLS = {
  ast.Eq: '==', ast.NotEq: '!=', ast.Lt: '<', ast.LtE: '<=',
  ast.Gt: '>', ast.GtE: '>=', ast.Is: 'is', ast.IsNot: 'is not',
  ast.In: 'in', ast.NotIn: 'not in', ast.And: 'and', ast.Or: 'or',
  ast.Add: '+', ast.Sub: '-', ast.Mult: '*', ast.Div: '/',
  ast.FloorDiv: '//', ast.Pow: '**',
}

_COMPARE = {
  ast.Eq: (ast.NotEq,),
  ast.NotEq: (ast.Eq,),
  ast.Lt: (ast.LtE, ast.Gt),
  ast.LtE: (ast.Lt, ast.GtE),
  ast.Gt: (ast.GtE, ast.Lt),
  ast.GtE: (ast.Gt, ast.LtE),
  ast.Is: (ast.IsNot,),
  ast.IsNot: (ast.Is,),
  ast.In: (ast.NotIn,),
  ast.NotIn: (ast.In,),
}

_BINARY = {
  ast.Add: ast.Sub,
  ast.Sub: ast.Add,
  ast.Mult: ast.Add,
  ast.Div: ast.Mult,
  ast.FloorDiv: ast.Div,
  ast.Pow: ast.Mult,
}

_BUILTINS = {'min': 'max', 'max': 'min', 'any': 'all', 'all': 'any'}

_DELETABLE = (
  ast.Expr, ast.Assign, ast.AugAssign, ast.AnnAssign, ast.Raise,
  ast.Continue, ast.Break, ast.Delete,
)

_STATEMENT_LISTS = ('body', 'orelse', 'finalbody')

_SKIP_TARGETS = ('__all__', '__slots__')

_SCOPES = (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)


def _describeKinds() -> str:
  return """
  cmp      a comparison operator replaced: == and != swap, < becomes
           <= or >, and so on; is, is not, in and not in swap.
  bool     'and' and 'or' swap.
  not      a 'not' is dropped.
  flag     'True' and 'False' swap.
  num      an integer literal is one more or one less.
  str      a string literal of one line becomes '' or, if empty, 'XX'.
  binop    an arithmetic operator replaced: + and - swap, * becomes +,
           / becomes *, // becomes /, ** becomes *.
  aug      the same for an augmented assignment.
  ret      a returned value becomes None.
  cond     the condition of an if or a conditional expression becomes
           True or False; of a while, False.
  loopctl  'continue' and 'break' swap.
  builtin  min and max swap, any and all swap.
  slice    a one-sided slice moves its bound to the other side.
  tup      one element is dropped from a tuple that is an argument of
           isinstance or issubclass, the right side of in or not in,
           the value of an assignment, or the types of an except.
  del      a statement inside a function body is replaced by pass: a
           call, an assignment, a raise, a continue, a break or a del.
  """


def _replacing(parent: ast.AST, field: str, index: object, new: ast.AST):
  def apply() -> None:
    if index is None:
      setattr(parent, field, new)
    else:
      getattr(parent, field)[index] = new

  return apply


def _setting(node: ast.AST, field: str, value: object):
  def apply() -> None:
    setattr(node, field, value)

  return apply


def _settingItem(node: ast.AST, field: str, index: int, value: object):
  def apply() -> None:
    getattr(node, field)[index] = value

  return apply


def _dropping(node: ast.AST, field: str, index: int):
  def apply() -> None:
    del getattr(node, field)[index]

  return apply


def _isDocstring(scope: ast.AST, field: str, items: list) -> bool:
  if field != 'body' or not isinstance(scope, _SCOPES):
    return False
  if not items or not isinstance(items[0], ast.Expr):
    return False
  value = items[0].value
  return isinstance(value, ast.Constant) and isinstance(value.value, str)


def _isNoneConstant(node: ast.AST) -> bool:
  return isinstance(node, ast.Constant) and node.value is None


def _namesTarget(node: ast.AST, names: tuple) -> bool:
  if isinstance(node, ast.Assign):
    targets = node.targets
  elif isinstance(node, ast.AnnAssign):
    targets = [node.target]
  else:
    return False
  for target in targets:
    if isinstance(target, ast.Name) and target.id in names:
      return True
  return False


def _tupleContext(parent: ast.AST, field: str, index: object) -> bool:
  if isinstance(parent, ast.Call) and field == 'args':
    func = parent.func
    if isinstance(func, ast.Name):
      return func.id in ('isinstance', 'issubclass')
    return False
  if isinstance(parent, ast.Compare) and field == 'comparators':
    return isinstance(parent.ops[index], (ast.In, ast.NotIn))
  if isinstance(parent, (ast.Assign, ast.AnnAssign)) and field == 'value':
    return True
  if isinstance(parent, ast.ExceptHandler) and field == 'type':
    return True
  return False


class _Collector:
  """
  The walk over one file, collecting a mutant for every change the
  kinds above allow, in source order.
  """

  def __init__(self, file: str) -> None:
    self.file = file
    self.out = []
    self.counts = dict()

  def add(
      self,
      node: ast.AST,
      kind: str,
      description: str,
      apply: object,
  ) -> None:
    key = (node.lineno, node.col_offset, kind)
    if key in self.counts:
      variant = self.counts[key]
    else:
      variant = 0
    self.counts[key] = variant + 1
    mutant = Mutant(
        self.file, node.lineno, node.col_offset, kind, variant,
        description, apply,
    )
    self.out.append(mutant)

  @staticmethod
  def _skipped(node: ast.AST) -> bool:
    if isinstance(node, (ast.arguments, ast.Import, ast.ImportFrom)):
      return True
    if isinstance(node, ast.If):
      test = node.test
      if isinstance(test, ast.Name) and test.id == 'TYPE_CHECKING':
        return True
    return _namesTarget(node, _SKIP_TARGETS)

  def walk(
      self,
      node: ast.AST,
      parent: ast.AST,
      field: str,
      index: object,
      depth: int,
  ) -> None:
    if self._skipped(node):
      return
    self._collect(node, parent, field, index, depth)
    if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
      fields = ['body']
    elif isinstance(node, ast.AsyncFunctionDef):
      fields = ['body']
    elif isinstance(node, ast.Lambda):
      fields = ['body']
    else:
      fields = [name for name, _ in ast.iter_fields(node)]
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
      depth += 1
    if isinstance(node, ast.Lambda):
      depth += 1
    for name in fields:
      value = getattr(node, name)
      if isinstance(value, list):
        first = 1 if _isDocstring(node, name, value) else 0
        for i, item in enumerate(value):
          if i < first:
            continue
          if isinstance(item, ast.AST):
            self.walk(item, node, name, i, depth)
      elif isinstance(value, ast.AST):
        self.walk(value, node, name, None, depth)

  def _collect(
      self,
      node: ast.AST,
      parent: ast.AST,
      field: str,
      index: object,
      depth: int,
  ) -> None:
    if isinstance(node, ast.Compare):
      self._compare(node)
    elif isinstance(node, ast.BoolOp):
      self._boolOp(node)
    elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
      apply = _replacing(parent, field, index, node.operand)
      self.add(node, 'not', "drop 'not'", apply)
    elif isinstance(node, ast.Constant):
      self._constant(node)
    elif isinstance(node, ast.BinOp):
      self._binary(node, 'binop')
    elif isinstance(node, ast.AugAssign):
      self._binary(node, 'aug')
    elif isinstance(node, ast.Return):
      self._return(node)
    elif isinstance(node, (ast.If, ast.IfExp)):
      self._condition(node, True)
      self._condition(node, False)
    elif isinstance(node, ast.While):
      self._condition(node, False)
    elif isinstance(node, ast.Continue):
      new = ast.copy_location(ast.Break(), node)
      apply = _replacing(parent, field, index, new)
      self.add(node, 'loopctl', "'continue' -> 'break'", apply)
    elif isinstance(node, ast.Break):
      new = ast.copy_location(ast.Continue(), node)
      apply = _replacing(parent, field, index, new)
      self.add(node, 'loopctl', "'break' -> 'continue'", apply)
    elif isinstance(node, ast.Call):
      self._call(node)
    elif isinstance(node, ast.Slice):
      self._slice(node)
    elif isinstance(node, ast.Tuple):
      self._tuple(node, parent, field, index)
    if depth > 0 and isinstance(node, _DELETABLE):
      self._delete(node, parent, field, index)

  def _compare(self, node: ast.Compare) -> None:
    for i, op in enumerate(node.ops):
      if type(op) not in _COMPARE:
        continue
      for new in _COMPARE[type(op)]:
        description = "'%s' -> '%s'" % (_SYMBOLS[type(op)], _SYMBOLS[new])
        self.add(node, 'cmp', description, _settingItem(node, 'ops', i, new()))

  def _boolOp(self, node: ast.BoolOp) -> None:
    if isinstance(node.op, ast.And):
      new = ast.Or
    else:
      new = ast.And
    description = "'%s' -> '%s'" % (_SYMBOLS[type(node.op)], _SYMBOLS[new])
    self.add(node, 'bool', description, _setting(node, 'op', new()))

  def _constant(self, node: ast.Constant) -> None:
    value = node.value
    if isinstance(value, bool):
      description = '%r -> %r' % (value, not value)
      self.add(node, 'flag', description, _setting(node, 'value', not value))
    elif isinstance(value, int):
      for new in (value + 1, value - 1):
        description = '%r -> %r' % (value, new)
        self.add(node, 'num', description, _setting(node, 'value', new))
    elif isinstance(value, str):
      if '\n' in value:
        return
      new = '' if value else 'XX'
      description = '%r -> %r' % (value, new)
      self.add(node, 'str', description, _setting(node, 'value', new))

  def _binary(self, node: ast.AST, kind: str) -> None:
    if type(node.op) not in _BINARY:
      return
    new = _BINARY[type(node.op)]
    description = "'%s' -> '%s'" % (_SYMBOLS[type(node.op)], _SYMBOLS[new])
    self.add(node, kind, description, _setting(node, 'op', new()))

  def _return(self, node: ast.Return) -> None:
    if node.value is None or _isNoneConstant(node.value):
      return
    new = ast.copy_location(ast.Constant(None), node.value)
    self.add(node, 'ret', 'return None', _setting(node, 'value', new))

  def _condition(self, node: ast.AST, value: bool) -> None:
    new = ast.copy_location(ast.Constant(value), node.test)
    self.add(node, 'cond', 'condition -> %r' % value, _setting(node, 'test', new))

  def _call(self, node: ast.Call) -> None:
    func = node.func
    if not isinstance(func, ast.Name) or func.id not in _BUILTINS:
      return
    new = _BUILTINS[func.id]
    description = "'%s' -> '%s'" % (func.id, new)
    self.add(node, 'builtin', description, _setting(func, 'id', new))

  def _slice(self, node: ast.Slice) -> None:
    if node.step is not None:
      return
    if node.lower is None and node.upper is not None:
      def apply() -> None:
        node.lower, node.upper = node.upper, None

      self.add(node, 'slice', '[:b] -> [b:]', apply)
    elif node.upper is None and node.lower is not None:
      def apply() -> None:
        node.lower, node.upper = None, node.lower

      self.add(node, 'slice', '[a:] -> [:a]', apply)

  def _tuple(
      self,
      node: ast.Tuple,
      parent: ast.AST,
      field: str,
      index: object,
  ) -> None:
    if len(node.elts) < 2:
      return
    for element in node.elts:
      if isinstance(element, ast.Starred):
        return
    if not _tupleContext(parent, field, index):
      return
    for i, element in enumerate(node.elts):
      description = 'drop %s' % ast.unparse(element)
      self.add(node, 'tup', description, _dropping(node, 'elts', i))

  def _delete(
      self,
      node: ast.AST,
      parent: ast.AST,
      field: str,
      index: object,
  ) -> None:
    if field not in _STATEMENT_LISTS or index is None:
      return
    if isinstance(node, ast.Expr):
      kinds = (ast.Call, ast.Await, ast.Yield, ast.YieldFrom)
      if not isinstance(node.value, kinds):
        return
    if isinstance(node, ast.AnnAssign) and node.value is None:
      return
    new = ast.copy_location(ast.Pass(), node)
    source = ast.unparse(node).splitlines()[0]
    description = 'delete: %s' % source[:60]
    self.add(node, 'del', description, _replacing(parent, field, index, new))


def collectFile(text: str, file: str) -> tuple:
  """Returns the tree of 'text' and its mutants, bound to that tree."""
  tree = ast.parse(text)
  collector = _Collector(file)
  collector.walk(tree, None, None, None, 0)
  return tree, collector.out


def packageDir(package: str) -> str:
  return os.path.join(SRC, *package.split('.'))


def packageFiles(package: str) -> list:
  """The '.py' files of the package and its subpackages, relative to
  the package directory, in a fixed order."""
  root = packageDir(package)
  out = []
  for dirPath, dirNames, fileNames in os.walk(root):
    dirNames[:] = sorted(d for d in dirNames if d != '__pycache__')
    for fileName in sorted(fileNames):
      if not fileName.endswith('.py'):
        continue
      absolute = os.path.join(dirPath, fileName)
      relative = os.path.relpath(absolute, root).replace(os.sep, '/')
      out.append(relative)
  return out


def collectPackage(package: str) -> list:
  root = packageDir(package)
  out = []
  for file in packageFiles(package):
    text = readText(os.path.join(root, file))
    _, mutants = collectFile(text, file)
    out.extend(mutants)
  return out


def packageHashes(package: str) -> dict:
  """The SHA-256 of every file of the package, keyed like the mutant
  table, so a resumed run can tell whether the source it was built on
  is still the source on disk."""
  root = packageDir(package)
  out = dict()
  for file in packageFiles(package):
    text = readText(os.path.join(root, file))
    out[file] = hashlib.sha256(text.encode('utf-8')).hexdigest()
  return out


def mutateSource(text: str, mutantId: str, file: str) -> str:
  """The source of 'file' with the mutant of 'mutantId' applied."""
  tree, mutants = collectFile(text, file)
  for mutant in mutants:
    if mutant.id == mutantId:
      mutant.apply()
      break
  else:
    raise RuntimeError('No mutant %s in the current source' % mutantId)
  ast.fix_missing_locations(tree)
  return ast.unparse(tree) + '\n'


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  RUNS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Run:
  """
  The files of one run, named by package and start time.
  """

  def __init__(self, package: str, stamp: str) -> None:
    self.package = package
    self.stamp = stamp
    self.prefix = os.path.join(RUNS, '%s_%s' % (package, stamp))

  def path(self, kind: str) -> str:
    return '%s_%s' % (self.prefix, kind)

  @property
  def meta(self) -> dict:
    return readJson(self.path('meta.json'), dict())

  @property
  def results(self) -> list:
    return readJsonLines(self.path('results.jsonl'))

  @property
  def attempts(self) -> list:
    return readJsonLines(self.path('attempts.jsonl'))

  @property
  def ids(self) -> list:
    return [m['id'] for m in self.meta['mutants']]

  def latest(self) -> dict:
    """The latest result line of every mutant that has one."""
    out = dict()
    for line in self.results:
      out[line['id']] = line
    return out


def listRuns(package: str) -> list:
  head = '%s_' % package
  tail = '_meta.json'
  out = []
  if not os.path.isdir(RUNS):
    return out
  for name in sorted(os.listdir(RUNS)):
    if name.startswith(head) and name.endswith(tail):
      stamp = name[len(head):-len(tail)]
      if '_' in stamp or '.' in stamp:
        continue
      out.append(Run(package, stamp))
  return out


def latestRun(package: str) -> Run:
  runs = listRuns(package)
  if not runs:
    raise SystemExit('No run of %s found under %s' % (package, RUNS))
  return runs[-1]


def unfinishedRun(package: str) -> object:
  """The latest run whose sweep has a mutant without a result, or None."""
  runs = listRuns(package)
  if not runs:
    return None
  run = runs[-1]
  recorded = set()
  for line in run.results:
    if line['pass'] == 0:
      recorded.add(line['id'])
  for mutantId in run.ids:
    if mutantId not in recorded:
      return run
  return None


def newStamp() -> str:
  return datetime.now().strftime('%Y%m%d-%H%M%S')


def writeRun(run: Run, mutants: list) -> None:
  """Writes the first files of a new run: the mutant table and the two
  empty logs."""
  package = run.package
  stamp = run.stamp
  meta = dict(
      package=package,
      stamp=stamp,
      python=PYTHON,
      created=datetime.now().isoformat(timespec='seconds'),
      total=len(mutants),
      files=packageHashes(package),
      mutants=[m.record() for m in mutants],
  )
  os.makedirs(RUNS, exist_ok=True)
  writeText(run.path('meta.json'), json.dumps(meta, indent=1))
  appendLine(run.path('results.jsonl'), '')
  appendLine(run.path('attempts.jsonl'), '')


def changedFiles(run: Run) -> list:
  """The files of the package whose source differs from the one the
  run was built on, in a fixed order."""
  recorded = run.meta['files']
  current = packageHashes(run.package)
  out = []
  for file in sorted(set(recorded) | set(current)):
    if file not in recorded or file not in current:
      out.append(file)
    elif recorded[file] != current[file]:
      out.append(file)
  return out


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  TESTS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def prepareSandbox(sandbox: str, index: int) -> str:
  """A fresh copy of 'src' for worker 'index' under 'sandbox'; returns
  the path of the copy."""
  box = os.path.join(sandbox, str(index))
  if os.path.exists(box):
    shutil.rmtree(box)
  os.makedirs(box)
  boxSrc = os.path.join(box, 'src')
  shutil.copytree(SRC, boxSrc, ignore=IGNORE_CACHE)
  return boxSrc


def runTests(boxSrc: str, timeout: float) -> dict:
  """
  Runs the suite against the sandbox and returns the status, the exit
  code, the duration and, for a kill, the first failing test.
  """
  command = [
    PYTHON, '-B', '-m', 'pytest', 'tests', '-x', '-q', '--no-header',
    '-p', 'no:cacheprovider', '-o', 'addopts=', '-o', 'pythonpath=%s' % boxSrc,
  ]
  env = dict(os.environ)
  env['PYTHONDONTWRITEBYTECODE'] = '1'
  started = time.monotonic()
  try:
    completed = subprocess.run(
        command, cwd=REPO, env=env, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, text=True,
    )
  except subprocess.TimeoutExpired:
    duration = time.monotonic() - started
    return dict(status=TIMEOUT, exit=None, duration=round(duration, 3))
  duration = time.monotonic() - started
  code = completed.returncode
  out = dict(exit=code, duration=round(duration, 3))
  if code in (0, 5):
    out['status'] = SURVIVED
  elif code in (1, 2, 3):
    out['status'] = KILLED
    out['killedBy'] = _firstFailure(completed.stdout)
  else:
    out['status'] = ERROR
    out['error'] = completed.stdout[-500:]
  return out


def _firstFailure(output: str) -> str:
  for line in output.splitlines():
    if line.startswith('FAILED ') or line.startswith('ERROR '):
      return line[:200]
  for line in output.splitlines():
    if 'Error' in line:
      return line[:200]
  return ''


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  SWEEP  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Recorder:
  """
  The one writer of the attempts, the results and the progress line of
  a run, locked so workers may report from their threads.
  """

  def __init__(
      self,
      run: Run,
      passNo: int,
      total: int,
      done: int,
      counts: dict,
      timeout: float,
  ) -> None:
    self.run = run
    self.passNo = passNo
    self.total = total
    self.done = done
    self.counts = counts
    self.timeout = timeout
    self.started = time.monotonic()
    self.running = []
    self.lock = threading.Lock()
    self.progress()

  def attempt(self, mutant: Mutant) -> None:
    line = dict(
        id=mutant.id,
        at=datetime.now().isoformat(timespec='seconds'),
    )
    line['pass'] = self.passNo
    with self.lock:
      appendLine(self.run.path('attempts.jsonl'), json.dumps(line))
      self.running.append(mutant.id)
      self.progress()

  def result(self, line: dict) -> None:
    line['pass'] = self.passNo
    line['at'] = datetime.now().isoformat(timespec='seconds')
    with self.lock:
      appendLine(self.run.path('results.jsonl'), json.dumps(line))
      if line['id'] in self.running:
        self.running.remove(line['id'])
      self.done += 1
      self.counts[line['status']] += 1
      self.progress()

  def progress(self) -> None:
    elapsed = int(time.monotonic() - self.started)
    clock = '%02d:%02d:%02d' % (
      elapsed // 3600, elapsed % 3600 // 60, elapsed % 60,
    )
    running = ','.join(self.running) if self.running else '-'
    line = (
        '%d/%d killed=%d survived=%d timeouts=%d errors=%d crashed=%d '
        'elapsed=%s pass=%d timeout=%ds pid=%d running=%s'
    ) % (
      self.done, self.total, self.counts[KILLED], self.counts[SURVIVED],
      self.counts[TIMEOUT], self.counts[ERROR], self.counts[CRASHED],
      clock, self.passNo, int(self.timeout), os.getpid(), running,
    )
    writeText(self.run.path('progress.txt'), line + '\n')


def _work(
    mutant: Mutant,
    package: str,
    boxes: queue.Queue,
    originals: dict,
    timeout: float,
    recorder: Recorder,
) -> dict:
  boxSrc = boxes.get()
  line = mutant.record()
  try:
    recorder.attempt(mutant)
    original = originals[mutant.file]
    mutated = mutateSource(original, mutant.id, mutant.file)
    target = os.path.join(boxSrc, *package.split('.'), mutant.file)
    writeText(target, mutated)
    try:
      line.update(runTests(boxSrc, timeout))
    finally:
      writeText(target, original)
  except Exception as exception:
    line['status'] = ERROR
    line['exit'] = None
    line['duration'] = 0.0
    line['error'] = '%s: %s' % (type(exception).__name__, exception)
  finally:
    boxes.put(boxSrc)
  return line


def _executeBatch(
    mutants: list,
    package: str,
    boxes: queue.Queue,
    jobs: int,
    originals: dict,
    timeout: float,
    recorder: Recorder,
) -> None:
  if not mutants:
    return
  pool = ThreadPoolExecutor(max_workers=jobs)
  futures = []
  for mutant in mutants:
    future = pool.submit(
        _work, mutant, package, boxes, originals, timeout, recorder,
    )
    futures.append(future)
  try:
    for future in as_completed(futures):
      recorder.result(future.result())
  except KeyboardInterrupt:
    #  Ctrl-C reaches the running pytests too, which exit at once with
    #  code 2, a kill that is not the mutant's: their lines are dropped,
    #  so the resume reruns them alone, and the queued mutants never
    #  start.
    pool.shutdown(wait=True, cancel_futures=True)
    raise
  pool.shutdown(wait=True)


def _selectTargets(run: Run, passNo: int, only: list) -> list:
  """The IDs this pass runs, in the order of the mutant table: every
  mutant for the sweep, the current survivors for a rerun, or those
  given."""
  ids = run.ids
  if only:
    chosen = set(only)
    unknown = chosen - set(ids)
    if unknown:
      raise SystemExit('Unknown mutant IDs: %s' % ', '.join(sorted(unknown)))
    return [i for i in ids if i in chosen]
  if passNo == 0:
    return ids
  latest = run.latest()
  out = []
  for mutantId in ids:
    if mutantId in latest and latest[mutantId]['status'] == SURVIVED:
      out.append(mutantId)
  return out


def _baselineRefusal(baseline: dict, package: str) -> str:
  """The reason a run must not start, or '' when the baseline is sound:
  a suite that fails on the pristine source measures nothing, and so
  does one in which pytest collects no tests, which is exit code 5."""
  if baseline['exit'] == 5:
    return (
      'pytest collected no tests under tests/, so a sweep would mark\n'
      'every mutant survived and measure nothing. The map of a suite\n'
      'that does not exist yet is the listing, not a sweep:\n'
      '  mutate.py list --package %s --verbose\n'
      'Write the first tests from it, then sweep.' % package
    )
  if baseline['status'] != SURVIVED:
    return 'The tests fail on the pristine source; nothing to measure.\n%s' % (
      baseline.get('killedBy', baseline.get('error', '')),
    )
  return ''


def commandRun(args: argparse.Namespace) -> int:
  package = args.package
  mutants = collectPackage(package)
  byId = {m.id: m for m in mutants}
  only = [i for i in args.ids.split(',') if i] if args.ids else []
  created = False
  if args.passNo == 0 and not args.fresh:
    run = unfinishedRun(package)
    if run is None:
      run = Run(package, newStamp())
      created = True
  elif args.passNo == 0:
    run = Run(package, newStamp())
    created = True
  else:
    run = latestRun(package)
  if not created:
    changed = changedFiles(run)
    if changed:
      print('The source of %s changed since run %s was built:' % (
        package, run.stamp,
      ))
      for file in changed:
        print('  %s' % file)
      print('An ID is a position, so the mutants of that run are no '
            'longer the ones it recorded. Sweep the current source '
            'with --fresh.')
      return 2
  sandbox = run.path('sandbox')
  timeout = args.timeout
  boxes = queue.Queue()
  jobs = max(1, args.jobs)
  boxSrcs = [prepareSandbox(sandbox, k) for k in range(jobs)]
  for boxSrc in boxSrcs:
    boxes.put(boxSrc)
  baseline = runTests(boxSrcs[0], 600.0)
  print('Baseline: %s in %.1fs (exit %s)' % (
    baseline['status'], baseline['duration'], baseline['exit'],
  ))
  refusal = _baselineRefusal(baseline, package)
  if refusal:
    print(refusal)
    if not args.keepSandbox and os.path.exists(sandbox):
      shutil.rmtree(sandbox)
    return 2
  if timeout is None:
    timeout = max(20.0, baseline['duration'] * 10.0 + 5.0)
  if created:
    writeRun(run, mutants)
    print('New run %s with %d mutants' % (run.prefix, len(mutants)))
  elif args.passNo == 0:
    print('Resuming run %s' % run.prefix)
  else:
    print('Rerun pass %d on run %s' % (args.passNo, run.prefix))
  targets = _selectTargets(run, args.passNo, only)
  recorded = dict()
  for line in run.results:
    if line['pass'] == args.passNo:
      recorded[line['id']] = line
  attempts = dict()
  for line in run.attempts:
    if line['pass'] == args.passNo:
      attempts[line['id']] = attempts.get(line['id'], 0) + 1
  counts = {status: 0 for status in STATUSES}
  for mutantId in targets:
    if mutantId in recorded:
      counts[recorded[mutantId]['status']] += 1
  pending = [i for i in targets if i not in recorded]
  crashed = [i for i in pending if attempts.get(i, 0) >= 2]
  retried = [i for i in pending if attempts.get(i, 0) == 1]
  fresh = [i for i in pending if attempts.get(i, 0) == 0]
  recorder = Recorder(
      run, args.passNo, len(targets), len(recorded), counts, timeout,
  )
  for mutantId in crashed:
    line = byId[mutantId].record()
    line['status'] = CRASHED
    line['exit'] = None
    line['duration'] = 0.0
    line['error'] = 'started twice without a result'
    recorder.result(line)
  print('Pass %d: %d targets, %d recorded, %d crashed, %d retried, '
        '%d fresh, timeout %ds, jobs %d' % (
          args.passNo, len(targets), len(recorded), len(crashed),
          len(retried), len(fresh), timeout, jobs,
        ))
  originals = dict()
  root = packageDir(package)
  for file in packageFiles(package):
    originals[file] = readText(os.path.join(root, file))
  retriedMutants = [byId[i] for i in retried]
  freshMutants = [byId[i] for i in fresh]
  interrupted = False
  try:
    _executeBatch(
        retriedMutants, package, boxes, 1, originals, timeout, recorder,
    )
    _executeBatch(
        freshMutants, package, boxes, jobs, originals, timeout, recorder,
    )
  except KeyboardInterrupt:
    interrupted = True
  if not args.keepSandbox and os.path.exists(sandbox):
    shutil.rmtree(sandbox)
  writeReport(run)
  progress = readText(run.path('progress.txt')).strip()
  if interrupted:
    print('Interrupted: %s' % progress)
    print('The same command resumes the run.')
    return 130
  print('Done: %s' % progress)
  return 0


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  REPORT   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def _sourceLine(package: str, file: str, line: int) -> str:
  path = os.path.join(packageDir(package), file)
  if not os.path.exists(path):
    return ''
  lines = readText(path).splitlines()
  if 0 < line <= len(lines):
    return lines[line - 1].strip()
  return ''


def writeReport(run: Run) -> str:
  """
  Writes 'survivors.md': the totals, every survivor grouped by file
  with its verdict from 'verdicts.json', the mutants killed in rerun
  passes with the test that killed them, and 'notes.md' if present.
  """
  meta = run.meta
  package = meta['package']
  latest = run.latest()
  verdicts = readJson(run.path('verdicts.json'), dict())
  counts = {status: 0 for status in STATUSES}
  pendingCount = 0
  for record in meta['mutants']:
    if record['id'] in latest:
      counts[latest[record['id']]['status']] += 1
    else:
      pendingCount += 1
  survivors = [
    r for r in meta['mutants']
    if r['id'] in latest and latest[r['id']]['status'] == SURVIVED
  ]
  needTest = 0
  equivalent = 0
  unclassified = 0
  for record in survivors:
    if record['id'] not in verdicts:
      unclassified += 1
    elif verdicts[record['id']]['verdict'] == 'equivalent':
      equivalent += 1
    else:
      needTest += 1
  lines = []
  lines.append('# Survivors of %s, run %s' % (package, run.stamp))
  lines.append('')
  lines.append(
      'Latest result per mutant: %d mutants, %d killed, %d survived, '
      '%d timed out, %d errors, %d crashed, %d not yet run.' % (
        len(meta['mutants']), counts[KILLED], counts[SURVIVED],
        counts[TIMEOUT], counts[ERROR], counts[CRASHED], pendingCount,
      )
  )
  lines.append('')
  lines.append(
      'Survivors: %d need a test, %d equivalent, %d unclassified.' % (
        needTest, equivalent, unclassified,
      )
  )
  lines.append('')
  byFile = dict()
  for record in survivors:
    byFile.setdefault(record['file'], []).append(record)
  for file in sorted(byFile):
    lines.append('## %s' % file)
    lines.append('')
    for record in byFile[file]:
      mutantId = record['id']
      if mutantId in verdicts:
        verdict = verdicts[mutantId]
        if verdict['verdict'] == 'equivalent':
          mark = 'equivalent: %s' % verdict['reason']
        elif verdict.get('reason', ''):
          mark = 'needs a test: %s' % verdict['reason']
        else:
          mark = 'needs a test'
      else:
        mark = 'unclassified'
      source = _sourceLine(package, file, record['line'])
      lines.append('- `%s` line %d: %s' % (
        mutantId, record['line'], record['description'],
      ))
      if source:
        lines.append('  `%s`' % source)
      lines.append('  %s' % mark)
    lines.append('')
  rerunKilled = [
    r for r in meta['mutants']
    if r['id'] in latest
    and latest[r['id']]['status'] == KILLED
    and latest[r['id']]['pass'] > 0
  ]
  if rerunKilled:
    lines.append('## Killed in rerun passes')
    lines.append('')
    for record in rerunKilled:
      line = latest[record['id']]
      lines.append('- `%s` (pass %d): %s' % (
        record['id'], line['pass'], line.get('killedBy', ''),
      ))
    lines.append('')
  others = [
    r for r in meta['mutants']
    if r['id'] in latest
    and latest[r['id']]['status'] in (TIMEOUT, ERROR, CRASHED)
  ]
  if others:
    lines.append('## Timeouts, errors and crashes')
    lines.append('')
    for record in others:
      line = latest[record['id']]
      lines.append('- `%s`: %s %s' % (
        record['id'], line['status'], line.get('error', ''),
      ))
    lines.append('')
  notesPath = run.path('notes.md')
  if os.path.exists(notesPath):
    lines.append('## Notes')
    lines.append('')
    lines.append(readText(notesPath).rstrip())
    lines.append('')
  text = '\n'.join(lines)
  writeText(run.path('survivors.md'), text)
  return text


def commandReport(args: argparse.Namespace) -> int:
  run = latestRun(args.package)
  text = writeReport(run)
  print(text.splitlines()[2])
  print(text.splitlines()[4])
  print('Written: %s' % run.path('survivors.md'))
  return 0


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  LIST, SHOW, CHECK  # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def commandList(args: argparse.Namespace) -> int:
  package = args.package
  root = packageDir(package)
  if not os.path.isdir(root):
    raise SystemExit('No package directory at %s' % root)
  byFile = dict()
  byKind = dict()
  total = 0
  for file in packageFiles(package):
    text = readText(os.path.join(root, file))
    tree, mutants = collectFile(text, file)
    again = ast.parse(ast.unparse(tree))
    if ast.dump(again) != ast.dump(ast.parse(text)):
      print('WARNING: %s does not round-trip through ast.unparse' % file)
    byFile[file] = len(mutants)
    total += len(mutants)
    for mutant in mutants:
      byKind[mutant.kind] = byKind.get(mutant.kind, 0) + 1
      if args.verbose:
        print('%s  %s' % (mutant.id, mutant.description))
  for file in sorted(byFile):
    print('%5d  %s' % (byFile[file], file))
  print('%5d  total' % total)
  for kind in sorted(byKind):
    print('%5d  %s' % (byKind[kind], kind))
  return 0


def writeListing(run: Run) -> str:
  """
  Writes 'mutants.txt': every source line of the package that has a
  mutant, followed by the kind, variant and description of each mutant
  on it, grouped by file, so the map of the run can be read beside the
  code.
  """
  meta = run.meta
  package = meta['package']
  root = packageDir(package)
  byFile = dict()
  for record in meta['mutants']:
    byFile.setdefault(record['file'], []).append(record)
  lines = []
  for file in packageFiles(package):
    if file not in byFile:
      continue
    source = readText(os.path.join(root, file)).splitlines()
    lines.append('=' * 70)
    lines.append('%s  (%d mutants)' % (file, len(byFile[file])))
    byLine = dict()
    for record in byFile[file]:
      byLine.setdefault(record['line'], []).append(record)
    for line in sorted(byLine):
      if 0 < line <= len(source):
        text = source[line - 1].rstrip()
      else:
        text = ''
      lines.append('%4d | %s' % (line, text))
      for record in byLine[line]:
        lines.append('       %s:%d  %s' % (
          record['kind'], record['variant'], record['description'],
        ))
  text = '\n'.join(lines) + '\n'
  writeText(run.path('mutants.txt'), text)
  return text


def commandListing(args: argparse.Namespace) -> int:
  run = latestRun(args.package)
  text = writeListing(run)
  print('Written: %s (%d lines)' % (
    run.path('mutants.txt'), len(text.splitlines()),
  ))
  return 0


def _findMutant(package: str, mutantId: str) -> Mutant:
  for mutant in collectPackage(package):
    if mutant.id == mutantId:
      return mutant
  raise SystemExit('No mutant %s in %s' % (mutantId, package))


def commandShow(args: argparse.Namespace) -> int:
  mutant = _findMutant(args.package, args.id)
  path = os.path.join(packageDir(args.package), mutant.file)
  text = readText(path)
  before = ast.unparse(ast.parse(text)) + '\n'
  after = mutateSource(text, mutant.id, mutant.file)
  diff = difflib.unified_diff(
      before.splitlines(), after.splitlines(),
      'original', mutant.id, lineterm='', n=2,
  )
  print(mutant.id, mutant.description)
  print('\n'.join(diff))
  return 0


def commandCheck(args: argparse.Namespace) -> int:
  """Runs the baseline and one mutant in a sandbox, writing no run."""
  mutant = _findMutant(args.package, args.id)
  sandbox = os.path.join(RUNS, '%s_check_sandbox' % args.package)
  boxSrc = prepareSandbox(sandbox, 0)
  baseline = runTests(boxSrc, 600.0)
  print('baseline: %s' % baseline)
  original = readText(os.path.join(packageDir(args.package), mutant.file))
  mutated = mutateSource(original, mutant.id, mutant.file)
  target = os.path.join(boxSrc, *args.package.split('.'), mutant.file)
  writeText(target, mutated)
  try:
    result = runTests(boxSrc, 600.0)
  finally:
    writeText(target, original)
  print('%s: %s' % (mutant.id, result))
  shutil.rmtree(sandbox)
  return 0


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  MAIN   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def main(argv: list) -> int:
  parser = argparse.ArgumentParser(
      description='Mutation testing of a worktoy package.',
      epilog=_describeKinds(),
      formatter_class=argparse.RawDescriptionHelpFormatter,
  )
  commands = parser.add_subparsers(dest='command', required=True)

  listParser = commands.add_parser('list', help='count the mutants')
  listParser.add_argument('--package', required=True)
  listParser.add_argument('--verbose', action='store_true')
  listParser.set_defaults(func=commandList)

  showParser = commands.add_parser('show', help='diff one mutant')
  showParser.add_argument('--package', required=True)
  showParser.add_argument('--id', required=True)
  showParser.set_defaults(func=commandShow)

  checkParser = commands.add_parser('check', help='try one mutant')
  checkParser.add_argument('--package', required=True)
  checkParser.add_argument('--id', required=True)
  checkParser.set_defaults(func=commandCheck)

  runParser = commands.add_parser('run', help='sweep or rerun')
  runParser.add_argument('--package', required=True)
  runParser.add_argument('--pass', dest='passNo', type=int, default=0)
  runParser.add_argument('--jobs', type=int, default=4)
  runParser.add_argument('--timeout', type=float, default=None)
  runParser.add_argument('--ids', default='')
  runParser.add_argument('--fresh', action='store_true')
  runParser.add_argument('--keep-sandbox', dest='keepSandbox',
                         action='store_true')
  runParser.set_defaults(func=commandRun)

  reportParser = commands.add_parser('report', help='write survivors.md')
  reportParser.add_argument('--package', required=True)
  reportParser.set_defaults(func=commandReport)

  listingParser = commands.add_parser('listing', help='write mutants.txt')
  listingParser.add_argument('--package', required=True)
  listingParser.set_defaults(func=commandListing)

  args = parser.parse_args(argv)
  return args.func(args)


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
