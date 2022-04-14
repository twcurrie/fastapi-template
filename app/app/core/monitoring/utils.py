import types
from functools import wraps
from inspect import signature
from collections import OrderedDict
from typing import Any, Callable


def contains_phi(cls, override_str=False):
    """
    This method overwrites the built-in `__repr__` and `__str__` functions
    by the schemas to obfuscate raw data stored within the class.

    Any schema that is directly accessed by a method should use this
    decorator if it contains PHI.

    NOTE: Sentry uses the `__repr__` method when serializing events.

    NOTE: Exceptions leverage the `__str__` method when serializing objects.
    """

    def __repr__(self):
        return f"{self.__class__.__name__}(***)"

    def __str__(self):
        return f"{self.__class__.__name__}(***)"

    setattr(cls, "__repr__", __repr__)
    setattr(cls, "has_phi", True)
    if override_str:
        setattr(cls, "__str__", __str__)
    return cls


def handles_phi(*args, **kwargs):
    """
    This method should be applied to functions that directly handle
    primitive types that contain PHI data.  By default, it will redact
    all values, but can optionally only redact kwargs listed in the
    `sensitive_fields` parameter.

    By decorating a function handling primitives containing PHI, any
    data sent to Sentry or other monitoring platforms will not contain
    the sensitive data.
    """
    sensitive_fields = kwargs.get("sensitive_fields")

    def _phi_decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Convert fields to redacted types
            if sensitive_fields:
                # Obtain params of function to enable args and kwargs lookup
                func_params = OrderedDict(signature(func).parameters)

                redacted_args = []
                for arg in args:
                    # Extract args, these follow strict ordering.
                    param = next(iter(func_params))
                    del func_params[param]
                    redacted_args.append(
                        redact(arg) if param in sensitive_fields else arg
                    )

                redacted_kwargs = {}
                for key, value in kwargs.items():
                    # Extract kwargs, do a lookup and drop it from the dictionary after.
                    del func_params[key]
                    redacted_kwargs[key] = (
                        redact(value) if key in sensitive_fields else value
                    )

                if len(func_params) != 0:
                    # If parameters still present, ensure the function signature defaults are passed on
                    for key, value in func_params.items():
                        default = value.default
                        # NOTE: The decorator supports redaction of the default values of fields.
                        redacted_kwargs[key] = (
                            redact(default) if key in sensitive_fields else default
                        )
                return func(*redacted_args, **redacted_kwargs)

            # Convert all fields to redacted types
            return func(
                *[redact(arg) for arg in args],
                **{key: redact(value) for key, value in kwargs.items()},
            )

        return wrapper

    if len(args) == 1 and callable(args[0]):
        # This allows for the decorator to be executed without any parameters.
        return _phi_decorator(args[0])

    # This will call the decorator with parameters.
    return _phi_decorator


def redact(value: Any) -> Any:
    """
    Python builtins cannot have the `__str__`, `__repr__` methods overrides them, so this
    method creates a new class that inherits from both a class that does override them and
    the type class that the primitive is.  In this way, it ensures the methods that will
    modify, operate, or otherwise utilize the data within the 'value' can continue to leverage
    the same functions and have the same type expectations, but any request to print or view
    the raw data value will only show it as `redacted(***)`

    """
    return types.new_class(
        f"Sensitive{type(value).__name__.capitalize()}",
        bases=(contains_phi(type("BaseClass", (), {}), override_str=True), type(value)),
    )(value)
