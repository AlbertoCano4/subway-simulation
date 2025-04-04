from passenger_module import Passenger, passenger_counter


class Station:
    # Constructor
    def __init__(self, env, name, arrival_rate, rng, time_formatter=None, log_writer=None):
        self.env = env
        self.name = name  
        self.arrival_rate = arrival_rate  
        self.waiting_passengers = []  
        self.time_formatter = time_formatter  
        self.log_writer = log_writer  
        self.line = None  
        self.rng = rng  

        self.env.process(self.generate_passengers())

    # Setter of the line
    def set_line(self, line):
        self.line = line

    # Function to define the arrival rates based on thehour of the day
    def get_hourly_arrival_rate(self, hour):
        if 6 <= hour < 10 or 17 <= hour < 21:
            return self.arrival_rate * 2  
        elif 10 <= hour < 14:
            return self.arrival_rate * 1.5
        elif 14 <= hour < 17:
            return self.arrival_rate * 1.2
        elif 21 <= hour < 24:
            return self.arrival_rate * 1.2
        else:
            return self.arrival_rate  

    def get_random_destination(self):
        possible_destinations = [s.name for s in self.line.stations if s.name != self.name]
        return self.rng.choice(possible_destinations)

    def generate_passengers(self):
        while True:
            current_hour = (6 + int(self.env.now) // 60) % 24
            rate = self.get_hourly_arrival_rate(current_hour)
            yield self.env.timeout(self.rng.exponential(1 / rate))

            # Create a passenger 
            destination = self.get_random_destination()
            passenger_counter[0] += 1
            passenger = Passenger(f'Passenger_{passenger_counter[0]}', destination)
            self.waiting_passengers.append(passenger)

            timestamp = self.time_formatter(self.env.now) if self.time_formatter else str(self.env.now)
            print(f'[{timestamp}] {passenger.name} arrives at {self.name} heading to {destination}')
            if self.log_writer:
                self.log_writer.writerow([timestamp, 'Arrives', passenger.name, self.name, '', '', destination])
