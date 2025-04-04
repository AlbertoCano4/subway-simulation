class Train:
    # Constructor
    def __init__(self, env, name, capacity, line, frequency_schedule, time_formatter,
                 direction='clockwise', log_writer=None, delay_base=0,
                 active_trains=None, rng=None):
        self.env = env
        self.name = name  
        self.capacity = capacity  
        self.line = line  
        self.frequency_schedule = frequency_schedule  
        self.current_station_index = 0  
        self.passengers = []  
        self.time_formatter = time_formatter
        self.active = True  
        self.direction = direction  
        self.log_writer = log_writer
        self.delay_base = delay_base
        self.active_trains = active_trains or []
        self.rng = rng

        # Start train process with delay
        self.action = env.process(self.start_with_delay())

    # Function to start with delay
    def start_with_delay(self):
        delay = self.delay_base + self.rng.integers(0, 4)
        yield self.env.timeout(delay)
        yield from self.run()

    def run(self):
        while True:
            current_station = self.line.stations[self.current_station_index]
            timestamp = self.time_formatter(self.env.now) if self.time_formatter else str(self.env.now)
            print(f'[{timestamp}] {self.name} ({self.direction}) arrives at {current_station.name}')
            if self.log_writer:
                self.log_writer.writerow([timestamp, 'Arrives', self.name, current_station.name, self.name, self.direction, ''])

            # Passengers getting off
            self.passengers = [p for p in self.passengers if not self.try_to_alight(p, current_station)]

            # Passengers getting on
            boarding_passengers = []
            for passenger in current_station.waiting_passengers:
                if len(self.passengers) >= self.capacity:
                    break
                if self.line.is_correct_direction(current_station.name, passenger.destination, self.direction):
                    boarding_passengers.append(passenger)

            for passenger in boarding_passengers:
                self.passengers.append(passenger)
                current_station.waiting_passengers.remove(passenger)
                print(f'[{timestamp}] {passenger.name} boards {self.name} ({self.direction}) at {current_station.name}')
                if self.log_writer:
                    self.log_writer.writerow([timestamp, 'Boards', passenger.name, current_station.name, self.name, 
                                              self.direction, passenger.destination])

            # Check if train should be retired
            if not self.active and (
                (self.direction == 'clockwise' and self.current_station_index == len(self.line.stations) - 1) or
                (self.direction == 'counterclockwise' and self.current_station_index == 0)
            ):
                print(f'[{timestamp}] {self.name} is withdrawn at {current_station.name}')
                if self.log_writer:
                    self.log_writer.writerow([timestamp, 'Withdraws', self.name, current_station.name, 
                                              self.name, self.direction, ''])
                # Drop off all remaining passengers
                for passenger in self.passengers:
                    current_station.waiting_passengers.append(passenger)
                self.passengers.clear()
                return

            # Wait if a collision is detected
            while self.detect_collision():
                yield self.env.timeout(1)

            # Move to the next station
            origin = current_station.name
            next_index = (self.current_station_index + 1) % len(self.line.stations) if self.direction == 'clockwise' else (self.current_station_index - 1) % len(self.line.stations)
            destination = self.line.stations[next_index].name
            travel_time = self.line.get_travel_time(origin, destination)
            yield self.env.timeout(travel_time)

            self.current_station_index = next_index

    def try_to_alight(self, passenger, station):
        timestamp = self.time_formatter(self.env.now) if self.time_formatter else str(self.env.now)
        if passenger.destination == station.name:
            print(f'[{timestamp}] {passenger.name} alights at {station.name}')
            if self.log_writer:
                self.log_writer.writerow([timestamp, 'Alights', passenger.name, station.name, self.name, self.direction, station.name])
            return True
        return False

    # Function to dont have two trains in the same station
    def detect_collision(self):
        if not self.active_trains:
            return False

        positions_to_check = []
        total_stations = len(self.line.stations)

        for i in range(1, 3):
            if self.direction == 'clockwise':
                pos = (self.current_station_index + i) % total_stations
            else:
                pos = (self.current_station_index - i) % total_stations
            positions_to_check.append(pos)

        for other in self.active_trains:
            if other is self:
                continue
            if not other.active or other.direction != self.direction:
                continue
            if other.current_station_index in positions_to_check:
                return True

        return False
