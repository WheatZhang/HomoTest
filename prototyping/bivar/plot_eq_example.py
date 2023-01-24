import numpy as np
import matplotlib.pyplot as plt
xlist = np.linspace(-10.0, 10.0, 100)
ylist = np.linspace(-10.0, 10.0, 100)
X, Y = np.meshgrid(xlist, ylist)
Z1 = 2*X**3+2*X*Y-21*X+Y**2-7
Z2 = X**2+2*X*Y+2*Y**3+13*Y-11

fig = plt.figure(figsize=(10,6))
plt.subplot(121)
ax=plt.gca()
cp = ax.contourf(X, Y, Z1)
fig.colorbar(cp) # Add a colorbar to a plot

plt.subplot(122)
ax=plt.gca()
cp = ax.contourf(X, Y, Z2)
fig.colorbar(cp) # Add a colorbar to a plot
plt.savefig("eq_example")
