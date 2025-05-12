# Subway Simulation Project

This repository implements a discrete-event simulation of a circular metro line in Python, now enhanced with AI-driven optimization and built‐in CSV logging for easy post–run analysis.

## Overview

The simulation models a circular metro line with 10 stations and trains running in both directions (clockwise and counter‐clockwise). Passengers arrive at stations according to configurable demand rates. Every key event—train arrivals, passenger boardings and alightings—is logged with a timestamp in a single `event_log.csv` file for downstream analysis.

In addition to the core simpy‐based engine, we’ve integrated a **Particle Swarm Optimization (PSO)** module that automatically tunes:

- **Train frequency (headway)**: the interval between consecutive train departures.  
- **Fleet size**: the total number of trains operating over the day.

The PSO optimizer minimizes the **average passenger waiting time** by repeatedly running the simulation under different headway + fleet configurations.

## Project Structure

```plaintext
/ (Directorio raíz del proyecto)
│
├── src/
│   ├── main.py # Entry point: sets seeds, runs PSO and sim
│   ├── sim/ # simulation_manager.py
│   ├── optim/ # PSO implementation 
│   ├── modules/ # Lifted simulation components reused by PSO
│
├── data_analysis/
│   ├── analisis.ipynb  # Notebook de análisis de datos
│   ├── results.csv     # Resultados del análisis
│
├── doc/
│   ├── (Ficheros LaTeX para documentación)
│
└── README.md  # Este archivo
```

## New Features

1. **CSV Event Logging**  
   - Generates `event_log.csv` in `data_analysis/`, containing columns:
     ```text
     Time,Event,Entity,Station,Train,Direction,Destination
     ```
   - Captures every passenger arrival, boarding, alighting, and train arrival.

2. **PSO‐Based Optimization**  
   - Automatically searches for the headway (in minutes) and number of trains that minimize average passenger wait.  
   - Reports the **optimized frequency**, **fleet size**, and **resulting average wait time** in the console.

3. **Built‐In Data Analysis Notebook**  
   - `data_analysis/analysis.ipynb` includes:
     - Distribution of passenger wait times  
     - Average headways per station  
     - Circular histogram of events by hour  
     - Additional custom plots you can extend  

## Installation & Usage

1. **Clone the repo** and enter the root folder:
   ```bash
   git clone <repo-url>
   cd <project-root>
