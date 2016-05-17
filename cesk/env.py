from collections import namedtuple
from cesk.control import Variable

class Env:

    def __init__(self, bindings, outer_scope=None):
        self.bindings = bindings
        self.outer_scope = outer_scope

    def __getitem__(self, key):
        if key in self.bindings:
            return self.bindings[key].val
        elif self.outer_scope is None:
            raise NameError('name %s is not defined' % key)
        else:
            return self.outer_scope[key]

    def __setitem__(self, key, val):
        if key in self.bindings:
            self.bindings[key].val = val
        elif self.outer_scope is None:
            self.bindings[key] = Cell(val)
        else:
            self.outer_scope[key] = val

    def updated(self, bindings):
        return Env({key:Cell(val) for key, val in bindings.items()}, self)


class Cell:

    def __init__(self, val=None):
        self.val = val

    def __repr__(self):
        return 'Cell(%s)' % self.val


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
