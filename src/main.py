import simpy
import numpy as np
import csv
from train_module import Train
from station_module import Station
from line_module import Line

# Initialize random number generator with a fixed seed as said in class by professor
rng = np.random.default_rng(seed=42)

# Functio to convert minutes into HH:MM format
def minutes_to_time(minutes):
    total_min = int(minutes)
    hour = (6 + (total_min // 60)) % 24
    minute = total_min % 60
    return f'{hour:02d}:{minute:02d}'

# We set the arrival rate of passengers per station
arrival_rates = {
    'Castellana': 0.2,
    'Chamartin (station)': 0.15,
    'Pinar de Chamartin': 0.1,
    'Sanchinarro': 0.15,
    'La Moraleja': 0.1,
    'Las Tablas': 0.2,
    'Tres Olivos': 0.15,
    'Montecarmelo': 0.1,
    'Mirasierra': 0.15,
    'Paco de Lucia': 0.1
}

# Names of the stations
station_names = [
    'Castellana',
    'Chamartin (station)',
    'Pinar de Chamartin',
    'Sanchinarro',
    'La Moraleja',
    'Las Tablas',
    'Tres Olivos',
    'Montecarmelo',
    'Mirasierra',
    'Paco de Lucia'
]

# Create and initialize CSV file to log events
csv_file = open('../data_analysis/event_log.csv', mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Time', 'Event', 'Entity', 'Station', 'Train', 'Direction', 'Destination'])

# Global counter to assign unique IDs to trains
global_train_id = [0]

# Function to determine the frequency and number of trains based on time of day
def get_schedule_parameters(current_minute):
    hour = (6 + (current_minute // 60)) % 24
    if 6 <= hour < 10 or 17 <= hour < 21:
        return 5, 3  
    elif 10 <= hour < 14:
        return 8, 2
    elif 14 <= hour < 17:
        return 6, 2
    elif 21 <= hour < 24:
        return 8, 2
    else:
        return 10, 1

# Function to generate and manage trains dynamically
def generate_trains(env, line):
    active_trains = []
    max_trains_per_direction = 3

    while True:
        frequency, _ = get_schedule_parameters(env.now)

        # Remove trains that are no longer active
        active_trains = [t for t in active_trains if t.active and t.action.is_alive]

        for direction in ['clockwise', 'counterclockwise']:
            # Count trains currently running in this direction
            trains_in_direction = [t for t in active_trains if t.direction == direction]
            trains_missing = max_trains_per_direction - len(trains_in_direction)

            # Create missing trains up to the max allowed
            for i in range(trains_missing):
                global_train_id[0] += 1
                train_id = global_train_id[0]
                delay_base = 2 if direction == 'clockwise' else 6
                delay_scaled = delay_base + i * 3

                # New train
                train = Train(env, f'Train {train_id}', capacity=3, line=line,
                              frequency_schedule={'peak': frequency, 'off_peak': frequency},
                              time_formatter=minutes_to_time, direction=direction,
                              log_writer=csv_writer, delay_base=delay_scaled,
                              active_trains=active_trains, rng=rng)
                active_trains.append(train)

        # We check again every 30 minutes of simulation time
        yield env.timeout(30)

# Initialization of the SimPy environment
env = simpy.Environment()

# We create all the stations and we set up their arrival processes
stations = []
for name in station_names:
    station = Station(env, name, arrival_rates[name], rng,
                      time_formatter=minutes_to_time, log_writer=csv_writer)
    stations.append(station)

# We create the metro line and assign it to each station
line = Line('Main Line', stations)
for station in stations:
    station.set_line(line)

# Begin the train generation process
env.process(generate_trains(env, line))

# Run the simulation  
# We do it from 06:00 to 02:00 (which is 1200 minutes total)
env.run(until=1200)

# We close the CSV file at the end of the simulation
csv_file.close()
