"""
This module provides the control structures for cesk interpreter.
"""
from abc import ABC
from collections import namedtuple

__all__ = [
    'Expr',
    'Atomic',
    'Lambda',
    'Variable',
    'Call',
    'If',
    'Set',
    'Let',
    'CallCC',
    'LetRec',
]

class Expr(ABC): pass

class Atomic(Expr): pass
class Lambda(Atomic, namedtuple('Lambda', ['args', 'body'])): pass
class Variable(Atomic, namedtuple('Variable', ['name'])): pass
class Literal(Atomic): pass
Literal.register(type(None))
Literal.register(int)
Literal.register(bool)
Literal.register(str)
Literal.register(list)

class Call(Expr, namedtuple('Call', ['func', 'args'])): pass
class If(Expr, namedtuple('If', ['cond', 'true', 'false'])): pass
class Set(Expr, namedtuple('Set', ['var', 'expr'])): pass
class Let(Expr, namedtuple('Let', ['var', 'expr', 'body'])): pass
class CallCC(Expr, namedtuple('CallCC', ['func'])): pass
class LetRec(Expr, namedtuple('LetRec', ['bindings', 'body'])): pass
