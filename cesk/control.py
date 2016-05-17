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
Atomic.register(type(None))
Atomic.register(int)
Atomic.register(bool)
Atomic.register(str)
Atomic.register(list)

class Call(Expr, namedtuple('Call', ['func', 'args'])): pass
class If(Expr, namedtuple('If', ['cond', 'true', 'false'])): pass
class Set(Expr, namedtuple('Set', ['var', 'expr'])): pass
class Let(Expr, namedtuple('Let', ['var', 'expr', 'body'])): pass
class CallCC(Expr, namedtuple('CallCC', ['func'])): pass
class LetRec(Expr, namedtuple('LetRec', ['bindings', 'body'])): pass
