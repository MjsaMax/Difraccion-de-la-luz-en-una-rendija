# Simulación de Difracción Láser

Este proyecto contiene una simulación interactiva de difracción láser utilizando una rendija única. La simulación está implementada en Python utilizando la biblioteca Tkinter para la interfaz gráfica.

## Contenido del Proyecto

- [Descripción](#descripción)
- [Código Fuente](#código-fuente)
- [Documentación Detallada](#documentación-detallada)
- [Instalación y Uso](#instalación-y-uso)
- [Contribuciones](#contribuciones)

## Descripción

La simulación permite a los usuarios explorar el fenómeno de difracción de la luz a través de una rendija única. Los usuarios pueden ajustar parámetros como el ancho de la rendija, la distancia a la pantalla y la posición de observación en la pantalla. La simulación muestra en tiempo real:

1. El montaje experimental
2. El patrón de difracción en la pantalla
3. La distribución de intensidad de la luz difractada

## Código Fuente

El código fuente principal de la simulación se encuentra en el archivo [main.py](./main.py). Este archivo contiene la clase `SimulacionDifraccionLaser`, que implementa toda la lógica de la simulación y la interfaz gráfica.

Características principales del código:

- Implementación en Python con Tkinter
- Cálculos físicos basados en la teoría de difracción de Fraunhofer
- Interfaz gráfica interactiva con controles deslizantes y botones
- Visualización en tiempo real del montaje, patrón de difracción y distribución de intensidad

## Documentación Detallada

Para una explicación más profunda de la teoría física detrás de la simulación y detalles técnicos de la implementación, consulte el archivo [Difraccion_de_la_luz_en_una_rendija.pdf](./Difraccion_de_la_luz_en_una_rendija.pdf). Este documento incluye:

- Fundamentos teóricos de la difracción de la luz
- Derivación de las fórmulas utilizadas en la simulación
- Guía detallada de la arquitectura del código
- Explicaciones de las decisiones de diseño y optimizaciones

## Instalación y Uso

Para ejecutar la simulación:

1. Asegúrese de tener Python 3.x instalado en su sistema.
2. Clone este repositorio o descargue el archivo [main.py](./main.py).
3. Ejecute el script con el comando:
