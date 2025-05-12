class Train:
    """Simula un tren que recorre estaciones y transporta pasajeros.

    @autor: Alberto Cano e Ignacio Fernández
    """
    def __init__(self, env, name, capacity, line, direction,
                 time_formatter, delay, active_trains, rng, metrics, log_writer=None):
        # Parámetros básicos
        self.env = env
        self.name = name
        self.capacity = capacity
        self.line = line
        self.direction = direction
        self.time_formatter = time_formatter
        self.delay = delay
        self.active_trains = active_trains
        self.rng = rng
        self.metrics = metrics
        self.log_writer = log_writer
        # Estado inicial
        self.station_idx = 0
        self.passengers = []
        self.active = True
        # Arranca el proceso del tren
        self.action = env.process(self.start())

    def start(self):
        # Espera el retraso inicial y comienza el recorrido
        yield self.env.timeout(self.delay)
        yield from self.run()

    def run(self):
        # Bucle principal: llega a cada estación, baja/sube pasajeros y avanza
        while True:
            station = self.line.stations[self.station_idx]
            # Registrar llegada
            if self.log_writer:
                self.log_writer.writerow([
                    self.time_formatter(self.env.now), 'Arrives',
                    self.name, station.name, self.name, self.direction, ''
                ])

            # Bajada de pasajeros cuya destino coincide
            for p in list(self.passengers):
                if p.destination == station.name:
                    if self.log_writer:
                        self.log_writer.writerow([
                            self.time_formatter(self.env.now), 'Alights',
                            p.name, station.name, self.name, self.direction, station.name
                        ])
                    self.passengers.remove(p)

            # Subida de pasajeros si hay espacio y van en la dirección correcta
            to_board = []
            for p in list(station.waiting):
                if len(self.passengers) < self.capacity and \
                   self.line.is_correct_direction(station.name, p.destination, self.direction):
                    # Calcular tiempo de espera
                    wait = self.env.now - p.arrival_time
                    self.metrics.append(wait)
                    to_board.append(p)
            for p in to_board:
                station.waiting.remove(p)
                self.passengers.append(p)
                if self.log_writer:
                    self.log_writer.writerow([
                        self.time_formatter(self.env.now), 'Boards',
                        p.name, station.name, self.name, self.direction, ''
                    ])

            # Evitar colisiones con trenes cercanos
            while self.detect_collision():
                yield self.env.timeout(1)

            # Calcular siguiente estación y tiempo de viaje
            next_idx = self.line.next_index(self.station_idx, self.direction)
            time_travel = self.line.get_travel_time(
                self.line.stations[self.station_idx].name,
                self.line.stations[next_idx].name)
            # Desplazarse a la siguiente estación
            yield self.env.timeout(time_travel)
            self.station_idx = next_idx

    def detect_collision(self):
        # Comprueba si hay otro tren en las dos estaciones siguientes
        total = len(self.line.stations)
        checks = (
            [(self.station_idx + i) % total for i in (1, 2)]
            if self.direction == 'clockwise'
            else [(self.station_idx - i) % total for i in (1, 2)]
        )
        for t in self.active_trains:
            if t is not self and t.active and t.direction == self.direction:
                if t.station_idx in checks:
                    return True
        return False
