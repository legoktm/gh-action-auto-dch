# GitHub Action to generate Debian changelog entries

This Action automatically generates `debian/changelog` entries based off of
Git metadata using `dch`.

## Configuration

* `fullname`: Name to be used in changelog
* `email`: Email to be used in changelog
* `distro`: Distribution to build for (e.g. buster, focal). Any `debian-` or
`ubuntu-` prefix will be stripped.

## Version scheme

If the event is a tag push, the tag name will be the version, with the
distro appended. E.g. `2.1.2~buster`.

On normal commit pushes, the base version will be read from a meson.build if
it exists, then the previous `debian/changelog` entry, otherwise falling back
to `0.0.0`. The git timestamp and hash will be appended, along with distro.
E.g. `2.1.2+git202005272117.a2e10b9~buster`.

The expectation is that the base version is from the previous release, so the
package version is <XX commits> ahead of <base version>.

## Example

```yaml
on: [push, pull_request]

jobs:
  build-deb:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        distro: [debian-buster, ubuntu-focal]
    steps:
      - uses: actions/checkout@v2

      - uses: legoktm/gh-action-auto-dch@main
        with:
          fullname: First Last
          email: firstlast@example.org
          distro: ${{ matrix.distro }}

      - uses: legoktm/gh-action-build-deb@debian-buster
        if: matrix.distro == 'debian-buster'
        name: Build package for debian-buster
        id: build-debian-buster
        with:
          args: --no-sign

      - uses: legoktm/gh-action-build-deb@ubuntu-focal
        if: matrix.distro == 'ubuntu-focal'
        name: Build package for ubuntu-focal
        id: build-ubuntu-focal
        with:
          args: --no-sign

      - uses: actions/upload-artifact@v2
        with:
          name: Packages for ${{ matrix.distro }}
          path: output
```

## Related actions

* [gh-action-build-deb](https://github.com/legoktm/gh-action-build-deb) build Debian packages.
* [gh-action-dput](https://github.com/legoktm/gh-action-dput) uploads built packages to a PPA or repository.

## License
Copyright © 2020 Kunal Mehta under the GPL, version 3 or any later version.
