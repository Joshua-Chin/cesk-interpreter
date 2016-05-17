from cesk.interpreter import *

factorial = Variable('factorial')
t0 = Variable('t0')
t1 = Variable('t1')
t2 = Variable('t2')
t3 = Variable('t3')
t4 = Variable('t4')

eval(

Let(t4,
    LetRec(
        [(factorial,
            Lambda([t0],
                Let(t1, Call(Variable('=='), [t0, 0]),
                    If(t1,
                        1,
                        Let(t2, Call(Variable('-'), [t0, 1]),
                            Let(t3, Call(factorial, [t2]),
                                Call(Variable('*'), [t0, t3])))))))],
        Call(factorial, [5])
    ),
    Call(Variable('print'), [t4])
)

)
