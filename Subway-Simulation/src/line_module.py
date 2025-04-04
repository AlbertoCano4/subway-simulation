class Line:
    # Constructor
    def __init__(self, name, stations):
        self.name = name  
        self.stations = stations  

        # We set the travel times between stations
        self.distances = {
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

    # Function to determine which is the next station
    def next_station_index(self, current_index, direction='clockwise'):
        if direction == 'clockwise':
            return (current_index + 1) % len(self.stations)
        else:
            return (current_index - 1) % len(self.stations)

    # Function to check if the passenger's destination is in the current direction
    def is_correct_direction(self, origin, destination, direction):
        indices = {s.name: i for i, s in enumerate(self.stations)}
        origin_i = indices[origin]
        destination_i = indices[destination]

        if direction == 'clockwise':
            return (destination_i - origin_i) % len(self.stations) > 0
        else:
            return (origin_i - destination_i) % len(self.stations) > 0

    # Function to determine the number of stops between origin and destination
    def steps_to_destination(self, origin, destination, direction):
        indices = {s.name: i for i, s in enumerate(self.stations)}
        origin_i = indices[origin]
        destination_i = indices[destination]

        if direction == 'clockwise':
            return (destination_i - origin_i) % len(self.stations)
        else:
            return (origin_i - destination_i) % len(self.stations)

    # Function to get the stops between origin and destination
    def get_travel_time(self, origin, destination):
        return self.distances.get((origin, destination)) or self.distances.get((destination, origin), 5)
