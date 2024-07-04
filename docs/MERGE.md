# Merge requests
===
## pre-commit
### test
```shell
isort --check --diff --profile black filename
black --check --diff filename
flake8 --show-source --max-line-length=88 --exclude __init__.py,types.py --extend-ignore=W605,F811,E402,E203 filename
```
### run
```shell
isort --profile black filename
black filename
flake8 --show-source --max-line-length=88 --exclude __init__.py,types.py --extend-ignore=W605,F811,E402,E203 filename
```
## instructions
* branch from Master
* make your changes
* make sure your branch is up-to-date to the current Master
* update CHANGELOG.md under **Unreleased**, but don't change the 'unreleased' part just add a new line underneath.
```
**Unreleased**
* fixed something
* new feature
* improved existing
```