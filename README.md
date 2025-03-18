# Proyecto de Simulación de Metro con IA

Este repositorio contiene una simulación de eventos discretos para una línea de metro, con una posterior implementación de inteligencia artificial para mejorar el sistema. 

## Estructura del Proyecto

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

## Descripción General

Este proyecto está dividido en dos partes:
1. **Simulación de eventos discretos:** Implementa pasajeros, trenes, estaciones y la línea de metro, junto con eventos como llegada de trenes, subida y bajada de pasajeros, retrasos y emergencias.
2. **Optimización con IA:** En la segunda fase, se introduce inteligencia artificial para mejorar la eficiencia del sistema.

## Requisitos
- Python 3.x
- Bibliotecas necesarias (especificadas en `requirements.txt`)
- Ubuntu Linux (recomendado para compatibilidad)

## Instalación
```bash
git clone https://github.com/tuusuario/tu-repo.git
cd tu-repo
pip install -r requirements.txt
```

## Uso
Ejecuta la simulación con:
```bash
python src/main.py
```

Para realizar análisis de datos:
```bash
jupyter notebook data_analysis/analisis.ipynb
```

## Contribución
Si deseas contribuir, por favor abre un _pull request_ o reporta problemas en la sección de _issues_.

## Licencia
Este proyecto está bajo la licencia MIT.
