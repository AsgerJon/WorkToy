# Security Policy

## Supported Versions

As this project is in a pre-release state, we are not currently offering
official support for any versions. However, we welcome contributions and
reports on security issues.

## Reporting a Vulnerability

Anyone finding bugs or security vulnerabilities is invited and encouraged
to submit an [issue](https://github.com/AsgerJon/WorkToy/issues). Include
as much information as possible, including steps to reproduce the issue,
potential impact, and any suggestions for solutions.

For security vulnerabilities that require immediate attention, please also
email [asgerjon2@gmail.com](mailto:asgerjon2@gmail.com). In your report,
prioritize speed and detail; you may disregard the normal guidelines for
reporting issues at your discretion.

### Immediate Escalation for Critical Vulnerabilities

If you do not receive a response promptly or you believe the issue 
requires more urgent attention, please contact:

- **CERT/CC (Computer Emergency Response Team/Coordination Center)** or
  your local equivalent. These organizations are equipped to handle severe
  security issues with the necessary urgency and confidentiality.

We encourage responsible disclosure within a timeframe that you deem
reasonable under the circumstances. We appreciate your efforts in
reporting issues responsibly and will do our best to acknowledge your
contributions.

## Prohibited Features
The following features are *banned* completely without exception:
- `exec`
- `eval`
- `__import__`
- `os.exec*`

Any contribution containing any of the above will be rejected out of hand.
These are not safe for production code, development code, testing code
or any code.

When importing `os` it must be imported canonically.
Examples of allowed usage
```python
import os
import os  # Comment is allowed, but that nothing else
```
Examples of disallowed usage:
```python
from os import system as print
from os import _exit as open
from os import popen as borrowChecker  # No we will not rewrite!
from os import fork as panic
from os import *  # Right to jail, right away!
```
