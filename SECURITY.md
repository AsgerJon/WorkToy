# Security Policy

## Supported Versions

worktoy is currently in 1.0 release-candidate. Security fixes
land in the next RC; please upgrade to the latest RC before
reporting. Once 1.0 ships, fixes will be issued against the
1.x line.

## Reporting a Vulnerability

Do not open a public issue. Report privately through one of:

- **GitHub Private Vulnerability Reporting (preferred)**:
  open the
  [Security tab](https://github.com/AsgerJon/WorkToy/security)
  and click "Report a vulnerability".
- **Email**: asgerjon2@gmail.com.

A minimal reproducer and the affected version do the most to
get a fix out quickly.

## Security Posture

`src/worktoy/` uses `import os` and `import sys` only as
needed for filesystem and module-lookup work. The dynamic-
execution builtins `exec`, `eval`, and `__import__` are not
used anywhere in the package, and contributions that
introduce them will be rejected.

This is a posture statement, not a guarantee. Bugs that
expand the attack surface beyond it are exactly what this
file is for reporting.
