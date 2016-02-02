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


def test_wrapped_method():
    # method wrapping should work the same as function wrapping,
    # so this only does a minimum of sanity checks
    class Foo(object):
        @kwargify
        def bar(self, x, y, z):
            return x, y, z

    f = Foo()
    args = 1, 2, 3

    # method fails correctly with incorrect args, just like a function does
    with pytest.raises(TypeError):
        f.bar(**dict(zip(('x', 'y'), args)))

    # This should not explode (self is handled correctly)
    ret = f.bar(**dict(zip(('x', 'y', 'z'), args)))

    # Values should be returned in the same way that they were given
    assert ret == args


def test_wrapped():
    # double check that the function wrapper does its job
    def f():
        """doctring!"""
        pass
    f.custom_attr = True

    wrapped_f = kwargify(f)
    # __wrapped__ should be set
    assert wrapped_f.__wrapped__ is f
    # dunder attrs should be copied over
    assert wrapped_f.__doc__ == f.__doc__
    # any public attrs on the wrapped func should be available
    assert wrapped_f.custom_attr


def test_wrap_method():
    """Tst whether wrapping already existing method works."""
    class A(object):
        def a(self):
            return True

        def b(self, a, b):
            return locals()

        def c(self, a, b=None):
            return locals()

    a = A()
    k_a = kwargify(a.a)
    k_b = kwargify(a.b)
    k_c = kwargify(a.c)

    # Plain function
    assert k_a()

    # Without nonrequired parameters
    with pytest.raises(TypeError):
        k_b()

    result = k_b(1, 2)
    assert result["a"] == 1
    assert result["b"] == 2

    # With nonrequired params
    with pytest.raises(TypeError):
        k_c()

    result_1 = k_c(1, 2)
    result_2 = k_c(1)
    assert result_1["a"] == result_2["a"] == 1
    assert result_1["b"] == 2
    assert result_2["b"] is None


def test_wrap_class_constructor():
    class A(object):
        def __init__(self, a, b=None):
            self.a = a
            self.b = b

    cons = kwargify(A)
    a = cons(a=1)
    assert a.a == 1
    assert a.b is None
