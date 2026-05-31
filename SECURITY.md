# Security Policy

## Reporting a vulnerability

Please do not report security issues through public issues. Report them
privately through either:

- GitHub Private Vulnerability Reporting: the
  [Security tab](https://github.com/AsgerJon/WorkToy/security), "Report a
  vulnerability".
- Email to asgerjon2@gmail.com with `worktoy security` in the subject.

A report is most useful with a description of the issue, the steps to
reproduce it, the affected version, and the impact.

## Scope

*worktoy* is a pure-Python library with no runtime dependencies. It opens
no sockets, starts no processes, and reads no files it is not given. The
dynamic-execution builtins `exec`, `eval`, and `__import__` are not used
in the package.

In scope is any behaviour that lets the library compromise a program using
it as documented, including faults in the class-construction machinery
(metaclasses, namespaces, and descriptors). Out of scope is anything that
requires already-hostile code in the same process, or hostile input passed
to an interface documented as trusting its caller.

## Supported versions

Pre 1.0 versions of *worktoy* should be regarded as unstable alpha
software. From 1.0 onwards, versions that no longer receive security updates
will be clearly marked as "End-of-Life".
