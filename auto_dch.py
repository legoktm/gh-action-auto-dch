#!/usr/bin/env python3
"""
Copyright 2020, 2024 Kunal Mehta <legoktm@debian.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import datetime
import os
import re
import subprocess


def is_release() -> bool:
    return os.environ.get('GITHUB_REF', '').startswith('refs/tags/')


def base_version() -> str:
    """Base version for new changelog entry"""
    if is_release():
        # Tag, use that as the version string
        return os.environ['GITHUB_REF'].split('/', 3)[2]
    # Get version from meson config
    if os.path.exists('meson.build'):
        with open('meson.build') as f:
            meson = f.read()
        # XXX: hopefully this is good enough
        search = re.search(r"version : '(.*?)',", meson)
        if search:
            return search.group(1)
    # Get version from kiwix-desktop.pro
    # FIXME: Use some non-Kiwix specific method for doing this
    if os.path.exists('kiwix-desktop.pro'):
        with open('kiwix-desktop.pro') as f:
            pro = f.read()
        search = re.search(r'VERSION="(.*?)"', pro)
        if search:
            return search.group(1)
    # Get version from debian/changelog
    try:
        version = subprocess.check_output(
            ['dpkg-parsechangelog', '-S', 'version']).strip().decode()
        return version.split('~')[0]
    except subprocess.CalledProcessError:
        pass
    # Fallback to zero
    return '0.0.0'


def git_version() -> str:
    unix = subprocess.check_output(
        ['git', 'log', '--format=%ct', '-n1']).strip().decode()
    dt = datetime.datetime.fromtimestamp(int(unix)).strftime('%Y%m%d%H%M')
    sha1 = subprocess.check_output(
        ['git', 'log', '--format=%h', '-n1']).strip().decode()
    # Timestamp first so versions are always increasing, then commit sha1
    return f'git{dt}.{sha1}'


def get_distro() -> str:
    env = os.environ['INPUT_DISTRO']
    # If it starts with "debian-" or "ubuntu-" strip that
    if env.startswith(('debian-', 'ubuntu-')):
        env = env.split('-', 1)[1]
    return env


def main():
    version = base_version()
    if not is_release():
        # Add git info to version
        version += '+' + git_version()
    distro = get_distro()
    # Always append distro info
    version += f'~{distro}'
    print(f'New version: {version}')
    subprocess.check_call([
        'dch',
        '--newversion', version,
        '--distribution', distro,
        'New automated build'
    ], env={
        'DEBEMAIL': os.environ['INPUT_EMAIL'],
        'DEBFULLNAME': os.environ['INPUT_FULLNAME']
    })
    subprocess.check_call([
        'git',
        "-c", f"user.name={os.environ['INPUT_FULLNAME']}",
        "-c", f"user.email={os.environ['INPUT_EMAIL']}",
        'commit', '-a', '-m', 'New automated build'
    ])


if __name__ == '__main__':
    main()
