fordpass-python release process (performed by CODEOWNERS)
===

Version bumping is done using `bump-my-version`.

    bump-my-version bump patch --dry-run --verbose
    bump-my-version bump major|minor|patch
    git push; git push --tags

bump-my-version:
- Would prepare Git commit
- Would add changes in file 'CHANGELOG.md' to Git
- Would add changes in file 'pyproject.toml' to Git
- Would add changes in file 'fordpass/__init__.py' to Git
- Would commit to Git with message 'Bump version: `CURRENT_VERSION` → `NEW_VERSION`
- Would tag 'v1.0.1' with message 'Bump version: `CURRENT_VERSION` → `NEW_VERSION` in Git

and `git push; git push --tags`, will push these changes to remote.
