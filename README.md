# Simulador del Algoritmo de Planificación FIFO

Aplicación de escritorio con interfaz gráfica para simular la planificación de procesos con el algoritmo **FIFO (First In, First Out)**, con cola de capacidad limitada, métricas de rendimiento y control de velocidad.

## Descripción

Este simulador reproduce cómo un sistema operativo atiende procesos con la política FIFO: los procesos llegan de forma aleatoria, esperan en una cola de capacidad limitada y la CPU los atiende estrictamente en orden de llegada, sin interrumpirlos hasta que terminan. Si la cola está llena cuando llega un proceso nuevo, este es rechazado.

El proyecto está construido siguiendo el patrón MVC (Modelo - Vista - Controlador), lo que separa claramente la lógica del algoritmo, la interfaz gráfica y el control de eventos, facilitando su mantenimiento y futuras extensiones (por ejemplo, agregar otros algoritmos como SJF o Round Robin).

## Características

- Cola FIFO con capacidad configurable (10 procesos por defecto)
- Generación aleatoria de procesos (tiempo de ejecución, tamaño e intervalo de llegada)
- Tabla en tiempo real con colores según el estado del proceso
- Panel con reloj simulado, ocupación de la cola y proceso que usa la CPU
- Control de velocidad de simulación (1x, 2x, 5x y 10x)
- Botones para iniciar/reanudar, detener y reiniciar la simulación
- Estadísticas al detener: procesos creados, atendidos, finalizados y rechazados
- Métricas de planificación: tiempo promedio de ejecución, espera y retorno, y uso de CPU
- Simulación sin hilos (basada en ticks), lo que evita condiciones de carrera
- Arquitectura MVC para facilitar mantenimiento y escalabilidad

## Estados de un Proceso

| Estado | Descripción |
|--------|-------------|
| **Espera** | El proceso está en la cola esperando su turno |
| **Ejecución** | El proceso está usando la CPU |
| **Terminado** | El proceso completó su tiempo de ejecución |
| **Rechazado** | La cola estaba llena cuando el proceso llegó |

## Cómo funciona

La simulación avanza por *ticks* de 1 segundo simulado. En cada tick, en este orden:

1. **La CPU consume** un segundo del proceso en ejecución; si termina, pasa a Terminado y la CPU queda libre.
2. **Llegadas**: cuando se cumple el intervalo aleatorio, se crea un proceso. Entra a la cola si hay espacio; si no, es rechazado.
3. **Despacho**: si la CPU está libre, toma el primer proceso de la cola (el que lleva más tiempo esperando).

### Métricas

- **Tiempo de espera** = instante de inicio − instante de llegada
- **Tiempo de retorno** = instante de fin − instante de llegada
- **Uso de CPU** = segundos con la CPU ocupada / tiempo simulado total

## Tecnologías

- Lenguaje: Python 3.8+
- Interfaz: Tkinter (ttk)
- Persistencia: ninguna (la simulación vive en memoria)
- Configuración: archivo `config.py`
- Empaquetado (opcional): PyInstaller

## Requisitos

- Python >= 3.8
- Tkinter (incluido en el instalador oficial de Python para Windows; en Linux: `sudo apt install python3-tk`)

No requiere librerías externas.

## Descarga

Si solo quieres usar el simulador, descarga el ejecutable desde la sección
[Releases](https://github.com/IngFonseca/Algoritmo_FIFO/releases) (Windows, no requiere Python).

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/IngFonseca/Algoritmo_FIFO.git
cd Algoritmo_FIFO
```

2. (Opcional) Crea y activa un entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows
```

3. No hay dependencias que instalar: el proyecto usa solo la biblioteca estándar de Python.

## Uso

Ejecuta la aplicación desde la raíz del proyecto (la carpeta que contiene `main.py`):

```bash
python main.py
```

### Controles de la interfaz

| Control | Acción |
|---------|--------|
| **Iniciar / Reanudar** | Arranca la simulación o la continúa donde quedó |
| **Detener** | Pausa la simulación y muestra las estadísticas |
| **Reiniciar** | Limpia todo y vuelve al estado inicial |
| **Velocidad** | Acelera el tiempo simulado (1x, 2x, 5x, 10x) |

## Estructura del Proyecto

```
Algoritmo_FIFO/
├── main.py                      # Punto de entrada de la aplicación
├── config.py                    # Parámetros de la simulación
├── .gitignore
├── models/                      # MODELO
│   ├── __init__.py
│   ├── proceso.py               # Entidad Proceso y sus estados
│   └── simulador.py             # Lógica FIFO (sin interfaz)
├── views/                       # VISTA
│   ├── __init__.py
│   └── vista_principal.py       # Interfaz Tkinter
└── controllers/                 # CONTROLADOR
    ├── __init__.py
    └── controlador.py           # Une vista y modelo, maneja el temporizador
```

| Capa | Responsabilidad |
|------|-----------------|
| **Modelo** | Reglas del algoritmo: llegadas, cola, despacho a la CPU y métricas. No conoce Tkinter. |
| **Vista** | Dibuja la interfaz y recibe los clics. No contiene lógica de la simulación. |
| **Controlador** | Recibe los eventos de la vista, avanza el modelo cada segundo simulado y refresca la vista. |

## Configuración

Los parámetros están en `config.py`:

| Parámetro | Descripción | Valor por defecto |
|-----------|-------------|-------------------|
| `CAPACIDAD_COLA` | Procesos máximos en espera | `10` |
| `TIEMPOS_EJECUCION` | Duraciones posibles de un proceso (s) | `(10, 15, 20, 25, 30, 35)` |
| `RANGO_TAMANO` | Rango del tamaño aleatorio | `(1, 100)` |
| `INTERVALO_LLEGADA` | Segundos entre llegadas (mín, máx) | `(2, 4)` |
| `VELOCIDADES` | Multiplicadores de velocidad disponibles | `(1, 2, 5, 10)` |

Con los valores por defecto, los procesos llegan mucho más rápido de lo que la CPU los atiende, por lo que la cola se satura y la mayoría se rechazan. Para ver más procesos completados, prueba `INTERVALO_LLEGADA = (10, 20)`.

## Generar el Ejecutable (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name Algoritmo_FIFO main.py
```

El archivo queda en `dist/Algoritmo_FIFO.exe`. No se versiona en el repositorio; se distribuye desde la sección *Releases* de GitHub.

## Notas sobre Credenciales y Datos

Este proyecto no usa credenciales, API keys, variables de entorno ni servicios externos, y tampoco guarda datos en disco. Aun así, el `.gitignore` excluye archivos `.env`, claves y los archivos generados por PyInstaller (`build/`, `dist/`, `*.spec`), que pueden contener rutas locales del equipo donde se compiló.

## Roadmap

- [ ] Pruebas unitarias con pytest para el simulador
- [ ] Implementar otros algoritmos de planificación (SJF, Round Robin, Prioridades)
- [ ] Comparativa de métricas entre algoritmos
- [ ] Diagrama de Gantt de la ejecución
- [ ] Exportación de estadísticas a CSV/Excel
- [ ] Parámetros configurables desde la interfaz

## Autor

Juan Fernando Fonseca Martínez

## Licencia

Este proyecto no especifica una licencia por el momento.

## Soporte

Para reportar problemas o sugerir mejoras:

- Abre un Issue en GitHub.
- Describe claramente el problema encontrado.
- Incluye los pasos necesarios para reproducirlo.
- Si es posible, proporciona mensajes de error o capturas de pantalla.
