"""Modelo de un proceso."""
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

import config


class Estado(Enum):
    ESPERA = "Espera"
    EJECUCION = "Ejecución"
    TERMINADO = "Terminado"
    RECHAZADO = "Rechazado"


@dataclass
class Proceso:
    id: int
    tiempo: int
    tamano: int
    llegada: int
    estado: Estado = Estado.ESPERA
    inicio: Optional[int] = None
    fin: Optional[int] = None
    restante: int = field(init=False)

    def __post_init__(self):
        self.restante = self.tiempo

    @classmethod
    def aleatorio(cls, id: int, llegada: int) -> "Proceso":
        return cls(
            id=id,
            tiempo=random.choice(config.TIEMPOS_EJECUCION),
            tamano=random.randint(*config.RANGO_TAMANO),
            llegada=llegada,
        )

    @property
    def espera(self) -> Optional[int]:
        return None if self.inicio is None else self.inicio - self.llegada

    @property
    def retorno(self) -> Optional[int]:
        return None if self.fin is None else self.fin - self.llegada