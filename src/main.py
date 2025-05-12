import numpy as np
import random
from sim.simulation_manager import SimulationManager
from optim.pso_optim import PSO_Optimizer

# Fijar semillas para los resultados sean iguales de una ejecución a otra
random.seed(42)
np.random.seed(42)

if __name__ == '__main__':
    # Tasas de llegada de pasajeros por estación (clientes por minuto)
    arrival_rates = {
        'Castellana': 0.2,
        'Chamartin (station)': 0.15,
        'Pinar de Chamartin': 0.1,
        'Sanchinarro': 0.15,
        'La Moraleja': 0.1,
        'Las Tablas': 0.2,
        'Tres Olivos': 0.15,
        'Montecarmelo': 0.1,
        'Mirasierra': 0.15,
        'Paco de Lucia': 0.1
    }
    
    # Distancias entre estaciones (kilómetros)
    distances = {
        ('Castellana', 'Chamartin (station)'): 3,
        ('Chamartin (station)', 'Pinar de Chamartin'): 4,
        ('Pinar de Chamartin', 'Sanchinarro'): 2,
        ('Sanchinarro', 'La Moraleja'): 3,
        ('La Moraleja', 'Las Tablas'): 5,
        ('Las Tablas', 'Tres Olivos'): 2,
        ('Tres Olivos', 'Montecarmelo'): 3,
        ('Montecarmelo', 'Mirasierra'): 2,
        ('Mirasierra', 'Paco de Lucia'): 4,
        ('Paco de Lucia', 'Castellana'): 5
    }
    
    # Duración total de la simulación en minutos
    SIM_MINUTES = 1200  # Equivale a 20 horas (de 6am a 2am)

    # Número de días a simular para promediar resultadoss
    NUM_DAYS = 1

    # Aforo del tren
    TRAIN_CAP = 200

    # Inicializar un generador de números aleatorios de NumPy para usarlo en la simulación
    RNG = np.random.default_rng(42)

    # Crear el administrador de la simulación con todos los parámetros definidos
    sim = SimulationManager(arrival_rates, distances, SIM_MINUTES, NUM_DAYS, RNG, TRAIN_CAP)

    # Definir los límites inferiores y superiores para los parámetros a optimizar:
        # Frecuencia entre trenes (minutos)
        # Número de trenes disponibles
    lb = [3, 1]
    ub = [15, 5]

    # Instanciar el optimizador PSO con la simulación 
    optimizer = PSO_Optimizer(sim, lb, ub)

    # Ejecutar la optimización:
        # iters: número de iteraciones del algoritmo
        # particles: número de partículas en la población
    best_pos, best_cost = optimizer.optimize(iters=20, particles=15)

    # Imprimir los resultados óptimos:
    print(
        f"Optimized frequency: {best_pos[0]:.2f} min" # best_pos[0] -> frecuencia óptima entre trenes (minutos)
        f" \nNumber of trains: {int(round(best_pos[1]))}" # best_pos[1] -> número óptimo de trenes
        f" \nAverage passenger wait: {best_cost:.2f} min" # best_cost -> espera media de los pasajeros (minutos)
        f" \nCSV correctly generated and saved in data_analysis"
    )
