"""
This script maintains 'token_stats.json', the ledger of how many tokens
Claude Code has spent on this repository over time, and which
'token_stamp.py' reads to render the README badge.

The ledger holds a 'cumulative' grand total and a 'releases' list, one
entry per time this script was run, each carrying a UTC timestamp, the
tokens spent since the previous entry ('periodTokens'), and the running
cumulative. The very first run seeds the ledger by counting every token to
date.

Counting reads the local Claude Code session transcripts, which record a
token 'usage' object and a UTC 'timestamp' on every assistant message.
Claude Code stores these per project under
'~/.claude/projects/<encoded-path>', where the encoded path is the
repository's absolute path with each separator replaced by a dash. Only
messages newer than the previous ledger entry's timestamp count toward the
next period, so the cumulative accumulates deltas and survives later
pruning of old transcripts.

This data lives only on the machine that ran the sessions, so the count
cannot be produced inside CI. The intended flow is local: run this script
before cutting a release to advance 'token_stats.json', commit the change,
and let the release workflow stamp the badge from it. The transcript
directory may be given as the first argument to override the derived
default.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
import os
import json
from datetime import datetime, timezone

STATS_FILE = 'token_stats.json'
_TOKEN_KEYS = (
    'input_tokens',
    'cache_creation_input_tokens',
    'cache_read_input_tokens',
    'output_tokens',
)


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
  The ledger file is not required, since the first run creates it.

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


def _defaultTranscriptDir() -> str:
  """
  This function derives the Claude Code transcript directory for this
  repository from its absolute path, using the dash-encoding Claude Code
  applies to the project path.

  Returns
  -------
  str
    The absolute path to the derived transcript directory.
  """
  encoded = str.replace(_root(), os.sep, '-')
  return os.path.join(os.path.expanduser('~'), '.claude', 'projects', encoded)


def _transcriptFiles(transcriptDir: str) -> list[str]:
  """
  This function collects every '.jsonl' transcript file beneath
  'transcriptDir', walking nested session directories.

  Parameters
  ----------
  transcriptDir : str
    The absolute path to the transcript directory.

  Returns
  -------
  list[str]
    The absolute paths of the transcript files, sorted for stable output.
  """
  out = []
  for dirPath, _, fileNames in os.walk(transcriptDir):
    for fileName in fileNames:
      if str.endswith(fileName, '.jsonl'):
        out.append(os.path.join(dirPath, fileName))
  return sorted(out)


def _readText(path: str) -> str:
  """
  This function reads and returns the full text of the file at 'path'.

  Parameters
  ----------
  path : str
    The absolute path to the file to read.

  Returns
  -------
  str
    The file contents.
  """
  f = None
  try:
    f = open(path, 'r', encoding='utf-8', errors='ignore')
  except Exception as exception:
    raise exception
  else:
    return f.read()
  finally:
    try:
      f.close()  # noqa: F821
    except AttributeError:
      pass


def _writeText(path: str, text: str) -> None:
  """
  This function writes 'text' to the file at 'path'.

  Parameters
  ----------
  path : str
    The absolute path to the file to write.
  text : str
    The text to write.
  """
  f = None
  try:
    f = open(path, 'w', encoding='utf-8')
  except Exception as exception:
    raise exception
  else:
    f.write(text)
  finally:
    try:
      f.close()  # noqa: F821
    except AttributeError:
      pass


def _loadStats() -> dict:
  """
  This function loads the ledger from 'token_stats.json', returning a fresh
  empty ledger when the file is absent.

  Returns
  -------
  dict
    The ledger, with 'cumulative' and 'releases' keys.
  """
  statsPath = os.path.join(_here(), STATS_FILE)
  if not os.path.isfile(statsPath):
    return dict(cumulative=0, releases=[])
  stats = json.loads(_readText(statsPath))
  stats.setdefault('cumulative', 0)
  stats.setdefault('releases', [])
  return stats


def _writeStats(stats: dict) -> None:
  """
  This function writes the ledger to 'token_stats.json', pretty-printed
  with a trailing newline.

  Parameters
  ----------
  stats : dict
    The ledger to write.
  """
  statsPath = os.path.join(_here(), STATS_FILE)
  _writeText(statsPath, '%s\n' % json.dumps(stats, indent=2))


def _nowStamp() -> str:
  """
  This function returns the current UTC time formatted to match the
  transcript timestamps, so the two compare lexicographically.

  Returns
  -------
  str
    The current UTC time, for example '2026-06-14T10:00:00.000000Z'.
  """
  return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def countSince(transcriptDir: str, sinceTimestamp: str = None) -> int:
  """
  This function sums every token type across all transcript messages newer
  than 'sinceTimestamp'. With no timestamp, every message counts.

  Parameters
  ----------
  transcriptDir : str
    The absolute path to the transcript directory.
  sinceTimestamp : str, optional
    The UTC timestamp below which messages are ignored. None counts all.

  Returns
  -------
  int
    The grand total of tokens spent in the window.
  """
  total = 0
  for path in _transcriptFiles(transcriptDir):
    for line in str.split(_readText(path), '\n'):
      if '"usage"' not in line:
        continue
      try:
        record = json.loads(line)
      except ValueError:
        continue
      if not isinstance(record, dict):
        continue
      if sinceTimestamp is not None:
        stamp = record.get('timestamp')
        if not isinstance(stamp, str) or stamp <= sinceTimestamp:
          continue
      message = record.get('message')
      usage = message.get('usage') if isinstance(message, dict) else None
      if not isinstance(usage, dict):
        usage = record.get('usage')
      if not isinstance(usage, dict):
        continue
      for key in _TOKEN_KEYS:
        total += usage.get(key, 0) or 0
  return total


def main(*args: str) -> int:
  """
  This is the main function of the script. The optional first argument
  overrides the derived transcript directory. It counts the tokens spent
  since the last ledger entry, appends a new entry advancing the
  cumulative, and writes the ledger. It returns 0 on success, and a
  non-zero integer on failure.

  Parameters
  ----------
  *args : str
    The command-line arguments passed to the script, excluding the script
    name. The optional first argument is the transcript directory.

  Returns
  -------
  int
    0 on success, and a non-zero integer on failure. Possible failure
    codes:
    - 1: More than one argument provided.
    - 2: The transcript directory does not exist.
    - 3: Could not resolve the repository root.
    - 4: Exception raised while counting or writing.
  """
  if len(args) > 1:
    print('Usage: python bin/release_tooling/token_count.py [TRANSCRIPT_DIR]')
    return 1
  if _badLocation():
    print('Could not validate location of this script!')
    return 3
  transcriptDir = args[0] if args else _defaultTranscriptDir()
  if not os.path.isdir(transcriptDir):
    infoSpec = """Transcript directory not found: '%s'. Pass the directory
    explicitly as the first argument."""
    print(str.join(' ', str.split(infoSpec % transcriptDir)))
    return 2
  try:
    stats = _loadStats()
    releases = stats['releases']
    sinceTimestamp = releases[-1]['timestamp'] if releases else None
    lastCumulative = releases[-1]['cumulative'] if releases else 0
    periodTokens = countSince(transcriptDir, sinceTimestamp)
    cumulative = lastCumulative + periodTokens
    releases.append(dict(
        timestamp=_nowStamp(),
        periodTokens=periodTokens,
        cumulative=cumulative,
    ))
    stats['cumulative'] = cumulative
    _writeStats(stats)
  except Exception as exception:
    print(exception)
    return 4
  print('period tokens (since last entry): %d' % periodTokens)
  print('cumulative total:                 %d' % cumulative)
  print('ledger entries:                   %d' % len(releases))
  return 0


if __name__ == '__main__':
  sys.exit(main(*sys.argv[1:]))
