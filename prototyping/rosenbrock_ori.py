import numpy as np
from pyomo.environ import *
model = ConcreteModel()
model.x1 = Var(initialize=0, bounds=(-10,10))
model.x2 = Var(initialize=0, bounds=(-10,10))
model.t = Var(initialize=0, bounds=(-2,2))

def obj(m):
    # return (1 - m.x1) ** 2 + 5 * (m.x2  - m.x1 ** 2) ** 2 + m.t*m.t -m.t*m.t
    return (1-m.x1)**2+5*(m.x2+m.t-m.x1**2)**2 + 100*(m.t-1)**2
model.obj = Objective(rule=obj)

solver = SolverFactory("ipopt", executable=r"/home/zhang/IpoptWork/Ipopt-stable-3.14/build/src/Apps/AmplSolver/ipopt") #

import os
new_lib = '/usr/local/lib'
os.environ['LD_LIBRARY_PATH']=new_lib

result = solver.solve(model, tee=True)
model.display("result.txt")

