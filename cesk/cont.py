"""This module contains the continuation objects used by the interpreter
"""
from collections import namedtuple

__all__ = [
    'Cont',
    'HaltCont',
    'LetCont',
    'Halt',
]

class Cont: pass
class HaltCont(Cont, namedtuple('Haltcont', [])): pass
class LetCont(Cont, namedtuple('LetCont', ['var', 'body', 'env', 'cont'])): pass

class Halt(Exception): pass
