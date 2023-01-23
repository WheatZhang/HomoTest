#!/usr/bin/env python
#-*- coding:utf-8 -*-
import numpy as np
from pyomo.environ import *

wocstr = ConcreteModel()
wocstr.Reactions = Set(initialize=[1, 2, 3])
wocstr.Components = Set(initialize=['A', 'B', 'C', 'E', 'G', 'P'])
wocstr.XFa = Param(wocstr.Components, initialize={'A': 1, 'B': 0, 'C': 0, 'E': 0, 'G': 0, 'P': 0})
wocstr.XFb = Param(wocstr.Components, initialize={'A': 0, 'B': 1, 'C': 0, 'E': 0, 'G': 0, 'P': 0})
wocstr.Ka = Param(wocstr.Reactions, initialize={1: 1.6599e6, 2: 7.2117e8, 3: 2.6745e12})
wocstr.Kb = Param(wocstr.Reactions, initialize={1: 6666.7, 2: 8333.3, 3: 11111})
wocstr.MolarMass = Param(wocstr.Components,
                         initialize={'A': 100, 'B': 100, 'C': 200, 'E': 200, 'G': 300, 'P': 100})  # kg/mol
stoichiometry = {(1, 'A'): -1, (1, 'B'): -1, (1, 'C'): 1, (1, 'E'): 0, (1, 'G'): 0, (1, 'P'): 0,
                 (2, 'A'): 0, (2, 'B'): -1, (2, 'C'): -1, (2, 'E'): 1, (2, 'G'): 0, (2, 'P'): 1,
                 (3, 'A'): 0, (3, 'B'): 0, (3, 'C'): -1, (3, 'E'): 0, (3, 'G'): 1, (3, 'P'): -1
                 }
wocstr.stoichiometry = Param(wocstr.Reactions, wocstr.Components, initialize=stoichiometry)

# homotopy variables
wocstr.Fa_scaled = Var(initialize=1)  # 1.8275 kg/s
wocstr.MassHoldup_scaled = Var(initialize=1)  # 2105 kg
wocstr.Fa = Var(initialize=1.8275)  # 1.8275 kg/s
wocstr.MassHoldup = Var(initialize=2105)  # 2105 kg
def Fa_homotopy_con(m):
    return m.Fa_scaled == m.Fa/1.8275
wocstr.Fa_homotopy_con = Constraint(rule=Fa_homotopy_con)
def MassHoldup_homotopy_con(m):
    return m.MassHoldup_scaled == m.MassHoldup/2105
wocstr.MassHoldup_homotopy_con = Constraint(rule=MassHoldup_homotopy_con)

wocstr.Fb = Var(initialize=4, within=NonNegativeReals,bounds=(3,6))  # kg/s
wocstr.Tr = Var(initialize=90,bounds=(70,100))  # Celsius degree
wocstr.Fr = Var(initialize=5, within=NonNegativeReals)  # kg/s
wocstr.XFr = Var(wocstr.Components, bounds=(0, 1))
wocstr.K = Var(wocstr.Reactions, initialize=0.1)
def Kmxx(m, r):
    if r == 1:
        return m.K[1] * m.XFr['A'] * m.XFr['B'] / m.MolarMass['A']
    elif r == 2:
        return m.K[2] * m.XFr['B'] * m.XFr['C'] / m.MolarMass['B']
    elif r == 3:
        return m.K[3] * m.XFr['C'] * m.XFr['P'] / m.MolarMass['C']
wocstr.Kmxx = Expression(wocstr.Reactions, rule=Kmxx)
def react_massblnc(m, comp):
    return m.Fa * m.XFa[comp] + m.Fb * m.XFb[comp] - m.Fr * m.XFr[comp] + sum(
        [m.MolarMass[comp] * m.stoichiometry[r, comp] * m.Kmxx[r] * m.MassHoldup for r in m.Reactions]) == 0
wocstr.react_massblnc = Constraint(wocstr.Components, rule=react_massblnc)
def overall_massblnc(m):
    return m.Fa + m.Fb == m.Fr
wocstr.overall_massblnc = Constraint(rule=overall_massblnc)
def kinetic_coff(m, r):
    return (m.K[r] - m.Ka[r] * exp(-m.Kb[r] / (m.Tr + 273.15))) * 1e1 == 0
wocstr.kinetic_coff = Constraint(wocstr.Reactions, rule=kinetic_coff)
def profit(m):
    return 1143.38 * m.Fr * m.XFr['P'] + 25.92 * m.Fr * m.XFr['E'] - 76.23 * m.Fa - 114.34 * m.Fb
wocstr.profit = Expression(rule=profit)
def obj(m):
    return -m.profit+\
        wocstr.Fa_scaled*wocstr.Fa_scaled-wocstr.Fa_scaled*wocstr.Fa_scaled+\
        wocstr.MassHoldup_scaled*wocstr.MassHoldup_scaled-wocstr.MassHoldup_scaled*wocstr.MassHoldup_scaled
wocstr.objective = Objective(rule=obj, sense=minimize)

wocstr.homotopy_begin=Suffix(direction=Suffix.EXPORT, datatype=Suffix.FLOAT)
wocstr.homotopy_begin.set_value(wocstr.Fa_scaled, 1)  #Fa_scaled i=12
wocstr.homotopy_begin.set_value(wocstr.MassHoldup_scaled, 2)  #MassHoldup_scaled i=13

wocstr.write('wocstr.nl')
solver = SolverFactory("ipopt", executable=r"/usr/local/bin/ipopt") #

import os
new_lib = '/usr/local/lib'
os.environ['LD_LIBRARY_PATH']=new_lib

solver.solve(wocstr, tee=True)
wocstr.display("result.txt")