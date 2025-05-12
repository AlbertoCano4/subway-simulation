import simpy
from modules.train_module import Train

class Scheduler:
    """Genera trenes en ambas direcciones cada 'freq' minutos.
    @author: Ignacio Fernández
    """
    def __init__(self, env, line, freq, n_trains, capacity,
                 time_formatter, rng, metrics, log_writer=None):
        self.env = env                      # Entorno SimPy
        self.line = line                    # Línea de metro
        self.freq = freq                    # Intervalo de despliegue
        self.n_trains = n_trains            # Máximo trenes activos por dirección
        self.capacity = capacity            # Capacidad de cada tren
        self.time_formatter = time_formatter
        self.rng = rng
        self.metrics = metrics              # Lista compartida de métricas de espera
        self.log_writer = log_writer
        self.active_trains = []             # Seguimiento de trenes en circulación
        env.process(self.generate())        # Iniciar proceso de generación

    def generate(self):
        # Bucle infinito, cada freq de minutos intentamos mantener n_trains
        while True:
            for direction in ('clockwise', 'counterclockwise'):
                # Filtrar trenes activos en esta dirección
                running = [t for t in self.active_trains if t.direction == direction and t.active]
                missing = self.n_trains - len(running)  # Cuántos faltan por lanzar
                
                for _ in range(missing):
                    # Retraso aleatorio inicial para dispersar los despachos
                    delay = self.rng.integers(0, self.freq)
                    name = f"Train_{len(self.active_trains) + 1}"
                    # Instanciar tren con los parámetros básicos y añadirlos al seguimiento
                    train = Train(
                        self.env, name, self.capacity, self.line,
                        direction, self.time_formatter, delay,
                        self.active_trains, self.rng, self.metrics,
                        log_writer=self.log_writer
                    )
                    self.active_trains.append(train)
            # Esperar antes de la siguiente ronda de despliegue
            yield self.env.timeout(self.freq)
