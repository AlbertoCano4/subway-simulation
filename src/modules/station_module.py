from modules.passenger_module import Passenger, passenger_counter

class Station:
    """Representa una estación y genera pasajeros.
    @author: Gonzalo Ruiz
    """
    def __init__(self, env, name, base_rate, rng, time_formatter, log_writer=None):
        # Parámetros de la estación
        self.env = env
        self.name = name
        self.base_rate = base_rate
        self.rng = rng
        self.time_formatter = time_formatter
        self.waiting = []       # Lista de pasajeros en espera
        self.line = None        # Línea a la que pertenece
        self.log_writer = log_writer
        # Iniciar generación de pasajeros
        self.env.process(self.generate_passengers())

    def set_line(self, line):
        # Asignar línea de metro
        self.line = line

    def hourly_rate(self, hour):
        # Varía la demanda según la hora (pico y valle)
        # Ajusta tasa según hora punta o valle
        if 6 <= hour < 10 or 17 <= hour < 21:
            return self.base_rate * 2
        if 10 <= hour < 14:
            return self.base_rate * 1.5
        if 14 <= hour < 17 or 21 <= hour < 24:
            return self.base_rate * 1.2
        return self.base_rate

    def random_destination(self):
        # Seleccionar destino distinto de la estación actual
        opts = [s.name for s in self.line.stations if s.name != self.name]
        return self.rng.choice(opts)

    def generate_passengers(self):
        # Genera pasajeros: calcula tiempo de espera usando distribución exponencial según la tasa actual
        # Genera pasajeros con tiempo entre llegadas exponencial
        while True:
            hour = (6 + int(self.env.now)//60) % 24
            # Tasa variable según hora
            rate = self.hourly_rate(hour)
            # Esperar hasta próxima llegada
            # Pausa la simulación durante el tiempo hasta la próxima llegada
            yield self.env.timeout(self.rng.exponential(1/rate))

            # Crear pasajero y registrar
            # Incrementar el contador para asignar ID único a cada pasajero
            # Incrementa el contador global para generar un ID único
            passenger_counter[0] += 1
            arrival = self.env.now
            dest = self.random_destination()
            p = Passenger(f"P{passenger_counter[0]}", dest, arrival)
            self.waiting.append(p)
            # Registrar evento en CSV si está habilitado
            if self.log_writer:
                self.log_writer.writerow([
                    self.time_formatter(arrival), 'Arrives', p.name,
                    self.name, '', '', dest
                ])
