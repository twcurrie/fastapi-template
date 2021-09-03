def contains_phi(cls):
    """
    This method overwrites the built-in `__repr__` function provided
    by the schemas to obfuscate all raw data stored within the class.

    Any schema that is directly accessed by a method should use this
    decorator if it contains PHI.

    NOTE: Sentry uses the `__repr__` method when serializing events.
    """

    def __repr__(self):
        return f"{self.__class__.__name__}(***)"

    setattr(cls, "__repr__", __repr__)
    return cls
