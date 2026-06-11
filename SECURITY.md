# Security Policy

## Supported versions

Security fixes land on the most recent stable line. Earlier lines are
supported at the maintainer's discretion and are marked "End-of-Life"
once they stop receiving fixes. Pre-1.0 releases were alpha software and
receive nothing.

| Version | Status                |
| ------- | --------------------- |
| 1.0.x   | Supported             |
| < 1.0   | Not supported (alpha) |

## Reporting a vulnerability

Please do not report security issues publicly. Report them privately
through either:

- GitHub Private Vulnerability Reporting: the
  [Security tab](https://github.com/AsgerJon/WorkToy/security), "Report a
  vulnerability".
- Email to asgerjon2@gmail.com with `worktoy security` in the subject.

A report is most useful with a description of the issue, the steps to
reproduce it, the affected version, and the impact.

*worktoy* is maintained by one person, so there is no guaranteed
response time. Reports are taken seriously and acknowledged as soon as
is practical. Please allow a reasonable period for a fix before any
public disclosure.

## How a report is handled

When a report comes in, the issue is confirmed, fixed, and released as a
patched version on the supported line. The reporter is told when the fix
is out and is credited for it unless they would rather stay anonymous.
Please keep the details private until the fix is released, so that people
can update before the issue is public.

Good-faith research and responsible disclosure are welcome. A reporter
who acts in good faith, gives a reasonable chance to fix the issue
before going public, and does not exploit it beyond what is needed to
show that it exists, has nothing to fear from the project.

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
