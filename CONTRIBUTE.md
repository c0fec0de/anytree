# Contribute

## Branches

* `2.x.x` main line for 2.x.x
* `3.x.x` actual main line
    * documentation links refer to `3.x.x`
    * 2.x.x can be merged to 3.x.x
* `main`
    * documentation links refer to `latest`
    * 3.x.x can be merged to main
* `stable` main line for 2.x.x with release tags

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

# Update main
git checkout main
git pull origin 3.x.x
git push origin main

# Update release branch - currently 2.x.x
git checkout stable
git pull origin 2.x.x

prev_version=$(poetry version -s)

# Version Bump
poetry version minor
# OR
poetry version patch

# Commit, Tag and Push
version=$(poetry version -s)

sed "s/$prev_version/$version/g" -i README.rst
sed "s/$prev_version/$version/g" -i docs/index.rst

git commit -m"version bump to ${version}" pyproject.toml README.rst docs/index.rst
git tag "${version}" -m "Release ${version}"
git push
git push --tags

# Publishing is handled by CI
```
