import numpy as np
from pyomo.environ import *
model = ConcreteModel()
#model.s = Var(initialize=0, bounds=(0,10))
#model.x1 = Var(initialize=0, bounds=(-10,10))
#model.x2 = Var(initialize=1, bounds=(-10,10))

model.x1 = Var(initialize=0, bounds=(-10,10))
model.x2 = Var(initialize=0, bounds=(-10,10))
model.s = Var(initialize=0)
model.homotopy_begin=Suffix(direction=Suffix.EXPORT, datatype=Suffix.FLOAT)
model.homotopy_begin.set_value(model.s, 2)
model.homotopy_begin.set_value(model.x2, 1)

def con1(m):
    return m.s*(2*m.x1**3+2*m.x1*m.x2-21*m.x1+m.x2**2-7)+(1-m.s)*(m.x1-2)==0
model.con1 = Constraint(rule=con1)
def con2(m):
    return m.s*(m.x1**2+2*m.x1*m.x2+2*m.x2**3+13*m.x2-11)+(1-m.s)*(m.x2-2)==0
model.con2 = Constraint(rule=con2)
model.obj = Objective(expr=1)
solver = SolverFactory("ipopt", executable=r"/usr/local/bin/ipopt") #
solver.options["output_file"]=r"/home/zhang/PythonWork/Homotopy/ipopt2.log"

import os
new_lib = '/usr/local/lib'
# new_lib = '/home/zhang/IpoptWork/Ipopt-stable-3.14-homo/build/src/Apps/AmplSolver/ipopt'
os.environ['LD_LIBRARY_PATH']=new_lib

result = solver.solve(model, tee=True)
model.display("result.txt")

