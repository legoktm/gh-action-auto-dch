#!/usr/bin/env python3
"""
Copyright 2020 Kunal Mehta <legoktm@member.fsf.org>

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


def base_version():
    """Base version for new changelog entry"""
    if 'NEW_VERSION' in os.environ:
        return os.environ['NEW_VERSION']
    if os.path.exists('meson.build'):
        with open('meson.build') as f:
            meson = f.read()
        # XXX: hopefully this is good enough
        search = re.search(r"version : '(.*?)',", meson)
        if search:
            return search.group(1)
    try:
        version = subprocess.check_output(['dpkg-parsechangelog', '-S', 'version']).strip().decode()
        return version.split('~')[0]
    except subprocess.CalledProcessError:
        pass
    return '0.0.0'


def git_version():
    unix = subprocess.check_output(['git', 'log', '--format=%ct', '-n1']).strip().decode()
    dt = datetime.datetime.fromtimestamp(int(unix)).strftime('%Y%m%d%H%M')
    sha1 = subprocess.check_output(['git', 'log', '--format=%h', '-n1']).strip().decode()
    # Timestamp first so versions are always increasing, then commit sha1
    return f'~git{dt}.{sha1}'


def main():
    new_version = '{}{}'.format(base_version(), git_version())
    subprocess.check_call([
        'dch',
        '--newversion', new_version,
        '--distribution', os.getenv('INPUT_DISTRO'),
        'New automated build'
    ], env={
        'DEBEMAIL': os.getenv('INPUT_EMAIL'),
        'DEBFULLNAME': os.getenv('INPUT_FULLNAME')
    })
    subprocess.check_call(['git', 'commit', '-a', '-m', 'New automated build'])


if __name__ == '__main__':
    main()

