# -*- coding: utf-8 -*-
import pytest
from kwargify import kwargify


class TestFunctionWithNoArgs(object):
    @pytest.fixture(scope="class")
    def function(self):
        @kwargify
        def f():
            return True
        return f

    def test_no_args_given(self, function):
        function()

    @pytest.mark.xfail
    @pytest.mark.parametrize("n", range(1, 4))
    def test_args_given(self, function, n):
        function(*range(n + 1))

    def test_kwargs_passed(self, function):
        function(foo="bar")


class TestFunctionWithOnlyArgs(object):
    @pytest.fixture(scope="class")
    def function(self):
        @kwargify
        def f(a, b):
            return True
        return f

    @pytest.mark.xfail
    def test_no_args_given(self, function):
        function()

    @pytest.mark.xfail
    def test_args_given_not_enough(self, function):
        function(1)

    def test_args_given_enough(self, function):
        function(1, 2)

    @pytest.mark.xfail
    def test_only_kwargs_passed_wrong(self, function):
        function(foo="bar")

    @pytest.mark.xfail
    def test_only_kwargs_passed_not_enough(self, function):
        function(a="bar")

    def test_only_kwargs_passed(self, function):
        function(a=1, b=2)

    def test_both_passed(self, function):
        function(1, b=2)


class TestFunctionWithDefaultValues(object):
    @pytest.fixture(scope="class")
    def function(self):
        @kwargify
        def f(a, b=None):
            return locals()
        return f

    def test_pass_only_required(self, function):
        assert function(1)["b"] is None

    def test_override_default_with_arg(self, function):
        assert function(1, 2)["b"] == 2

    def test_override_default_with_kwarg(self, function):
        assert function(1, b=2)["b"] == 2


class TestKwargifyMethod(object):
    class _TestClass(object):
        def noargs(self):
            return locals()

        def onlyargs(self, a, b):
            return locals()

        def withdefault(self, a, b=None):
            return locals()

    @pytest.fixture(scope="class")
    def o(self):
        return self._TestClass()

    # No args test
    def test_no_args_given(self, o):
        kwargify(o.noargs)()

    @pytest.mark.xfail
    @pytest.mark.parametrize("n", range(1, 4))
    def test_args_given(self, o, n):
        kwargify(o.noargs)(*range(n + 1))

    def test_kwargs_passed(self, o):
        kwargify(o.noargs)(foo="bar")

    # Only args
    @pytest.mark.xfail
    def test_no_args_given_fails(self, o):
        kwargify(o.onlyargs)()

    @pytest.mark.xfail
    def test_args_given_not_enough(self, o):
        kwargify(o.onlyargs)(1)

    def test_args_given_enough(self, o):
        kwargify(o.onlyargs)(1, 2)

    @pytest.mark.xfail
    def test_only_kwargs_passed_wrong(self, o):
        kwargify(o.onlyargs)(foo="bar")

    @pytest.mark.xfail
    def test_only_kwargs_passed_not_enough(self, o):
        kwargify(o.onlyargs)(a="bar")

    def test_only_kwargs_passed(self, o):
        kwargify(o.onlyargs)(a=1, b=2)

    def test_both_passed(self, o):
        kwargify(o.onlyargs)(1, b=2)

    # Default values
    def test_pass_only_required(self, o):
        assert kwargify(o.withdefault)(1)["b"] is None

    def test_override_default_with_arg(self, o):
        assert kwargify(o.withdefault)(1, 2)["b"] == 2

    def test_override_default_with_kwarg(self, o):
        assert kwargify(o.withdefault)(1, b=2)["b"] == 2
