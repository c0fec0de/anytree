# Contribute

## Branches

* `2.x.x` main line for `2.x.x`
* `3.x.x` main line for `3.x.x`
    * documentation links refer to `3.x.x`
    * 2.x.x can be merged to 3.x.x
* `main`
    * 2.x.x can be merged to main

## Testing

### Create Environment

Run these commands just the first time:

```bash
# Ensure python3 is installed
python3 -m venv .venv
source .venv/bin/activate
pip install tox "poetry>=1.4" "crashtest==0.4.1"
```

### Enter Environment

Run this command once you open a new shell:

```bash
source .venv/bin/activate
```

### Test Your Changes

```bash
# test
tox
```

### Release

```bash
# Update 3.x.x
git checkout 3.x.x
git pull origin 2.x.x
git push origin 3.x.x

prev_version=$(poetry version -s)

# Version Bump
poetry version minor
# OR
poetry version patch

# Commit, Tag and Push
version=$(poetry version -s)

sed "s/$prev_version/$version/g" -i anytree/__init__.py

git commit -m"version bump to ${version}" pyproject.toml anytree/__init__.py
git tag "${version}" -m "Release ${version}"
git push
git push --tags

# Update main
git checkout main
git pull origin 2.x.x
git push origin main

# Publishing is handled by CI
```
