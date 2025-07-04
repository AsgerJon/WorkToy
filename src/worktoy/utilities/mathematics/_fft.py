"""
The 'fft' function implements the Fast Fourier Transform.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import pi, cos, sin
from .. import textFmt, maybe

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, Union, TypeAlias

  Signal: TypeAlias = tuple[Union[float, complex], ...]


def fft(signal: Signal, N: int = None) -> Signal:
  """The 'fft' function implements the Fast Fourier Transform."""
  N = maybe(N, len(signal))
  if N == 1:
    return signal
  if N & (N - 1):
    infoSpec = """The 'fft' function requires signals of length that is a 
    power of two, but received signal of length: '%d'!"""
    info = infoSpec % N
    raise ValueError(textFmt(info))

  evens = fft(signal[0::2])
  odds = fft(signal[1::2])

  out = [complex() for _ in range(N)]

  for k in range(N // 2):
    angle = -2 * pi * k / N
    twiddle = cos(angle) + sin(angle) * 1j
    out[k] = evens[k] + twiddle * odds[k]
    out[k + N // 2] = evens[k] - twiddle * odds[k]

  if N == len(signal):
    return (*[arg / N for arg in out],)
  return (*out,)
