class Line:
    """Representa una línea circular de metro.

    @author: Ignacio Fernández
    """
    def __init__(self, name, stations, distances):
        self.name = name            # Nombre de la línea
        self.stations = stations    # Lista de objetos Station en orden
        self.distances = distances  # Mapa de distanciias/tiempos entre estaciones

    def next_index(self, current_index, direction='clockwise'):
        # Índice de la siguiente estación según dirección
        if direction == 'clockwise':
            return (current_index + 1) % len(self.stations)
        return (current_index - 1) % len(self.stations)

    def is_correct_direction(self, origin, destination, direction):
        # Comprueba si ir de origin a destination sigue la dirección dada
        idx = {s.name: i for i, s in enumerate(self.stations)}
        orig, dest = idx[origin], idx[destination]
        if direction == 'clockwise':
            return (dest - orig) % len(self.stations) > 0
        return (orig - dest) % len(self.stations) > 0

    def get_travel_time(self, origin, destination):
        # Devuelve tiempo de viaje entre dos estaciones (bidireccional)
        return self.distances.get((origin, destination),
               self.distances.get((destination, origin), 5))  # 5 por defecto si no existe
