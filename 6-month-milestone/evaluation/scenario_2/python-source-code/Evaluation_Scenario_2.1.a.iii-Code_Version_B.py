# import statements
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------------------------------------------------------
# Function Definitions
# -----------------------------------------------------------------------------

# define SIDARTHE_model
def SIDARTHE_model(y, t, alpha, beta, gamma, delta, epsilon, mu, zeta, lamb, eta, rho, theta, kappa, nu, xi, sigma, tau):
    S, I, D, A, R, T, H, E = y
    dSdt = -S*(alpha(t)*I + beta(t)*D + gamma(t)*A + delta(t)*R)
    dIdt = S*(alpha(t)*I + beta(t)*D + gamma(t)*A + delta(t)*R) - (epsilon(t) + zeta(t) + lamb(t))*I
    dDdt = epsilon(t)*I - (eta(t) + rho(t))*D
    dAdt = zeta(t)*I - (theta(t) + mu(t) + kappa(t))*A
    dRdt = eta(t)*D + theta(t)*A - (nu(t) + xi(t))*R
    dTdt = mu(t)*A + nu(t)*R - (sigma(t) + tau(t))*T
    dHdt = lamb(t)*I + rho(t)*D + kappa(t)*A + xi(t)*R + sigma(t)*T
    dEdt = tau(t)*T
    
    return dSdt, dIdt, dDdt, dAdt, dRdt, dTdt, dHdt, dEdt

#  plot SIDARTHE model
def plotSIDARTHE(t, S, I, D, A, R, T, H, E):
    f, ax = plt.subplots(1,1,figsize=(10,4))
    ax.plot(t, S, 'b', alpha=0.7, linewidth=2, label='Susceptible')
    ax.plot(t, I, 'r', alpha=0.7, linewidth=2, label='Infected (Asymptomatic, Infected, Undetected)')
    ax.plot(t, D, 'r.', alpha=0.7, linewidth=2, label='Diagnosed (Asymptomatic, Infected, Detected)')
    ax.plot(t, A, 'r:', alpha=0.7, linewidth=2, label='Ailing (Symptomatic, Infected, Undetected)')
    ax.plot(t, R, 'r--', alpha=0.7, linewidth=2, label='Recognized (Symptomatic, Infected, Detected)')
    ax.plot(t, T, 'r-.', alpha=0.7, linewidth=2, label='Threatened (Acutely Symptomatic)')
    ax.plot(t, H, 'g', alpha=0.7, linewidth=2, label='Healed')
    ax.plot(t, E, 'k', alpha=0.7, linewidth=2, label='Extinct (Dead)')

    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Fraction of population')

    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    
    plt.show();


# -----------------------------------------------------------------------------
# Example Simulation and Plot
# -----------------------------------------------------------------------------

# set parameter values
def alpha(t): return np.piecewise(t, [t>=0], [0.75])
def beta(t): return np.piecewise(t, [t>=0], [0.1])
def delta(t): return np.piecewise(t, [t>=0], [0.05])
def gamma(t): return np.piecewise(t, [t>=0], [0.2])

def epsilon(t): return np.piecewise(t, [t>=0], [0.1])
def theta(t): return np.piecewise(t, [t>=0], [0.1])

def zeta(t): return np.piecewise(t, [t>=0], [0.05])
def eta(t): return np.piecewise(t, [t>=0], [0.05])

def mu(t): return np.piecewise(t, [t>=0], [0.05])
def nu(t): return np.piecewise(t, [t>=0], [0.05])
def lamb(t): return np.piecewise(t, [t>=0], [0.05])
def rho(t): return np.piecewise(t, [t>=0], [0.05])

def kappa(t): return np.piecewise(t, [t>=0], [0.01])
def xi(t): return np.piecewise(t, [t>=0], [0.01])
def sigma(t): return np.piecewise(t, [t>=0], [0.01])

def tau(t): return np.piecewise(t, [t>=0], [0.01])

# set initial conditions
N0 = 1e6
I0, D0, A0, R0, T0, H0, E0 = 50/N0, 50/N0, 1/N0, 1/N0, 0, 0, 0
S0 = 1-I0-D0-A0-R0-T0-H0-E0
y0 = S0, I0, D0, A0, R0, T0, H0, E0 # Initial conditions vector

# set simulation parameters
dt = .5
tstart = 0
tend = 50
tvect = np.arange(tstart, tend, dt) 

# solve odes
sim = odeint(SIDARTHE_model, y0, tvect, args=(alpha, beta, gamma, delta, epsilon, mu, zeta, lamb, eta, rho, theta, kappa, nu, xi, sigma, tau))
S, I, D, A, R, T, H, E = sim.T

# plot results
plotSIDARTHE(tvect, S, I, D, A, R, T, H, E)