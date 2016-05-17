from cesk.control import *
from cesk.env import *
from cesk.store import *
from cesk.cont import *

Cesk = namedtuple('Cesk', ['control', 'env', 'store', 'cont'])

def eval(control):
    cesk = Cesk(control, default_env(), Store(), HaltCont())
    while cesk is not None:
        cesk = step(*cesk)


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
        cont = LetCont(control.var, control.body, env, cont)
        return Cesk(control.expr, env, store, cont)

    if isinstance(control, LetRec):
        bindings = {}
        for var, expr in control.bindings:
            address = fresh_address(store)
            bindings[var] = address
        env = env.updated(bindings)
        for var, expr in control.bindings:
            store[env[var]] = eval_atomic(expr, env, store)
        return Cesk(control.body, env, store, cont)

    if isinstance(control, CallCC):
        func = eval_atomic(control.func, env, store)
        return apply_func(func, [cont], store, cont)

    assert(not isinstance(control, Expr))
    raise ValueError('%s is not an expression' % control)


def eval_atomic(atomic, env, store):

    if isinstance(atomic, Lambda):
        return Closure(atomic, env)

    if isinstance(atomic, Variable):
        return store[env[atomic]]

    if isinstance(atomic, (int, bool, str, list, type(None))):
        return atomic

    assert(not isisinstance(atomic, Atomic))
    raise ValueError("%s is not an atomic value" % atomic)


def apply_func(func, args, store, cont):
    if isinstance(func, Closure):
        if len(func.lambda_.args) != len(args):
            raise TypeError(
                '%s takes at exactly %s arguments (%s given)' %
                (func.lambda_, len(func.lambda_.args), len(args)))

        bindings = {}
        for var, val in zip(func.lambda_.args, args):
            address = fresh_address(store)
            bindings[var] = address
            store[address] = val
        env = func.env.updated(bindings)
        return Cesk(func.lambda_.body, env, store, cont)

    if hasattr(func, '__call__'):
        return apply_cont(cont, func(*args), store)

    raise ValueError('%s is not a function' % func)


def apply_cont(cont, val, store):
    if isinstance(cont, LetCont):
        address = fresh_address(store)
        env = cont.env.updated({cont.var: address})
        store[address] = val
        return Cesk(cont.body, env, store, cont.cont)

    if isinstance(cont, HaltCont):
        return

    assert(not isinstance(cont, Cont))
    raise ValueError('%s is not a continuation' % cont)
