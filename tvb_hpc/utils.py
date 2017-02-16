import os.path
import numpy as np
import pymbolic as pm
from pymbolic import parse
from pymbolic.mapper.stringifier import SimplifyingSortingStringifyMapper
from sympy.parsing.sympy_parser import parse_expr


here = os.path.dirname(os.path.abspath(__file__))
include_dir = os.path.normpath(os.path.join(here, '..', 'include'))


class NoSuchExecutable(RuntimeError):
    pass


def which(exe):
    if os.path.exists(exe):
        return exe
    for path in os.environ['PATH'].split(os.path.pathsep):
        maybe_path = os.path.join(path, exe)
        if os.path.exists(maybe_path):
            return maybe_path
    raise NoSuchExecutable(exe)



def simplify(expr):
    "Simplify pymbolic expr via SymPy."
    # TODO switch entirely to SymPy?
    parts = SimplifyingSortingStringifyMapper()(expr)
    simplified = parse_expr(parts).simplify()
    return parse(repr(simplified))


def vars(svars):
    return np.array([pm.var(var) for var in svars.split()])


def exprs(sexprs):
    exprs = []
    for expr in sexprs:
        if isinstance(expr, (int, float)):
            exprs.append(expr)
        else:
            try:
                exprs.append(pm.parse(expr))
            except Exception as exc:
                raise Exception(repr(expr))
    return np.array(exprs)