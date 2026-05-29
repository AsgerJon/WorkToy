# yeetDirectory (archived)

Pulled from `worktoy.work_io` before the 1.0 release.

## Why

`yeetDirectory` was documented as 'effectively the same as rm -rf', but
it used `os.path.isdir(itemPath)`, which follows symlinks, and then
recursed into the result. A symlink sitting inside the target directory
and pointing somewhere outside it caused the contents of that outside
location to be deleted, after which the function died with
`NotADirectoryError` trying to `os.rmdir` the dangling link. Real
`rm -rf` removes the link itself and never recurses through it.

Confirmed repro: a `target/` holding only a symlink to an external
`victim/` directory lost `victim/`'s files when `yeetDirectory(target)`
ran. That is silent data loss outside the named directory, which is the
worst failure mode for a deletion helper, so the function was removed
rather than shipped at 1.0.

## Resurrecting

If reinstated, fix the traversal first: test `os.path.islink` before
recursing (remove the link with `os.remove`, do not follow it), or use
`os.scandir` with `entry.is_dir(follow_symlinks=False)`, or just delegate
to `shutil.rmtree`. Then move `_yeet_directory.py` back to
`src/worktoy/work_io/`, restore the import and `__all__` entry in
`work_io/__init__.py`, and move `test_yeet_directory.py` back to
`tests/test_work_io/`.
