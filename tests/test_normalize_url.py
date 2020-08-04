#!/usr/bin/env python

"""Tests for `recrawler` package."""

import pytest


from recrawler.containers import normalize_url


def test_normalize():
    assert normalize_url("http://ruslan.rv.ua/python-starter/") == "http://ruslan.rv.ua/python-starter"


def test_something():
    return True
