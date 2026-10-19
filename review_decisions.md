# Decisions reviewed:

## core

### C2:

Asger implemented a fix himself, please verify.

### C3:

Have `AttriBox.__set_name__` refuse a second box on the same owner whose
storage name is already taken.

### C6:

Implement your stated recommendation

### C8:

Document the behaviour per your recommendation

### D2:

Expand `_refuseMethodKinds` to also refuse objects that lack `__call__`.

### D10:

Implement your stated recommendation

### D11:

Implement your stated recommendation. Would this fix the issue where
someone tries to set a new `Dispatcher` with `setattr`?

### D14:

Implement option (a) in your recommendation

### E2:

Implement your stated recommendation.

### E4:

Implement your stated recommendation.

### E7:

Implement your suggestion of unwrapping `__func__` for bound methods as
in `hookSetName`.

### M2:

Query: The vanilla Python behavour treats this as a normal attribute
assignment, so it just keeps the later one. Could we do the same here?

### M4:

Implement your stated recommendation.

### M5:

Add your suggested note to the documentation.

### M8:

Add your suggested note to the documentation.

### X1:

This seems similar to D11. Implement your stated recommendation.

### X2:

Suggestion: when a decorator in the descriptor system receives a nameless
function, for example a lambda, is it feasible to have an automatically
generated name assigned to it and then wrap the lambda in a proper
function with that name?

### X3:

Place a note in documentation that pickling of certain components in
`worktoy` may lead to undefined behaviour.

### X4:

Implement the ability to restore `THIS` per your recommendation.

### S1:

Disregard. Is a work in progress.

### S2:

Update stale documentation to reflect the current state of affairs.

### S3:

The annotation related ones are because of the changes made to
annotations in 3.14. Before removing, double check that they are unused.

I am unable to recollect the purpose of `__global_scope__`.

### S4:

Because of the presense of the other phases, `getItemPhase` would be
expected to exist. Similar to the existence of both `preGet` and
`postGet`, whose utility seems marginal at best, but whose presence would
be expected.

### S6:

Soften the language discouraging overriding the mentioned methods.
Include references to exceptions present.

### S7:

Please expect the workflows at /.github/workflows and advice further.
