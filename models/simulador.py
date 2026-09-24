"""Lógica de la simulación FIFO. No conoce Tkinter ni hilos."""
import random
from collections import deque
from typing import List, Optional

import config
from models.proceso import Estado, Proceso


class SimuladorFIFO:
    def __init__(self):
        self.reiniciar()

    def reiniciar(self) -> None:
        self.reloj = 0
        self.cola = deque()
        self.en_ejecucion: Optional[Proceso] = None
        self.finalizados: List[Proceso] = []
        self.rechazados: List[Proceso] = []
        self.total_creados = 0
        self.total_atendidos = 0
        self.ticks_cpu_ocupada = 0
        self._siguiente_id = 1
        self._cuenta_llegada = self._nuevo_intervalo()

    # ---------- avance de la simulación (1 tick = 1 s simulado) ----------
    def tick(self) -> None:
        self.reloj += 1
        self._consumir_cpu()
        self._gestionar_llegada()
        self._despachar()

    def _consumir_cpu(self) -> None:
        proceso = self.en_ejecucion
        if proceso is None:
            return
        self.ticks_cpu_ocupada += 1
        proceso.restante -= 1
        if proceso.restante == 0:
            proceso.estado = Estado.TERMINADO
            proceso.fin = self.reloj
            self.finalizados.append(proceso)
            self.en_ejecucion = None

    def _gestionar_llegada(self) -> None:
        self._cuenta_llegada -= 1
        if self._cuenta_llegada > 0:
            return
        self._cuenta_llegada = self._nuevo_intervalo()

        proceso = Proceso.aleatorio(self._siguiente_id, self.reloj)
        self._siguiente_id += 1
        self.total_creados += 1

        if len(self.cola) < config.CAPACIDAD_COLA:
            self.cola.append(proceso)
        else:
            proceso.estado = Estado.RECHAZADO
            self.rechazados.append(proceso)

    def _despachar(self) -> None:
        if self.en_ejecucion is None and self.cola:
            proceso = self.cola.popleft()          # FIFO
            proceso.estado = Estado.EJECUCION
            proceso.inicio = self.reloj
            self.en_ejecucion = proceso
            self.total_atendidos += 1

    @staticmethod
    def _nuevo_intervalo() -> int:
        return random.randint(*config.INTERVALO_LLEGADA)

    # ---------- consultas para la vista ----------
    def todos(self) -> List[Proceso]:
        lista = list(self.cola) + self.finalizados + self.rechazados
        if self.en_ejecucion:
            lista.append(self.en_ejecucion)
        return sorted(lista, key=lambda p: p.id)

    def estadisticas(self) -> dict:
        def promedio(valores):
            return sum(valores) / len(valores) if valores else 0.0

        fin = self.finalizados
        return {
            "reloj": self.reloj,
            "en_cola": len(self.cola),
            "capacidad": config.CAPACIDAD_COLA,
            "cpu_id": self.en_ejecucion.id if self.en_ejecucion else None,
            "creados": self.total_creados,
            "atendidos": self.total_atendidos,
            "finalizados": len(fin),
            "rechazados": len(self.rechazados),
            "prom_ejecucion": promedio([p.tiempo for p in fin]),
            "prom_espera": promedio([p.espera for p in fin]),
            "prom_retorno": promedio([p.retorno for p in fin]),
            "uso_cpu": (100 * self.ticks_cpu_ocupada / self.reloj) if self.reloj else 0.0,
        }