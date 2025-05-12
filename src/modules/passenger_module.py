passenger_counter = [0]  # Contador global para asignar ID único a cada pasajero

class Passenger:
    """Representa un pasajero con destino y tiempo de llegada.

    @author: Gonzalo Ruiz
    """
    def __init__(self, name, destination, arrival_time):
        # Identificador del pasajero (e.g., 'P1')
        self.name = name
        # Estación de destino
        self.destination = destination
        # Tiempo (en minutos desde inicio de simulación) en que llega a la estación
        self.arrival_time = arrival_time
