# -*- coding: utf-8 -*-
"""
Created on Sun May 10 22:06:21 2020

@author: Kosta
"""
from math import cos, sqrt, exp
from numpy import random, mean, std
import matplotlib.pyplot as plt
import os

def makePrediction(x, t, noise_var):
    wt = random.normal(0, sqrt(noise_var))
    x_next = 0.5*x + 25*x/(1+x**2) + 8*cos(1.2*t*0.01) + wt
    return x_next
def simulateProcess(x0, time_steps, w_var, v_var):
    x = x0
    Y = [None]*time_steps
    X_true = [None]*time_steps
    for t in range(time_steps):
        X_true[t] = makePrediction(x, t, w_var)
        Y[t] = (X_true[t]**2)/20 + random.normal(0, sqrt(v_var))
        x = X_true[t]
    return X_true, Y
def getWeight(x, y, var):
    weight = exp(-((y - (x**2)/20)**2)/(2*var))
    return weight
def normalizeWeights(weights):
    alpha = sum(weights)
    for i, weight in enumerate(weights):
        weights[i] = weight/alpha
    return weights
def getStatistics(X, weights):
    mean = 0
    for x,weight in zip(X,weights):
        mean += x*weight
    var = 0
    for x,weight in zip(X,weights):
        var += weight*(x-mean)**2
    return mean, sqrt(var)
def getSquaredError(x_true, x_est):
    return (x_true - x_est)**2
def resample(X, weights):
    X_new = random.choice(a=X, size=len(X), replace=True, p=weights)
    return X_new
def makeReport(X_true, X_est_opt, Y, X_std_opt,time_steps, sample_size, MSE, X21, weights21):
    plots_dir = os.path.join(os.getcwd(),'plots')
    os.makedirs(plots_dir, exist_ok=True)
    # MSE plot
    fig = plt.figure(figsize=(12, 6))
    plt.xlabel('Number of particles')
    plt.ylabel('MSE')
    plt.title('Mean Squared Error')
    plt.plot(sample_size, MSE, figure=fig)
    plt.savefig(os.path.join(plots_dir,"MSE.png"))
    # True states, opservations, estimations
    time = range(1,time_steps+1)
    fig = plt.figure(figsize=(12,6))
    plt.xlabel('Time')
    plt.plot(time, X_true, 'b', label='True states', figure=fig) 
    plt.plot(time, Y, 'r', label='Opservations', figure=fig) 
    plt.plot(time, X_est_opt, 'k', label='Mean value estimation', figure=fig) 
    lower_limit = [mean-std for mean,std in zip(X_est_opt, X_std_opt)]
    upper_limit = [mean+std for mean,std in zip(X_est_opt, X_std_opt)]
    plt.fill_between(time,lower_limit,upper_limit,facecolor='gray')
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(plots_dir,"Results.png"))
    # histogram at t=21
    fig = plt.figure(figsize=(12,6))
    plt.hist(X21, density='True', weights=weights21, label='Histogram for the aposterior distribution for t=21')
    plt.axvline(X_true[20],color='red',label='True value for t=21')
    plt.legend(loc='upper left')
    plt.savefig(os.path.join(plots_dir,"Histogram.png"))
    
if __name__ == "__main__":
    #=======================
    time_steps = 50
    sample_size = range(10,200,5)
    w_var = 10
    v_var = 1
    x0 = 0.1
    optimal_num_of_particles = 35 # determined from the plot of MSE over the number of particles
    #=======================
    MSE = [0]*len(sample_size)
    MSE_prev = 0
    X_true, Y = simulateProcess(x0, time_steps, w_var, v_var)
    for ind,num_of_particles in enumerate(sample_size):
        X = [x0]*num_of_particles
        weights = [None]*num_of_particles
        X_est = [None]*time_steps
        X_std = [None]*time_steps
        
        for t in range(time_steps):
            for i in range(num_of_particles):
                X[i] = makePrediction(X[i], t, w_var)
                weights[i] = getWeight(X[i], Y[t], v_var)
            weights = normalizeWeights(weights)
            if (num_of_particles == optimal_num_of_particles):
                if(t == 21):
                    X21, weights21 = X, weights
            X_est[t], X_std[t] = getStatistics(X, weights)
            MSE[ind] += getSquaredError(X_true[t], X_est[t])/time_steps
            X = resample(X, weights) 
        if (num_of_particles == optimal_num_of_particles):
            X_est_opt = X_est
            X_std_opt = X_std
    makeReport(X_true, X_est_opt, Y, X_std_opt,time_steps, sample_size, MSE, X21, weights21)
    
        
            
            
            
            
            
            