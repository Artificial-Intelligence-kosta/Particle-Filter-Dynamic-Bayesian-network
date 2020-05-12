# Particle-Filter-Dynamic-Bayesian-network
Scalar random process is given with the model:

![Model](https://github.com/Artificial-Intelligence-kosta/Particle-Filter-Dynamic-Bayesian-network/blob/master/Process.png)

where wt and vt are white Gaussian noises with variances 10 and 1.

Process is simulalted for 50 time steps, and for inital state X0 = 0.1 the aposterior distribution **p(xt|e1:t)** is evaluated using the **Particle Filter**. Optimal number of particles is found by calculating MSE.
### RESULTS
![results](https://github.com/Artificial-Intelligence-kosta/Particle-Filter-Dynamic-Bayesian-network/blob/master/plots/Results.png)
![MSE](https://github.com/Artificial-Intelligence-kosta/Particle-Filter-Dynamic-Bayesian-network/blob/master/plots/MSE.png)
![histogram](https://github.com/Artificial-Intelligence-kosta/Particle-Filter-Dynamic-Bayesian-network/blob/master/plots/Histogram.png)
