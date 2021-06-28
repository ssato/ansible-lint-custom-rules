# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Common utility test routines and classes - utilities.
"""
import pathlib
import typing


DataT = typing.Iterable[typing.Optional[pathlib.Path]]


class TData(typing.NamedTuple):
    """A namedtuple object keeps test data info."""
    datadir: pathlib.Path
    inpath: pathlib.Path
    conf: typing.Dict[str, typing.Any]
    env: typing.Dict[str, typing.Any]

# vim:sw=4:ts=4:et:
