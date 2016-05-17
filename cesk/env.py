from collections import namedtuple
from cesk.control import Variable
from cesk.store import Cell

class Env:

    def __init__(self, bindings, outer_scope=None):
        self.bindings = bindings
        self.outer_scope = outer_scope

    def __getitem__(self, key):
        if key in self.bindings:
            return self.bindings[key]
        if self.outer_scope is None:
            raise NameError('name %s is not defined' % key)
        return self.outer_scope[key]

    def updated(self, bindings):
        return Env(bindings, self)

Closure = namedtuple('Closure', ['lambda_', 'env'])


def default_env():
    env = {
        'print': print,
        'sum': sum,
        '-': lambda x,y: x - y,
        '>': lambda x,y: x > y,
        '==': lambda x,y: x == y,
        '*': lambda x,y: x*y,
    }
    return Env({
        Variable(name): Cell(val) for name, val in env.items()
    })
