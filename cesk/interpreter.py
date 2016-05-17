from cesk.control import *
from cesk.env import *
from cesk.cont import *

Cesk = namedtuple('Cesk', ['control', 'env', 'cont'])

def eval(control):
    cesk = Cesk(control, default_env(), HaltCont())
    while cesk is not None:
        cesk = step(*cesk)


def step(control, env, cont):

    if isinstance(control, Atomic):
        result = eval_atomic(control, env)
        return apply_cont(cont, result)

    if isinstance(control, Call):
        func = eval_atomic(control.func, env)
        args = [eval_atomic(arg, env) for arg in control.args]
        return apply_func(func, args, cont)

    if isinstance(control, If):
        if eval_atomic(control.cond, env):
            return Cesk(control.true, env, cont)
        else:
            return Cesk(control.false, env, cont)

    if isinstance(control, Set):
        expr = eval_atomic(control.expr, env)
        env[control.var] = expr
        return apply_cont(cont, None)

    if isinstance(control, Let):
        cont = LetCont(control.var, control.body, env, cont)
        return Cesk(control.expr, env, cont)

    if isinstance(control, LetRec):
        bindings = {}
        for var, expr in control.bindings:
            bindings[var] = None
        env = env.updated(bindings)
        for var, expr in control.bindings:
            env[var] = eval_atomic(expr, env)
        return Cesk(control.body, env, cont)

    if isinstance(control, CallCC):
        func = eval_atomic(control.func, env)
        return apply_func(func, [cont], cont)

    assert(not isinstance(control, Expr))
    raise ValueError('%s is not an expression' % control)


def eval_atomic(atomic, env):

    if isinstance(atomic, Lambda):
        return Closure(atomic, env)

    if isinstance(atomic, Variable):
        return env[atomic]

    if isinstance(atomic, (int, bool, str, list, type(None))):
        return atomic

    assert(not isisinstance(atomic, Atomic))
    raise ValueError("%s is not an atomic value" % atomic)


def apply_func(func, args, cont):
    if isinstance(func, Closure):
        if len(func.lambda_.args) != len(args):
            raise TypeError(
                '%s takes at exactly %s arguments (%s given)' %
                (func.lambda_, len(func.lambda_.args), len(args)))

        bindings = {}
        for var, val in zip(func.lambda_.args, args):
            bindings[var] = val
        env = func.env.updated(bindings)
        return Cesk(func.lambda_.body, env, cont)

    if hasattr(func, '__call__'):
        return apply_cont(cont, func(*args))

    raise ValueError('%s is not a function' % func)


def apply_cont(cont, val):
    if isinstance(cont, LetCont):
        env = cont.env.updated({cont.var: val})
        return Cesk(cont.body, env, cont.cont)

    if isinstance(cont, HaltCont):
        return

    assert(not isinstance(cont, Cont))
    raise ValueError('%s is not a continuation' % cont)
