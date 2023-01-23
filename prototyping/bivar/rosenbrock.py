import numpy as np
from pyomo.environ import *
model = ConcreteModel()
model.x1 = Var(initialize=0, bounds=(-10,10))
model.x2 = Var(initialize=0, bounds=(-10,10))
model.t = Var(initialize=0, bounds=(-2,2))
model.t2 = Var(initialize=0, bounds=(-2,2))
# if suffix is required in IPOPT but no suffix is given here, IPOPT will report an error.
model.homotopy_begin=Suffix(direction=Suffix.EXPORT, datatype=Suffix.FLOAT)
model.homotopy_begin.set_value(model.x1, 1)
model.homotopy_begin.set_value(model.x2, 2)
model.homotopy_begin.set_value(model.t, 3)

def obj(m):
    return (1-m.x1)**2+5*(m.x2+m.t-m.x1**2)**2+m.t2**2-m.t2**2
model.obj = Objective(rule=obj)

solver = SolverFactory("ipopt", executable=r"/usr/local/bin/ipopt") #

import os
new_lib = '/usr/local/lib'
os.environ['LD_LIBRARY_PATH']=new_lib

result = solver.solve(model, tee=True)
model.display("result.txt")

