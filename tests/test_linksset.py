#!/usr/bin/env python

"""Tests for `recrawler` package."""

import pytest


from recrawler.containers import LinksSet


def test_links_set():
    u = "http://ruslan.rv.ua/python-starter/"
    s = LinksSet()
    assert len(s) == 0
    s.add(u)
    assert len(s) == 1
    s.add(u)
    assert len(s) == 1
