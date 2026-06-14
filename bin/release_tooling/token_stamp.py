"""
This script stamps the cumulative token-usage badge in 'README.md'. The
badge reports how many tokens Claude Code has spent building 'worktoy',
shown in a human-readable form such as '7.6B'.

The cumulative count is read from the 'cumulative' field of
'token_stats.json', the ledger maintained by 'token_count.py'. An optional
first argument overrides that source with a raw integer count, which the
release workflows can pass directly. The count is then formatted with a
'K', 'M', 'B', or 'T' suffix and written into the shields.io badge URL on
the 'README.md' line beginning with '[![Tokens]'.

The split mirrors the version tooling: 'token_count.py' measures the count
locally and advances the ledger, while this script formats and stamps the
badge during the release workflow.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
import os
import json

STATS_FILE = 'token_stats.json'

TOKENS_PREFIX = '[![Tokens]'
_BADGE_SPEC = (
    '[![Tokens](https://img.shields.io/badge/Tokens-%s-D97757)]'
    '(https://claude.com/claude-code)'
)
_UNITS = (('T', 10 ** 12), ('B', 10 ** 9), ('M', 10 ** 6), ('K', 10 ** 3),)


def _here() -> str:
  """
  This function resolves the path to the present directory containing this
  script.

  Returns
  -------
  str
    The absolute path to the present directory containing this script.
  """
  filePath: str = os.path.abspath(__file__)
  return os.path.dirname(filePath)


def _root() -> str:
  """
  This function resolves the repository root by walking up from this
  script's directory until it finds the directory holding 'pyproject.toml',
  so the script works regardless of how deeply it is nested under the root.

  Returns
  -------
  str
    The absolute path to the repository root.

  Raises
  ------
  RuntimeError
    If no ancestor directory holds 'pyproject.toml'.
  """
  current = _here()
  while current != os.path.dirname(current):
    if os.path.isfile(os.path.join(current, 'pyproject.toml')):
      return current
    current = os.path.dirname(current)
  raise RuntimeError("Could not locate the repository root!")


def _badLocation() -> int:
  """
  This function validates that the repository root can be resolved and
  carries the expected project layout.

  Returns
  -------
  int
    0 if the script is correctly located, 1 otherwise.
  """
  requiredItems = ['src', 'tests', 'README.md']
  presentItems = os.listdir(_root())
  for item in requiredItems:
    if item not in presentItems:
      break
  else:
    return 0
  return 1


def _readLines(path: str) -> list[str]:
  """
  This function reads the file at 'path' and returns its lines without
  trailing newline characters.

  Parameters
  ----------
  path : str
    The absolute path to the file to read.

  Returns
  -------
  list[str]
    The lines of the file.
  """
  f = None
  try:
    f = open(path, 'r', encoding='utf-8')
  except Exception as exception:
    raise exception
  else:
    return str.split(f.read(), '\n')
  finally:
    try:
      f.close()  # noqa: F821
    except AttributeError:
      pass


def _writeLines(path: str, lines: list[str]) -> None:
  """
  This function writes 'lines' to the file at 'path', joined by newline
  characters.

  Parameters
  ----------
  path : str
    The absolute path to the file to write.
  lines : list[str]
    The lines to write.
  """
  f = None
  try:
    f = open(path, 'w', encoding='utf-8')
  except Exception as exception:
    raise exception
  else:
    f.write(str.join('\n', lines))
  finally:
    try:
      f.close()  # noqa: F821
    except AttributeError:
      pass


def _readTokenCount() -> int:
  """
  This function reads the cumulative token count from the 'cumulative'
  field of 'token_stats.json' beside this script.

  Returns
  -------
  int
    The cumulative token count.

  Raises
  ------
  ValueError
    If the ledger holds no non-negative integer 'cumulative' field.
  """
  statsPath = os.path.join(_here(), STATS_FILE)
  stats = json.loads(str.join('\n', _readLines(statsPath)))
  return _parseCount(str(stats.get('cumulative', '')))


def _parseCount(raw: str) -> int:
  """
  This function parses a raw token count string into an integer.

  Parameters
  ----------
  raw : str
    The raw token count, a string of decimal digits.

  Returns
  -------
  int
    The parsed token count.

  Raises
  ------
  ValueError
    If 'raw' is empty or not a non-negative integer.
  """
  raw = str.strip(raw)
  if not str.isdigit(raw):
    infoSpec = """Expected a non-negative integer token count, but
    received: '%s'!"""
    raise ValueError(str.join(' ', str.split(infoSpec % raw)))
  return int(raw)


def formatTokens(count: int) -> str:
  """
  This function formats a raw token count into the human-readable label
  shown on the badge, using a 'K', 'M', 'B', or 'T' suffix. A count below
  one thousand is shown verbatim. The largest fitting unit is used, with a
  single decimal place that drops a trailing '.0'.

  Parameters
  ----------
  count : int
    The cumulative token count.

  Returns
  -------
  str
    The badge label, for example '7.6B', '950M', or '512'.
  """
  for symbol, size in _UNITS:
    if count >= size:
      text = '%.1f' % (count / size)
      if str.endswith(text, '.0'):
        text = text[:-2]
      return '%s%s' % (text, symbol)
  return '%d' % count


def _stampBadge(label: str) -> None:
  """
  This function replaces the 'README.md' line beginning with '[![Tokens]'
  with a freshly built badge carrying 'label'. A README without such a
  line is an error, since the badge is expected to already be present.

  Parameters
  ----------
  label : str
    The human-readable token label to stamp into the badge.
  """
  readmePath = os.path.join(_root(), 'README.md')
  lines = _readLines(readmePath)
  for i, line in enumerate(lines):
    if str.startswith(str.lstrip(line), TOKENS_PREFIX):
      lines[i] = _BADGE_SPEC % label
      break
  else:
    infoSpec = """Found no line starting with '%s' in 'README.md'!"""
    raise RuntimeError(infoSpec % TOKENS_PREFIX)
  _writeLines(readmePath, lines)


def main(*args: str) -> int:
  """
  This is the main function of the script. The optional first argument is a
  raw integer token count that overrides the 'TOKENS' file; with no
  argument the count is read from 'TOKENS'. It returns 0 on success, and a
  non-zero integer on failure.

  Parameters
  ----------
  *args : str
    The command-line arguments passed to the script, excluding the script
    name. The optional first argument is a raw integer token count.

  Returns
  -------
  int
    0 on success, and a non-zero integer on failure. Possible failure
    codes:
    - 1: More than one argument provided.
    - 2: The token count could not be read or parsed.
    - 3: Could not resolve the repository root.
    - 4: Exception raised while stamping the badge.
  """
  if len(args) > 1:
    print('Usage: python bin/release_tooling/token_stamp.py [TOKEN_COUNT]')
    return 1
  if _badLocation():
    print('Could not validate location of this script!')
    return 3
  try:
    count = _parseCount(args[0]) if args else _readTokenCount()
  except (ValueError, OSError) as exception:
    print(exception)
    return 2
  try:
    label = formatTokens(count)
    _stampBadge(label)
  except Exception as exception:
    print(exception)
    return 4
  else:
    print('Stamped token badge: %s' % label)
    return 0


if __name__ == '__main__':
  sys.exit(main(*sys.argv[1:]))
