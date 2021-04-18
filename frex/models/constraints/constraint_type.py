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
    def __less(x, y):
        return x < y

    @staticmethod
    def __geq(x, y):
        return x >= y

    @staticmethod
    def __grtr(x, y):
        return x > y

    @staticmethod
    def __neq(x, y):
        return x != y

    @staticmethod
    def __am1(x, y):
        return x + y <= 1

    @staticmethod
    def __ex1(x, y):
        return x + y == 1

    EQ = __eq
    LEQ = __leq
    LESS = __less
    GEQ = __geq
    GRTR = __grtr
    NEQ = __neq
    AM1 = __am1
    EX1 = __ex1

    def __call__(self, *args):
        return self.value(*args)
