import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pandas as pd
import os

states = pd.read_csv(r'state_population.csv')#getting the population file
states.columns
Pop_list = []
State_list = []
for rows in states.itertuples():
    my_list =[rows.Population]
    Pop_list.append(my_list)
    
def SIR_mod(N,I0,R0):
    # Total population, N.
    # Initial number of infected and recovered individuals, I0 and R0.
    # Everyone else, S0, is susceptible to infection initially.
    S0 = N - I0 - R0
    # Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
    beta, gamma = 0.07, 1./32 
    # A grid of time points (in days)
    t = np.linspace(0, 10, 60)
    #print(t)
    # The SIR model differential equations.
    def deriv(y, t, N, beta, gamma):
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        
        return dSdt, dIdt, dRdt
    
    # Initial conditions vector
    y0 = S0, I0, R0
    # Integrate the SIR equations over the time grid, t.
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T
    
    #print("S:", S[-1])
    #print("I:", I[-1])
    #print("R:", R[-1])
    
    #print("New infections: ", I[-1] - I0)
    new_inf = I[-1]-I0
    return new_inf
    
dict1={} # dictionary containing new infection per state
for i in range(len(Pop_list)):
    Pop = Pop_list[i][0]
    pathname1 = '.\States' #change this path to the path containing all the state files, 
    #note that all the files must be in the smae order as the first column of pop file
    def foo(path):
        var = os.listdir(path)[i]
        return var
    
    klingon = foo(pathname1)
    klingon_long = os.path.join(pathname1,klingon)
    key = klingon.split(".")
    key_name = key[0]
    state_each = pd.read_csv(klingon_long)
    Test_pos = state_each.loc[(state_each.shape[0]-61),'Confirmed']
    Recover_test_pos = state_each.loc[(state_each.shape[0]-61),'Recovered']
    Decease = state_each.loc[(state_each.shape[0]-61),'Deceased']
    Removed = Recover_test_pos+Decease
    var = SIR_mod(Pop,Test_pos,Removed)   
    dict1[key_name] = var

print(dict1)
