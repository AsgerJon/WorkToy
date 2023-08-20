"""The importify function provides customized import functionality"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
import time
import builtins
from types import ModuleType

originalImport = builtins.__import__


def customImport(name: str,
                 gls=None,
                 lcs=None,
                 fromlist=None,
                 level=None, **kwargs) -> ModuleType:
  """Stop using star imports!"""
  if fromlist is None:
    fromlist = ()
  if level is None:
    level = 0
  if fromlist == ('*',) and name not in ['_lzma', '_bisect',
                                         'shiboken6.Shiboken']:
    here = os.path.dirname(os.path.abspath(__file__))
    lyricsPath = os.path.join(here, 'lyrics.txt')
    noobPath = os.path.join(here, 'nooberror.txt')
    with open(lyricsPath, 'r', encoding='utf-8') as f:
      lyrics = f.read().split('\n')
    with open(noobPath, 'r', encoding='utf-8') as f:
      noob = f.read()
    for lyric in lyrics:
      print(lyric)
    n00bError = type('n00bError', (Exception,), {})
    msgBase = """Only n00bs use star imports!\nFor more info:"""
    tutorial = r'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    jail = '\n\nRight to jail, right away!'
    msg = '%s\n%s\n%s\n%s' % (jail, noob, msgBase, tutorial)
    raise n00bError(msg)
  return originalImport(name, gls, lcs, fromlist, level)
