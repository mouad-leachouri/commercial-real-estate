import pandas as pd
import cvxpy as cp
import numpy as np
from matplotlib import pyplot as plt

dataset = pd.read_csv('data/markowitz_dataset.csv', encoding='latin1', usecols=['N°DPE', 'taux_credit', 'Emission_GES_kgCO2_m2_an'])

# Inputs
r = np.array(dataset.taux_credit)
e = np.array(dataset.Emission_GES_kgCO2_m2_an)
n = len(r)

# Problem
w = cp.Variable(n, nonneg=True)
e_max = 6
objective = cp.Minimize(- w@r)
contraints = [
    cp.sum(w) == 1, 
    w@e <= e_max
]


# Résolution
prob = cp.Problem(objective, contraints)
prob.solve()

# Affichage des résultats
print("Portefeuille optimal :")
w_opt = w.value
print(w_opt)  # Affiche la fraction de capital à allouer à chaque bien
print(sum(w_opt))
print("Rendement optimal :", w_opt@r)
print("Emissions minimales:", w_opt@e)

# Visualisation
plt.bar(x=range(n), height=w_opt)
plt.show()

r_opt = []
e_opt = []
w_opt = []

for t in np.arange(0.5, 10, 0.1):
    w = cp.Variable(n, nonneg=True)
    objective = cp.Minimize(- w@r)
    contraints = [
        cp.sum(w) == 1, 
        w@e <= t
    ]


    # Résolution
    prob = cp.Problem(objective, contraints)
    prob.solve()
    
    w = w.value
    
    w_opt.append(w)
    r_opt.append(w@r)
    e_opt.append(w@e)

def singularities(x, y, tol):
    singu = []
    for i in range(1, len(y)-1):
        if abs(((y[i+1] - y[i])/(x[i+1] - x[i])) - ((y[i] - y[i-1])/(x[i] - x[i-1])))>tol:
            singu.append([x[i], y[i]])
    return singu


singu = np.array(singularities(e_opt, r_opt, tol=1e-6))
plt.scatter(x=e_opt, y=r_opt)
plt.scatter(x=singu[:, 0], y=singu[:, 1], color='red')
for s in singu:
    print(s)
    plt.axvline(x=s[0], linestyle='--', color='black')
    plt.axhline(y=s[1], linestyle='--', color='black')

plt.grid(True)
plt.ylabel("Rendement du portefeuille")
plt.xlabel("Emissions GES (kg/m$^2$/an)")
plt.title("Frontière efficiente")
plt.tight_layout()
plt.show()
