from collections import namedtuple

__all__ = [
    'Cont',
    'HaltCont',
    'LetCont',
]

class Cont: pass
class HaltCont(Cont, namedtuple('Haltcont', [])): pass
class LetCont(Cont, namedtuple('LetCont', ['var', 'body', 'env', 'cont'])): pass
