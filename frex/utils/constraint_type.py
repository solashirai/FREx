from enum import Enum


class ConstraintType(Enum):
    """
    ConstraintType is a callable Enum for use in the integer programming solver.
    """

    @staticmethod
    def __eq(x, y):
        return x == y

    @staticmethod
    def __leq(x, y):
        return x <= y

    @staticmethod
    def __geq(x, y):
        return x >= y

    EQ = __eq
    LEQ = __leq
    GEQ = __geq

    def __call__(self, *args):
        return self.value(*args)
