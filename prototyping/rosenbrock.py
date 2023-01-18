import numpy as np
from pyomo.environ import *
model = ConcreteModel()
model.x1 = Var(initialize=0, bounds=(-10,10))
model.x2 = Var(initialize=0, bounds=(-10,10))
model.t = Var(initialize=0, bounds=(-2,2))
# if suffix is required in IPOPT but no suffix is given here, IPOPT will report an error.
model.homotopy_begin=Suffix(direction=Suffix.EXPORT, datatype=Suffix.FLOAT)
model.homotopy_begin.set_value(model.x1, 1)
model.homotopy_begin.set_value(model.x2, 2)
model.homotopy_begin.set_value(model.t, 3)

def obj(m):
    # return (1 - m.x1) ** 2 + 5 * (m.x2  - m.x1 ** 2) ** 2 + m.t*m.t -m.t*m.t
    return (1-m.x1)**2+5*(m.x2+m.t-m.x1**2)**2
model.obj = Objective(rule=obj)
# def con1(m):
#     return m.t*(2*m.x1**3+2*m.x1*m.x2-21*m.x1+m.x2**2-7)+(1-m.t)*(m.x1-2)==0
# model.con1 = Constraint(rule=con1)
# def con2(m):
#     return m.t*(m.x1**2+2*m.x1*m.x2+2*m.x2**3+13*m.x2-11)+(1-m.t)*(m.x2-2)==0
# model.con2 = Constraint(rule=con2)
# model.obj = Objective(expr=1)
solver = SolverFactory("ipopt", executable=r"/usr/local/bin/ipopt") #

import os
new_lib = '/usr/local/lib'
os.environ['LD_LIBRARY_PATH']=new_lib

result = solver.solve(model, tee=True)
model.display("result.txt")

