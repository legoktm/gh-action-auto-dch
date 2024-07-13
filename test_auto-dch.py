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

import os

import pytest

import auto_dch


@pytest.mark.parametrize('value,expected', (
    ('refs/heads/main', False),
    ('refs/tags/1.0.0', True),
    ('', False),
))
def test_is_release(value, expected):
    os.environ['GITHUB_REF'] = value
    assert auto_dch.is_release() is expected


@pytest.mark.parametrize('value,expected', (
    ('foobar', 'foobar'),
    ('buster', 'buster'),
    ('ubuntu-focal', 'focal'),
    ('debian-stretch', 'stretch'),
))
def test_get_distro(value, expected):
    os.environ['INPUT_DISTRO'] = value
    assert auto_dch.get_distro() == expected
