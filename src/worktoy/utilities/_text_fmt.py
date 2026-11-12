"""
The 'textFmt' function collapses whitespace in multi-line string literals.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import os


def textFmt(*args, **kwargs) -> str:
  """Collapse whitespace and honor explicit '<br>'/'<tab>' tokens.

  Joins 'args' with single spaces, replaces any run of
  whitespace (including embedded newlines from triple-quoted
  literals) with a single space, drops the space on either side
  of a '<br>', then expands '<br>' to a newline and '<tab>' to
  one indentation step.

  The whole text is treated alike, a value written into it before the
  call included: 'textFmt(spec % value)' collapses the whitespace
  inside 'value' and expands a '<br>' or '<tab>' found in it. Every
  exception and warning in 'worktoy.waitaminute' words its message
  that way, so a value quoted in a message is shown tidied, not as it
  is. The texts '{{NEWLINE}}' and '{{TAB}}' are reserved: they stand
  in for the two tokens while the whitespace is collapsed, and a text
  that already holds them has them replaced as the tokens are.

  Parameters
  ----------
  *args : Any
      Strings to format. Non-string arguments are converted via
      'str(arg)'.
  **kwargs
      newLineToken : str, optional
          Token marking a desired line break. Defaults to '<br>'.
      tabToken : str, optional
          Token marking a desired indent. Defaults to '<tab>'.
      newLineSymbol : str, optional
          Replacement for 'newLineToken' in the output. Defaults
          to 'os.linesep'.
      indentSymbol : str, optional
          Replacement for 'tabToken' in the output. Defaults to
          two spaces.

  Returns
  -------
  str
      The formatted string. Empty if no non-empty arguments were
      provided.

  Warns
  -----
  RedundantKeyword
      If a keyword other than the four above is given, such as a
      misspelled one. The keyword is not read.

  Examples
  --------
  >>> textFmt('many    spaces   here')
  'many spaces here'
  >>> print(textFmt('paragraph<br><tab>indented line'))
  paragraph
    indented line
  """
  options = ('newLineToken', 'tabToken', 'newLineSymbol', 'indentSymbol')
  for key in kwargs:
    if key not in options:
      from ..waitaminute import RedundantKeyword
      RedundantKeyword(textFmt, key, *options).warn()
  if not args:
    return ''
  words = []
  for arg in args:
    if isinstance(arg, str):
      if arg:
        words.append(arg)
    else:
      words.append(str(arg))
  if not words:
    return ''
  #  Specify tokens and symbols
  nLIn = kwargs.get('newLineToken', '<br>')
  tabIn = kwargs.get('tabToken', '<tab>')
  newTemp = '{{NEWLINE}}'
  tabTemp = '{{TAB}}'
  nLOut = kwargs.get('newLineSymbol', os.linesep)
  tabOut = kwargs.get('indentSymbol', '  ')
  #  Replace tokens with temporary symbols
  parts = [a.replace(nLIn, newTemp).replace(tabIn, tabTemp) for a in words]
  #  Join the parts into a single string
  text = ' '.join(str(part) for part in parts)
  #  Replace multiple spaces with a single space
  text = ' '.join(text.split())
  #  A space next to a line break belongs to neither line
  text = text.replace(' %s' % newTemp, newTemp)
  text = text.replace('%s ' % newTemp, newTemp)
  #  Replace newlines and tabs with the appropriate symbols
  return text.replace(newTemp, nLOut).replace(tabTemp, tabOut)
