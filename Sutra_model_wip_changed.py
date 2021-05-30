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


    
    

def SUTRA(P, T0, Rt0, D0):
    # Total population, P.
    # Initial number of infected and recovered individuals, I0 and R0.
    #I0, R0 = 1, 0 # initial tested positive #Initial recovered after being tested positive
    U0 = T0*0.5 # Initial Undetected positive cases
    Ru0 = U0*0.3 #Initial recovered from Undetected positive cases# initia deaths
    N = P-D0 # remaining population
    
    S0 = N - U0 - T0 - Ru0 - Rt0 - D0 #S0, is susceptible to infection initially.
    
    #print("N:", N)
    #print("S0", S0)
    #print("Number immune:", N-S0)
    
    # beta = P(infection|contact between susceptible and Undetected)
    # gamma = rate at which infected people recover i.e rate of change of recover wrt time
    beta, gamma = 0.2, 1./31 #1./31
    
    #epsilon = fraction of undetected that get tested positive
    epsilon =  0.3
    
    #the rate a which people are dying
    eta = 0.063951
    
    # A grid of time points linspace(start, stop, num), (in days)
    t = np.linspace(0, 10, 10) 
    #print(t)
    # The SUTRA model differential equations.
    def deriv(y, t, N, beta, gamma, epsilon, eta):
        S, U, T, Ru, Rt, D = y
        
        dSdt = (-beta * S * U )/ N
        dUdt = (beta * S * U / N ) - ((epsilon * beta * S * U) / N )- (gamma * U)
        dTdt = ((epsilon * beta * S * U) / N ) - (gamma * T)
        dRudt = gamma * U
        dRtdt = gamma * T
        dDdt = eta * T
        
        return dSdt, dUdt, dTdt, dRudt, dRtdt, dDdt
    
    # Initial conditions vector
    y0 = S0, U0, T0, Ru0, Rt0, D0
    # Integrate the SUTRA equations over the time grid, t.
    ret = odeint(deriv, y0, t, args=(N, beta, gamma, epsilon, eta))
    S, U, T, Ru, Rt, D = ret.T
    
    #print("S", S[-1])
    #print("U", U[-1])
    #print("T", T[-1])
    #print("Ru", Ru[-1])
    #print("Rt", Rt[-1])
    #print("D:", D[-1])
    #print("N", S[-1]+U[-1]+T[-1]+Ru[-1]+Rt[-1])
    #print("Tested +ve:", T)
    #print("New infections: ", T[-1] - T0)
    new_inf = T[-1]-T0
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
    Test_pos = state_each.loc[(state_each.shape[0]-11),'Confirmed']
    Recover_test_pos = state_each.loc[(state_each.shape[0]-11),'Recovered']
    Decease = state_each.loc[(state_each.shape[0]-11),'Deceased']
    var = SUTRA(Pop,Test_pos,Recover_test_pos,Decease)   
    dict1[key_name] = var

print(dict1)

# Plot the data on three separate curves for S(t), I(t) and R(t)
# fig = plt.figure(facecolor='w')
# ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
# ax.plot(t, S/N, 'b', alpha=0.5, lw=2, label='Susceptible')
# ax.plot(t, U/N, 'r', alpha=0.5, lw=2, label='Undetected')
# ax.plot(t, T/N, 'g', alpha=0.5, lw=2, label='Recovered from Undected')
# ax.plot(t, Ru/N, 'y', alpha=0.5, lw=2, label='Recovered from Undected')
# ax.plot(t, Rt/N, 'k', alpha=0.5, lw=2, label='Recovered from tested positive')

# ax.set_xlabel('Time /days')
# ax.set_ylabel('Number ('+str(N)+')')
# ax.set_ylim(0,1.2)
# ax.yaxis.set_tick_params(length=0)
# ax.xaxis.set_tick_params(length=0)
# ax.grid(b=True, which='major', c='w', lw=2, ls='-')
# legend = ax.legend()
# legend.get_frame().set_alpha(0.5)
# for spine in ('top', 'right', 'bottom', 'left'):
    # ax.spines[spine].set_visible(False)
# plt.show()