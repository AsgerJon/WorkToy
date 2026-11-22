"""
The 'design.refusals' package holds what 'worktoy' refuses: the
mistakes that raise an exception where they are made, instead of
passing in silence. A refusal says that a certain mistake raises, and
names the exception it raises as of a stated version of 'worktoy'.
Which exception that is, is not promised and may change in any release.
What an exception carries once it is raised is promised by the
exception itself, in 'design.promises.waitaminute'.

A refusal may be relaxed: a later release may accept what an earlier
one refused, as a class keyword lifting a rule does, or a rule that
turned out stricter than it had to be. Relaxing a refusal is not a
deprecation. It gives no notice and waits for no major update, since
nothing that worked stops working when a mistake is no longer refused.
Nor is it a confession: no promise is taken back.

Each package of 'worktoy' has a subfolder of its own, and each file
holds the refusals that belong with the promise file of the same name.
The docstring of its class names the version its exceptions are stated
for. Each test is one refusal. Its 'with' block holds what the refusal
says, that the mistake raises, and the line after the block records the
exception raised as of that version, which is edited, with the version,
when the exception changes.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations
