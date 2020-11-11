from enum import Enum


class ConstraintType(Enum):
    """
    ConstraintType is a callable Enum for use in the integer programming solver.
    """

    @staticmethod
    def eq(x, y):
        return x == y

    @staticmethod
    def leq(x, y):
        return x <= y

    @staticmethod
    def geq(x, y):
        return x >= y

    EQ = eq
    LEQ = leq
    GEQ = geq

    def __call__(self, *args):
        return self.value(*args)
