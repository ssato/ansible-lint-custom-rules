# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=inherit-non-class
"""Common utility functios and classes - datatypes.
"""
import typing


class SubData(typing.NamedTuple):
    """A namedtuple object keep environment variables and configs.
    """
    conf: typing.Dict[str, typing.Any]
    env: typing.Dict[str, str]

# vim:sw=4:ts=4:et:
