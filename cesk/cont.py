from collections import namedtuple

class Cont: pass
class HaltCont(Cont, namedtuple('Haltcont', [])): pass
class LetCont(Cont, namedtuple('LetCont', ['var', 'body', 'env', 'cont'])): pass
