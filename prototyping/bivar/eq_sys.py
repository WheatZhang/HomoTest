import numpy as np
from pyomo.environ import *
model = ConcreteModel()
model.x1 = Var(initialize=0, bounds=(-10,10))
model.x2 = Var(initialize=0, bounds=(-10,10))
model.s1 = Var(initialize=0, bounds=(-2,2))
model.s2 = Var(initialize=0, bounds=(-2,2))

def con1(m):
    return m.s1*(2*m.x1**3+2*m.x1*m.x2-21*m.x1+m.x2**2-7)+(1-m.s1)*(m.x1-2)==m.s2
model.con1 = Constraint(rule=con1)
def con2(m):
    return m.s1*(m.x1**2+2*m.x1*m.x2+2*m.x2**3+13*m.x2-11)+(1-m.s1)*(m.x2-2)==m.s2
model.con2 = Constraint(rule=con2)
model.obj = Objective(expr=model.s1*model.s1-model.s1*model.s1+model.s2*model.s2-model.s2*model.s2)

model.homotopy_begin=Suffix(direction=Suffix.EXPORT, datatype=Suffix.FLOAT)
model.homotopy_begin.set_value(model.s1, 1)  #
model.homotopy_begin.set_value(model.s2, 2)  #

model.write('eq_sys.nl')
solver = SolverFactory("ipopt", executable=r"/usr/local/bin/ipopt") #

import os
new_lib = '/usr/local/lib'
os.environ['LD_LIBRARY_PATH']=new_lib

solver.solve(model, tee=True)
model.display("result.txt")
