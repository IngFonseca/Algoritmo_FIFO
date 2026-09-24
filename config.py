"""Parámetros globales de la simulación."""

CAPACIDAD_COLA = 10                        # procesos máximos en espera
TIEMPOS_EJECUCION = (10, 15, 20, 25, 30, 35)  # segundos simulados
RANGO_TAMANO = (1, 100)                    # tamaño del proceso
INTERVALO_LLEGADA = (2, 4)                 # segundos entre llegadas
MS_POR_SEGUNDO_SIMULADO = 1000             # 1 tick = 1 s a velocidad 1x
VELOCIDADES = (1, 2, 5, 10)                # multiplicadores disponibles