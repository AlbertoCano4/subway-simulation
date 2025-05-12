import simpy  # Motor de simulación de eventos discretos
import numpy as np
from modules.station_module import Station      # Módulo de estaciones
from modules.line_module import Line            # Módulo de la línea de metro
from modules.scheduler_module import Scheduler  # Módulo de planificación de trenes
import csv  # Para exportar logs de eventos

class SimulationManager:
    """Clase para hacer las simulaciones y calcular métricas.

    @author: Alberto Cano
    """
    def __init__(self, stations_info, distances, sim_minutes, num_days, rng, capacity):
        self.stations_info = stations_info  # Información de estaciones y tasas de llegada
        self.distances = distances          # Distancias en km entre pares de estaciones
        self.sim_minutes = sim_minutes      # Duración de la simulación en minutos
        self.num_days = num_days            # Número de días a ejecutar para promediar resultados
        self.rng = rng                      # Generador de números aleatorios para la simulación
        self.capacity = capacity            # aforo de cada tren

    def run_one_day(self, freq, n_trains):
        # Crear entorno de SimPy para un día de simulación
        env = simpy.Environment()
        metrics = []  # Lista para almacenar tiempos de espera de pasajeros
        
        # Función auxiliar para formatear tiempos en hh:mm (empezando a las 06:00)
        def fmt(m):
            h = (6 + int(m) // 60) % 24
            mm = int(m) % 60
            return f"{h:02d}:{mm:02d}"
        
        stations = []  # Lista de objetos Station
        # Inicializr cada estación con su tasa de llegada
        for name, rate in self.stations_info.items():
            st = Station(env, name, rate, self.rng, fmt, log_writer=self.log_writer)
            stations.append(st)
        
        # Crear línea de metro con las estaciones y sus distancias
        line = Line('Metro', stations, self.distances)
        # Asignar la línea a cada estación
        for st in stations:
            st.set_line(line)
        
        # Activar scheduler para programar trenes según frecuencia y número de unidades
        Scheduler(env, line, freq, n_trains, self.capacity, fmt, self.rng, metrics, log_writer=self.log_writer)
        
        # Ejecutar la simulación hasta el fin del día (sim_minutes)
        env.run(until=self.sim_minutes)
        
        # Calcular y devolver la espera media de ese día
        return float(np.mean(metrics)) if metrics else float('inf')

    def run_simulation(self, freq, n_trains):
        # Abrir CSV para registrar el log de eventos de todos los días simulados
        with open('../data_analysis/event_log.csv', mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            # Encabezado del fichero de log
            csv_writer.writerow(['Time', 'Event', 'Entity', 'Station', 'Train', 'Direction', 'Destination'])
            self.log_writer = csv_writer  # Guardar para usarlo en la simulación
            # Ejecutar run_one_day para cada día y obtener métricas
            days = [self.run_one_day(freq, n_trains) for _ in range(self.num_days)]
        # Devolver la espera media a lo largo de todos los días simulados
        return float(np.mean(days))
