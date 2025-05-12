import numpy as np  # Operaciones numéricas
from pyswarm import pso  # Implementación de PSO genérico

"""
PSO Optimizer

Este módulo define la clase PSO_Optimizer, que utiliza el algoritmo de (PSO) para encontrar 
la frecuencia óptima de trenes y el número de unidades necesarias en la simulacion.

Autores: Gonzalo Ruiz e Ignacio Fernández
"""
class PSO_Optimizer:
    def __init__(self, sim_manager, lb, ub, options=None):
        # sim_manager: inicializa el método run_simulation(freq, nt)
        # lb, ub: límites inferior/superior para frecuencia y número de trenes
        # options: parámetros de PSO (no utilizados con pyswarm)
        self.sim = sim_manager
        self.lb = lb
        self.ub = ub
        self.options = options or {}

    def objective(self, x):
        # Calcula el coste (espera media) para una partícula x = [freq, nt]
        freq = x[0]
        nt = int(round(x[1]))  # Convertir número de trenes a entero
        return self.sim.run_simulation(freq, nt)

    def optimize(self, iters=20, particles=15):
        # Ejecuta PSO 
        xopt, fopt = pso(
            self.objective,  # función objetivo que retorna un float
            self.lb,
            self.ub,
            swarmsize=particles,
            maxiter=iters
        )
        return xopt, fopt