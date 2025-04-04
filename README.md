# Subway Simulation Project

This repository contains a discrete-event simulation of a metro system implemented in Python, with future extensions that include Artificial Intelligence techniques.

## Overview

The simulation models a circular metro line with 10 stations and trains running in both directions (clockwise and counter-clockwise). Passengers dynamically arrive at stations based on time-dependent demand patterns. All major events—such as train arrivals, boardings, and alightings are logged with timestamps for later analysis.

The current implementation supports:
- Dynamic passenger and train generation.
- Rush-hour and off-peak demand simulation.
- Direction-aware boarding and routing.
- Event logging for post-simulation analysis.

## Project Structure


```plaintext
/ (Directorio raíz del proyecto)
│
├── src/
│   ├── (Módulos y carpetas del código del proyecto)
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


## How to Run

1. Make sure you have Python 3.8+ installed.
2. Install dependencies:

   ```bash
   pip install simpy numpy pandas matplotlib 



