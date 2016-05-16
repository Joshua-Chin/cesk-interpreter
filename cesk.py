from abc import ABC
from collections import namedtuple

Cesk = namedtuple('Cesk', ['control', 'env', 'store', 'cont'])

class Expr(ABC): pass

class Atomic(Expr): pass
class Lambda(Atomic, namedtuple('Lambda', ['args', 'body'])): pass
class Variable(Atomic, namedtuple('Variable', ['name'])): pass
class Nil(Atomic, namedtuple('Nil', [])): pass
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

class Cont: pass
class HaltCont(Cont, namedtuple('Haltcont', [])): pass
class LetCont(Cont, namedtuple('LetCont', ['var', 'body', 'env', 'cont'])): pass

Closure = namedtuple('Closure', ['lambda_', 'env'])


def default_env():
    env = {
        'print': print,
        'sum': sum,
        '-': lambda x,y: x - y
        '>': lambda x,y: x > y,
        '==': lambda x,y: x == y,
    }
    return {
        Variable(name): Cell(val) for name, val in env.items()
    }

def eval(control):
    cesk = Cesk(control, default_env(), Store(), HaltCont())
    while cesk is not None:
        cesk = step(*cesk)


def eval_atomic(atomic, env, store):
    if isinstance(atomic, Lambda):
        return Closure(atomic, env)

    if isinstance(atomic, Variable):
        return store[env[atomic]]

    if isinstance(atomic, (int, bool, str, list, Nil)):
        return atomic

    assert(not isisinstance(atomic, Atomic))
    raise ValueError("%s is not an atomic value" % atomic)


def step(control, env, store, cont):
    if isinstance(control, Atomic):
        result = eval_atomic(control, env, store)
        return apply_cont(cont, result, store)

    if isinstance(control, Call):
        func = eval_atomic(control.func, env, store)
        args = [eval_atomic(arg, env, store) for arg in control.args]
        return apply_func(func, args, store, cont)

    if isinstance(control, If):
        if eval_atomic(control.cond, env, store):
            return Cesk(control.true, env, store, cont)
        else:
            return Cesk(control.false, env, store, cont)

    if isinstance(control, Set):
        expr = eval_atomic(control.expr, env, store)
        store[env[control.var]] = expr
        return apply_cont(cont, None, store)

    if isinstance(control, Let):
        cont = LetCont(control.var, control.body, store, cont)
        return Cesk(control.expr, env, store, cont)

    if isinstance(control, LetRec):
        bindings = {}
        for var, expr in control.bindings:
            address = fresh_address()
            bindings[var] = address
        env = env.updated(bindings)
        for var, expr in control.bindings:
            store[env[var]] = eval_atomic(expr, env, store)
        return Cesk(control.body, env, store, cont)

    if isinstance(control, CallCC):
        func = eval_atomic(control.func, env, store)
        return apply_func(func, [cont], env, store)

    assert(not isinstance(control, Expr))
    raise ValueError('%r is not an expression' % control)


def apply_func(func, args, store, cont):
    if isinstance(func, Closure):
        if len(closure.lambda_.args) != args:
            raise TypeError(
                '%r takes at exactly %r arguments (%s given)' %
                (closure.lambda_, len(closure.lambda_.args), len(args)))

        bindings = {}
        for var, val in zip(closure.lambda_.args, args):
            address = fresh_address(store)
            bindings[var] = address
            store[address] = var
        env = closure.env.updated(bindings)
        return Cesk(closure.lambda_.body, env, store, cont)

    if hasattr(func, '__call__'):
        return apply_cont(cont, func(*args), store)

    raise ValueError('%r is not a function' % func)


def apply_cont(cont, val, store):
    if isinstance(cont, LetCont):
        address = fresh_address(store)
        env = cont.env.updated({cont.var: address})
        store[address] = val
        return Cesk(cont.body, cont.env, store, cont.cont)

    if isinstance(cont, HaltCont):
        return

    assert(not isinstance(cont, Cont))
    raise ValueError('%r is not a continuation' % cont)


def fresh_address(store):
    return Cell(None)


Cell = namedtuple('Cell', 'val')


class Env:

    def __init__(self, bindings, outer_scope=None):
        self.bindings = bindings
        self.outer_scope = outer_scope

    def __getitem__(self, key):
        if key in self.bindings:
            return self.bindings[key]
        if self.outer_scope is None:
            raise NameError('name %r is not defined' % key)
        return self.outer_scope[key]

    def updated(self, bindings):
        return Env(bindings, self)


class Store:

    def __getitem__(self, cell):
        return cell.val

    def __setitem__(self, cell, val):
        cell.val = val
