# Global counter to assign unique IDs to the passengers
passenger_counter = [0]

class Passenger:
    # Constructor
    def __init__(self, name, destination):
        self.name = name  
        self.destination = destination  
    def __repr__(self):
        return f'Passenger({self.name}, Destination: {self.destination})'
